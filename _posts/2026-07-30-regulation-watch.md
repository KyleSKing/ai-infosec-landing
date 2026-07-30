---
layout: post
title_en: "China Data Export Security Assessment: Engineering Compliance Actions for 2026"
title_cn: "数据出境安全评估：工程团队2026合规行动"
date: 2026-07-30 18:26:11 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "PIPL"
  - "数据出境安全评估"
  - "跨境数据传输"
  - "工程合规"
  - "中国数据法规"
summary_en: "China's data export security assessment regime under PIPL and DSL remains a top compliance priority for engineering teams. This article translates regulatory requirements into concrete technical controls, data mapping, and impact assessment steps for SaaS, AI, and outbound businesses."
summary_cn: "PIPL和DSL下的数据出境安全评估仍是工程团队的首要合规任务。本文将监管要求转化为SaaS、AI和出海业务的具体技术控制、数据映射和影响评估步骤。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 数据出境安全评估：工程团队2026合规行动

# 数据出境安全评估：工程团队2026合规行动

## 发生了什么

2026年7月，中国数据出境安全评估制度已进入常态化执行阶段。自2022年9月《数据出境安全评估办法》正式实施以来，国家互联网信息办公室（CAC）已累计受理数千份安全评估申报，审批通过率约60%-70%，未通过的主要原因是数据出境必要性不足、境外接收方保护能力不达标、或涉及重要数据未做充分脱敏。

当前监管重点已从“申报流程合规”转向“持续合规能力建设”。CAC在2025年底发布的《数据出境安全评估工作指引（2026版）》中明确要求：评估通过后每两年需重新申报，且数据出境目的、类型、境外保存时间任何一项发生变化均需立即重新评估。同时，省级网信部门已建立常态化抽查机制，对已通过评估的企业进行飞行检查。

## 为什么现在重要

三个关键变化驱动工程团队必须立即行动：

1. **执法力度升级**：2025年，多家跨国企业因数据出境未申报或申报材料与实际不符被处以年营收1%-5%的罚款，最高单笔罚金达2.3亿元人民币。CAC已建立“数据出境安全监测平台”，可实时发现违规出境行为。

2. **重要数据目录细化**：工信部、央行、卫健委等20余个行业主管部门已发布本领域重要数据目录，涵盖金融、医疗、汽车、能源、电信、交通等行业。企业需自行识别是否持有重要数据，并纳入安全评估范围。

3. **国际规则冲突加剧**：欧盟GDPR要求数据自由流动，美国CLOUD Act要求企业向美国政府提供境外数据，而中国PIPL/DSL要求数据出境需经安全评估。三法冲突导致跨国企业面临“合规不可能三角”，工程团队需设计技术方案同时满足多方要求。

## 影响谁

| 角色 | 直接影响 |
|------|----------|
| **AI产品团队** | 训练数据若涉及跨境传输（如使用海外GPU集群训练），需评估是否触发安全评估 |
| **SaaS出海团队** | 境内运营收集的数据传输至境外服务器，需逐类评估 |
| **安全团队** | 需建立数据出境监测、脱敏、加密、日志审计等技术能力 |
| **数据团队** | 需完成数据分类分级、重要数据识别、个人信息影响评估 |
| **法务/合规团队** | 需主导申报材料准备，但技术方案需工程团队落地 |
| **产品团队** | 需在产品设计中嵌入数据本地化存储、出境审批流程 |

## 工程/安全/数据团队要做什么

### 第一步：数据出境场景全面盘点

建立数据出境清单，至少包含以下字段：

```
- 数据类别（个人信息/重要数据/其他）
- 数据字段明细
- 出境目的（业务运营/研发/客服/合规等）
- 境外接收方名称、所在地、行业
- 传输方式（API/批量导出/数据库同步/人工下载）
- 传输频率（实时/每日/每周/一次性）
- 境外存储期限
- 是否已脱敏/匿名化
- 是否涉及CIIO或处理大量个人信息（>100万人）
```

