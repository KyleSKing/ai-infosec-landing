---
layout: post
title_en: "AI Agent Loops & Harnesses: The New Engineering Practice for Reliable Autonomous Workflows"
title_cn: "AI Agent循环与治理框架：可靠自主工作流的工程新实践"
date: 2026-06-22 01:19:16 +0800
category: ai
content_type: trend_explainer
content_type_cn: "趋势分析"
content_type_en: "Trend Analysis"
tags:
  - "AI Agent"
  - "Agent Loop"
  - "Agent Harness"
  - "Claude Code"
  - "Codex"
summary_en: "AI agent loops (perceive-reason-plan-act-observe) are becoming built-in features in coding tools like Claude Code and Codex, replacing custom infrastructure. Agent harnesses emerge as governance layers ensuring reliability, observability, and compliance, with engineering practices maturing into 4-12 week build cycles."
summary_cn: "AI agent循环（感知-推理-规划-执行-观察）正成为Claude Code、Codex等编码工具的内置功能，取代自定义基础设施。Agent治理框架作为保证可靠性、可观测性和合规性的治理层出现，工程实践已成熟至4-12周构建周期。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## AI Agent循环与治理框架：可靠自主工作流的工程新实践

# AI Agent 循环与治理框架：可靠自主工作流的工程新实践

## 这个趋势是什么

2026 年上半年，AI Agent 的开发范式正在从“写一个 prompt + 调一个 API”转向**工程化循环（Loop）与可治理的无人机架（Harness）**。简单说，你不再把大模型当作单次问答工具，而是让它在一个**感知—推理—规划—行动—观察**的闭环中反复迭代，直到完成复杂任务。同时，你需要给这个循环套上一层基础设施：工具权限、状态管理、数据溯源、评估与监控——这就是“Harness”。

代表性进展：
- Claude Code 内置了 `/loop` 命令、cron 调度和动态工作流，无需自己搭编排层。
- Codex 推出 Automations 标签页，支持定时任务和子 Agent 派生。
- METR 最新基准显示，Claude Opus 4.6 可在 12 小时内完成 50% 的测试任务，而一年前的 Opus 4 据能处理最长 1 小时 40 分钟的任务——天花板前移了约 **6 倍**。

这不是 demo，而是正在进入生产环境的工程模式。

## 为什么现在重要

过去一年，Agent 的主要瓶颈不是模型能力，而是**稳定性与治理**。单次调用很容易做，但要让 Agent 自主运行数小时、数十小时，处理不断变化的状态，并且不出错、不泄密、可审计，就必须把循环和治理当成基础设施来建。

三点核心驱动：
1. **模型上下文的延长**让 Agent 可以维持更长的感知-行动-观察循环，不再频繁“失忆”。
2. **工具生态成熟**：Claude Code、Codex、Cursor 等 IDE 工具原生支持循环调度，LangGraph、CrewAI、Mastra、OpenAI Agents SDK 提供编排框架。
3. **企业合规压力**：自主工作流越多，越需要可追溯、可回放、可审计的 governance。没有 Harness 的 Agent 无法通过 SOC 2 或 PIPL 审查。

## 它和旧做法的区别

| 维度 | 旧做法 | 新实践 |
|------|--------|--------|
| 任务长度 | 每次对话独立，任务上限 1-2 小时 | 12 小时+ 的连续任务，通过循环维持上下文 |
| 编排方式 | 手动写 while 循环、自建状态管理 | 框架原生提供 Loops、Cron、子 Agent 调度 |
| 可靠性 | 缺乏可观测性，失败后难以定位 | Harness 包含评估、日志、WORM 审计、Merkl 验证 |
| 数据治理 | 依赖模型自身的记忆或纯提示 | 用认证数据层、指标标定提升 SQL 准确率 38% |
| 部署复杂度 | 需要自定义基础设施 | 4-12 周可搭建生产级 Harness，代码量 5000-20000 行 |

