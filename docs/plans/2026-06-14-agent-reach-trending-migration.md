# Agent Reach Trending Migration Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Replace Tavily-first search in `ai-infosec-landing` with Agent Reach / `twitter-cli` trending-topic discovery, while keeping Tavily unchanged until the next scheduled run is observed.

**Architecture:** Use X/Twitter as the trend-discovery layer, optionally Serper as a future fact-check/source-enrichment layer, and OpenRouter/DeepSeek for article generation. The pipeline will classify daily hot discussions into AI and Infosec topics, rank tweets by engagement, then pass structured sources into the existing Jekyll post generator.

**Tech Stack:** Python stdlib, `requests`, `python-dateutil`, Agent Reach, `twitter-cli`, GitHub Actions, Jekyll, OpenRouter DeepSeek V4 Flash.

---

## Current Decision

Do **not** migrate immediately.

Tomorrow, let the existing Tavily-based GitHub Action run once more and inspect the result:

- If Tavily succeeds consistently: defer migration.
- If Tavily fails again with 403/quota/auth instability: implement this plan.
- If Tavily succeeds but content quality is weak: implement Agent Reach as trend discovery while keeping Tavily/Serper only for source enrichment.

---

## Target Pipeline

```text
Daily Article Publisher
  ├─ load topic keyword config
  ├─ twitter-cli search via Agent Reach
  ├─ score/filter/dedupe X posts
  ├─ select AI top topic
  ├─ select Infosec top topic
  ├─ pass trend context to OpenRouter/DeepSeek
  ├─ write _posts/YYYY-MM-DD-ai-weekly.md
  ├─ write _posts/YYYY-MM-DD-infosec-weekly.md
  └─ Jekyll build/deploy
```

---

## Keywords

### AI Keywords

```text
AI
LLM
agent
AI agent
vibe coding
coding agent
harness
eval harness
loop
agent loop
OpenAI
Anthropic
Claude
DeepSeek
Gemini
```

### Infosec Keywords

```text
cybersecurity
CVE
zero-day
ransomware
data breach
exploit
compliance
regulation
regime
data privacy
privacy
zero trust
zerotrust
DevSecOps
```

### X Noise Terms

Apply only to X/Twitter filtering/search, not to GitHub or other sources:

```text
crypto
trading
forex
airdrop
memecoin
giveaway
```

---

## Task 1: Observe Tomorrow's Tavily Run

**Objective:** Decide whether migration is necessary based on one more real scheduled run.

**Files:**
- No code changes.

**Steps:**

1. Check latest action runs:

```bash
gh run list --repo KyleSKing/ai-infosec-landing --limit 5
```

2. If failed, inspect logs:

```bash
gh run view <RUN_ID> --repo KyleSKing/ai-infosec-landing --log-failed
```

3. Decision rule:

```text
Tavily 403 again      → implement migration
Tavily success        → keep current pipeline for now
Other LLM/JSON error  → fix generate.py robustness separately
```

**Verification:** Clear conclusion recorded before coding.

---

## Task 2: Add Topic Configuration

**Objective:** Move topic keywords out of `generate.py` into a dedicated config file.

**Files:**
- Create: `scripts/topic_config.py`
- Modify: `scripts/generate.py`

**Implementation sketch:**

```python
TOPICS = {
    "ai": {
        "slug": "ai-weekly",
        "min_likes": 50,
        "keywords": [
            "AI", "LLM", "agent", "AI agent", "vibe coding", "coding agent",
            "harness", "eval harness", "loop", "agent loop",
            "OpenAI", "Anthropic", "Claude", "DeepSeek", "Gemini",
        ],
        "noise_terms": ["crypto", "trading", "forex", "airdrop", "memecoin", "giveaway"],
    },
    "infosec": {
        "slug": "infosec-weekly",
        "min_likes": 30,
        "keywords": [
            "cybersecurity", "CVE", "zero-day", "ransomware", "data breach",
            "exploit", "compliance", "regulation", "regime", "data privacy",
            "privacy", "zero trust", "zerotrust", "DevSecOps",
        ],
        "noise_terms": ["crypto", "trading", "forex", "airdrop", "memecoin", "giveaway"],
    },
}
```

**Verification:**

```bash
python3 -m py_compile scripts/topic_config.py scripts/generate.py
```

---

## Task 3: Add Twitter Trend Source Module

**Objective:** Call `twitter search --json` from Python and return normalized trend items.

**Files:**
- Create: `scripts/trend_sources.py`