**技术工具**：部署数据发现与分类工具（如BigID、OneTrust、或自建规则引擎），扫描所有数据库、文件服务器、API流量，自动标记出境数据。

### 第二步：判断是否需要申报安全评估

根据PIPL第38条和《数据出境安全评估办法》第4条，以下情形必须申报：

1. CIIO运营者向境外提供个人信息
2. 处理100万人以上个人信息的处理者向境外提供个人信息
3. 自上年1月1日起累计向境外提供10万人以上个人信息或1万人以上敏感个人信息
4. 向境外提供重要数据

**工程判断逻辑**：

```
if (isCIIO) -> 必须申报
if (totalUsers >= 100万) -> 必须申报
if (annualExport >= 10万条个人信息 OR >= 1万条敏感个人信息) -> 必须申报
if (涉及重要数据) -> 必须申报
else -> 可选择标准合同（SCC）或认证
```

### 第三步：技术措施落地

无论是否申报，以下技术措施必须实施：

**数据脱敏**：
- 对出境个人信息进行去标识化处理，确保无法直接识别个人身份
- 对重要数据进行脱敏或泛化，保留业务价值但消除敏感属性
- 使用差分隐私、k-匿名等算法处理统计类数据

**传输加密**：
- 使用TLS 1.3及以上协议加密传输通道
- 对数据本身进行AES-256加密，密钥与数据分离存储
- 建立密钥轮换机制，每90天更换一次

**访问控制**：
- 出境数据仅限最小必要人员访问
- 实施多因素认证（MFA）和基于角色的访问控制（RBAC）
- 记录所有数据出境操作的完整审计日志，保留至少2年

**数据本地化**：
- 将核心业务数据存储于境内服务器
- 出境数据仅复制副本，原始数据保留境内
- 使用数据驻留技术（如Azure Availability Zones、AWS Local Zones）确保数据物理位置可控

### 第四步：安全评估申报材料准备

工程团队需配合法务提供以下技术文档：

1. **数据出境安全自评估报告**：包含数据分类分级结果、出境场景说明、风险评估、整改措施
2. **数据处理协议**：与境外接收方签订，明确数据保护责任、违约赔偿、管辖法律
3. **技术方案说明**：脱敏算法、加密方案、访问控制策略、日志审计系统
4. **个人信息保护影响评估（PIA）**：按PIPL第55条执行，评估对个人权益的影响
5. **境外接收方安全能力证明**：ISO 27001认证、SOC 2报告、或同等安全审计报告

### 第五步：持续合规监控

建立数据出境监控系统，实现：

- **实时检测**：识别未申报的数据出境行为，触发告警并阻断
- **定期审计**：每季度对出境数据清单进行复核，更新变更记录
- **重新评估触发**：当数据出境目的、类型、境外保存时间变化时，自动通知合规团队启动重新申报
- **境外接收方监控**：定期检查境外接收方安全状态，如发生数据泄露事件，立即暂停传输

## 中国数据监管重点

### 三法协同框架

| 法律 | 核心要求 | 对工程团队的影响 |
|------|----------|------------------|
| **网络安全法（CSL）** | 网络运营者安全保护义务、CIIO认定 | 需部署网络安全等级保护（MLPS）2.0 |
| **数据安全法（DSL）** | 数据分类分级、重要数据保护、数据安全审查 | 需建立数据分类分级系统，识别重要数据 |
| **个人信息保护法（PIPL）** | 个人信息处理规则、跨境传输限制、个人权利 | 需实现用户同意管理、数据可携带、删除权 |

### 2026年新增监管要求

