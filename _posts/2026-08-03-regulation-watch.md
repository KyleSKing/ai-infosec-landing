---
layout: post
title_en: "China's Revised Cybersecurity Law in Effect: What It Means for Data Export Compliance"
title_cn: "网络安全法修订生效：数据出境合规新要求"
date: 2026-08-03 01:07:40 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "Cybersecurity Law"
  - "cross-border data transfer"
  - "PIPL"
  - "DSL"
  - "compliance"
summary_en: "The revised Cybersecurity Law, effective January 1, 2026, aligns with the DSL and PIPL, imposing stricter cross-border data transfer obligations. Engineering teams must update their data classification, impact assessments, and transfer mechanisms to ensure compliance."
summary_cn: "修订后的《网络安全法》于2026年1月1日生效，与数据安全法和个人信息保护法协调一致，对跨境数据传输提出了更严格的要求。工程团队必须更新数据分类、影响评估和传输机制以确保合规。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 网络安全法修订生效：数据出境合规新要求

# 网络安全法修订生效：数据出境合规新要求

## 发生了什么

2025年，《中华人民共和国网络安全法》（CSL）完成第一次修订，并于2026年1月1日正式生效。修订后的CSL与《数据安全法》（DSL，2021年实施）、《个人信息保护法》（PIPL，2021年实施）实现了制度层面的协调统一。核心变化包括：明确网络运营者的数据出境安全义务、强化重要数据保护、细化与DSL和PIPL的衔接条款。同时，《数据出境安全评估办法》《个人信息出境标准合同办法》《个人信息保护认证办法》等配套规则继续生效，形成了“安全评估—标准合同—认证”三条出境路径。各自由贸易区（如海南、上海、北京等）也相继发布数据出境负面清单，部分场景可豁免评估或合同备案。

## 为什么现在重要

CSL修订生效三个月以来，监管层面已开始按照新要求执行检查。对于仍在沿用旧有备案或未完成数据出境合规的企业，当前是硬性整改窗口期。尤其是处理个人信息超过100万人、运营关键信息基础设施（CII）、或涉及重要数据出境的实体，必须重新评估自身义务是否满足新规。此外，自贸区负面清单的推出允许部分低风险业务数据自由流动，但负面清单之外的出境场景仍需遵循严格的评估或备案程序。如果企业未及时调整数据出境方案，将面临行政处罚、业务暂停乃至刑事责任风险。

## 影响谁

- **AI产品/大模型公司**：训练数据涉及跨境流转、模型输出返回境外、或向海外客户提供服务，需重点审查是否触发安全评估。
- **出海SaaS/互联网平台**：用户数据存储在境外服务器、或向境外提供客户行为分析数据，需判断个人信息出境合规路径。
- **跨国企业（外企在华子公司）**：内部管理数据（HR、财务）传回总部，可能涉及重要数据和大量个人信息。
- **数据/安全/工程团队**：负责数据分类分级、数据映射、技术防护措施（加密、去标识化）、配合PIA和申报。
- **法律/合规团队**：需重新梳理现有合同条款，确保符合PIPL第38条及CSL修订后的要求。
- **CIIO（关键信息基础设施运营者）**：出境安全评估强制义务，且不能以标准合同替代。

## 工程/安全/数据团队要做什么

1. **数据发现与分类分级**  
   - 扫描内部数据库、API日志、云存储，识别哪些数据包含个人信息（尤其是超过100万条）、重要数据（如地理信息、经济统计数据、基因数据）。
   - 按照《数据安全法》第21条和行业标准进行分类分级，标记出境数据范围。

2. **数据出境影响评估（PIA）**  
   - 针对每一类出境数据，完成个人信息保护影响评估（PIPL第55条），内容需包括：处理目的、必要性、对个人权益的影响、安全风险、与境外接收方的合同约定。
   - 保留PIA报告至少3年，供监管检查。

