#!/usr/bin/env python3
"""
Daily article generator for AI Infosec Landing
Uses Tavily for search + DeepSeek V4 Flash via OpenRouter for writing
"""

import os
import json
import re
import requests
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from content_config import (
    CONTENT_TYPE_LABELS,
    CONTENT_TYPE_PROMPTS,
    SYSTEM_PROMPT,
    select_daily_article,
)

# Config
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
MODEL = "deepseek/deepseek-v4-flash"
POSTS_DIR = Path("_posts")
POSTS_DIR.mkdir(exist_ok=True)

# 北京时间
BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime("%Y-%m-%d")
TODAY_CN = datetime.now(BJT).strftime("%Y年%m月%d日")


def tavily_search(query: str, max_results: int = 3) -> list[dict]:
    """Search for latest news using Tavily"""
    resp = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": True,
            "days": 3,  # 最近3天
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    answer = data.get("answer", "")
    return results, answer


def call_llm(system: str, user: str) -> str:
    """Call DeepSeek V4 Flash via OpenRouter with retry/backoff"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
        "max_tokens": 3000,
    }
    print("Using model:", payload["model"])
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://ai-infosec-landing.github.io",
                    "X-Title": "AI Infosec Landing",
                },
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429 and attempt < max_retries - 1:
                wait = 2 ** attempt  # 1,2,4 seconds
                print(f"Rate-limited (429), retrying in {wait}s...")
                time.sleep(wait)
                continue
            else:
                raise


def _extract_and_parse_json(raw: str, llm_func, system_prompt: str, user_prompt: str) -> dict:
    """Extract JSON from LLM response, fix common issues, retry on failure."""
    import json as _json

    # Try up to 2 times (first attempt + one regeneration)
    for attempt in range(2):
        text = raw.strip()

        # Strip markdown code fences
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    text = part
                    break
        text = text.strip()
        # Find JSON boundaries
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]

        # Fix unescaped control characters inside JSON strings
        sanitized = []
        in_string = False
        escape_next = False
        for ch in text:
            if escape_next:
                sanitized.append(ch)
                escape_next = False
            elif ch == '\\' and in_string:
                sanitized.append(ch)
                escape_next = True
            elif ch == '"':
                sanitized.append(ch)
                in_string = not in_string
            elif in_string and ch == '\n':
                sanitized.append('\\n')
            elif in_string and ch == '\r':
                sanitized.append('\\r')
            elif in_string and ch == '\t':
                sanitized.append('\\t')
            else:
                sanitized.append(ch)
        text = ''.join(sanitized)

        # Fix unescaped double quotes inside strings (e.g., 说"你好" -> 说\"你好\")
        # Strategy: within strings, any " that is preceded by a non-structural char
        # is likely an unescaped quote. We try parsing first; fall back to heuristic fix.
        try:
            return _json.loads(text)
        except _json.JSONDecodeError as e:
            # Try to fix unescaped quotes: find all " positions in string context
            # and escape those that are likely content quotes
            fixed = []
            in_str = False
            prev_char = None
            i = 0
            while i < len(text):
                ch = text[i]
                if ch == '\\' and in_str:
                    fixed.append(ch)
                    if i + 1 < len(text):
                        fixed.append(text[i + 1])
                        i += 2
                    continue
                elif ch == '"':
                    # Check if this is a structural quote (colon/comma/brace before/after)
                    if not in_str:
                        in_str = True
                        fixed.append(ch)
                    else:
                        # Look ahead: if next non-space char is : , ] } then it's structural
                        j = i + 1
                        while j < len(text) and text[j] in ' \t\n\r':
                            j += 1
                        next_structural = j < len(text) and text[j] in ':,'']}'
                        if next_structural or prev_char in ('{', ',', '['):
                            in_str = False
                            fixed.append(ch)
                        else:
                            # Likely unescaped content quote — escape it
                            fixed.append('\\"')
                else:
                    fixed.append(ch)
                prev_char = ch
                i += 1
            text = ''.join(fixed)

            try:
                return _json.loads(text)
            except _json.JSONDecodeError:
                if attempt == 0:
                    print(f"⚠️  JSON parse failed, re-asking LLM... ({e})")
                    print(f"  Raw preview: {raw[:200]}")
                    # Re-ask the LLM with stricter instruction
                    retry_prompt = user_prompt + "\n\nIMPORTANT: Your previous response had invalid JSON. Please output ONLY valid JSON with all strings properly escaped. No markdown, no code fences."
                    raw = llm_func(system_prompt, retry_prompt)
                else:
                    raise


def generate_article(topic: str, category: str, content_type: str, search_queries: list[str]) -> dict:
    """Generate a bilingual article on given topic"""
    print(f"🔍 Searching for: {topic}")

    # Gather search results
    all_results = []
    all_answers = []
    for query in search_queries:
        results, answer = tavily_search(query)
        all_results.extend(results)
        if answer:
            all_answers.append(answer)

    # Deduplicate by URL
    seen = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique_results.append(r)

    # Build context
    context_parts = []
    for i, r in enumerate(unique_results[:5], 1):
        context_parts.append(
            f"[{i}] {r['title']}\nURL: {r['url']}\n{r.get('content', '')[:500]}"
        )
    context = "\n\n".join(context_parts)
    summary = "\n".join(all_answers[:2])

    print(f"📝 Generating article with {len(unique_results)} sources...")

    content_type_prompt = CONTENT_TYPE_PROMPTS[content_type]
    content_type_label = CONTENT_TYPE_LABELS[content_type]
    system_prompt = SYSTEM_PROMPT

    user_prompt = f"""Today is {TODAY_CN}. Write a bilingual practical technology article.

