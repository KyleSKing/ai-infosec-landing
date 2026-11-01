---
layout: post
title_en: "China Cross-Border Data Transfer Compliance: Security Assessments, Standard Contracts & Certification in 2026"
title_cn: "2026中国数据出境合规：安全评估、标准合同与认证"
date: 2026-11-02 04:24:51 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "PIPL"
  - "cross-border data transfer"
  - "data localization"
  - "China compliance"
  - "security assessment"
summary_en: "China's PIPL mandates security assessments for organizations processing over 1 million individuals' data before any export, and standard contracts or certification for other transfers. This article explains the latest requirements, enforcement signals, and practical steps for engineering and compliance teams."
summary_cn: "中国PIPL数据出境规则要求：处理100万人以上个人信息的数据处理者必须通过安全评估，其他情况需标准合同或认证。本文解析最新法规动态、执法信号，并提供工程与合规团队的实操建议。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 2026中国数据出境合规：安全评估、标准合同与认证

# 2026中国数据出境合规：安全评估、标准合同与认证

## 发生了什么

截至2026年11月，中国数据出境合规体系已形成“安全评估—标准合同—认证”三轨并行的完整框架。核心法规包括：

- **《数据出境安全评估办法》**（2022年9月生效，2024年修订版）
- **《个人信息出境标准合同办法》**（2023年6月生效，2025年更新版）
- **《个人信息出境认证办法》**（2025年发布，2026年正式实施）

2025-2026年间，监管重点从“框架建立”转向“执行细化”和“执法落地”。主要变化包括：

1. **安全评估有效期明确为2年**，到期需重新申请，且数据接收方或出境场景发生重大变化时须重新申报。
2. **标准合同备案流程简化**，允许电子化提交，但增加了对“数据接收方所在国法律环境”的评估要求。
3. **个人信息保护认证（认证）** 正式成为第三条出境路径，适用于不符合安全评估门槛、但标准合同无法覆盖的复杂场景（如集团内部数据共享、多层级数据接收方）。
4. **自贸区负面清单制度** 在海南、上海、北京、天津等地试点，允许清单内场景免于安全评估或标准合同备案。

## 为什么现在重要

2026年是中国数据出境合规的“执行年”。多个信号表明监管正在收紧：

- **CAC已启动多轮执法检查**，重点针对大型互联网平台、跨国企业、云服务商。
- **安全评估通过率下降**，2025年下半年以来，首次申请通过率约60%，补正后通过率约85%。
- **标准合同备案驳回率上升**，常见原因包括：未充分评估接收方所在国法律风险、未明确数据删除或返还机制、未提供中文版本合同。
- **认证路径的申请量激增**，但认证机构（中国网络安全审查技术与认证中心等）审核周期较长（3-6个月）。

对于任何处理中国境内个人信息的组织——无论是否在中国境内运营——现在必须确认自己的出境路径是否合规，否则面临最高5000万元人民币或上一年度营收5%的罚款，以及业务暂停、数据销毁等处罚。

## 影响谁

| 角色 | 影响程度 | 核心行动 |
|------|----------|----------|
| **AI产品团队** | 高 | 训练数据、推理数据出境需评估；大模型API调用可能触发出境 |
| **SaaS企业** | 高 | 客户数据存储、员工数据管理、技术支持数据出境 |
| **跨国企业** | 极高 | 全球HR系统、CRM、ERP数据同步；中国子公司与总部数据共享 |
| **安全团队** | 高 | 数据分类分级、出境风险评估、加密/脱敏方案 |
| **数据团队** | 高 | 数据映射、数据流图、出境数据量统计 |
| **法务/合规团队** | 极高 | 路径选择、合同起草、监管沟通 |
| **产品经理** | 中 | 功能设计需考虑数据本地化要求 |

## 工程/安全/数据团队要做什么

### 1. 数据映射与分类分级（立即执行）