3. **选择合规出境路径**  
   - **安全评估**：CIIO、处理100万人以上个人信息且出境、重要数据出境，必须申报国家网信办（CAC）安全评估。
   - **标准合同备案**：非上述情形、且不属于重要数据，可与境外接收方签署《个人信息出境标准合同》，向属地省级网信办备案。
   - **个人信息保护认证**：申请专业机构认证（如CCRC），替代标准合同。
   - **自贸区负面清单**：检查公司注册地自贸区负面清单，若出境数据场景在清单允许范围内（如国际航运、船员管理、会员管理等），可免评估或简化流程。注意负面清单仅适用于自贸区内注册企业。

4. **技术措施实施**  
   - 对出境数据进行匿名化或去标识化处理，降低风险等级（PIPL第4条：匿名化后不属于个人信息）。
   - 部署加密传输通道（TLS 1.3+），对敏感字段进行字段级加密。
   - 实施访问控制，最小化出境数据范围，避免无关数据流出。

5. **申报流程跟进**  
   - 安全评估：提交自评估报告、合同草案、PIA报告等至CAC，评审周期通常45-60天。
   - 标准合同备案：签署合同后10个工作日内提交备案材料，若被要求补充说明，需及时响应。
   - 认证：选择认证机构，通过现场检查后获得认证证书。

6. **持续监控与更新**  
   - 建立数据出境台账，定期（至少每年一次）复核出境场景是否发生变化（如数据量增加、接收方变更、处理目的改变），如有变化需重新评估或备案。
   - 关注监管动态：重要数据目录（各行业陆续发布）、自贸区负面清单更新、CAC执法重点。

## 中国数据监管重点

- **PIPL第38条**：明确了数据出境的四个法定条件（安全评估、标准合同、认证、其他法律行政法规规定）。修订后的CSL未推翻此路径，而是加强了网络运营者的记录和报告义务。
- **PIPL第40条**：CIIO和处理100万人以上个人信息的运营者，出境原则上应通过安全评估。修订后的CSL进一步要求此类运营者将个人信息和重要数据存储在境内，出境需单独评估。
- **DSL第31条**：重要数据出境安全评估由CAC牵头，国家行业主管部门配合。重要数据定义模糊，但范围广——非个人信息但关系国家安全、经济发展。
- **自贸区负面清单**：目前海南、上海、北京等已发布，允许特定场景（如国际航运、跨境支付、生物医药临床试验）不经安全评估即出境，但负面清单之外一律从严。企业需核实自己是否在清单白名单内。
- **CSL修订后新增条款**：网络运营者应制定数据安全管理制度、实施技术措施、定期进行风险评估；违反者罚款最高可达100万元（对直接责任人）。对于出境违规，可能同时触发PIPL（最高5000万元或上年营业额5%）和DSL的处罚。

## 国际规则对照

- **GDPR**：中国出境合规类似于GDPR的“适当保障措施”（标准合同条款、约束性公司规则BCR）。但中国没有“充分性认定”机制，所有出境原则上需经境内评估或备案。对于欧盟向中国传输数据，则需满足GDPR第45条的要求（中国是否被欧盟认定为充分性国家？目前未认定，因此需依赖标准条款或BCR）。
- **EU AI Act**：若AI产品将训练数据或用户数据从欧洲传出中国，需同时满足GDPR的跨境传输限制和PIPL的接收方义务。尤其是有高风险AI系统时，需确保境外数据保护水平不低于欧洲标准。
- **NIS2/DORA**：欧盟金融业或关键实体若在中国开展业务，需遵守CSL修订后的网络安全管理要求（如CII识别、安全评估），同时满足NIS2的供应链安全规定。
- **SOC 2 / ISO 27001**：虽非强制法律，但作为合规证明，可帮助展示数据安全能力。在安全评估或认证中，拥有ISO 27001认证可作为加分项，但不能替代法定的评估程序。

## 可以提前准备的检查清单

