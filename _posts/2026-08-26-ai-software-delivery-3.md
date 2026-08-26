---
layout: post
title_en: "From Vibe Coding to Spec-Driven: AI-Assisted Software Delivery Workflow"
title_cn: "从Vibe Coding到Spec驱动：AI辅助软件交付工作流"
date: 2026-08-26 18:47:41 +0800
category: ai
content_type: trend_explainer
content_type_cn: "趋势分析"
content_type_en: "Trend Analysis"
tags:
  - "AI-assisted software delivery"
  - "spec-driven development"
  - "coding agents"
  - "test automation"
  - "release automation"
summary_en: "Spec-driven development replaces vibe coding by using detailed markdown specs to guide AI agents, improving intent fidelity. AI automates test generation, code review scans, and release notes, while humans focus on edge cases and business logic validation."
summary_cn: "规范驱动开发取代了vibe coding，通过详细规格说明书引导AI agent，提高意图一致性。AI自动生成测试、代码审查扫描和发布说明，人类专注于边界情况和业务逻辑验证。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 从Vibe Coding到Spec驱动：AI辅助软件交付工作流

# 从Vibe Coding到Spec驱动：AI辅助软件交付工作流

## 这个趋势是什么

2026年，AI辅助软件开发的讨论已经从“能不能用AI写代码”转向了“怎么用AI写对代码”。一个清晰的分水岭正在形成：一端是Vibe Coding——让AI自由生成代码，开发者凭感觉验收；另一端是Spec-Driven Development（规范驱动开发）——先写详细的Markdown规范，再让编码Agent按规范实现。

这不是一个学术概念。DeepLearning.AI与JetBrains合作推出的课程《Spec-Driven Development with Coding Agents》已经将这套方法系统化，Paul Everitt在课程中展示了如何通过“项目章程（Project Constitution）”、迭代验证循环和跨会话上下文保持，让AI输出始终对齐开发者的真实意图。

同时，FirstLine Software和DevCom的工程团队正在生产系统中实践AI加速的交付工作流：从Ticket到Merge的全链路中，AI负责实现、测试脚手架和文档生成，而规范制定、代码审查和发布审批仍然由人掌控。

## 为什么现在重要

Vibe Coding的致命缺陷正在暴露：AI生成的代码看起来对，但经常不对。一个典型的例子是，AI会为“有效邮箱”和“有效日期”生成通用测试模式，但完全忽略土耳其字符对文本处理的影响——这种业务边界问题，AI无法自己发现。

更深层的问题是，Vibe Coding产生的代码缺乏可维护性。没有规范约束，AI每次生成的代码结构可能完全不同，跨会话上下文丢失，项目越大越混乱。这直接导致了“认知债务（Cognitive Debt）”的累积——你花在理解AI为什么这么写上的时间，超过了你自己写的时间。

Spec-Driven Development解决的就是这个问题：用规范锁定意图，让AI在边界内执行。这不是让开发者写更少的规范，而是写更精确的规范，然后把实现交给AI。

## 它和旧做法的区别

| 维度 | 传统开发 | Vibe Coding | Spec-Driven Development |
|------|----------|-------------|------------------------|
| 规范 | 详细PRD+技术设计文档 | 无规范或口头描述 | 轻量Markdown规范，聚焦边界和行为 |
| 实现 | 开发者手写 | AI自由生成 | AI按规范实现 |
| 测试 | 开发者手写测试用例 | AI自动生成，但常遗漏边界 | AI生成基础测试，人工补充业务边界测试 |
| 审查 | 人工逐行审查 | 人工凭感觉验收 | 两轮审查：AI自动化扫描+人工聚焦业务逻辑 |
| 发布 | 手动整理Release Notes | 无结构化输出 | AI自动生成Release Notes，基于Jira/版本元数据 |

关键区别在于：**Spec-Driven不是让人少写代码，而是让人把精力从“怎么写”转移到“要什么”上。**

## 可以怎么开始试

### 第一步：写一份“项目章程”

这不是完整的PRD，而是一份1-2页的Markdown文件，包含：
- 项目目标和边界
- 技术栈和约束（例如“必须兼容Node 18+，不能引入新依赖”）
- 核心功能列表及其验收标准
- 已知的非功能性需求（性能、安全、可观测性）

### 第二步：为每个功能写“Feature Spec”

