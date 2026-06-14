# AI Infosec Landing Content Strategy Plan

> **For Hermes:** Use this plan as the source of truth for search strategy, content types, and writing prompts.

**Goal:** Move the project from generic AI/security news summaries to bilingual practical intelligence: tools, trends, defensive playbooks, and regulation tracking.

**Core positioning:** Pick one frontier tool, trend, risk, or regulation from AI/security/privacy/compliance; explain why it matters; then give developers, security teams, data teams, and outbound teams steps they can try, check, or add to workflow immediately.

---

## Final content type rotation

Publish exactly **one article per day**. Rotate across all four content types:

```text
Day 1: tool_guide
Day 2: trend_explainer
Day 3: defensive_playbook
Day 4: regulation_watch
Repeat
```

This keeps the feed focused and avoids publishing one AI post plus one security post every day.

### 1. `tool_guide`

Tools, APIs, open-source projects, plugins, CLIs, GitHub Actions, MCP servers.

Focus:
- What is it?
- How do I install/register/configure/use it?
- Is there API/CLI/VS Code/GitHub Actions/Docker/MCP/OpenAI-compatible access?
- Is it free? What are limits and risks?
- Who should try it?

### 2. `trend_explainer`

Trend tracking and practical analysis for emerging AI/security workflows.

Focus:
- What is the trend?
- What old problem does it solve?
- How is it different from the older way?
- What public examples/tools/discussions support it?
- What can readers try now?

### 3. `defensive_playbook`

Security, privacy, and DevSecOps defensive checklists.

Focus:
- What is the risk?
- Who is affected?
- How to check?
- How to remediate or add it to CI/CD/team workflow?
- What are false-positive/false-negative/operational risks?

### 4. `regulation_watch`

Legal/regulatory/compliance tracking translated into engineering actions.

Focus:
- What changed?
- Who is affected?
- What should engineering/security/data/product teams do?
- What checklist can teams prepare now?
- What uncertainty remains?

**Important weighting:** China data regulation and cross-border data transfer must receive 50%+ weight in regulation topics when relevant.

---

## Output language

Articles are bilingual:

- Chinese main article: complete, direct, high information density.
- English brief: concise, accurate, useful for SEO and English readers.

Recommended ratio: Chinese 70%, English 30%.

---

## Search strategy

Do not search only for generic `news`. Search for practical signals:

```text
tutorial
guide
how to
open source
GitHub
CLI
API
free
pricing
docs
release
workflow
GitHub Actions
VS Code
compliance
regulation
checklist
```

### AI search themes

```text
AI agent
coding agent
agent loop
AI workflow
vibe coding
AI harness
eval harness
MCP
Claude Code
Cursor
OpenCode
Cline
OpenRouter
free LLM API
OpenAI compatible API
long context model
1M context
LLM evaluation
agent orchestration
```

Example queries:

```text
free LLM API OpenAI compatible long context model tutorial
AI coding agent CLI GitHub open source VS Code extension
MCP server GitHub open source AI agent workflow docs
Cline OpenRouter Claude Code Cursor alternative API pricing guide
LLM evaluation eval harness AI agent tutorial GitHub
AI agent loop recurring agent loop coding workflow
AI harness eval harness agent governance workflow tutorial
vibe coding risks coding agent safety guardrails
Claude Code workflow subagents code review loop
agent orchestration MCP AI workflow best practices
```

### Security/privacy/DevSecOps search themes

```text
DevSecOps
security automation
policy as code
zero trust
SBOM
SAST
DAST
secret scanning
container scanner
CVE scanner
supply chain security
LLM security
prompt injection defense
privacy engineering
compliance automation
```

Example queries:

```text
DevSecOps GitHub Actions tutorial security scanning open source
SBOM open source scanner software supply chain security guide
secret scanning GitHub Actions CI/CD remediation guide
LLM security prompt injection defense checklist
container scanner CVE scanner SAST DAST open source workflow
```

### China regulation/compliance search themes

Chinese terms:

```text
网络安全法
数据安全法
个人信息保护法
数据出境
数据跨境
数据出境安全评估
个人信息出境标准合同
个人信息保护认证
重要数据
核心数据
关键信息基础设施
CIIO
等保
网络安全等级保护
生成式人工智能服务管理暂行办法
算法推荐管理规定
深度合成管理规定
数据合规
出海合规
```

English terms:

```text
China data export
China cross-border data transfer
China Cybersecurity Law
China Data Security Law
China PIPL
CAC data export security assessment
China standard contract personal information export
China important data
China CIIO
MLPS 2.0
China generative AI regulation
China algorithm recommendation regulation
China deep synthesis regulation
```

Example queries:

```text
中国 数据出境 安全评估 个人信息保护法 PIPL 合规 清单
网络安全法 数据安全法 个人信息保护法 CSL DSL PIPL 数据跨境
China data export CAC security assessment PIPL standard contract personal information export
重要数据 关键信息基础设施 CIIO 等保 MLPS 数据合规
生成式人工智能 服务 管理 暂行办法 算法推荐 深度合成 合规
EU AI Act GDPR NIS2 DORA SOC 2 ISO 27001 compliance engineering checklist
```

Regulation search weighting:

```text
China data regulation / data export: 50%+
EU / US / international compliance: about 30%
Security standards / audit practice: about 20%
```

---

## Selection scoring

Do not rank topics only by popularity.

Recommended scoring:

```text
Practicality: 30%
Freshness: 20%
Technical/security value: 20%
Actionability: 20%
Distribution hook: 10%
```

Prioritize topics with:

```text
tool entry
GitHub repo
official docs
free/open-source tier
clear tutorial
compliance action
GitHub Actions / VS Code / CLI integration
```

Downrank:

```text
pure funding news
vendor PR only
pure opinion
concept without action
vulnerability headline without defensive steps
regulatory news without engineering impact
```

---

## Implementation in this repo

### Current minimal implementation

- `scripts/content_config.py` stores:
  - shared bilingual system prompt
  - content-type-specific prompts
  - one-article-per-day four-content-type rotation
  - search queries by content type
- `scripts/generate.py` imports this config and chooses exactly one daily article by date.
- Current Tavily search remains the source fetcher for now.

### Future migration

When Tavily is replaced or augmented:

```text
X/Twitter via Agent Reach = trend discovery
GitHub search = open-source/tool discovery
Serper = factual source enrichment
LLM = bilingual practical article generation
```

---

## Verification commands

```bash
python3 -m py_compile scripts/content_config.py scripts/generate.py
python3 scripts/generate.py
bundle exec jekyll build --destination _site
```

Only run `python3 scripts/generate.py` when valid `OPENROUTER_API_KEY` and `TAVILY_API_KEY` are present and API usage is intended.
