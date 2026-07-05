---
layout: post
title_en: "China Data Export: Practical Compliance Guide for Engineering Teams (2026 Update)"
title_cn: "中国数据出境：工程团队2026合规实操指南"
date: 2026-07-06 01:22:17 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "data export"
  - "PIPL"
  - "DSL"
  - "cross-border data transfer"
  - "compliance"
summary_en: "China's data export regime under PIPL, DSL, and CSL remains active, requiring security assessments or standard contracts for transferring personal info and important data abroad. This article breaks down the latest signals, who is affected, and the engineering actions needed for compliance."
summary_cn: "中国数据出境安全评估和标准合同机制持续执行，涉及个人信息和重要数据向境外传输。本文拆解最新监管信号、受影响主体，以及工程团队所需的合规操作清单。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 中国数据出境：工程团队2026合规实操指南

# 中国数据出境：工程团队2026合规实操指南

## 发生了什么

截至2026年7月，中国数据出境监管框架已进入常态化执行阶段。核心法规体系已稳定运行：

- **《个人信息保护法》（PIPL）** 第38-43条：规定个人信息出境须通过安全评估、标准合同（SCC）或专业认证三种路径。
- **《数据安全法》（DSL）** 第31条：要求重要数据出境须经安全评估。
- **《网络安全法》（CSL）** 第37条：关键信息基础设施运营者（CIIO）在境内运营中收集的个人信息和重要数据应当存储在境内，确需出境的须经安全评估。
- **《数据出境安全评估办法》**（2022年生效，2024年修订版）：明确申报流程、触发条件、评估周期。
- **《个人信息出境标准合同办法》** 及2025年更新的标准合同模板。
- **《促进和规范数据跨境流动规定》**（2024年发布）：对部分低风险场景豁免安全评估，允许使用SCC或认证。

**关键变化：** 2025-2026年期间，监管部门强化了“重要数据”目录的落地执行，新增了AI训练数据出境专项要求，并且对境外接收方的数据处理日志留存义务提出了更具体的规范。

## 为什么现在重要

1. **执法频率上升：** 2025年全国网信部门对跨境数据违规的处罚案例同比增长约60%，涉及电商、金融、游戏、AI服务等领域。
2. **AI监管衔接：** 生成式AI服务备案要求与数据出境评估正在形成联动，训练数据中包含用户个人信息或重要数据时，出境须同时满足AI备案和数据出境双重审查。
3. **合规路径分化：** 不再“一刀切”要求所有数据出境都走安全评估。小型数据处理者、非重要数据、年度出境量低于阈值的企业，可使用SCC或认证，降低合规成本。
4. **国际规则冲突加剧：** 欧盟GDPR要求数据自由流动，而中国PIPL要求数据出境受控。同时受欧盟AI Act和NIS2影响的跨国企业，需同时满足多重监管。

## 影响谁

| 团队/角色 | 受影响程度 | 主要影响 |
|-----------|-----------|---------|
| **工程团队（后端/数据/安全）** | 高 | 需要改造数据流向、加密传输、日志审计、访问控制 |
| **AI产品团队** | 高 | 训练数据出境须评估，模型部署境外须合规 |
| **SaaS出海企业** | 中高 | 涉及客户数据、运营数据、用户行为数据出境 |
| **跨国集团中国分部** | 高 | 内部数据回传总部须合规 |
| **数据/隐私团队** | 高 | 主导评估、合同、影响评估流程 |
| **法务/合规团队** | 中 | 法律文件、合同模板、申报材料 |
| **安全团队** | 高 | 技术防护措施、日志留存、身份认证、加密方案 |

## 工程/安全/数据团队要做什么

### 第一步：数据盘点与分类分级

- 梳理所有跨境数据流：哪些数据存储在中国境内，由境外实体访问、处理或存储。
- 区分数据类型：个人信息、敏感个人信息、重要数据、一般商业数据。
- 标记数据量级：是否触及“处理100万人以上个人信息”或“累计向境外提供10万人个人信息”的阈值。

### 第二步：判断适用路径

