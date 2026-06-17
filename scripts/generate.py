#!/usr/bin/env python3
"""
Daily article generator for AI Infosec Landing.

Architecture:
- Tavily collects recent sources.
- LLM generates small metadata JSON only.
- LLM generates Chinese and English bodies as plain Markdown, not JSON.

This avoids the previous failure mode where large bilingual article bodies inside
one JSON string were truncated and caused JSONDecodeError.
"""

import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

import requests

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

# Beijing time
BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime("%Y-%m-%d")
TODAY_CN = datetime.now(BJT).strftime("%Y年%m月%d日")


def tavily_search(query: str, max_results: int = 3) -> tuple[list[dict], str]:
    """Search for latest news using Tavily."""
    resp = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "include_answer": True,
            "days": 3,
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", []), data.get("answer", "")


def call_llm(
    system: str,
    user: str,
    *,
    max_tokens: int = 3000,
    temperature: float = 0.45,
    json_mode: bool = False,
) -> str:
    """Call DeepSeek V4 Flash via OpenRouter with retry/backoff."""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    print("Using model:", payload["model"])
    max_retries = 3
    last_resp = None
    for attempt in range(max_retries):
        try:
            last_resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://ai-infosec-landing.github.io",
                    "X-Title": "AI Infosec Landing",
                },
                json=payload,
                timeout=150,
            )
            last_resp.raise_for_status()
            data = last_resp.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError:
            status = last_resp.status_code if last_resp is not None else None
            if status == 429 and attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Rate-limited (429), retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise

    raise RuntimeError("LLM call failed after retries")


def extract_json(raw: str) -> dict:
    """Extract and parse a JSON object from an LLM response."""
    text = raw.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]

    # Escape literal control characters inside strings.
    sanitized: list[str] = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            sanitized.append(ch)
            escape_next = False
        elif ch == "\\" and in_string:
            sanitized.append(ch)
            escape_next = True
        elif ch == '"':
            sanitized.append(ch)
            in_string = not in_string
        elif in_string and ch == "\n":
            sanitized.append("\\n")
        elif in_string and ch == "\r":
            sanitized.append("\\r")
        elif in_string and ch == "\t":
            sanitized.append("\\t")
        else:
            sanitized.append(ch)

    return json.loads("".join(sanitized))


def parse_json_with_retry(
    raw: str,
    *,
    retry_func: Callable[[str], str],
    retry_prompt: str,
) -> dict:
    """Parse small metadata JSON; retry with stricter prompt if needed."""
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            return extract_json(raw)
        except json.JSONDecodeError as exc:
            last_error = exc
            print(f"⚠️  Metadata JSON parse failed, retrying... ({exc})")
            print(f"  Raw preview: {raw[:220]}")
            if attempt < 2:
                raw = retry_func(
                    retry_prompt
                    + "\n\nYour previous response was invalid JSON. Output ONLY a compact valid JSON object. No markdown."
                )
    raise last_error or ValueError("metadata JSON parse failed")


