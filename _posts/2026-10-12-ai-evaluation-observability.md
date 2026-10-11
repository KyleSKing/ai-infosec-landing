---
layout: post
title_en: "How to Measure AI Agent Workflows: Opik, Arize Phoenix, Langfuse Guide"
title_cn: "AI Agent 工作流可观测性工具指南：Opik、Phoenix、Langfuse 实测"
date: 2026-10-12 04:07:23 +0800
category: ai
content_type: tool_guide
content_type_cn: "工具攻略"
content_type_en: "Tool Guide"
tags:
  - "AI Evaluation"
  - "LLM Observability"
  - "Agent Tracing"
  - "Open Source"
  - "Tool Guide"
summary_en: "This article compares three open-source tools for tracing and evaluating LLM agents: Opik, Arize Phoenix, and Langfuse. It covers installation, integration, free tiers, and production risks to help teams choose the right observability stack."
summary_cn: "本文对比三个开源 LLM Agent 可观测与评估工具：Opik、Arize Phoenix、Langfuse。涵盖安装集成、免费额度、生产风险，帮助团队选型。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## AI Agent 工作流可观测性工具指南：Opik、Phoenix、Langfuse 实测

# AI Agent 工作流可观测性工具指南：Opik、Phoenix、Langfuse 实测

这篇文章介绍三个主流开源工具——Opik、Arize Phoenix、Langfuse。它们能让你把 Agent 的每一步推理、工具调用、Token 消耗和成本变成可查询的 Trace，并把评估结果关联到具体版本，值得任何跑复杂 Agent 工作流的团队立刻尝试。与其靠日志和猜，不如用它们建立可复现的评估流程，否则 Agent 一旦在线上“抽风”你根本定位不了原因。

## 这是什么

三个工具都是“LLM/Agent 可观测性平台”，核心能力相似：追踪一次请求从用户输入到最终输出的完整链路，记录模型调用、工具执行、上下文检索、Token 用量、延迟和成本，并提供评估功能（Eval）来批量打分。区别在于架构侧重点和集成方式。

**Opik**（CometML 开源）主打“评估 + 追踪 + 仪表盘”一体化。根据其文档，它支持从 RAG 聊天到复杂 Agent 流水线的追踪，能直接把 Prompt 版本关联到对应的 Trace 和评估结果。这意味着当线上回归时，你能逆向定位到是哪个 Prompt 改动导致性能下降。

**Arize Phoenix** 的核心卖点是 OpenTelemetry 原生支持。它通过标准 OTLP 协议接收 Trace，可无缝融入你已有的可观测性栈（如 Grafana、Prometheus），避免厂商锁定。评估工具包含 LLM 评估器、代码指标、人工标注流程，并原生支持 LangChain、LlamaIndex、DSPy 以及 OpenAI、Anthropic、Bedrock 直接调用。

**Langfuse** 是这三个里 GitHub Star 最多的开源项目（截至 2026 年 3 月约 23k+ Star），最近被 ClickHouse 收购。它提供完整的 LLM 工程平台：追踪、提示管理、评估、数据集，自称拥有 78 项功能，适合团队全流程使用。MIT 许可证，隐私上更灵活。

| 工具 | 开源许可 | 核心优势 | 主要作者/维护方 |
|------|---------|---------|----------------|
| Opik | 开源（Apache-2.0） | 评估与追踪强关联 | CometML |
| Arize Phoenix | 开源 | OpenTelemetry 原生，OOTB 评估器 | Arize AI |
| Langfuse | MIT | 功能全，社区大，托管化 | ClickHouse 收购 |

## 怎么用

所有三个工具都支持两种部署方式：云端 SaaS 免费尝鲜，或 Docker 自托管。下面给出最简起步路径。

### 1. 通用集成步骤

无论选哪个，第一步都是注册/启动后端，然后在代码里安装 SDK 并配置 API Key 或本地端点。

- **Opik**：Python 环境执行 `pip install opik`，免费云平台注册后拿到 API Key；自托管则用 Docker 运行 `docker run -d -p 5173:5173 -v opik-data:/opik-data cometml/opik`。配置：`import opik; opik.configure(api_key="...", base_url="...")`。支持 OpenAI SDK 无缝集成——只需把 `OpenAI()` 替换为 `opik.OpenAI()`，自动捕获 Trace。
- **Arize Phoenix**：使用 OpenTelemetry Collector 最省事。`pip install arize-phoenix`，然后启动本地实例 `phoenix serve`。将 OTLP 端点（如 `http://localhost:6006/v1/traces`）配置给你的应用。如果你用 LangChain，直接设置环境变量 `PHOENIX_COLLECTOR_ENDPOINT` 即可，官方提供 LangChain `Tracer` 插件。也支持通过 `phoenix.trace.openai` 包拦截纯 OpenAI 调用。
- **Langfuse**：`pip install langfuse`，云平台创建项目后拿密钥。自托管可 Docker 或直接使用其官方部署模板。集成 OpenAI：调用 `langfuse.openai.OpenAI()` 替代原生对象；LangChain 则通过 `CallbackHandler` 注入。Langfuse 还提供 REST API，适合非 Python 语言。