**Implementation requirements:**

- Source `TWITTER_AUTH_TOKEN` and `TWITTER_CT0` from environment.
- In local/cron contexts, allow fallback to `source ~/.bashrc`.
- Run `twitter whoami` before searches.
- Search with `--type top`, `--lang en`, `--since YYYY-MM-DD`, `--exclude retweets`, `--json`.
- Return normalized fields:
  - `text`
  - `url`
  - `author`
  - `metrics`
  - `created_at`

**Verification:**

```bash
source ~/.bashrc
python3 - <<'PY'
from scripts.trend_sources import search_x_trends
items = search_x_trends(["AI", "agent", "vibe coding"], min_likes=10, limit=5)
print(len(items))
print(items[0].keys() if items else "empty")
PY
```

Expected: returns a list or a clear actionable auth/search error.

---

## Task 4: Add Trend Scoring

**Objective:** Filter noise and rank X posts by engagement.

**Files:**
- Create: `scripts/trend_scoring.py`

**Scoring:**

```python
def score_tweet(t):
    m = t.get("metrics", {})
    likes = m.get("likes", 0)
    retweets = m.get("retweets", 0)
    replies = m.get("replies", 0)
    views = m.get("views", 0)
    return likes * 3 + retweets * 5 + replies * 2 + views * 0.001
```

**Filtering:**

- Drop text shorter than 80 chars.
- Drop obvious giveaway/crypto/trading noise.
- Dedupe by URL and normalized text.
- Keep top 5-8 items per category.

**Verification:** Unit-style local smoke test with sample dicts.

---

## Task 5: Refactor `generate.py`

**Objective:** Replace Tavily search context with trend context from X.

**Files:**
- Modify: `scripts/generate.py`

**Change:**

Replace:

```python
results, answer = tavily_search(query)
```

With:

```python
topic_data = discover_hot_topic(category)
context = build_context_from_trends(topic_data["sources"])
```

Prompt requirement:

```text
Treat X posts as trend signals, not verified facts.
Do not invent facts beyond the supplied context.
If a claim appears only in one tweet, phrase it as community discussion or a widely shared post claim.
Focus on why this topic is gaining attention today.
```

**Verification:**

```bash
python3 -m py_compile scripts/*.py
python3 scripts/generate.py
```

Expected:

```text
✅ Saved: _posts/YYYY-MM-DD-ai-weekly.md
✅ Saved: _posts/YYYY-MM-DD-infosec-weekly.md
✨ Done! All articles generated successfully.
```

---

## Task 6: Update GitHub Actions

**Objective:** Run Agent Reach/twitter-cli in GitHub Actions if keeping GitHub-hosted automation.

**Files:**
- Modify: `.github/workflows/daily-publish.yml`

**Change dependencies:**

```yaml
- name: Install Python dependencies
  run: |
    pip install requests python-dateutil
    pip install agent-reach
    agent-reach install --channels twitter
```

**Change env:**

```yaml
- name: Generate articles
  env:
    OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
    TWITTER_AUTH_TOKEN: ${{ secrets.TWITTER_AUTH_TOKEN }}
    TWITTER_CT0: ${{ secrets.TWITTER_CT0 }}
  run: python scripts/generate.py
```

**Secrets required:**

```text
TWITTER_AUTH_TOKEN
TWITTER_CT0
```

**Verification:** Manual workflow dispatch succeeds.

---

## Task 7: Optional Reliability Upgrade

**Objective:** Avoid X/Twitter becoming the next single point of failure.

**Recommended fallback order:**

```text
1. X/Twitter via Agent Reach for trend discovery
2. Serper for factual source enrichment
3. If both fail, skip publishing rather than hallucinating
```

**Reason:** X is good for trends but weak as a factual source. Serper should be used to find official posts, vendor blogs, CVEs, docs, or credible media references.

---

## Do Not Do Yet

- Do not delete Tavily code before tomorrow's run is observed.
- Do not add GitHub Action Twitter secrets until deciding to migrate.
- Do not treat X posts as verified news sources.
- Do not overbuild clustering; first version can simply score and rank top posts.

---

## Final Decision Gate

After tomorrow's Tavily run:

```text
If run success and output quality acceptable:
  Keep current pipeline.

If run fails with Tavily 403 or unstable search:
  Implement Tasks 2-6.

If run succeeds but topics are stale/boring:
  Implement X trend discovery but optionally keep Tavily/Serper as enrichment.
```
