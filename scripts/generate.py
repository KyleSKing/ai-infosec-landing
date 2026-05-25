#!/usr/bin/env python3
"""
Daily article generator for AI Infosec Landing
Uses Tavily for search + DeepSeek V4 Flash via OpenRouter for writing
"""

import os
import json
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

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


def tavily_search(query: str, max_results: int = 5) -> list[dict]:
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
    """Call DeepSeek V4 Flash via OpenRouter"""
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://ai-infosec-landing.github.io",
            "X-Title": "AI Infosec Landing",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.7,
            "max_tokens": 4000,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def generate_article(topic: str, category: str, search_queries: list[str]) -> dict:
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
    for i, r in enumerate(unique_results[:6], 1):
        context_parts.append(
            f"[{i}] {r['title']}\nURL: {r['url']}\n{r.get('content', '')[:500]}"
        )
    context = "\n\n".join(context_parts)
    summary = "\n".join(all_answers[:2])

    print(f"📝 Generating article with {len(unique_results)} sources...")

    system_prompt = """You are an expert technology journalist and security researcher who writes for a bilingual (Chinese/English) tech publication. Your articles combine breaking news analysis with deep technical insight.

Writing style:
- Sharp, incisive, and authoritative
- Balance technical depth with accessibility
- Include concrete examples and real-world implications
- Chinese sections should feel natural and native, not translated
- English sections should be crisp and professional

Output format: Strictly follow the JSON structure requested. No markdown outside the JSON."""

    user_prompt = f"""Today is {TODAY_CN}. Write a comprehensive bilingual article about: {topic}

Category: {category}

Recent news and sources:
{context}

AI-generated summary:
{summary}

Return ONLY valid JSON in this exact structure:
{{
  "title_en": "English title (compelling, SEO-friendly)",
  "title_cn": "中文标题（吸引人，专业）",
  "summary_en": "2-3 sentence English summary for meta description",
  "summary_cn": "2-3句中文摘要",
  "tags": ["tag1", "tag2", "tag3", "tag4"],
  "body_cn": "完整中文正文（Markdown格式，800-1200字）\\n\\n包含：\\n- 热点摘要：本周/近期发生了什么\\n- 技术深度：核心技术原理或漏洞分析\\n- 行业影响：对企业/开发者/用户的影响\\n- 作者点评：独到见解和预判",
  "body_en": "Full English article body (Markdown format, 600-900 words)\\n\\nInclude:\\n- News Brief: What happened\\n- Technical Deep-Dive: Core technical analysis\\n- Industry Impact: Implications for the field\\n- Editor's Take: Unique insights and predictions",
  "sources": [
    {{"title": "source title", "url": "source url"}}
  ]
}}"""

    raw = call_llm(system_prompt, user_prompt)

    # Extract JSON from response
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()

    return json.loads(raw)


def save_post(article: dict, category: str, slug: str):
    """Save article as Jekyll post"""
    tags_str = "\n".join(f"  - {t}" for t in article.get("tags", []))

    content = f"""---
layout: post
title_en: "{article['title_en']}"
title_cn: "{article['title_cn']}"
date: {TODAY}
category: {category}
tags:
{tags_str}
summary_en: "{article['summary_en']}"
summary_cn: "{article['summary_cn']}"
---

<!-- Chinese Version -->
<div class="lang-cn">

## {article['title_cn']}

{article['body_cn']}

</div>

---

<!-- English Version -->
<div class="lang-en">

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
    print(f"🚀 AI Infosec Landing — Daily Publisher [{TODAY}]")
    print("=" * 50)

    articles = [
        {
            "topic": "Latest AI model releases, research breakthroughs, and industry developments in artificial intelligence",
            "category": "ai",
            "slug": "ai-weekly",
            "queries": [
                "AI artificial intelligence news this week 2026",
                "large language model LLM release update 2026",
                "AI research breakthrough 2026",
            ],
        },
        {
            "topic": "Latest cybersecurity threats, vulnerabilities, data breaches, and defensive strategies",
            "category": "infosec",
            "slug": "infosec-weekly",
            "queries": [
                "cybersecurity vulnerability exploit 2026",
                "data breach ransomware attack news 2026",
                "information security CVE zero-day 2026",
            ],
        },
    ]

    for item in articles:
        try:
            article = generate_article(
                topic=item["topic"],
                category=item["category"],
                search_queries=item["queries"],
            )
            save_post(article, item["category"], item["slug"])
        except Exception as e:
            print(f"❌ Error generating {item['category']} article: {e}")
            raise

    print("\n✨ Done! All articles generated successfully.")


if __name__ == "__main__":
    main()