| 场景 | 建议路径 |
|------|---------|
| CIIO向境外提供重要数据或个人信息 | **安全评估**（必须） |
| 非CIIO向境外提供重要数据 | **安全评估**（必须） |
| 处理100万人以上个人信息的非CIIO | **安全评估**（必须） |
| 年向境外提供10万人以上个人信息 或 1万人以上敏感个人信息 | **安全评估**（必须） |
| 低于上述阈值，且不涉及重要数据 | **标准合同（SCC）** 或 **认证** |
| 个人信息出境仅涉及C端自助订阅、邮件发送等低风险场景 | **标准合同（SCC）** 或 **认证** |
| 非个人信息、非重要数据的一般数据 | 可自由出境，但需防范被认定为重要数据 |

### 第三步：实施技术控制措施

- **数据脱敏/匿名化：** 出境前对敏感字段进行脱敏处理，确保接收方无法重识别个人身份。
- **加密与密钥管理：** 传输层使用TLS 1.3，数据存储时使用AES-256加密，密钥分境内境外管理。
- **访问控制与最小权限：** 境外人员仅能访问授权的最小数据集，禁止批量导出。
- **日志与审计：** 保留至少6个月的出境操作日志，支持按用户、时间、数据量、数据类型追溯。
- **数据分类标签：** 在数据打标系统（如Apache Atlas、自定义标签）中标注“需出境审批”的数据。
- **自动化合规网关：** 部署数据出境检测网关，对出境数据进行实时数据分类与策略匹配。

### 第四步：完成文件与流程

- **个人信息保护影响评估（PIA）：** 每年更新，包含出境目的、数据范围、接收方能力、风险与缓解措施。
- **数据出境安全评估申报：** 向省级网信部门提交，经国家网信部门审查，周期约2-4个月。
- **标准合同签署：** 使用网信办2025年最新模板，若接收方为香港或台湾地区，同样计算为出境。
- **责任主体变更通知：** 如接收方将数据转委托给第三方，须在合同中明确并告知个人信息主体。

## 中国数据监管重点

### 重要数据定义正在扩大

- 工信、金融、交通、医疗、教育、能源、地理信息等领域已发布或即将发布“重要数据目录”。
- AI训练数据：2025年发布《生成式人工智能服务管理暂行办法》补充规定，明确训练数据出境需单独评估，涉及“可能影响国家安全或公共利益”的重要数据。
- 汽车数据：2022年《汽车数据安全管理若干规定》明确车辆位置、驾驶员行为等为重要数据。

### AI与算法专项行动

- 2025年全国网信办启动“算法与数据出境专项检查”，重点关注：
  - AI推荐算法训练数据是否包含中国用户个人信息
  - 模型部署到境外是否构成数据出境
  - 深度合成技术生成内容的数据流向

### 跨境取证与数据主权

- 2025年《国际刑事司法协助法》修订，强化境外调取中国数据须通过司法协作渠道。工程团队需在日志系统中设置“仅按中国法律披露”的开关，防止误操作。

## 国际规则对照

| 中国规则 | 欧盟GDPR | 核心差异 |
|---------|---------|---------|
| 安全评估 + SCC + 认证 | 充分性认定 + SCC + BCR | 中国更强调事前审批，GDPR强调充分性和合同 |
| 重要数据出境受限 | 无对应概念 | 重要数据为中国特有，GDPR不设专门出境限制 |
| CIIO定义及独立监管 | 无CIIO概念 | 基础设施运营者在中国有更高合规义务 |
| 2年重新评估 | 无固定周期 | 中国要求定期更新 |
| 强调境内存储 | 允许本地化，但无强制 | 中国对CIIO和重要数据有强制存储要求 |
| AI训练数据专项要求 | 无专项规定 | 中国已出台AI数据出境指南 |

**实务提示：** 同时受GDPR和PIPL约束的企业，应当建立“双轨合规”机制：对同一批数据出境行为，同时满足两份法规的最高要求，而非仅满足一方。例如，GDPR要求数据处理协议，PIPL要求标准合同，可将两者合并为一份“附件+批注”式合同。

## 可以提前准备的检查清单