- 绘制完整的数据流图，标注所有涉及中国境内个人信息的出境场景。
- 按PIPL要求对个人信息分类：一般个人信息、敏感个人信息（生物识别、金融账户、行踪轨迹等）、未成年人信息。
- 识别“重要数据”（如金融、能源、交通、医疗等行业的特定数据）。

### 2. 出境路径判断（按优先级）

```
是否涉及重要数据？ → 是 → 安全评估
否
是否CIIO？ → 是 → 安全评估
否
是否处理100万人以上个人信息？ → 是 → 安全评估
否
是否出境100万人以上个人信息？ → 是 → 安全评估
否
是否出境1万人以上敏感个人信息？ → 是 → 安全评估
否
是否出境1-99万人个人信息？ → 是 → 标准合同或认证
否
是否出境1-9999人敏感个人信息？ → 是 → 标准合同或认证
否
是否在自贸区负面清单内？ → 是 → 豁免
否
→ 标准合同或认证（建议）
```

### 3. 技术措施实施

- **数据脱敏/匿名化**：出境前对非必要字段进行脱敏，确保无法关联到特定个人。
- **加密传输**：使用TLS 1.3+、国密算法（SM2/SM3/SM4）进行传输加密。
- **访问控制**：对数据接收方实施最小权限原则，记录所有访问日志。
- **数据本地化**：对于非必要出境的场景，优先在中国境内部署服务器或使用本地云服务。

### 4. 持续合规机制

- 建立**数据出境台账**，记录每次出境的场景、数据量、接收方、法律依据。
- 每季度执行**自评估**，检查出境场景是否变化、接收方是否合规。
- 安全评估到期前6个月启动**续期申请**。

## 中国数据监管重点

### 核心原则

- **本地化优先**：能不出境就不出境，能少出就少出。
- **知情同意**：必须单独告知用户出境目的、接收方、数据范围，并获得明确同意。
- **目的限制**：出境数据只能用于申报时声明的目的，不得超范围使用。
- **接收方约束**：必须通过合同或认证确保接收方达到中国法律同等保护水平。

### 2026年新增关注点

- **生成式AI数据出境**：训练数据、用户输入、模型参数出境均受监管，CAC已发布专项指南。
- **算法推荐与深度合成**：涉及出境场景时，需额外评估算法合规性（如《算法推荐管理规定》《深度合成管理规定》）。
- **重要数据目录更新**：2026年多个行业（金融、汽车、医疗）发布了细化的重要数据目录，出境前必须对照检查。

## 国际规则对照

| 中国要求 | GDPR对应 | 差异点 |
|----------|----------|--------|
| 安全评估 | 数据保护影响评估（DPIA） | 中国需提交CAC审批，GDPR由企业自行评估 |
| 标准合同 | 标准合同条款（SCC） | 中国版本更详细，包含数据删除/返还条款 |
| 认证 | 认证机制（Art.42-43） | 中国认证为强制性路径之一，GDPR为自愿 |
| 数据本地化 | 无强制要求 | 中国对重要数据、CIIO数据有本地化要求 |
| 100万人门槛 | 无对应 | 中国特有，触发安全评估 |

**与SOC 2/ISO 27001的关系**：这些国际认证可作为数据安全能力的佐证，但不能替代中国合规路径。CAC在审核时会参考，但不会直接认可。

## 可以提前准备的检查清单

- [ ] 是否已完成数据映射，识别所有出境场景？
- [ ] 是否已对个人信息进行分类分级？
- [ ] 是否已判断适用的出境路径（安全评估/标准合同/认证）？
- [ ] 是否已起草或签署标准合同（中英文版本）？
- [ ] 是否已进行自评估并保留记录？
- [ ] 是否已实施数据脱敏/加密/访问控制？
- [ ] 是否已建立出境台账和定期审查机制？
- [ ] 是否已确认数据接收方所在国的法律环境？
- [ ] 是否已获得用户单独同意（如适用）？
- [ ] 是否已关注自贸区负面清单的适用性？

