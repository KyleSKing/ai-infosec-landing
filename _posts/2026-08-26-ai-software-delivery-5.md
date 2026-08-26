---
layout: post
title_en: "Spec-Driven AI Software Delivery: From Vibe Coding to Controlled Release Workflows"
title_cn: "规范驱动开发：从随意编程到可控交付"
date: 2026-08-26 19:24:54 +0800
category: ai
content_type: trend_explainer
content_type_cn: "趋势分析"
content_type_en: "Trend Analysis"
tags:
  - "spec-driven development"
  - "AI-assisted testing"
  - "release automation"
  - "coding agents"
  - "DevEx"
summary_en: "AI-assisted software delivery is shifting from ad-hoc vibe coding to spec-driven workflows where clear specifications guide coding agents through implementation, testing, review, and release. This trend reduces errors, preserves context across sessions, and keeps human oversight on business-critical decisions."
summary_cn: "AI辅助软件交付正从随意的vibe coding转向规范驱动开发，清晰规范引导编码代理完成实现、测试、审查和发布。该趋势减少错误、跨会话保留上下文，并让人工保持对业务关键决策的掌控。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 规范驱动开发：从随意编程到可控交付

# 规范驱动开发：从随意编程到可控交付

## 这个趋势是什么

“规范驱动开发”（Spec-Driven Development）正在成为AI辅助编码时代的一种新工作范式。它的核心流程是：在让AI代理（coding agent）写代码之前，先由人编写一份清晰的、结构化的规范文档（通常用Markdown），定义要构建的功能、技术栈、验收标准、边界条件等。然后，AI代理根据这份规范生成代码，人再对代码进行审查和测试。这与当前流行的“vibe coding”（凭感觉编程）形成鲜明对比——后者依赖开发者或产品经理口头描述需求，AI直接生成代码，结果往往与预期偏差很大。

这个趋势由Andrew Ng的DeepLearning.AI与JetBrains合作推出的课程《Spec-Driven Development with Coding Agents》正式推向大众。课程讲师Paul Everitt指出，许多顶尖开发者已经在使用这种方式：先写规范，再让AI实现。规范不仅控制代码生成，还能在多个AI会话之间保持上下文，减少认知负荷，提高意图保真度。

与此同时，AI辅助软件交付的其他环节也在规范化：自动化测试生成、代码审查的两阶段（自动扫描+人工聚焦）、发布说明的AI自动生成（如GitProtect在Jira工作流中的实践）等。这些共同构成了一个更可控的AI驱动交付流水线。

## 为什么现在重要

过去两年，AI编码工具（如GitHub Copilot、Claude Code、Cursor等）大幅降低了代码生成的门槛。开发者可以快速产出大量代码，但随之而来的是“代码质量失控”问题：AI生成的代码可能逻辑正确但不符合业务意图，或者遗漏了边界情况，甚至引入安全漏洞。在团队协作中，缺乏统一规范的AI生成代码会导致维护成本飙升。

规范驱动开发解决了三个关键痛点：

1. **意图对齐**：AI不理解业务上下文，但规范可以精确描述。例如，一个“用户注册”功能，规范可以写明“邮箱地址必须支持土耳其字符İ”，AI生成测试时就会覆盖这个边界。
2. **上下文持久化**：AI会话是短暂的，但规范是持久文档。下次继续开发时，AI可以重新加载规范，无需重复解释。
3. **可审查性**：人审查AI代码时，规范是唯一的评判标准。没有规范，审查者只能凭感觉判断“这代码对不对”。

此外，从工程管理角度看，规范驱动开发让AI的产出变得可预测、可度量。FirstLine Software的文章指出，AI加速工程工作流的关键在于“将规范、审查和批准保留在人类手中”，而将实现、测试脚手架和文档任务分配给AI代理。这种分工提高了交付速度，同时保持了控制。

## 它和旧做法的区别

