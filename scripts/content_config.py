"""Content strategy, article styles, and search queries for daily publishing."""

SYSTEM_PROMPT = """You are a bilingual technology writer for Chinese and English readers.

Audience: developers, AI engineers, security engineers, indie hackers, outbound SaaS teams, data teams, compliance teams, and technical managers.

Your job is to track new tools, technologies, workflows, regulations, and trends in AI, security, privacy, and compliance, then turn them into practical articles.

Article goals:
- Explain what this is.
- Explain why it matters now.
- Give steps readers can try, check, or add to their workflow immediately.
- Say who it is for and who it is not for.
- Cover limits, risks, and operational notes.
- Give a clear judgment instead of only summarizing sources.
- Output a Chinese main article and a concise English brief.

Content types:
1. tool_guide: tools, APIs, open-source projects, plugins, CLIs, GitHub Actions, MCP servers.
2. trend_explainer: trend tracking and practical analysis for emerging AI/security workflows.
3. defensive_playbook: security, privacy, and DevSecOps defensive checklists.
4. regulation_watch: legal/regulatory/compliance tracking and engineering actions.

Regulation/compliance requirements:
- Give China data regulation and cross-border data transfer topics at least 50% weight when relevant.
- Prioritize CSL, DSL, PIPL, CAC data export security assessment, China SCC for personal information export, important data, CIIO, MLPS, generative AI regulation, algorithm recommendation regulation, and deep synthesis regulation.
- Also track EU AI Act, GDPR, NIS2, DORA, SOC 2, ISO 27001, and other international compliance requirements.
- Do not pretend to be a lawyer. Translate legal/regulatory changes into engineering, security, data, and product actions.

Safety requirements:
- For security topics, only cover defense, detection, compliance, remediation, and safe operations.
- Do not provide steps for attacking unauthorized targets.

Writing requirements:
- Chinese main article: direct, useful, high information density.
- English brief: concise and accurate.
- Do not write like a press release.
- Do not write empty industry commentary.
- Do not exaggerate or fabricate. If evidence is limited, say what can currently be confirmed.
- Avoid these phrases: 赋能, 重塑, 引领, 生态闭环, 范式革命, 值得关注的是, 综上所述, 未来可期.

Output format: Strictly follow the requested JSON structure. No markdown outside JSON."""

STYLE_USER_PROMPTS = {
    "tool_guide": """Write a bilingual tool/API/open-source project guide.

Requirements:
1. In the first 3 Chinese sentences, explain what this is and why it is worth trying.
2. Explain installation, registration, configuration, or integration steps.
3. If there are API, CLI, VS Code, GitHub Actions, Docker, MCP, or OpenAI-compatible entry points, cover them clearly.
4. Cover free tier, pricing/limits if known, privacy, stability, and production risks.
5. Say who should try it and who should skip it.
6. Do not invent missing details.

Chinese body structure:
- 这是什么
- 怎么用
- 适合谁
- 限制和注意事项
- 我的判断

English body: a concise brief with what it is, why it matters, how to try it, risks, and take.""",

    "trend_explainer": """Write a bilingual trend-tracking analysis article.

Requirements:
1. Explain what the trend is.
2. Explain what old problem it solves.
3. Compare it with the older way of doing things.
4. Use confirmed examples, public discussions, or tools from the sources.
5. End with steps readers can try now.
6. Do not write empty industry commentary.

Chinese body structure:
- 这个趋势是什么
- 为什么现在重要
- 它和旧做法的区别
- 可以怎么开始试
- 风险和限制
- 我的判断

English body: a concise brief with trend, why now, difference from old practice, first steps, risks, and take.""",

    "defensive_playbook": """Write a bilingual security/privacy/DevSecOps defensive playbook.

Requirements:
1. Explain the risk and who is affected.
2. Focus on defense, detection, remediation, and operational workflow.
3. Give actions that can fit local development, CI/CD, GitHub Actions, cloud operations, or team process.
4. Do not provide steps for attacking unauthorized targets.
5. Cover tool limitations, false positives, false negatives, and operational risk.

Chinese body structure:
- 风险是什么
- 谁会受影响
- 怎么检查
- 怎么修 / 怎么接入流程
- 注意事项
- 我的判断

English body: a concise brief with risk, affected teams, checks, remediation workflow, caveats, and take.""",

    "regulation_watch": """Write a bilingual legal/regulatory/compliance tracking analysis.

Requirements:
1. Explain what changed in the regulation, policy, standard, or enforcement signal.
2. Prioritize China data regulation, cross-border data transfer, and personal information protection. If sources involve CSL, DSL, PIPL, data export, important data, CIIO, MLPS, generative AI regulation, algorithm recommendation, or deep synthesis, expand that part.
3. Explain the relationship with international rules such as GDPR, EU AI Act, NIS2, DORA, SOC 2, and ISO 27001 when relevant.
4. Explain who is affected: AI products, SaaS, outbound businesses, security teams, data teams, legal/compliance teams, and product teams.
5. Translate requirements into engineering, security, data, and product actions.
6. Do not write legal advice or pretend to be a lawyer.
7. If evidence is limited, state what can currently be confirmed.

Chinese body structure:
- 发生了什么
- 为什么现在重要
- 影响谁
- 工程/安全/数据团队要做什么
- 中国数据监管重点
- 国际规则对照
- 可以提前准备的检查清单
- 风险和不确定性
- 我的判断

English body: a concise brief with what happened, who is affected, engineering/security actions, China data compliance angle, and take.""",
}