- [ ] 确认企业是否属于CIIO（通过行业主管部门通知或自查）。
- [ ] 统计所处理的个人信息总量是否超过100万人（注意：累计统计，非年度单一场景）。
- [ ] 识别所有涉及数据出境的系统、API、第三方服务商。
- [ ] 完成数据分类分级，标出重要数据和敏感个人信息。
- [ ] 为每一条出境场景撰写PIA报告，覆盖目的、必要性、风险、合同约定。
- [ ] 选择出境路径（安全评估/标准合同/认证），并准备相应材料（合同草案、评估报告）。
- [ ] 若适用自贸区负面清单，准备场景证明材料（如合同、业务说明）。
- [ ] 技术层面：实施数据脱敏/加密/审计日志。
- [ ] 建立数据出境治理流程，指定专人负责，定期（至少每半年）复核。
- [ ] 与法律顾问共同审核与境外接收方的合同是否包含同等保护条款（PIPL第38条第3项）。

## 风险和不确定性

1. **重要数据定义不清晰**：各行业重要数据目录出台进度不一，企业可能错判。目前通用做法：涉及国家安全、经济运行、人口健康、自然资源等未公开信息，一律按重要数据处理。
2. **安全评估周期长**：CAC安全评估通常需要45-60天，复杂场景可能延长至90天以上。业务紧急时可能被迫暂停出境。
3. **自贸区负面清单适用性有限**：负面清单仅针对自贸区内注册企业，且行业范围有限（航运、医药、贸易等）。对于大多数互联网和AI企业，几乎不适用。
4. **执法不确定性**：2026年以来，CAC对短视频平台、AI企业开展专项检查，处罚案例可能迅速增多。企业不能等待细则明确再行动。
5. **国际规则冲突**：当中国要求本地化存储与欧盟要求数据自由流动冲突时（如金融数据），企业需同时满足两地要求，尚无明确协调机制。

## 我的判断

**CSL修订的生效不是一次简单的法律更新，而是一次监管逻辑的收网**。此前PIPL和DSL的很多条款依赖CSL的修订才能落地执行，而2026年1月1日正是这个衔接点。对于工程和数据团队，最紧迫的任务不是读法条，而是**画出企业的数据出境全景图**——哪些数据流向哪些国家，是否有CII身份，个人信息量是否超过100万。只有在此基础上，才能避免“一揽子评估”或“一刀切禁止”的极端做法。AI产品尤其要警惕：训练数据若涉及跨境，且包含大量用户原始数据或生成式内容，极可能被归类为“重要数据”或触发安全评估。我的建议是：先走标准合同备案作为快速合规路径（非CII且个人信息量小于100万），同时启动重要数据识别和PIA，为未来可能转向安全评估留出缓冲期。自贸区负面清单只适用于极少数场景，不要抱侥幸心理。最后，保持与行业同行和监管机构的沟通——当前合规实践正在快速演进，早期投入可以避免后期被动整改。

---

**English Brief**

**What happened**: China's Cybersecurity Law (CSL) amendment took effect on January 1, 2026, aligning with PIPL and DSL. Cross-border data transfer now requires either a security assessment (for CIIOs, >1M personal records, or important data), a standard contract filing, or certification. Free trade zones have issued negative lists exempting certain scenarios.

**Who is affected**: AI/ML companies, SaaS exporters, multinationals, CIIOs, data/security/legal teams. Any organization sending personal or important data outside China.

**Engineering/security actions**:  
- Conduct data discovery and classification (personal info volume, important data).  
- Perform PIA for each export scenario.  
- Choose the correct path (security assessment / SCC / certification).  
- Implement technical controls (encryption, anonymization).  
- Submit filings within required timeframes.

**China data compliance angle**: The CSL revision enforces the existing PIPL+DSL framework. The key is identifying whether your entity qualifies for the mandatory security assessment (CIIO or >1M personal info). Standard contracts remain the most practical route for most non-CII companies, but important data triggers higher obligations.

**Take**: Treat this as a hard deadline. Build a complete data export inventory now, file PIA and contract drafts immediately. Don't rely on vague definitions; prioritize mapping before the regulatory audit wave hits. For AI products, training data cross-border flows are high-risk — assess if they constitute important data or trigger the 1M-person threshold. Use standard contracts as a fast track, but prepare for potential escalation to security assessment later.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## China's Revised Cybersecurity Law in Effect: What It Means for Data Export Compliance