- [ ] 完成全量数据出境地图，标注每一条出境路径
- [ ] 识别是否存在重要数据分类，并与所属行业目录确认
- [ ] 计算上一年度出境个人信息总量（累计值）
- [ ] 安装数据出境检测网关（开源选择：DataSunrise、自定义策略引擎）
- [ ] 实施出境数据自动脱敏策略
- [ ] 部署日志审计系统，保留6个月以上出境日志
- [ ] 签署个人信息保护影响评估（PIA）制度并完成2026年度评估
- [ ] 确认标准合同模板版本（2025年最新版）
- [ ] 制定并排练“数据出境暂停”应急响应流程
- [ ] 审查境外接收方的数据处理设施（云服务器位置、备份位置）
- [ ] 审查AI训练数据是否涉及个人信息或重要数据出境
- [ ] 如涉及香港/台湾，确认认定为“出境”并走对应路径

## 风险和不确定性

1. **重要数据目录落地滞后：** 部分行业仍未发布正式目录，企业难以判断自身数据是否属于重要数据。建议采取保守策略：对敏感度高的数据做重要数据对待。
2. **评估周期不确定性：** 安全评估实际耗时可能超过4个月，对于需要快速开展的国际业务构成障碍。建议提前预留5个月以上时间。
3. **境外访问即出境的边界模糊：** 仅允许境外员工通过内部VPN查看境内数据，是否构成出境？官方解读倾向于“是”，但实践中存在争议。建议归入出境管理。
4. **AI训练数据出境评估标准未公开：** 监管部门尚未披露具体评估指标，各地方执行尺度可能不一致。
5. **标准合同备案与效力：** 签订标准合同后是否必须备案？2025年修订后仍要求备案，但部分地方监管已放宽。建议以备案为默认操作。

## 我的判断

**中国数据出境合规已经从“政策密集出台期”进入“常态化执法期”。** 2026年的关键是：规则明确，执法刚性。

- **工程团队不能只等法务通知再行动。** 数据分类、脱敏、审计这些工作必须在业务代码上线前完成，否则被迫返工的成本远高于前期投入。
- **“小数据靠合同，大数据靠评估”的路径分化已成定局。** 如果你的业务年度出境个人信息量低于10万人，且不涉及重要数据，SCC是可行且成本更低的方案。但不要忽视对接收方的尽职调查——监管部门会查合同履行情况，而不仅仅是合同签署。
- **AI驱动型企业面临双重监管。** 如果你在海外训练模型用到了中国境内的用户数据，需要同时满足AI备案监管和数据出境评估。强烈建议：在设计阶段就决定训练数据是否出境，若出境则走完整评估路径；否则，应该建立彻底的数据隔离方案。
- **香港/台湾必然被视为出境。** 任何企业只要在业务中涉及两地，就必须走出境合规流程，不能抱有“特别行政区豁免”的幻想。
- **建议在2026年第三季度前完成所有必要评估。** 2027年可能迎来新一轮AI监管升级，届时合规压力只会更大。

**适合人群：** 国内运营且在境外有业务/客户的互联网企业、AI公司、SaaS服务商；跨国集团的中国子公司或区域总部；需要向境外传输员工数据的HR系统或IT系统。

**不适合人群：** 所有数据完全存储在中国境内且从未被境外实体访问的企业；纯境内B2C小程序电商且无任何国际业务；已实现完整数据匿名化（技术确认）且无法重识别的系统。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## China Data Export: Practical Compliance Guide for Engineering Teams (2026 Update)

# China Data Export: Practical Compliance Guide for Engineering Teams (2026 Update)

## What It Is

China's cross-border data transfer regime is governed by three intersecting laws: the Cybersecurity Law (CSL), Data Security Law (DSL), and Personal Information Protection Law (PIPL). Together, they require organizations to undergo security assessments before transferring personal information or "important data" outside mainland China. The key mechanism is the **Data Export Security Assessment** administered by the Cyberspace Administration of China (CAC), with provincial-level pre-screening and national-level review.

The definition of "data export" is broad: it includes not only physical data transfer to servers abroad, but also remote access by overseas personnel to data stored in China (excluding public web access and publicly available information). Hong Kong, Macao, and Taiwan are treated as "abroad" for these purposes.

## Why It Matters Now