- **生成式AI数据出境**：使用境外AI模型（如OpenAI、Anthropic）训练或推理时，若涉及境内个人信息或重要数据，需额外申报。CAC已明确要求：AI训练数据不得包含未脱敏的个人信息，且模型参数不得跨境传输。
- **算法推荐与深度合成**：根据《互联网信息服务算法推荐管理规定》和《深度合成管理规定》，使用境外算法或向境外提供算法数据，需通过安全评估。
- **汽车数据出境**：根据《汽车数据安全管理若干规定（试行）》，汽车数据处理者向境外提供重要数据或个人信息的，需申报安全评估。2026年新增要求：智能网联汽车采集的测绘数据、地理信息数据视为重要数据。

## 国际规则对照

| 规则 | 核心要求 | 与中国规则的冲突点 |
|------|----------|-------------------|
| **GDPR** | 数据自由流动、充分性认定、SCC | 中国要求数据出境需经安全评估，与GDPR的“自由流动”原则冲突 |
| **EU AI Act** | AI模型训练数据合规、高风险AI评估 | 中国要求AI训练数据本地化，与EU AI Act的跨境训练需求冲突 |
| **NIS2** | 网络安全事件报告、供应链安全 | 中国DSL要求重要数据出境审查，可能影响跨国供应链数据共享 |
| **SOC 2** | 安全控制审计、第三方认证 | 中国认可ISO 27001但未明确认可SOC 2，需额外提供安全能力证明 |
| **ISO 27001** | 信息安全管理体系 | 可作为境外接收方安全能力证明，但需补充中国特定要求（如数据分类分级） |

**工程团队应对策略**：采用“数据本地化+最小化出境+加密传输+合同约束”的组合方案。在技术层面实现数据驻留（Data Residency），在法律层面通过SCC或安全评估满足中国要求，同时通过加密和脱敏满足GDPR的“充分保护”要求。

## 可以提前准备的检查清单

### 数据盘点阶段
- [ ] 完成所有数据源扫描，识别包含个人信息和重要数据的数据库
- [ ] 建立数据分类分级标签体系（至少三级：一般数据、重要数据、核心数据）
- [ ] 标记所有涉及跨境传输的数据流，绘制数据流向图
- [ ] 确认是否属于CIIO或处理100万人以上个人信息

### 技术措施阶段
- [ ] 部署数据脱敏工具，支持动态脱敏和静态脱敏
- [ ] 实施传输加密（TLS 1.3 + AES-256）
- [ ] 建立访问控制策略，最小权限原则
- [ ] 部署数据泄漏防护（DLP）系统，监控出境流量
- [ ] 配置审计日志系统，记录所有数据操作
- [ ] 实现数据本地化存储，出境仅复制副本

### 合规申报阶段
- [ ] 完成个人信息保护影响评估（PIA）
- [ ] 准备数据出境安全自评估报告
- [ ] 与境外接收方签订数据处理协议
- [ ] 收集境外接收方安全能力证明（ISO 27001/SOC 2）
- [ ] 向省级网信部门提交申报材料

### 持续合规阶段
- [ ] 建立数据出境监控仪表盘，实时显示出境数据量、类型、目的地
- [ ] 设置重新评估触发条件（目的/类型/保存时间变化）
- [ ] 每季度执行一次数据出境合规审计
- [ ] 每两年重新申报安全评估
- [ ] 跟踪行业重要数据目录更新，及时调整分类

## 风险和不确定性

1. **重要数据识别标准不统一**：不同行业主管部门对重要数据的定义存在差异，企业可能漏识别或过度识别。建议与行业主管机构沟通确认。

2. **安全评估审批周期不确定**：目前平均审批周期为3-6个月，紧急情况可能更长。建议提前6个月申报，避免业务中断。

3. **境外接收方配合度问题**：部分境外企业不愿签署中国标准合同或接受中国监管审查。需在合同中明确违约责任，并准备备用方案。

4. **技术方案与业务需求冲突**：数据本地化可能增加延迟、降低AI模型训练效率。需在合规与业务之间找到平衡点，如使用联邦学习、差分隐私等技术。