旧模式里，Agent 是**一次性工具**；新模式里，Agent 是**持续的在线工作者**。

## 可以怎么开始试

### 第一步：选择一个自带循环能力的工具（1 天）
如果你在写代码任务，直接使用 **Claude Code** 的 `/loop` 命令，或 **Codex** 的 Automations 标签页。这些工具已经把循环、定时、子 Agent 拆成了配置项，你只需要定义任务和目标。

### 第二步：理解并定义你的 Agent Loop（2-3 天）
画出你自己的五个阶段：**感知**（输入源是什么）、**推理**（用哪个模型、怎么组织 context）、**规划**（有没有子任务拆分逻辑）、**行动**（工具集：API、数据库、文件系统）、**观察**（如何捕捉结果、异常、超时）。不需要一开始写代码，先用流程图记录。

### 第三步：引入 Harness 组件（2-4 周）
参考 Atlan 的研究或开源项目（如 [ai-agent-eval-harness](https://github.com/najeed/ai-agent-eval-harness)），逐步添加：
- **状态保存与回放**：每次循环的输入输出写入 Flight Recorder。
- **权限与沙箱**：用 Docker 隔离 Agent 执行环境，用 OIDC 控制 API 访问。
- **评估与监控**：设置 drift gauge 仪表盘，对比预期输出与实际结果。
- **审计日志**：采用 WORM（一次写入多次读取）方式记录循环全程，防止篡改。

### 第四步：压测并迭代（1-2 周）
拿一个你现有的业务流程（比如自动化 bug 分类、数据清洗、报告生成），让 Agent 连续执行 10 次，观察错误率、超时率、资源消耗。收集失败案例，调整 prompt 或添加 retry 策略。

### 适合人群
- **AI 工程师**：需要搭建生产级 Agent 服务的团队。
- **DevSecOps / 安全工程师**：关注 Agent 的访问控制和审计。
- **SaaS 产品经理**：想在产品内嵌入自主工作流功能。
- **合规负责人**：需要证据体系证明 Agent 行为可追溯。

### 不适合人群
- **只做实验性 Prototype**：如果任务不超过 5 分钟，不需要 Loop 和 Harness。
- **没有明确长期任务需求的团队**：Loop 的价值在于连续运行，如果每个任务都是独立的，传统 prompt 即可。

## 风险和限制

1. **成本不可控**：Agent 循环可能产生远高于预期的 token 消耗，尤其在没有设置预算上限或停止条件时。必须加上 max_steps 和 cost_watch。
2. **错误级联**：一个错误的观察结果会导致后续整个链路的偏差。需要引入“checkpoint”和人工审核节点。
3. **安全风险**：Agent 自主调用 API 可能导致数据泄露或越权。必须用 Harness 的权限层（OIDC、沙箱）限制工具范围。
4. **可解释性不足**：即使有审计日志，LLM 的推理过程仍然难以完全还原。可能需要引入“推理追踪（trace）”辅助。
5. **依赖特定工具生态**：目前 Claude Code 和 Codex 的 Loop 功能与自家模型深度绑定，迁移成本较高。

## 我的判断

**Agent Loop + Harness 是 2026 年 Agent 从 Demo 走向生产的必须基础设施**。过去我们高估了 prompt 工程，低估了循环和治理的重要性。现在的事实是：模型能力已经足够支持数小时的任务，但缺乏有效循环管理的项目往往在 prototype 阶段就停滞。

开源 eval harness 和商业工具的同步成熟，使得构建生产级 Agent 的门槛大幅降低。我建议任何计划上线自主 Agent 的团队，**先花 1 周定义你的 Loop 和 Harness 需求，再用 4 周搭建最小可行版本，比直接调模型跑任务更高效**。

同时也请记住：治理不是事后修补，而是从第一天就要嵌入的。选择框架时，优先考虑自带审计、状态管理和权限模型的方案（如 LangGraph + 自定义工具，或直接使用 Claude Code 的企业版）。不要等到 Agent 出错或合规审计上门才后悔。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## AI Agent Loops & Harnesses: The New Engineering Practice for Reliable Autonomous Workflows

# AI Agent Loops & Harnesses: The New Engineering Practice for Reliable Autonomous Workflows

## What It Is

An AI agent loop is the iterative execution cycle that enables autonomous task completion: **perceive → reason → plan → act → observe**. The loop repeats until the task finishes or a stop condition is met. An AI agent harness is the surrounding infrastructure that makes the loop reliable — tools, state management, permissions, evals, observability, and governed data. Together they form the production foundation for autonomous AI agents.

## Why It Matters Now

The ceiling for autonomous agent tasks has moved dramatically. METR benchmarks show Claude Opus 4.6 completing 50% of tasks that take 12 hours — a 6x jump from a year ago when the same model topped out at 1 hour 40 minutes. Built-in loop support has arrived: Claude Code ships `/loop`, cron scheduling, and dynamic workflows; Codex offers recurring schedules and subagent spawning. You no longer need custom infrastructure for basic loops.

But loops alone aren't enough. Without a harness, agents run ungoverned — no evals, no permission boundaries, no audit trail. Research across 522 enterprise queries shows that governed metadata lifts SQL accuracy by 38% (2.15x on medium-complexity queries). Building a production harness takes 4–12 weeks and 5,000–20,000 lines of infrastructure code.

## Practical Next Steps

1. **Start with built-in loops** — Use Claude Code's `/loop` or Codex Automations for recurring, well-scoped tasks before building custom loops.
2. **Design a minimal harness early** — Define state schema, tool permissions, logging, and basic evals before scaling.
3. **Run evals on every loop iteration** — Governed metadata and structured evaluations catch failures early. Open-source eval harnesses exist (e.g., the MultiAgentOps verification harness on GitHub).
4. **Add observability and audit logs** — WORM (write once, read many) logs, cryptographic sealing, and drift gauges help trace agent decisions and meet compliance requirements.
5. **Sandbox execution** — Use hardened Docker isolation for code execution; gate file system and network access.

## Risks & Limits

- **Cost and latency** — Each loop iteration incurs LLM API costs and response time. Complex planning steps can slow throughput.
- **Harness complexity** — Building a full harness takes weeks. Teams often skip evals and permission boundaries, leading to unreliable or insecure agents.
- **State corruption** — If the harness does not enforce data integrity, agents can operate on stale or polluted context.
- **Security surface** — Agents with tool access and loop autonomy increase attack surface. Without proper sandboxing and audit, a compromised agent can cause real damage.

## Take

Agent loops are the engine; agent harnesses are the chassis. For production autonomous workflows, you need both. Start with built-in loop support from Claude Code or Codex, but invest early in a minimal harness — evals, governed data, and permission boundaries. The models are ready; your engineering practice needs to catch up. The teams that ship reliable autonomous agents will be those that treat harness engineering as a first-class concern, not an afterthought.

</div>

---

### 参考来源 / Sources

- [Loop Engineering: How to Build AI Agent Loops That Run ...](https://www.requesty.ai/blog/loop-engineering-how-to-build-ai-agent-loops-that-run-themselves)
- [What Is the AI Agent Loop? The Core Architecture Behind ...](https://blogs.oracle.com/developers/what-is-the-ai-agent-loop-the-core-architecture-behind-autonomous-ai-systems)
- [Agent Loops: Complete Guide (Claude Code + Codex) - YouTube](https://www.youtube.com/watch?v=RVEaDvh6f5A)
- [How to Build an AI Agent Harness: Step-by-Step Tutorial (2026) - Atlan](https://atlan.com/know/how-to-build-ai-agent-harness)
- [GitHub - najeed/ai-agent-eval-harness: The open-source MultiAgentOps evaluation and verification harness for any industry business workflow. · GitHub](https://github.com/najeed/ai-agent-eval-harness)