### 2. 评估与回归测试的接入点

- **Opik** 内置 `evaluate` 函数：定义数据集、评分函数（如用户自定义的 LLM 评判），然后传入一个应用函数，它会跑完整个测试集并输出报告。
- **Phoenix** 提供 `evaluate` API，含预置的 LLM 评估器（如回答相关性、有害性），支持 `llm_eval` 和 `code_eval`，还能人工标注。
- **Langfuse** 通过 `langfuse.evaluations` 模块，可把评估脚本挂到 Trace 上；它支持在测试数据集上批量跑 Prompt 并生成对比报告。

### 3. 高级入口：MCP 与 CI/CD

- 三个工具最近都推出了 **MCP Server**（Model Context Protocol）。例如 Langfuse 的 MCP server 可让 Claude Code 直接查询 Trace 和评估结果；Opik 也有类似 MCP 扩展，允许 Agent 调试工具访问数据。Phoenix 的 MCP 支持还在早期阶段。
- 把它们用进 **GitHub Actions**：每次 PR 推送时，运行一个评估脚本，把结果上报到对应平台的 API，然后评论到 PR。这是最实用的回归测试方式。参考各工具的 Python SDK 都有 `export` 或 `log` 方法，可以写一个 `pytest` 测试用例。

## 适合谁

- 正在生产环境运行多步 Agent（工具调用、搜索、代码生成）的团队，尤其是客服、代码助手、自动化研究等场景。
- 需要证明“Prompt 改动后效果确实提了”的工程团队，或者因上游模型更新导致行为漂移而痛苦的组。
- 已经有 OpenTelemetry 基础设施、不想再引入新数据库的组织——首选 Phoenix。
- 重度依赖 LangChain / LlamaIndex / DSPy 的开发组，三者的集成都很顺滑。

不适合：只做单次提示调用的玩具项目，或已经有监控平台（如 Grafana）但懒得再学新工具的人。另外，如果团队没有能力写评估测试脚本，这三个工具只能给你看日志，带不来实质提升。

## 限制和注意事项

**免费层与价格**：三个工具都有开源免费版和商业托管版，托管版有免费额度但有限。Opik 的云免费版提供一定量的 Trace/评估次数，超出付费；Langfuse 免费版有每月 Trace 量限制，商业版按量计费；Phoenix 开源版完全免费，但 Arieze 的云服务收费。具体数字请以官网为准，因为变化快。

**隐私与数据安全**：如果你用官方云，所有 Trace 数据会经过第三方服务器。对于国内企业，这涉及 **PIPL** 跨境传输数据合规。建议对含个人信息（如用户ID、聊天内容）的应用，必须自托管。三个工具都支持 Docker/私有部署，但需要你维护 PostgreSQL/ClickHouse 等组件——Langfuse 本身基于 ClickHouse，Phoenix 依赖 Arrow 等存储，Opik 需要 SQLite/PostgreSQL。自托管时注意备份。

**稳定性与生产风险**：这三个项目迭代极快，API 可能向后不兼容。目前 Opik 和 Phoenix 的 API 变动较多，Langfuse 相对稳定。不要在生产环境中用它们作为唯一 Trace 存储，最好同时使用标准 OTLP 备份到你的基础监控系统。另外，引入 SDK 会增加一定延迟（每个 Trace 有序列化开销），高并发场景下会拖慢主链路，建议用异步或批处理方式。

**数据误传**：自动捕获会记下所有 LLM 输入输出，如果里面含密钥、个人敏感信息，自托管存储也会成为攻击面。务必配置脱敏规则——三个工具都支持手动屏蔽字段，但默认不开。

## 我的判断

如果团队已经标准化 OpenTelemetry，选 **Phoenix** 没有悬念，它不会被额外锁定。如果主要痛点是“评估跟不上开发速度”——每次改动 Prompt 都靠人肉看结果，那选 **Opik**，因为它把版本、Trace、评估绑得最紧，非常适合 Agent 调试。如果团队规模大、需要提示管理、数据集、协作功能，**Langfuse** 的全栈能力更强，但功能多也意味着上手更复杂。

实测中我最推荐的做法是：先全部用本地 Docker 跑通示例，用同一个 Agent 项目分别接入三个工具，跑 50 次请求 + 一个小的评估集，看哪个部署起来最顺手、查询界面你最习惯。数据上它们差异不大——真正的壁垒在团队工作流是否用得起来。另外注意，当前 AI Agent 的稳定性问题通常是“评估跑太少”，而不是工具不够强，所以不管选哪个，先建立一套可重复的回归数据集，比挑选平台更优先。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## How to Measure AI Agent Workflows: Opik, Arize Phoenix, Langfuse Guide