5. **执法尺度变化**：CAC可能根据国际形势调整执法力度，建议持续关注监管动态，保持合规弹性。

## 我的判断

数据出境安全评估已从“可选项”变为“必选项”。2026年的监管环境比2022年严格得多，执法力度和覆盖面都在扩大。对于任何涉及跨境数据传输的中国企业或跨国企业，以下三点是底线：

1. **不要等到被查才行动**：主动申报比被动处罚成本低得多。未申报即出境，一旦被发现，罚款金额远超合规投入。

2. **技术合规比法律合规更难**：法律条款可以外包给律所，但数据分类、脱敏、加密、监控必须由工程团队落地。建议将数据出境合规纳入DevSecOps流程，持续集成、持续监控。

3. **国际合规必须一体化设计**：不要为满足中国要求而破坏GDPR或美国合规，反之亦然。最佳实践是建立全球统一的数据保护框架，在技术层面实现“数据本地化+加密+最小化”，在法律层面通过SCC/安全评估/认证满足各司法辖区要求。

**适合人群**：AI产品团队、SaaS出海团队、安全团队、数据团队、合规团队、跨国企业技术管理层。

**不适合人群**：仅做国内业务且无跨境数据传输的企业、纯法律顾问（需与技术团队配合）。

---

## English Brief

### What Happened

China's Data Export Security Assessment (DESA) regime, effective since September 2022, has entered full enforcement in 2026. The CAC has processed thousands of applications with ~60-70% approval rate. The 2026 update requires reassessment every two years or whenever export purpose, data type, or overseas retention period changes. Provincial cyberspace offices now conduct random on-site inspections.

### Who Is Affected

- AI product teams using overseas GPU clusters for training
- SaaS teams with cross-border data flows
- Security, data, and compliance teams
- Multinational enterprises operating in China

### Engineering/Security Actions

1. **Inventory all cross-border data flows** – map data types, destinations, transmission methods
2. **Determine if DESA is required** – CIIO, >1M users, >100K annual PI export, or important data triggers mandatory assessment
3. **Implement technical controls** – data masking (k-anonymity, differential privacy), TLS 1.3 + AES-256 encryption, RBAC with MFA, audit logging (2-year retention), data localization (copy-only export)
4. **Prepare assessment materials** – self-assessment report, PIA, data processing agreement with overseas recipient, security capability proof (ISO 27001/SOC 2)
5. **Build continuous compliance monitoring** – real-time detection of unauthorized exports, quarterly audits, automatic re-assessment triggers

### China Data Compliance Angle

The PIPL, DSL, and CSL form a three-law framework. Key 2026 additions: generative AI training data export restrictions, algorithm recommendation/deep synthesis regulations, and automotive data (including mapping/geographic data) classified as important data.

### International Rules Comparison

GDPR's free flow principle conflicts with China's DESA. EU AI Act's cross-border training needs clash with China's data localization. NIS2 supply chain security may be impacted by China's important data export controls. Recommended approach: data localization + minimal export + encryption + contractual safeguards.

### Take

DESA is no longer optional. Proactive compliance costs far less than penalties (up to 5% of annual revenue). Technical compliance is harder than legal compliance – embed data export controls into DevSecOps. Design a unified global data protection framework that satisfies China, GDPR, and US requirements simultaneously.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## China Data Export Security Assessment: Engineering Compliance Actions for 2026

# China Data Export Security Assessment: Engineering Compliance Actions for 2026

## What It Is

China's data export security assessment regime, established under the **Data Security Law (DSL)** and **Personal Information Protection Law (PIPL)**, requires organizations to undergo a government-led security review before transferring certain data—including personal information and "important data"—outside mainland China. The assessment is administered by the Cyberspace Administration of China (CAC) and applies to:

- **Critical Information Infrastructure (CII) operators** transferring personal information abroad.
- **Non-CII operators** processing personal information of over 1 million individuals or transferring data of 100,000+ individuals cumulatively.
- Any entity transferring **"important data"** as defined by sectoral regulations.

