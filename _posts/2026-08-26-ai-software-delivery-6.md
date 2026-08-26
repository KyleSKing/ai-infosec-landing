---
layout: post
title_en: "Spec-Driven AI Delivery: From Vibe Coding to Controlled Software Releases"
title_cn: "从随性编码到规范交付：AI辅助软件工程新范式"
date: 2026-08-26 19:37:16 +0800
category: ai
content_type: trend_explainer
content_type_cn: "趋势分析"
content_type_en: "Trend Analysis"
tags:
  - "AI-assisted development"
  - "spec-driven development"
  - "software delivery workflow"
  - "AI testing"
  - "release automation"
summary_en: "AI-assisted software delivery is shifting from unstructured vibe coding to spec-driven workflows, where human-written specifications guide AI agents in implementation, testing, and release. This trend reduces cognitive debt and improves intent fidelity, but requires domain experts for edge-case testing and human oversight for security and compliance."
summary_cn: "AI辅助软件交付正从随性编码转向规范驱动的工作流：人类编写详细规范，AI代理负责实现、测试和发布。这一趋势降低了认知负担并提升了意图一致性，但仍需领域专家进行边界测试，以及人工监督确保安全与合规。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 从随性编码到规范交付：AI辅助软件工程新范式

# 从随性编码到规范交付：AI辅助软件工程新范式

## 这个趋势是什么

2025年下半年开始，AI辅助软件工程正在经历一次关键转向：从“让AI写代码”的粗放模式，转向“用规范驱动AI交付”的工程化流程。这个趋势的核心特征是——**规格先行、AI实现、人工验证**。

具体来说，新的工作流不再是“写个prompt让AI生成代码→手动修bug→再prompt”，而是：

1. **写规格文档**（Markdown spec）：定义功能、边界、技术栈、验收标准
2. **AI代理按规格实现**：自动生成代码、测试脚手架、文档
3. **自动化扫描 + 人工审查**：两轮审查，AI先过逻辑/安全/风格，人再过业务边界
4. **自动化发布摘要**：AI从Jira/Linear等工具提取变更，生成结构化的发布说明

这个流程已经在Claude Code、JetBrains生态、以及多个工程管理工具中落地。Andrew Ng和JetBrains联合推出的《Spec-Driven Development with Coding Agents》课程，标志着这个范式正在从少数先锋团队走向主流。

## 为什么现在重要

### 旧问题：vibe coding的三大痛点

2024年兴起的“vibe coding”（随性编码）让开发者能快速用自然语言生成代码，但带来了三个严重问题：

- **意图漂移**：AI生成的代码经常和你想的不一样，尤其是复杂业务逻辑
- **上下文丢失**：每次新对话，AI忘记之前的决策，导致代码不一致
- **不可审计**：没有规格文档，代码改了什么都说不清楚，合规和安全团队无法追溯

### 新范式解决的痛点

Spec-driven development直接回应了这些问题：

- **意图保真**：规格文档是“契约”，AI按契约实现，偏差可检测
- **跨会话上下文**：规格文件保存了所有设计决策，新会话直接加载
- **可审计可追溯**：规格→代码→测试→发布说明，全链路可查

对于工程管理者来说，这意味着**周期时间缩短、审查负担降低、团队结构可调整**。Firstline Software的实践报告显示，AI加速工程流程后，从ticket到合并的周期可以缩短40-60%，同时保持甚至提升代码质量。

## 它和旧做法的区别

| 维度 | 旧做法（vibe coding） | 新范式（spec-driven + AI交付） |
|------|----------------------|-------------------------------|
| 起点 | 口头描述 / 粗略prompt | 结构化Markdown规格文档 |
| 实现 | AI一次性生成，人工反复调试 | AI按规格分步实现，人工在关键节点验证 |
| 测试 | 手动写测试用例 | AI从代码自动生成测试，人工补充业务边界用例 |
| 审查 | 人工逐行review | 两轮：AI扫描逻辑/安全/风格，人工聚焦业务 |
| 发布 | 手动整理变更日志 | AI从项目管理工具自动生成结构化发布说明 |
| 可追溯 | 几乎为零 | 规格→代码→测试→发布，全链路可查 |

### 具体场景对比