## 风险和不确定性

1. **监管标准仍在变化**：CAC可能随时发布新的解释或指南，已批准的路径可能需调整。
2. **自贸区负面清单差异大**：各自贸区清单内容不同，需逐区确认，且清单可能每年更新。
3. **认证路径尚不成熟**：认证机构审核标准不透明，申请周期长，通过率不确定。
4. **执法力度不可预测**：目前以大型企业为执法重点，但中小企业不应掉以轻心。
5. **国际关系影响**：中美、中欧数据流动政策可能影响CAC审核尺度。

## 我的判断

**2026年是中国数据出境合规的“分水岭”**。此前是政策制定期，企业有缓冲空间；此后是执法落地期，不合规将面临实质性处罚。

**对大多数企业而言，标准合同+认证是性价比最高的路径**。安全评估门槛高、周期长（3-6个月），适合大型平台和CIIO。中小企业应优先通过标准合同备案，并在条件允许时申请认证。

**技术团队应主动介入**，不要等法务通知。数据映射、脱敏、加密、日志审计等技术措施是合规的基础，也是降低风险的关键。

**不要试图“绕开”监管**。使用海外服务器、不申报、不备案的做法风险极高，一旦被查处，后果远超合规成本。

**最后，保持动态跟踪**。CAC的监管逻辑是“先立框架，再逐步细化”，未来2-3年还会有更多细则出台。建议每季度审查一次合规状态，并订阅监管动态。

---

## English Brief

### What Happened

China's cross-border data transfer regulatory framework has matured into three parallel paths: **Security Assessment**, **Standard Contract**, and **Personal Information Protection Certification**. Key updates in 2025-2026 include:

- Security Assessment validity set at 2 years, requiring renewal.
- Standard Contract filing simplified but now requires assessment of recipient country's legal environment.
- Certification path officially operational for complex scenarios (e.g., intra-group transfers, multi-tier recipients).
- Free Trade Zone negative lists piloted in Hainan, Shanghai, Beijing, Tianjin.

### Who is Affected

- **AI teams**: Training data, inference data, and model parameters may trigger export rules.
- **SaaS companies**: Customer data, employee data, and support data crossing borders.
- **Multinational corporations**: Global HR, CRM, ERP systems syncing with China.
- **Security/Data teams**: Must implement data mapping, classification, encryption, and access controls.
- **Legal/Compliance teams**: Must choose the correct path and manage regulatory communication.

### Engineering/Security Actions

1. **Data mapping**: Identify all outbound scenarios involving Chinese personal information.
2. **Path determination**: Use the threshold-based decision tree (see Chinese article).
3. **Technical measures**: Data masking, encryption (TLS 1.3+ or SM2/SM3/SM4), access logging, and data localization where possible.
4. **Continuous compliance**: Maintain an export ledger, conduct quarterly self-assessments, and renew Security Assessment 6 months before expiry.

### China Data Compliance Angle

- **Localization first**: Avoid export when possible.
- **Informed consent**: Separate notice and explicit consent required.
- **Purpose limitation**: Data can only be used for declared purposes.
- **Recipient constraints**: Contract or certification must ensure equivalent protection.

### Take

**2026 is the enforcement year.** The grace period is over. Most companies should prioritize **Standard Contract + Certification** over Security Assessment, which is reserved for large platforms and CIIOs. Technical teams must lead—data mapping, encryption, and logging are not optional. Avoid shortcuts; non-compliance penalties (up to 5% of annual revenue or RMB 50 million) far outweigh compliance costs. Review compliance status quarterly and monitor CAC updates.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## China Cross-Border Data Transfer Compliance: Security Assessments, Standard Contracts & Certification in 2026

## China Cross-Border Data Transfer Compliance: Security Assessments, Standard Contracts & Certification in 2026

### What this is