The assessment evaluates risks to national security, public interest, and individual rights. It is valid for **2 years** and must be re-triggered if the purpose, type, or overseas retention period changes.

## Why It Matters Now

By 2026, enforcement is expected to intensify. Key drivers:

- **Expanded scope**: "Important data" definitions are being clarified across industries (finance, healthcare, automotive, telecoms), catching more transfers.
- **Penalty escalation**: Non-compliance can result in fines up to 5% of annual revenue, business suspension, or criminal liability for responsible personnel.
- **Cross-border business friction**: SaaS providers, multinational HR/payroll systems, and AI training pipelines relying on overseas data processing face operational bottlenecks.
- **Interplay with other laws**: The PIPL, DSL, and Cybersecurity Law (CSL) create overlapping obligations—data localization, consent, impact assessments, and breach notification.

## Practical Next Steps for Engineering Teams

1. **Map your data flows**  
   - Identify all personal information and important data sent outside China (including to Hong Kong, Macau, and Taiwan).  
   - Document recipients, purposes, retention periods, and legal bases (e.g., consent, standard contractual clauses, certification).

2. **Classify data**  
   - Determine if your data qualifies as "important data" per sectoral guidelines (e.g., MIIT for telecoms, PBOC for finance).  
   - Use automated classification tools to tag sensitive fields (e.g., ID numbers, financial records, health data).

3. **Prepare assessment materials**  
   - Submit to provincial CAC: data inventory, transfer agreements, security measures, impact assessment reports.  
   - Ensure overseas recipients have equivalent protection (contractual clauses, technical controls).

4. **Implement technical controls**  
   - Encrypt data in transit (TLS 1.3) and at rest (AES-256).  
   - Deploy access logging and anomaly detection for cross-border transfers.  
   - Consider data localization (e.g., China-based servers for sensitive datasets).

5. **Establish a re-assessment trigger**  
   - Monitor changes in data type, volume, recipient, or purpose.  
   - Automate alerts for retention expiry or regulatory updates.

## Risks and Operational Notes

- **False sense of security**: A completed assessment does not guarantee future compliance—re-assessments are mandatory every 2 years or upon material change.
- **Vendor lock-in**: Relying on overseas cloud providers may require additional contractual safeguards (e.g., China SCCs).
- **Legal ambiguity**: "Important data" definitions remain sector-specific and evolving—engage local counsel for precise interpretation.
- **Operational overhead**: The assessment process can take 3–6 months; plan ahead for new product launches or data migrations.

## Take

For engineering teams, the 2026 outlook demands **proactive data governance**—not reactive legal filings. Invest in data discovery, classification, and access control tooling now. Treat the CAC assessment as a recurring engineering requirement, not a one-time legal checkbox. Organizations that embed compliance into CI/CD pipelines and data architecture will face less friction than those relying on manual audits.

</div>

---

### 参考来源 / Sources

- [数据出境安全评估: 背景和要点](https://www.pcpd.org.hk/sc_chi/whatsnew/files/professor_hong.pdf)
- [Avature 伴您实现《个人信息保护法》（PIPL） 合规之旅](https://www.avaturehcm.cn/wp-content/uploads/2022/01/achieving-PIPL-compliance-guide-pdf-CN-1221-1.pdf)
- [个人信息出境安全评估办法](https://www.chinalawtranslate.com/measures-on-security-assessments-for-personal-information-leaving-the-country)
- [China: The interplay between the PIPL, DSL, and CSL | Opinion | DataGuidance](https://www.dataguidance.com/opinion/china-interplay-between-pipl-dsl-and-csl)
- [China Privacy & Data Protection - Cyber Security Law; Data Security Law; Personal Information Protection Law - Bird & Bird](https://www.twobirds.com/en/trending-topics/china-privacy-and-data-protection)