# How to Measure AI Agent Workflows: Opik, Arize Phoenix, Langfuse Guide

## What this is

AI agents are no longer single prompt calls. They chain tool calls, retrieval steps, and model interactions, which makes failures hard to reproduce and regressions easy to miss. Evaluation, tracing, and observability tools close that gap by connecting what the agent did (traces) with how well it did (evaluations).

Three open-source options dominate the conversation:

- **Opik (CometML)** — an open-source platform for tracing, evaluation, and dashboards. Its key differentiator: prompt versions link directly to the traces and evaluation results they produced, so a regression can be traced back to the exact prompt change.
- **Arize Phoenix** — OpenTelemetry-native observability. It accepts traces via the standard OTLP protocol, so it fits existing observability stacks without vendor lock-in. Includes LLM-based evaluators, code-based metrics, human annotation, and instrumentation for LangChain, LlamaIndex, DSPy, and direct API calls.
- **Langfuse** — the open-source leader by adoption (28k+ GitHub stars, MIT license, recently acquired by ClickHouse). Covers tracing, prompt management, evaluation, datasets, and a large feature set for the full LLM engineering workflow.

Why it matters now: agent workflows are non-deterministic and multi-step. A single prompt change can break a downstream tool call or retrieval path. Without tracing + eval tied to versions, teams debug by guessing. The key differentiator is whether a prompt version links to the evaluation results and production traces it produced.

Practical next steps:
1. Start with OpenTelemetry-native tracing (Arize Phoenix) if you already run an OTel stack; use OTLP to avoid vendor lock-in.
2. If you want an all-in-one open-source platform, try Langfuse for tracing + prompt management + evaluation.
3. If you want eval harness tightly coupled to prompt versions and production traces, try Opik: log traces, annotate, run evals, and link prompt versions to results.
4. Set up regression checks: run a fixed eval set before and after prompt/model changes; trace regressions back to the exact prompt version.
5. Add LLM-based evaluators, code-based metrics, and human annotation.

Risks: no definitive best tool; each has tradeoffs. OpenTelemetry-native (Phoenix) avoids vendor lock-in. Langfuse acquired by ClickHouse — consider governance. Don't over-rely on LLM-as-judge; need human annotation. Tools don't fix bad eval design.

Take: start with one tool, wire tracing first, then eval harness.

Let me write 300-500 words. Markdown body only.# How to Measure AI Agent Workflows: Opik, Arize Phoenix, Langfuse Guide

## What this is

AI agents are no longer single prompt calls. They chain tool use, retrieval, and multi-step reasoning, which makes failures hard to reproduce and even harder to attribute. Three open-source tools have become the practical baseline for making agent workflows measurable:

- **Opik (CometML)** — an open-source platform for tracing, evaluation, and dashboards. Its key design point: prompt versions link directly to the traces and evaluation results they produced, so a regression can be traced back to the exact prompt change.
- **Arize Phoenix** — OpenTelemetry-native observability. It accepts traces via the standard OTLP protocol, so it fits existing observability stacks without vendor lock-in. Includes LLM-based evaluators, code-based metrics, and human annotation, with first-class instrumentation for LangChain, LlamaIndex, DSPy, and direct OpenAI/Anthropic/Bedrock calls.
- **Langfuse** — open source LLM engineering platform (recently acquired by ClickHouse), with 23k-28k GitHub stars depending on source date. Covers tracing, prompt management, evaluation, datasets, and session tracking.

Why it matters now: Agent workflows are non-deterministic and multi-step. A single prompt change can break a downstream tool call or retrieval path. Without tracing and eval harnesses, teams debug by guessing. The tools above connect prompt versions to traces and evaluation results, so regressions can be traced to the exact change.

Practical next steps:
- Start with OpenTelemetry-native tracing (Arize Phoenix) if you already have an observability stack, to avoid vendor lock-in.
- Use Opik if you want prompt versions linked directly to traces and eval results, so regressions map to exact prompt changes.
- Use Langfuse if you want the most complete open-source platform with prompt management, datasets, and evaluation.
- Build a repeatable

</div>

---

### 参考来源 / Sources

- [A Practical Guide to Integrate Evaluation and Observability into LLM Apps](https://www.dailydoseofds.com/a-practical-guide-to-integrate-evaluation-and-observability-into-llm-apps)
- [Best LLM Observability Tools in 2026](https://www.firecrawl.dev/blog/best-llm-observability-tools)
- [7 best free and open source LLM observability tools](https://posthog.com/blog/best-open-source-llm-observability-tools)
- [Best Prompt Management & Versioning Tools for AI Agents](https://www.comet.com/site/blog/prompt-management-tools)
- [Best AI Evaluation Tools for Prompt Experimentation in 2026 - Confident AI](https://www.confident-ai.com/knowledge-base/compare/best-ai-evaluation-tools-for-prompt-experimentation-2026)