def clean_markdown_body(raw: str) -> str:
    """Strip accidental code fences around Markdown bodies."""
    text = raw.strip()
    if text.startswith("```") and text.endswith("```"):
        text = re.sub(r"^```(?:markdown|md)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def build_context(search_queries: list[str]) -> tuple[str, str, list[dict]]:
    all_results: list[dict] = []
    all_answers: list[str] = []
    for query in search_queries:
        results, answer = tavily_search(query)
        all_results.extend(results)
        if answer:
            all_answers.append(answer)

    seen: set[str] = set()
    unique_results: list[dict] = []
    for result in all_results:
        url = result.get("url")
        if url and url not in seen:
            seen.add(url)
            unique_results.append(result)

    context_parts = []
    for i, result in enumerate(unique_results[:5], 1):
        context_parts.append(
            f"[{i}] {result.get('title', 'Untitled')}\n"
            f"URL: {result.get('url', '')}\n"
            f"{result.get('content', '')[:700]}"
        )

    return "\n\n".join(context_parts), "\n".join(all_answers[:2]), unique_results[:5]


def source_list_from_results(results: list[dict]) -> list[dict]:
    sources = []
    for result in results:
        title = str(result.get("title") or "Source").strip()
        url = str(result.get("url") or "").strip()
        if url:
            sources.append({"title": title[:160], "url": url})
    return sources


def generate_metadata(
    topic: str,
    category: str,
    content_type: str,
    content_type_prompt: str,
    context: str,
    summary: str,
) -> dict:
    prompt = f"""Today is {TODAY_CN}. Generate metadata for one bilingual practical technology article.

Topic: {topic}
Category: {category}
Content type: {content_type} / {CONTENT_TYPE_LABELS[content_type]['cn']} / {CONTENT_TYPE_LABELS[content_type]['en']}

Content-type-specific instructions:
{content_type_prompt}

Recent sources:
{context}

Search summary:
{summary}

Return ONLY compact valid JSON in this exact structure:
{{
  "title_en": "English title, under 90 chars",
  "title_cn": "中文标题，30字以内",
  "summary_en": "2 concise English sentences",
  "summary_cn": "2句中文摘要",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}"""

    def retry_func(p: str) -> str:
        return call_llm(SYSTEM_PROMPT, p, max_tokens=1400, temperature=0.25, json_mode=True)

    raw = retry_func(prompt)
    metadata = parse_json_with_retry(raw, retry_func=retry_func, retry_prompt=prompt)
    metadata["tags"] = [str(tag).strip() for tag in metadata.get("tags", []) if str(tag).strip()][:8]
    if not metadata["tags"]:
        metadata["tags"] = [category, content_type]
    return metadata


def generate_body_cn(
    topic: str,
    category: str,
    content_type: str,
    content_type_prompt: str,
    metadata: dict,
    context: str,
    summary: str,
) -> str:
    prompt = f"""Today is {TODAY_CN}. Write the Chinese main article as Markdown only. Do not output JSON.

Title: {metadata['title_cn']}
Topic: {topic}
Category: {category}
Content type: {content_type} / {CONTENT_TYPE_LABELS[content_type]['cn']}

Content-type-specific instructions:
{content_type_prompt}

Recent sources:
{context}

Search summary:
{summary}

Requirements:
- 1800-2600 Chinese characters; never exceed 3000 Chinese characters.
- Direct, high-density, practical.
- Include executable steps/checklists where appropriate.
- Include适合人群、限制/风险、我的判断.
- Do not invent unsupported facts.
- Output Markdown body only, no surrounding code fence."""
    return clean_markdown_body(call_llm(SYSTEM_PROMPT, prompt, max_tokens=6500, temperature=0.45))


def generate_body_en(
    topic: str,
    category: str,
    content_type: str,
    metadata: dict,
    context: str,
    summary: str,
) -> str:
    prompt = f"""Write a concise English brief as Markdown only. Do not output JSON.

Title: {metadata['title_en']}
Topic: {topic}
Category: {category}
Content type: {content_type}

Recent sources:
{context}

Search summary:
{summary}

Requirements:
- 300-500 words.
- Cover what it is, why it matters, practical next steps, risks, and take.
- Do not invent unsupported facts.
- Output Markdown body only, no surrounding code fence."""
    return clean_markdown_body(call_llm(SYSTEM_PROMPT, prompt, max_tokens=2200, temperature=0.4))


def generate_article(topic: str, category: str, content_type: str, search_queries: list[str]) -> dict:
    """Generate a bilingual article on the given topic."""
    print(f"🔍 Searching for: {topic}")
    context, summary, source_results = build_context(search_queries)
    print(f"📝 Generating article with {len(source_results)} sources...")

    content_type_prompt = CONTENT_TYPE_PROMPTS[content_type]
    metadata = generate_metadata(topic, category, content_type, content_type_prompt, context, summary)
    body_cn = generate_body_cn(topic, category, content_type, content_type_prompt, metadata, context, summary)
    body_en = generate_body_en(topic, category, content_type, metadata, context, summary)

    return {
        **metadata,
        "body_cn": body_cn,
        "body_en": body_en,
        "sources": source_list_from_results(source_results),
    }


def yaml_scalar(value: object) -> str:
    """Return a YAML-safe scalar using JSON string escaping."""
    return json.dumps(str(value), ensure_ascii=False)


def save_post(article: dict, category: str, content_type: str, slug: str) -> Path:
    """Save article as a Jekyll post."""
    tags = article.get("tags", []) or [category, content_type]
    tags_str = "\n".join(f"  - {yaml_scalar(tag)}" for tag in tags)

    content = f"""---
layout: post
title_en: {yaml_scalar(article['title_en'])}
title_cn: {yaml_scalar(article['title_cn'])}
date: {TODAY}
category: {category}
content_type: {content_type}
content_type_cn: {yaml_scalar(CONTENT_TYPE_LABELS[content_type]['cn'])}
content_type_en: {yaml_scalar(CONTENT_TYPE_LABELS[content_type]['en'])}
tags:
{tags_str}
summary_en: {yaml_scalar(article['summary_en'])}
summary_cn: {yaml_scalar(article['summary_cn'])}
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

    filepath = POSTS_DIR / f"{TODAY}-{slug}.md"
    filepath.write_text(content, encoding="utf-8")
    print(f"✅ Saved: {filepath}")
    return filepath


def main() -> None:
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
    except Exception as exc:
        print(f"❌ Error generating {item['category']} article: {exc}")
        raise

    print("\n✨ Done! Daily article generated successfully.")


if __name__ == "__main__":
    main()