每个功能一个Markdown文件，结构如下：
```markdown
## Feature: 用户注册
### 输入
- 邮箱（必须符合RFC 5321，支持国际化域名）
- 密码（至少8位，含大小写和数字）
- 邀请码（可选，6位字母数字）

### 行为
1. 验证邮箱格式，无效则返回400
2. 检查邮箱是否已注册，已注册返回409
3. 密码哈希存储（使用bcrypt，cost=12）
4. 生成验证邮件链接（有效期24小时）

### 边界情况
- 邮箱包含土耳其字符（ı, ş, ç）
- 密码包含Unicode字符
- 邀请码过期
- 并发注册同一邮箱
```

### 第三步：让Agent按Spec实现

使用Claude Code、Cursor或JetBrains AI Assistant，将Spec作为上下文输入。关键操作：
- 每次会话开始时，先加载项目章程和当前Feature Spec
- 要求Agent在实现前先输出实现计划
- 实现完成后，要求Agent对照Spec逐条验证

### 第四步：两轮测试策略

- **第一轮（AI自动化）**：让AI从现有代码生成测试，覆盖所有预期成功路径
- **第二轮（人工补充）**：领域专家补充AI无法预见的业务边界测试（如土耳其字符、并发竞态、第三方API超时）

### 第五步：自动化Release Notes

在Jira或GitHub中，让AI基于Ticket元数据、PR描述和Changelog自动生成Release Notes。GitProtect的实践表明，AI可以按项目、版本、Sprint或标签自动分类，并输出到Slack、邮件或Confluence。

## 风险和限制

1. **规范质量决定一切**：如果Spec写得模糊或错误，AI会放大这些错误。Spec-Driven不会降低对开发者业务理解能力的要求。
2. **AI无法处理非结构化需求**：当需求本身在探索阶段、频繁变动时，写Spec的成本可能超过收益。Spec-Driven更适合需求相对明确的场景。
3. **测试盲区依然存在**：AI生成的测试覆盖的是“它知道的路径”，不是“所有路径”。业务边界测试必须由人补充。
4. **工具链成熟度差异**：不同AI Agent对Spec的理解能力不同。Claude Code和JetBrains的Agent对结构化Markdown支持较好，但仍有解析偏差。
5. **团队习惯转变成本**：从“写代码”到“写规范”的思维转变需要时间。团队中如果没有人能写出好Spec，这个流程会失败。

## 适合人群

- **工程经理和DevEx负责人**：需要理解AI在交付流程中的准确角色，以及如何重新分配团队精力
- **独立开发者和小团队**：可以用Spec-Driven快速验证想法，同时保持代码可维护性
- **需要频繁交付的SaaS团队**：自动化测试和Release Notes生成可以显著缩短交付周期

## 不适合人群

- **探索阶段的原型团队**：需求每天都在变，写Spec的成本太高
- **对AI输出完全信任的团队**：Spec-Driven的前提是“AI会犯错，规范来兜底”
- **没有领域专家的团队**：业务边界测试必须由懂业务的人完成

## 我的判断

Vibe Coding是AI辅助开发的“野蛮生长”阶段，它证明了AI能写代码，但没解决“写对代码”的问题。Spec-Driven Development是行业走向成熟的关键一步——它把AI从“代码生成器”升级为“可执行的规范解释器”。

这个趋势的核心洞察是：**AI辅助开发的瓶颈不在AI的能力，而在人如何定义需求。** 写得好的Spec，能让AI的输出质量提升一个数量级；写得差的Spec，AI会帮你制造一个数量级的混乱。

未来12个月，我预计：
- 更多IDE和Agent工具会原生支持Spec模板和规范验证
- 团队会开始建立“Spec Review”作为独立环节，与Code Review并行
- 出现专门的“Spec工程师”角色，负责将产品需求转化为AI可执行的规范

现在就开始试：选一个下周要开发的小功能，写一份Feature Spec，用AI Agent实现，然后对比一下和Vibe Coding的结果。你会立刻看到差异。

---

## English Brief

**Trend**: The shift from Vibe Coding (AI generates code freely, developers approve by feel) to Spec-Driven Development (write a detailed Markdown spec first, then let AI agents implement against it).

**Why now**: Vibe Coding produces code that looks correct but misses business-critical edge cases (e.g., Turkish characters in email validation). It creates cognitive debt and lacks maintainability. Spec-Driven Development locks intent in a spec, reduces cognitive debt, and keeps AI aligned with what you actually want.