Topic: {topic}
Category: {category}
Content type: {content_type} / {content_type_label['cn']} / {content_type_label['en']}

Content-type-specific instructions:
{content_type_prompt}

Recent sources:
{context}

Search summary:
{summary}

Return ONLY valid JSON in this exact structure:
{{
  "title_en": "English title",
  "title_cn": "中文标题",
  "summary_en": "2-3 sentence English summary for meta description",
  "summary_cn": "2-3句中文摘要",
  "tags": ["tag1", "tag2", "tag3", "tag4"],
  "body_cn": "中文主文，Markdown格式，1000-1800字。按当前content type要求组织，必须包含可执行步骤、适合人群、限制/风险、我的判断。",
  "body_en": "Concise English brief, Markdown format, 300-600 words. Cover what it is, why it matters, practical next steps, risks, and take.",
  "sources": [
    {{"title": "source title", "url": "source url"}}
  ]
}}"""

    raw = call_llm(system_prompt, user_prompt)

    return _extract_and_parse_json(raw, call_llm, system_prompt, user_prompt)


def save_post(article: dict, category: str, content_type: str, slug: str):
    """Save article as Jekyll post"""
    tags_str = "\n".join(f"  - {t}" for t in article.get("tags", []))

    content = f"""---
layout: post
title_en: "{article['title_en']}"
title_cn: "{article['title_cn']}"
date: {TODAY}
category: {category}
content_type: {content_type}
content_type_cn: "{CONTENT_TYPE_LABELS[content_type]['cn']}"
content_type_en: "{CONTENT_TYPE_LABELS[content_type]['en']}"
tags:
{tags_str}
summary_en: "{article['summary_en']}"
summary_cn: "{article['summary_cn']}"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## {article['title_cn']}

{article['body_cn']}

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## {article['title_en']}

{article['body_en']}

</div>

---

### 参考来源 / Sources

"""
    for src in article.get("sources", []):
        content += f"- [{src['title']}]({src['url']})\n"

    filename = f"{TODAY}-{slug}.md"
    filepath = POSTS_DIR / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"✅ Saved: {filepath}")
    return filepath


def main():
    print(f"AI Infosec Landing — Daily Publisher [{TODAY}]")
    print("=" * 50)

    item = select_daily_article(datetime.now(BJT).toordinal())
    try:
        content_type = item["content_type"]
        print(f"🧭 Content type: {content_type}")
        article = generate_article(
            topic=item["topic"],
            category=item["category"],
            content_type=content_type,
            search_queries=item["queries"],
        )
        save_post(article, item["category"], content_type, item["slug"])
    except Exception as e:
        print(f"❌ Error generating {item['category']} article: {e}")
        raise

    print("\n✨ Done! Daily article generated successfully.")


if __name__ == "__main__":
    main()