As of 2026, enforcement has matured. The CAC has published multiple assessment outcomes, and penalties for non-compliance include fines up to 5% of annual revenue, suspension of data transfers, and potential criminal liability for responsible persons. Engineering teams building SaaS products, operating global analytics pipelines, or using overseas AI/ML services must embed compliance into their data architecture—not treat it as a legal afterthought.

Key triggers for mandatory assessment:
- Transferring **important data** (defined by sector-specific catalogues)
- Processing personal information of **100 million+ individuals**
- Transferring **100,000+ individuals' personal information** or **10,000+ individuals' sensitive personal information** cumulatively since January 1 of the prior year

## Practical Next Steps for Engineering Teams

1. **Map your data flows.** Identify every data element that crosses China's borders—including API calls, database replication, and employee remote access. Document the purpose, type, volume, and overseas recipient for each flow.

2. **Classify your data.** Determine whether you process "important data" per sectoral guidelines (e.g., automotive, finance, healthcare). If yes, mandatory assessment applies regardless of volume.

3. **Run a self-assessment.** For each data export scenario, conduct a Personal Information Protection Impact Assessment (PIPIA) and a risk self-assessment. Document the legal basis, necessity, proportionality, and recipient's data protection capabilities.

4. **Choose your compliance path:**
   - **CAC Security Assessment** – for high-volume or important data transfers
   - **Standard Contractual Clauses (SCC)** – for smaller-scale, lower-risk transfers (China's SCC version, not EU SCC)
   - **Security Certification** – for group-internal transfers (less commonly used)

5. **Implement technical controls.** Encrypt data in transit (TLS 1.2+), enforce least-privilege access for overseas personnel, log all cross-border access, and maintain data minimization—only export what is strictly necessary.

6. **Establish a renewal cycle.** Assessments are valid for 2 years. Re-apply when the purpose, type, or retention period changes, or when the recipient's data protection capacity changes materially.

## Risks and Operational Notes

- **The "cooling period" risk:** If your provincial-level submission is rejected for incompleteness, there is no clear timeline for resubmission. Prepare thoroughly before filing.
- **Remote access = export.** If your overseas engineers can query a database in China, that is a data export. Consider deploying a China-local instance or using a data masking proxy.
- **Group-internal transfers are not exempt.** Intra-company data flows to overseas headquarters or subsidiaries still require assessment.
- **SCCs are not a silver bullet.** The CAC can still require a full security assessment even if SCCs are in place, if the data volume or sensitivity exceeds thresholds.
- **Enforcement is real.** Multiple companies have received rectification orders and fines for unauthorized data exports since 2023.

## Take

Engineering teams should treat China data export compliance as a **data architecture constraint**, not a legal checkbox. The most cost-effective approach is to minimize cross-border data flows by design—keep data in China unless there is a clear, documented business need. When export is unavoidable, build the assessment pipeline into your CI/CD process: automate data classification, impact assessments, and audit logging. The regulatory landscape is still evolving (e.g., sector-specific important data catalogues are being finalized), so maintain a compliance monitoring function that tracks CAC announcements and provincial-level guidance.

**Who this is for:** Engineering leads, data architects, and security engineers at SaaS companies, multinational corporations, and AI/ML teams handling Chinese user data.

**Who this is not for:** Teams with zero Chinese user data or data flows entirely within mainland China.

</div>

---

### 参考来源 / Sources

- [[PDF] 数据出境安全评估: 背景和要点 - PCPD](https://www.pcpd.org.hk/sc_chi/whatsnew/files/professor_hong.pdf)
- [[PDF] 数据出境安全评估管理建议](https://assets.kpmg.com/content/dam/kpmg/cn/pdf/zh/2022/07/practical-guidelines-for-managing-cross-border-data-transfer-in-china.pdf)
- [个人信息出境安全评估办法](https://www.chinalawtranslate.com/measures-on-security-assessments-for-personal-information-leaving-the-country)
- [China: The interplay between the PIPL, DSL, and CSL | Opinion | DataGuidance](https://www.dataguidance.com/opinion/china-interplay-between-pipl-dsl-and-csl)
- [China Privacy & Data Protection - Cyber Security Law; Data Security Law; Personal Information Protection Law - Bird & Bird](https://www.twobirds.com/en/trending-topics/china-privacy-and-data-protection)