China's cross-border data transfer regime is a three-track system under PIPL Article 38. Depending on data type, volume, and processor category, organizations must use one of: (1) a CAC security assessment, (2) a standard contract filing (China SCC) with the local CAC, or (3) personal information protection certification. The two-year validity of a security assessment and re-application requirements on material changes make this an ongoing compliance burden, not a one-time filing.

### Why it matters now

Any organization processing personal information of individuals located in China is subject to PIPL — including foreign companies with no local entity, if they target Chinese users. The thresholds trigger specific obligations:

- **CAC security assessment (mandatory)** if: important data is exported; the processor is a CIIO; the processor handles PI of 1 million+ individuals; or the volume/sensitivity crosses set thresholds (e.g., large-scale export of sensitive PI).
- **Standard contract filing** applies for lower-volume PI exports (roughly 1–9,999 individuals for non-sensitive, with higher caps for sensitive depending on volume).
- A **self-assessment** must precede any filing or application. The security assessment, once granted, is valid for **only two years** and must be renewed even without changes.

Free trade zones (e.g., Hainan) have published negative lists that relax restrictions in specific sectors like shipping, maritime, and aerospace, but core data affecting national security remains blocked from export.

### Practical next steps

1. **Map your data flows.** Inventory what PI, sensitive PI, and potentially "important data" crosses China's border, and to which recipients.
2. **Determine your track.** Check whether your processor category (CIIO, 1M+ PI threshold) or data type (important data) forces a security assessment regardless of volume.
3. **Run a formal self-assessment** covering legality, legitimacy, necessity, and recipient-side risk — this document is the foundation for both SCC filings and CAC assessments.
4. **File or apply with the local CAC** — SCC filings go through provincial-level CAC offices; security assessments go to the central CAC.
5. **Build a renewal calendar.** Two-year expiry is real; start the renewal before it lapses. Any change in purpose, scope, recipient, or retention period triggers a new application.
6. **If you operate in a free trade zone**, check the negative list for your industry — lower-burden paths may exist.

### Risks and limits

- PIPL penalties: up to RMB 50 million or 5% of prior-year revenue (whichever is higher), plus personal fines for responsible individuals.
- The SCC is not a "sign and file" exercise — the overseas recipient must be bound by equivalent obligations, and you must verify their security capabilities.
- Avoid inventing an exemption: small-enterprise relief is not generally available under PIPL for cross-border transfers.
- The security assessment is not a rubber stamp; MNC filings have been rejected or revised multiple times before approval.

### Take

Treat China cross-border data transfer as a continuous engineering program, not a legal formality. Build data-flow visibility early, track volume thresholds dynamically, and align your vendor contracts and security controls with the SCC's terms from day one. If you're a smaller exporter, the standard contract path is the practical route — but it still demands real documentation and recipient-side diligence.

</div>

---

### 参考来源 / Sources

- [Pillsbury Law | China | 中国通过期待已久的《数据出境安全评估办法》](https://chinese.pillsburylaw.com/china-passes-measures-security-assessment-data-export)
- [什么是中国的 PIPL？定义、原则和法规 | Solix](https://www.solix.com/zh-CN/kb/pipl-china)
- [三尺之律四海之人——数据出境监管政策体系结构及实务操作指南（含自贸区数据出境负面清单全量梳理），兼解读《个人信息出境认证办法》 - 金杜律师事务所](https://www.kingandwood.com/cn/zh/insights/latest-thinking/china-s-cross-border-data-transfer-supervision-system-and-the-measures-for-certification-of-personal-information-export.html)
- [Navigating China's Personal Data Export Compliance: Insights from MNC's Successful Application for Security Assessment | China Law Vision](https://www.chinalawvision.com/2025/03/data-protection-privacy/navigating-chinas-personal-data-export-compliance-insights-from-mncs-successful-application-for-security-assessment)
- [China Unveils Draft Standard Contract and Provides ...](https://www.lw.com/en/insights/admin/upload/SiteAttachments/Alert%202984.pdf)