| 维度 | 旧做法（vibe coding / 无规范） | 规范驱动开发 |
|------|-------------------------------|--------------|
| 需求传递 | 口头描述、即时聊天、模糊的Jira ticket | 结构化的Markdown规范，包含验收标准、边界条件 |
| AI角色 | 直接生成代码，人被动接受 | 根据规范实现，人主动定义 |
| 审查方式 | 人通读代码，凭经验判断 | 自动扫描逻辑/安全/风格问题，人工聚焦业务逻辑 |
| 测试覆盖 | AI生成通用测试，遗漏业务边界 | 规范驱动测试生成，人工补充领域专家案例 |
| 上下文保持 | 每次新会话需要重新描述 | 规范作为持久上下文，跨会话复用 |
| 变更控制 | 难以追溯“为什么这样写” | 规范版本化，变更先改规范 |

具体例子：在旧做法中，开发者告诉AI“写一个日期验证函数”，AI可能生成一个检查YYYY-MM-DD格式的函数，但忽略了闰年或2月30日。在规范驱动开发中，规范会明确列出“必须验证日期存在性，包括闰年、月份天数、2月29日仅在闰年有效”，AI生成的测试就会覆盖这些边界。

## 可以怎么开始试

以下是一个可立即执行的步骤清单，适用于个人开发者或团队：

1. **选择一个项目**：最好是一个新功能或重构任务，避免在遗留代码中首次尝试。
2. **编写规范文档**：用Markdown创建`spec.md`，包含：
   - 功能名称和目标
   - 技术栈和约束（例如“使用Python 3.11+，依赖FastAPI”）
   - 输入/输出定义
   - 正常路径和异常路径（至少5个边界案例）
   - 验收标准（例如“所有测试通过，无安全警告”）
3. **配置AI代理**：使用支持规范驱动的工具（如Claude Code、Cursor的Agent模式、JetBrains AI Assistant）。将规范文件作为系统提示或初始上下文。
4. **迭代生成**：让AI根据规范生成代码和测试。每次生成后，对照规范检查：
   - 是否所有验收标准都实现了？
   - 是否有未在规范中定义的额外行为？
   - 测试是否覆盖了规范列出的边界？
5. **两阶段审查**：
   - 第一阶段：自动扫描（使用linter、SAST工具、类型检查器）检测逻辑错误、安全弱点、风格违规。
   - 第二阶段：人工审查，聚焦业务逻辑和规范中未覆盖的领域专家案例。
6. **更新规范**：如果发现规范遗漏，先更新规范，再让AI重新生成。规范是“真理源”。
7. **纳入CI/CD**：将规范文档作为制品，与代码一同版本化。可以在CI中检查规范是否与代码一致（例如，通过关键字匹配或自定义脚本）。

对于团队，可以进一步：
- 建立规范模板库（如“API端点规范”、“数据处理规范”）。
- 在Jira ticket中嵌入规范链接，让AI在生成代码时自动读取。
- 使用AI自动生成发布说明（如GitProtect的做法），但确保发布说明基于规范变更而非代码差异。

## 风险和限制

- **规范本身可能不完整**：如果规范写得太粗略，AI仍然会产出不符合预期的代码。规范驱动开发并不降低对领域知识的要求，反而要求开发者具备更强的抽象和定义能力。
- **过度规范导致僵化**：对于快速原型或探索性任务，写详细规范可能拖慢速度。规范驱动更适合有明确需求的生产级功能。
- **AI对规范的理解偏差**：当前AI模型对长文档的上下文理解仍有限，规范过长或逻辑复杂时，AI可能遗漏细节。建议规范控制在500-1000字以内，或分模块。
- **团队协作成本**：规范需要维护和同步，多人编写规范时可能产生冲突。需要引入规范审查流程。
- **安全风险**：AI生成的代码可能包含漏洞，规范中应包含安全要求（如输入验证、权限检查），但自动扫描不能替代人工安全审查。

## 我的判断

规范驱动开发不是“银弹”，但它是当前AI辅助编码中最务实的进步。它把AI从“黑盒生成器”变成了“可解释的执行器”，让人重新回到控制位。对于任何需要长期维护、多人协作或合规要求的项目，规范驱动开发应该成为默认工作流。