**测试生成**：旧做法中，开发者写完代码再手动写单元测试，容易遗漏边界情况。新做法中，AI从现有代码自动生成测试，覆盖所有预期成功路径。但正如DevCom的文章指出，**业务专家需要补充AI无法预见的失败场景**——比如一个包含土耳其字符的邮箱地址会破坏文本处理逻辑。

**代码审查**：旧做法是纯人工review，耗时且容易疲劳。新做法分两轮：第一轮AI自动扫描逻辑错误、安全漏洞、风格违规；第二轮人工聚焦业务逻辑和边界情况。这样人工审查的精力集中在真正需要判断力的地方。

**发布说明**：旧做法是开发者在发布前手动整理变更日志，经常遗漏或描述不清。新做法中，AI从Jira/Linear等工具自动提取issue信息，生成分类清晰的发布说明，并统一格式推送到Slack、邮件、Confluence等渠道。GitProtect的实践表明，AI还能自动识别issue类型、状态、描述和元数据，生成更准确的摘要。

## 可以怎么开始试

### 第一步：从一个小功能开始写规格

不要试图改造整个项目。选一个独立的、边界清晰的小功能，用Markdown写规格文档，包含：

```markdown
# 功能规格：用户邮箱验证

## 目标
用户注册后，发送验证邮件，用户点击链接后完成验证。

## 验收标准
- 发送邮件后，用户收到含验证链接的邮件
- 链接有效期24小时
- 验证成功后，用户状态更新为“已验证”
- 重复点击链接不报错
- 包含土耳其字符的邮箱地址能正常处理

## 技术约束
- 使用SendGrid API发送邮件
- 验证token使用JWT，签名密钥从环境变量读取
- 数据库字段：email_verified_at (timestamp, nullable)
```

### 第二步：配置AI代理的工作流

如果你使用Claude Code或类似工具：

1. 将规格文档作为初始上下文加载
2. 要求AI代理按规格分步实现，每完成一个验收标准就停下来让你验证
3. 让AI自动生成测试用例，覆盖所有预期成功路径
4. 运行AI自动扫描（逻辑、安全、风格）

### 第三步：建立两轮审查流程

- **第一轮（自动化）**：配置ESLint、SonarQube、或AI内置的代码审查功能，自动扫描所有变更
- **第二轮（人工）**：只审查业务逻辑和边界情况，重点关注AI可能遗漏的领域知识

### 第四步：自动化发布说明

如果使用Jira，配置AI工具：

1. 通过项目、版本、sprint或JQL过滤器识别本次发布的issue
2. AI分析issue类型、状态、描述和元数据
3. 生成分类清晰的发布说明（功能、修复、优化等）
4. 统一推送到Slack、邮件、Confluence

### 第五步：建立规格版本管理

将规格文档纳入版本控制（与代码同仓库或独立仓库），每次变更先更新规格，再让AI实现。这样：

- 规格变更历史可追溯
- 新成员可以快速理解设计决策
- 审计和合规检查有据可查

## 适合人群

- **工程管理者**：想缩短交付周期、降低review负担、提升团队可扩展性
- **独立开发者/小团队**：一个人要管多个模块，AI辅助能大幅提升效率
- **需要合规的团队**：金融、医疗、数据密集型行业，规格驱动可追溯
- **SaaS产品团队**：频繁发布，需要自动化发布说明和变更管理

## 风险和限制

1. **规格本身的质量决定一切**：如果规格写得模糊或有歧义，AI实现的质量会直接下降。写规格需要一定的训练和纪律。
2. **业务边界用例仍需人工**：AI擅长覆盖“正常路径”，但领域特定的边界情况（如土耳其字符、时区处理、并发冲突）需要业务专家补充。
3. **安全风险不能完全自动化**：AI生成的代码可能包含安全漏洞，自动扫描能覆盖常见模式，但逻辑漏洞和业务逻辑绕过仍需人工审查。
4. **上下文窗口限制**：对于超大型项目，规格文档可能超出AI的上下文窗口，需要拆分为多个模块。
5. **团队适应性**：从“写代码”转向“写规格+审查”，部分开发者可能不适应，需要培训和心态调整。

## 我的判断

**Spec-driven development + AI交付不是vibe coding的替代品，而是它的工程化升级。** 两者面向不同场景：

- **原型探索、一次性脚本、个人项目**：vibe coding仍然高效
- **生产系统、团队协作、合规要求**：spec-driven是唯一可行的路径

