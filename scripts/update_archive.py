#!/usr/bin/env python3
"""
Update article archive index:
- archive/README.md: full list by year/month
- archive/YYYY/MM.md: monthly list sorted by date descending
"""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import frontmatter

BJT = timezone(timedelta(hours=8))
ARCHIVE_ROOT = Path("archive")
POSTS_DIR = Path("_posts")

ARCHIVE_ROOT.mkdir(exist_ok=True, parents=True)


def parse_post(post_path: Path) -> Tuple[datetime, frontmatter.Post, Path]:
    """Parse post date from filename and frontmatter."""
    # filename: YYYY-MM-DD[-suffix]-slug.md
    name = post_path.name
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", name)
    if not m:
        raise ValueError(f"invalid post filename: {post_path.name}")
    year = int(m.group(1))
    month = int(m.group(2))
    day = int(m.group(3))

    post = frontmatter.loads(post_path.read_text(encoding="utf-8"))
    # prefer date from frontmatter (it has time)
    dt = post.get("date")
    if dt is None:
        dt = datetime(year, month, day, 8, 0, 0, tzinfo=BJT)
    elif isinstance(dt, str):
        # frontmatter returns string if date not parsed as datetime
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S %z")
    elif isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=BJT)
    elif type(dt).__name__ == "date":
        # handles raw date objects from YAML parsing
        dt = datetime.combine(dt, datetime.min.time()).replace(tzinfo=BJT)

    return dt, post, post_path


def main() -> None:
    print("📚 Updating article archive index...")
    posts: List[Tuple[datetime, frontmatter.Post, Path]] = []

    for post_path in POSTS_DIR.glob("*.md"):
        try:
            posts.append(parse_post(post_path))
        except Exception as e:
            print(f"⚠️  skipping {post_path.name}: {e}")

    # sort descending by date
    posts.sort(key=lambda x: x[0], reverse=True)
    print(f"✅ Found {len(posts)} posts")

    # group by year/month
    by_year_month: Dict[Tuple[int, int], List[Tuple[datetime, frontmatter.Post, Path]]] = {}
    for dt, post, path in posts:
        key = (dt.year, dt.month)
        by_year_month.setdefault(key, []).append((dt, post, path))

    # generate monthly pages
    for (year, month), m_posts in by_year_month.items():
        year_dir = ARCHIVE_ROOT / f"{year}"
        year_dir.mkdir(exist_ok=True)
        md_path = year_dir / f"{month:02d}.md"

        lines = [
            f"# {year} 年 {month} 月 文章归档",
            "",
            "| Date | 分类 | 类型 | 标题 | 文章 |",
            "|------|------|------|------|------|",
        ]
        for dt, post, path in m_posts:
            date_str = dt.strftime("%Y-%m-%d %H:%M")
            category = post.get("category", "-") or "-"
            content_type_cn = post.get("content_type_cn", "-") or "-"
            title_cn = post.get("title_cn", path.stem)
            rel_path = f"../_posts/{path.name}"
            lines.append(f"| {date_str} | {category} | {content_type_cn} | {title_cn} | [→]({rel_path}) |")

        md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  wrote: {md_path} ({len(m_posts)} posts)")

    # generate root README
    lines = [
        "# 文章归档",
        "",
        "按年月浏览文章：",
        "",
    ]

    years = sorted(by_year_month.keys(), reverse=True)
    for (year, month) in years:
        lines.append(f"- [{year} 年 {month} 月](./{year}/{month:02d}.md)")

    readme_path = ARCHIVE_ROOT / "README.md"
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n✅ Done. Root index: {readme_path}")
    print(f"   Total: {len(posts)} posts in {len(by_year_month)} month(s)")


if __name__ == "__main__":
    main()