**Difference from old practice**: Traditional dev writes detailed PRD + code by hand. Vibe Coding skips specs. Spec-Driven writes lightweight but precise specs, then delegates implementation to AI. The human shifts from "how to write" to "what to build."

**First steps**:
1. Write a 1-2 page Project Constitution (goals, constraints, tech stack).
2. For each feature, write a Feature Spec (inputs, behavior, edge cases).
3. Feed the spec to an AI agent (Claude Code, Cursor, JetBrains AI).
4. Use two-pass testing: AI generates base tests, humans add business edge cases.
5. Automate release notes from ticket metadata using AI.

**Risks**: Spec quality determines output quality. Not suitable for rapidly changing requirements. AI still misses non-obvious test cases. Team mindset shift from coding to spec-writing is non-trivial.

**For**: Engineering managers, indie devs, SaaS teams needing faster delivery with maintainability.

**Not for**: Early-stage prototyping teams, teams trusting AI output blindly, teams without domain experts.

**My take**: Vibe Coding proved AI can write code. Spec-Driven proves AI can write *correct* code when given a good spec. The bottleneck is no longer AI capability — it's how well humans define requirements. Try it on one feature next week and compare.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## From Vibe Coding to Spec-Driven: AI-Assisted Software Delivery Workflow

# From Vibe Coding to Spec-Driven: AI-Assisted Software Delivery Workflow

The software delivery workflow is shifting from unstructured "vibe coding" — where developers prompt AI to generate code on the fly — to a more disciplined, spec-driven approach. In this model, humans write a detailed specification (often in Markdown) defining what to build, and AI agents implement, test, and document against that spec. This is not a theoretical shift; it reflects how production teams using tools like Claude Code and JetBrains AI are already operating.

## Why It Matters Now

Vibe coding is fast but produces code that often drifts from intent. Spec-driven development preserves context across agent sessions, reduces cognitive debt, and keeps the human in control as projects grow. Combined with AI-assisted testing (where AI generates the bulk of unit tests and humans focus on edge cases) and automated release note generation (from Jira or Git metadata), the entire delivery pipeline becomes faster without sacrificing quality. Engineering managers report reduced cycle time from ticket to merge, with review load shifting from syntax to business logic.

## Practical Next Steps

1. **Write a project constitution.** Start each feature with a Markdown spec covering mission, tech stack, roadmap, and acceptance criteria. This gives the AI agent the context it needs to stay aligned.
2. **Adopt two-pass review.** First pass: automated scans for logic errors, security weaknesses, style violations. Second pass: human review focused on business-specific edge cases (e.g., Turkish characters in email fields).
3. **Automate release notes.** Use AI to scan JQL filters or Git commits and generate structured summaries for Slack, email, or Confluence. This eliminates manual write-ups and ensures consistency.
4. **Iterate spec-first.** When adding features to legacy code, write the spec for the change before touching code. Validate the spec with stakeholders, then let the agent implement.

## Risks and Limits

- **Over-reliance on AI-generated tests.** AI covers happy paths well but misses domain-specific failures. Without human domain experts, critical edge cases slip through.
- **Spec drift.** If specs are not kept in sync with code, the agent will produce misaligned output. Treat specs as living documents.
- **Security blind spots.** AI-generated code may introduce vulnerabilities (e.g., injection flaws, hardcoded secrets). Automated scanning is essential, but human security review remains necessary for sensitive systems.
- **Context loss across sessions.** Even with specs, large projects may exceed agent context windows. Break work into modular specs.

## Take

Spec-driven development is the disciplined alternative to vibe coding. It does not eliminate human judgment — it redirects it from syntax to intent. For teams shipping production software, this workflow reduces rework, improves intent fidelity, and makes AI assistance predictable. The next step is not more AI, but better specifications.

</div>

---

### 参考来源 / Sources

- [AI-Assisted Software Development: Workflow, Risks & ROI](https://devcom.com/tech-blog/ai-assisted-software-development)
- [AI-Accelerated Engineering Workflow: Ticket to Merge](https://firstlinesoftware.com/blog/blog-ai-accelerated-engineering-workflow)
- [How AI Automation Is Transforming Release Notes & Reports](https://gitprotect.io/blog/how-ai-automation-is-transforming-release-notes-reports)
- [Spec-Driven Development with Coding Agents](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents)
- [New course: Spec-Driven Development with Coding ...](https://www.facebook.com/andrew.ng.96/videos/new-course-spec-driven-development-with-coding-agents-built-in-partnership-with-/1509071804123051)