ARTICLES = [
    {
        "topic": "Practical AI tools, agent workflows, model APIs, and emerging AI engineering practices",
        "category": "ai",
        "slug": "ai-weekly",
        "style_cycle": ["tool_guide", "trend_explainer"],
        "queries_by_style": {
            "tool_guide": [
                "free LLM API OpenAI compatible long context model tutorial",
                "AI coding agent CLI GitHub open source VS Code extension",
                "MCP server GitHub open source AI agent workflow docs",
                "Cline OpenRouter Claude Code Cursor alternative API pricing guide",
                "LLM evaluation eval harness AI agent tutorial GitHub",
            ],
            "trend_explainer": [
                "AI agent loop recurring agent loop coding workflow",
                "AI harness eval harness agent governance workflow tutorial",
                "vibe coding risks coding agent safety guardrails",
                "Claude Code workflow subagents code review loop",
                "agent orchestration MCP AI workflow best practices",
            ],
        },
    },
    {
        "topic": "Security, privacy, DevSecOps, data compliance, and regulation changes with practical actions",
        "category": "infosec",
        "slug": "infosec-weekly",
        "style_cycle": ["defensive_playbook", "regulation_watch"],
        "queries_by_style": {
            "defensive_playbook": [
                "DevSecOps GitHub Actions tutorial security scanning open source",
                "SBOM open source scanner software supply chain security guide",
                "secret scanning GitHub Actions CI/CD remediation guide",
                "LLM security prompt injection defense checklist",
                "container scanner CVE scanner SAST DAST open source workflow",
            ],
            "regulation_watch": [
                "中国 数据出境 安全评估 个人信息保护法 PIPL 合规 清单",
                "网络安全法 数据安全法 个人信息保护法 CSL DSL PIPL 数据跨境",
                "China data export CAC security assessment PIPL standard contract personal information export",
                "重要数据 关键信息基础设施 CIIO 等保 MLPS 数据合规",
                "生成式人工智能 服务 管理 暂行办法 算法推荐 深度合成 合规",
                "EU AI Act GDPR NIS2 DORA SOC 2 ISO 27001 compliance engineering checklist",
            ],
        },
    },
]

def select_style(article: dict, day_ordinal: int) -> str:
    """Rotate article styles by date for predictable daily variety."""
    cycle = article.get("style_cycle") or ["tool_guide"]
    return cycle[day_ordinal % len(cycle)]