建议团队在下一个迭代中，选一个中等复杂度的功能，完整走一遍“写规范→AI实现→两阶段审查→更新规范”的循环。你会立即感受到：虽然前期写规范多花了30分钟，但后期调试和返工的时间减少了至少一半。

**适合人群**：工程经理、DevEx负责人、需要交付可靠产品的开发者、合规敏感团队。

**不适合人群**：纯探索性黑客马拉松、一次性脚本编写、对代码质量无要求的快速原型。

**风险提示**：不要迷信AI能理解所有规范。始终保留人类对“规范是否合理”的最终判断权。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## Spec-Driven AI Software Delivery: From Vibe Coding to Controlled Release Workflows

# Spec-Driven AI Software Delivery: From Vibe Coding to Controlled Release Workflows

**What it is**

A structured workflow where AI agents handle implementation, test scaffolding, and release documentation—but humans own specification, review, and approval. The key shift: moving from "vibe coding" (AI writes code from vague prompts) to **spec-driven development**, where a detailed markdown spec defines what to build, and the coding agent implements against it.

**Why it matters now**

- Vibe coding produces code that often doesn't match intent, creating rework and security holes.
- Engineering teams need to scale delivery without multiplying headcount or risks.
- CI/CD pipelines are integrating AI agents for test generation, vulnerability scanning, and release note summarization. The bottleneck is no longer code generation—it's **spec quality and review capacity**.

**How it works in practice**

1. **Specification** – A human writes a "project constitution": tech stack, mission, roadmap, and per-feature specs in markdown. This preserves context across agent sessions.
2. **Implementation** – AI agents (Claude Code, JetBrains AI, Copilot) generate code against the spec, reducing hallucination and misalignment.
3. **Automated review** – First pass by AI scanners for logic errors, security weaknesses, style violations.
4. **Human review** – Domain experts focus on edge cases AI can't anticipate (e.g., a Turkish character in an email field). This is the highest-value human contribution.
5. **Release automation** – AI pulls Jira tickets, writes release notes, categorizes changes, and posts to Slack/email/Confluence with consistent templates.

**Practical next steps for teams**

- Write a spec before any AI coding session. Start with a one-page markdown defining scope, constraints, and success criteria.
- Add a CI step that validates spec coverage in generated code (e.g., all listed test cases exist).
- Assign humans to review only "less obvious failures" specific to your domain—not generic patterns AI already handles.
- Automate release note generation from Jira metadata but require a human final sign-off.

**Risks and operational notes**

- Specs become stale quickly if not maintained alongside code. Treat spec as a living document, not a one-time artifact.
- AI-generated tests cover happy paths but miss business-specific edge cases. You need domain experts, not just QA generalists.
- Release notes generated from Jira tickets may miss context that a developer's commit message captures. Consider combining both sources.
- Over-reliance on AI for review can introduce consistent blind spots. Rotate human reviewers to catch different error types.

**Who this is for** – Engineering managers, DevEx leads, and teams shipping production software with velocity requirements.

**Who this is not for** – Solo prototypes, exploratory research, or teams without strong spec-writing discipline.

**Take**

Spec-driven delivery doesn't slow teams down—it reduces the rework cycles that vibe coding creates. The fastest way to ship is to slow down on spec writing. Teams that adopt this pattern report fewer post-deployment incidents, lower review fatigue, and better alignment between AI output and product intent. The workflow is mature enough to adopt today: write the spec, let the agent code, review the edge cases, and automate the release notes.

</div>

---

### 参考来源 / Sources

- [AI-Assisted Software Development: Workflow, Risks & ROI](https://devcom.com/tech-blog/ai-assisted-software-development)
- [AI-Accelerated Engineering Workflow: Ticket to Merge](https://firstlinesoftware.com/blog/blog-ai-accelerated-engineering-workflow)
- [How AI Automation Is Transforming Release Notes & Reports](https://gitprotect.io/blog/how-ai-automation-is-transforming-release-notes-reports)
- [Spec-Driven Development with Coding Agents](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents)
- [New course: Spec-Driven Development with Coding ...](https://www.facebook.com/andrew.ng.96/videos/new-course-spec-driven-development-with-coding-agents-built-in-partnership-with-/1509071804123051)