# China's Revised Cybersecurity Law in Effect: What It Means for Data Export Compliance

China’s revised Cybersecurity Law (CSL) took effect on 1 January 2026, marking its first major update since 2017. The revision achieves coordinated integration with the Personal Information Protection Law (PIPL) and the Data Security Law (DSL), creating a unified data export compliance framework for engineering and security teams.

## What It Is

The revised CSL now aligns with the PIPL and DSL, clarifying the three legally recognized routes for cross-border data transfers: security assessment, filing of standard contracts, and personal information protection certification. The update also codifies the triggers that force a security assessment, previously only found in separate regulations.

## Why It Matters Now

The revised CSL eliminates previous ambiguity. Any organization exporting personal information or important data from China must now clearly map which pathway applies. The most impactful change is the mandatory security assessment trigger: **any data processor that handles personal information of more than one million individuals must pass a CAC security assessment before any export**, regardless of the volume exported. This catches large internet platforms, app operators, and enterprise SaaS providers serving Chinese users. Additionally, CII operators and entities exporting important data remain subject to assessment.

## Practical Next Steps

1. **Data inventory and classification** – Identify all personal information (PI) and important data processed. Know the volume of PI subjects.
2. **Determine trigger status** – Check if your organization processes PI of 1M+ individuals, operates as a CIIO, or exports important data.
3. **Choose compliance pathway** – If triggered, initiate a CAC security assessment. Otherwise, use PIPL standard contracts or certification.
4. **Conduct PI protection impact assessment** – Required before any export, regardless of pathway.
5. **Obtain separate consent** – Inform data subjects of the export details and get their individual consent.
6. **Update internal policies** – Revise data export SOPs, retention policies, and contracts with overseas recipients.
7. **Monitor free trade zone rules** – Some zones (e.g., Hainan, Shanghai) have negative lists that simplify exports for specific industries.

## Risks and Operational Notes

- **Non-compliance penalties** under the revised CSL include fines up to 5% of annual revenue, suspension of operations, and revocation of licenses.
- **False positives matter** – Even if you only export 100 records, you must still assess if you cross the 1M threshold of total PI processed.
- **Third-party certification bodies** are still being accredited; if you choose the certification route, verify the body is CAC-approved.

## Take

The revised CSL does not introduce new data export requirements but **codifies and harmonizes existing ones**. Engineering teams should prioritize a full data flow audit and determine their export pathway before any cross-border data transfer. Start with the 1M-PI-subject test; if you fail it, begin the security assessment process immediately—it can take months. The framework is now stable; treat it as an operational baseline, not a moving target.

</div>

---

### 参考来源 / Sources

- [Pillsbury Law | China | 中国通过期待已久的《数据出境安全评估办法》](https://chinese.pillsburylaw.com/china-passes-measures-security-assessment-data-export)
- [三尺之律四海之人——数据出境监管政策体系结构及实务操作指南（含自贸区数据出境负面清单全量梳理），兼解读《个人信息出境认证办法》 - 金杜律师事务所](https://www.kingandwood.com/cn/zh/insights/latest-thinking/china-s-cross-border-data-transfer-supervision-system-and-the-measures-for-certification-of-personal-information-export.html)
- [Avature 伴您实现《个人信息保护法》（PIPL） 合规之旅](https://www.avaturehcm.cn/wp-content/uploads/2022/01/achieving-PIPL-compliance-guide-pdf-CN-1221-1.pdf)
- [China: The interplay between the PIPL, DSL, and CSL | Opinion | DataGuidance](https://www.dataguidance.com/opinion/china-interplay-between-pipl-dsl-and-csl)
- [Comparisons  | Global Practice Guides | Chambers and Partners](https://practiceguides.chambers.com/practice-guides/comparison/1129/18498/29027-29028-29029-29030-29031)
