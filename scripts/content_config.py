"""Content strategy, content types, and rotating topic tracks for weekly publishing."""

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

CONTENT_TYPE_LABELS = {
    "tool_guide": {"cn": "工具攻略", "en": "Tool Guide"},
    "trend_explainer": {"cn": "趋势分析", "en": "Trend Analysis"},
    "defensive_playbook": {"cn": "防御实操", "en": "Defensive Playbook"},
    "regulation_watch": {"cn": "法规追踪", "en": "Regulation Watch"},
}

CONTENT_TYPE_PROMPTS = {
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

WEEKLY_ARTICLE_ROTATION = [
    {
        "category": "ai",
        "content_type": "tool_guide",
        "topic_tracks": [
            {
                "topic": "AI evaluation, tracing, and observability tools that make agent workflows measurable",
                "slug": "ai-evaluation-observability",
                "queries": [
                    "LLM evaluation observability tracing open source GitHub tutorial",
                    "AI agent eval harness regression testing prompt versioning tools",
                    "OpenTelemetry LLM observability agent workflow practical guide",
                ],
            },
            {
                "topic": "Private and local AI deployment tools for teams that cannot send all data to hosted models",
                "slug": "private-local-ai",
                "queries": [
                    "local LLM private deployment OpenAI compatible API open source tutorial",
                    "self hosted AI gateway model routing privacy enterprise GitHub",
                    "local RAG document processing privacy open source deployment guide",
                ],
            },
            {
                "topic": "AI data connectors, knowledge ingestion, and retrieval tools for practical internal workflows",
                "slug": "ai-data-connectors",
                "queries": [
                    "AI data connector knowledge ingestion open source GitHub tool",
                    "RAG data pipeline document sync access control practical guide",
                    "MCP connector enterprise data source open source project",
                ],
            },
            {
                "topic": "Model serving, inference efficiency, and cost-control tools for AI application builders",
                "slug": "ai-inference-efficiency",
                "queries": [
                    "LLM inference serving cost optimization open source tutorial",
                    "model router caching batch inference AI API developer guide",
                    "vLLM llama cpp inference benchmark deployment practical",
                ],
            },
            {
                "topic": "Developer-facing AI coding and automation tools with clear workflow value",
                "slug": "ai-developer-automation",
                "queries": [
                    "AI coding agent CLI GitHub open source developer workflow",
                    "AI developer automation GitHub Actions code review open source",
                    "MCP server developer workflow tool GitHub documentation",
                ],
            },
        ],
    },
    {
        "category": "ai",
        "content_type": "trend_explainer",
        "topic_tracks": [
            {
                "topic": "Reliable AI agent operations: guardrails, approvals, evaluation, and failure recovery",
                "slug": "agent-reliability",
                "queries": [
                    "AI agent reliability guardrails approval workflow evaluation",
                    "agent failure recovery human in the loop engineering practices",
                    "AI agent governance production operations practical guide",
                ],
            },
            {
                "topic": "Multimodal AI workflows moving from demos into developer and operations tooling",
                "slug": "multimodal-workflows",
                "queries": [
                    "multimodal AI workflow developer operations tool practical",
                    "vision language model automation enterprise workflow examples",
                    "voice image document AI agent workflow engineering trend",
                ],
            },
            {
                "topic": "Small models, on-device inference, and hybrid model routing for cost-sensitive teams",
                "slug": "small-model-hybrid",
                "queries": [
                    "small language model on device inference enterprise workflow",
                    "hybrid local cloud LLM routing cost privacy engineering",
                    "quantized model deployment edge AI developer trend",
                ],
            },
            {
                "topic": "AI-assisted software delivery: specification, testing, review, and release workflows",
                "slug": "ai-software-delivery",
                "queries": [
                    "AI assisted software delivery testing review release workflow",
                    "coding agent specification driven development evaluation",
                    "AI code review testing workflow engineering practices",
                ],
            },
            {
                "topic": "Open agent protocols, tool interoperability, and the practical limits of agent ecosystems",
                "slug": "agent-interoperability",
                "queries": [
                    "agent protocol interoperability tool calling open standard",
                    "MCP A2A agent interoperability practical engineering",
                    "AI agent tool ecosystem security reliability limits",
                ],
            },
        ],
    },
    {
        "category": "infosec",
        "content_type": "defensive_playbook",
        "topic_tracks": [
            {
                "topic": "Identity, access, secrets, and service-account defenses for engineering teams",
                "slug": "identity-secrets-defense",
                "queries": [
                    "service account least privilege cloud IAM remediation guide",
                    "secret scanning credential rotation developer workflow",
                    "workload identity access control security checklist",
                ],
            },
            {
                "topic": "Cloud and Kubernetes runtime defenses that teams can monitor and remediate",
                "slug": "cloud-runtime-defense",
                "queries": [
                    "Kubernetes runtime security detection remediation practical",
                    "cloud workload posture IAM network security checklist",
                    "container runtime threat detection open source operations guide",
                ],
            },
            {
                "topic": "Web application and API security controls for modern product teams",
                "slug": "web-api-defense",
                "queries": [
                    "API security authorization testing remediation checklist",
                    "web application security headers session protection practical guide",
                    "OWASP API security defensive engineering workflow",
                ],
            },
            {
                "topic": "Security detection, incident readiness, and log-based investigation workflows",
                "slug": "detection-incident-readiness",
                "queries": [
                    "security detection engineering log investigation workflow",
                    "incident response tabletop cloud engineering checklist",
                    "SIEM detection rule tuning false positive remediation",
                ],
            },
            {
                "topic": "Software supply-chain security beyond SBOM: build provenance, dependencies, and release controls",
                "slug": "software-supply-chain",
                "queries": [
                    "software build provenance dependency security release controls",
                    "SLSA artifact signing CI CD remediation guide",
                    "open source dependency risk maintenance security workflow",
                ],
            },
            {
                "topic": "AI application security and privacy defenses for prompt, data, and tool-use risks",
                "slug": "ai-application-defense",
                "queries": [
                    "LLM application prompt injection defense practical checklist",
                    "AI agent tool use authorization data privacy security guide",
                    "generative AI security logging monitoring remediation",
                ],
            },
        ],
    },
    {
        "category": "infosec",
        "content_type": "regulation_watch",
        "topic_tracks": [
            {
                "topic": "China cross-border data transfer, personal information export, and data localization compliance",
                "slug": "china-cross-border-data",
                "queries": [
                    "中国 数据出境 安全评估 个人信息保护法 PIPL 合规 清单",
                    "China data export CAC security assessment PIPL standard contract personal information export",
                    "中国 数据跨境 个人信息出境 工程 安全 团队 实务",
                ],
            },
            {
                "topic": "China generative AI, algorithm recommendation, and deep synthesis governance for product teams",
                "slug": "china-ai-governance",
                "queries": [
                    "生成式人工智能 服务 管理 暂行办法 产品 合规 工程",
                    "算法推荐 深度合成 互联网信息服务 合规 技术措施",
                    "China generative AI regulation product security compliance checklist",
                ],
            },
            {
                "topic": "Important data, CIIO, MLPS, and cybersecurity compliance operations in China",
                "slug": "china-cybersecurity-operations",
                "queries": [
                    "重要数据 关键信息基础设施 CIIO 等保 MLPS 数据合规",
                    "网络安全法 数据安全法 企业 安全运营 合规 清单",
                    "China MLPS CIIO cybersecurity engineering compliance guide",
                ],
            },
            {
                "topic": "Privacy engineering and accountable data governance across PIPL and GDPR",
                "slug": "privacy-engineering-governance",
                "queries": [
                    "PIPL GDPR privacy engineering data inventory DPIA practical",
                    "个人信息保护 影响评估 数据最小化 工程 实务",
                    "privacy by design data retention access control compliance checklist",
                ],
            },
            {
                "topic": "International AI, cyber-resilience, and assurance rules affecting technical delivery",
                "slug": "international-assurance-rules",
                "queries": [
                    "EU AI Act engineering compliance implementation checklist",
                    "NIS2 DORA cyber resilience technical controls engineering",
                    "SOC 2 ISO 27001 evidence automation security compliance",
                ],
            },
        ],
    },
]


def select_weekly_article(day_ordinal: int) -> dict:
    """Select one weekly content type and rotate its topic track on each return."""
    publish_week = day_ordinal // 7
    article_index = publish_week % len(WEEKLY_ARTICLE_ROTATION)
    article = WEEKLY_ARTICLE_ROTATION[article_index]
    topic_tracks = article["topic_tracks"]
    topic_index = (publish_week // len(WEEKLY_ARTICLE_ROTATION)) % len(topic_tracks)
    topic_track = topic_tracks[topic_index]
    return {
        "category": article["category"],
        "content_type": article["content_type"],
        **topic_track,
    }