这个趋势的驱动力不是技术本身，而是**工程管理的现实需求**：当AI能写代码后，瓶颈从“写代码”转移到了“定义要写什么”和“验证写对了没有”。规格驱动正好回应了这两个新瓶颈。

对于大多数工程团队，我建议**不要全面切换**，而是选一个模块试点，跑通流程后再推广。关键在于建立“规格→实现→验证→发布”的闭环，而不是追求AI写代码的速度。

**最容易被忽视的一点**：规格文档本身需要版本管理和变更记录。如果规格改了但代码没跟上，或者代码改了但规格没更新，这个流程就会失效。所以，把规格纳入CI/CD流水线，让规格变更触发代码变更，才是真正的工程化。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## Spec-Driven AI Delivery: From Vibe Coding to Controlled Software Releases

# Spec-Driven AI Delivery: From Vibe Coding to Controlled Software Releases

**What it is**

Spec-driven development is a disciplined alternative to vibe coding. Instead of prompting an AI agent with vague instructions, you first write a detailed markdown specification that defines the feature, tech stack, roadmap, and acceptance criteria. The coding agent then implements against that spec. This approach preserves context across agent sessions, reduces cognitive debt, and keeps the generated code aligned with what you actually need. It applies to both greenfield and legacy codebases.

**Why it matters now**

AI coding agents are fast—sometimes too fast. Vibe coding can produce working code that misses requirements, introduces logic errors, or lacks handling for business-specific edge cases. As teams push AI agents into production delivery, the bottleneck shifts from writing code to verifying intent. Spec-driven development gives engineers and managers a repeatable workflow to control large code changes with a few words, while maintaining human oversight at the specification and review stages. Combined with automated test generation (source [1] notes that AI writes bulk tests, but domain experts must catch business-specific failures), this workflow reduces cycle time without sacrificing reliability.

**Practical next steps**

1. **Write specs as part of your ticket workflow** – Start with a clear markdown spec in the ticket description or a linked document. Include mission, constraints, expected behavior, and known edge cases.
2. **Use iterative spec loops** – Generate output, review against the spec, update the spec, then rerun the agent. This preserves intent across sessions (see source [4]).
3. **Automate test generation from specs** – Let AI produce unit and integration tests that cover the spec. Have domain experts add tests for business-specific failure modes.
4. **Integrate AI into release notes** – Tools like Jira can use AI to scan issues, categories, and versions to generate consistent release summaries and notifications (source [3]).

**Risks and limits**

- **Spec drift** – If the spec is not updated as understanding evolves, the agent will keep building against outdated requirements.
- **Over-specification** – Writing specs for trivial changes wastes time. Apply spec-driven discipline only to non-trivial features.
- **Human review remains essential** – AI cannot anticipate subtle business logic errors, edge cases involving internationalization, or security vulnerabilities that require deep domain knowledge. The two-pass review described in source [1] (automated scans + human review) remains the recommended practice.
- **Context length limits** – Very large specs may exceed agent context windows, requiring splitting or summarization.

**Take**

Spec-driven AI delivery is the natural evolution of vibe coding. It moves from "tell the AI what to write" to "tell the AI what to build and verify it did." The workflow—spec, implement, test, review, release—keeps humans in control of intent while letting AI handle implementation, test scaffolding, and reporting. For engineering teams moving AI-assisted development from experiments to production, adopting spec discipline is the fastest way to improve intent fidelity and reduce rework. It’s not a silver bullet, but it is a repeatable process that scales with project complexity.

</div>

---

### 参考来源 / Sources

- [AI-Assisted Software Development: Workflow, Risks & ROI](https://devcom.com/tech-blog/ai-assisted-software-development)
- [AI-Accelerated Engineering Workflow: Ticket to Merge](https://firstlinesoftware.com/blog/blog-ai-accelerated-engineering-workflow)
- [How AI Automation Is Transforming Release Notes & Reports](https://gitprotect.io/blog/how-ai-automation-is-transforming-release-notes-reports)
- [Spec-Driven Development with Coding Agents](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents)
- [New course: Spec-Driven Development with Coding ...](https://www.facebook.com/andrew.ng.96/videos/new-course-spec-driven-development-with-coding-agents-built-in-partnership-with-/1509071804123051)
