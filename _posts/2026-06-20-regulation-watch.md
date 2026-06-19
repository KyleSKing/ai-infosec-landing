---
layout: post
title_en: "China's Data Export Compliance: New Rules for Cross-Border Transfers"
title_cn: "中国数据出境合规新规：跨境传输实操指南"
date: 2026-06-20 01:48:14 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "data export"
  - "PIPL"
  - "cross-border"
  - "compliance"
  - "AI regulation"
summary_en: "China's PIPL and DSL require data export risk assessments and standard contracts for cross-border transfers. Non-compliance risks penalties, with new rules for AI and SaaS products."
summary_cn: "中国PIPL和DSL要求数据出境前进行安全评估并签订标准合同，违规面临处罚。新规对AI和SaaS产品跨境数据流动提出更严格合规要求。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 中国数据出境合规新规：跨境传输实操指南

# 中国数据出境合规新规：跨境传输实操指南

## 发生了什么

截至2026年6月，中国数据出境监管框架已基本成型，核心三法——《网络安全法》《数据安全法》《个人信息保护法》——下形成的“安全评估+标准合同+认证”三条合规路径在实践中走向细化与差异化。2024年3月发布的《促进和规范数据跨境流动规定》降低了部分场景的申报门槛，随后多个自贸区（北京、上海、天津、海南、福建等）陆续出台数据出境负面清单，允许清单外数据在特定场景下通过简化程序出境。2025年，国家网信办进一步明确重要数据识别标准，并试点“数据跨境流动分级分类管理”。当前，企业面对的不再是单一的“要不要申报”，而是一套基于数据类型、数量、接收方、业务场景的阶梯式决策树。

## 为什么现在重要

- **执法进入常态化**：截至2026年，已有数十家企业的数据出境安全评估申请被驳回或要求整改，罚款案例上升。监管不再只盯头部平台，中型SaaS、出海游戏、智能制造、医疗数据服务商均被纳入检查范围。
- **自贸区负面清单释放红利**：不触发负面清单的场景可免于安全评估或标准合同备案，但企业需自行举证数据不在清单范围内，内部数据分类分级能力成为合规前提。
- **国际冲突加剧数据主权博弈**：欧盟GDPR、美国CLOUD Act、中国数据法之间存在管辖重叠，跨国企业面临“双重合规”甚至“三向合规”压力。例如，中国员工数据存储于境外HR系统，同时需满足GDPR向第三国转移的要求。
- **AI与云服务带来新场景**：跨境调用AI API（如大模型推理）、境外员工远程运维境内系统、国际并购中的数据迁移，这些场景的数据出境认定和合规路径仍在持续细化。

## 影响谁

| 角色 | 直接影响 |
|------|----------|
| **AI产品团队** | 使用境外大模型API处理训练数据或用户查询，可能构成“数据出境”（即使数据未复制至境外，仅被境外模型访问）。 |
| **SaaS出海团队** | 中国用户数据与海外用户数据混合存储，需设计数据隔离架构并明确出境链路。 |
| **安全与数据团队** | 负责数据分类分级、跨境映射、安全影响评估、技术控制措施（加密、脱敏、审计日志）。 |
| **法务/合规团队** | 评估适用路径、起草标准合同、对接自贸区政策、应对监管检查。 |
| **外企中国分部** | 境内收集的个人信息传输至全球HR/CRM系统，需完成安全评估或签订标准合同。 |
| **供应链/制造业** | 涉及重要数据（如生产参数、供应链图谱）出境，风险自评估复杂。 |

## 工程/安全/数据团队要做什么

### 1. 构建数据出境映射矩阵
- 识别所有跨境流动的数据资产：包括通过API、DB同步、人工导出、第三方服务（如PaaS、SaaS、CDN）等路径。
- 标注数据类型（个人信息、敏感个人信息、重要数据、一般数据）、量级（当年累计、单次峰值）、接收方国家/地区、存储与处理目的。
- 采用数据分类分级工具（如DLP扫描+手动标注）并持续更新。

### 2. 实施技术控制措施
- **加密与脱敏**：出境数据在传输层（TLS 1.3）和应用层（字段级加密）加密；重要数据必须脱敏或匿名化后再出境（需确认脱敏后仍属于“重要数据”）。
- **访问日志**：记录所有出境请求的源IP、目标、数据量、审批号，保留至少2年（对应网信办安全评估复评周期）。
- **数据本地化实例**：对于CIIO或超100万人个人信息处理者，需确保主数据存储在国内节点，境外仅可访问脱敏副本。
- **API网关控制**：对境外API调用进行实时鉴权和流量审计，防止未申报的数据通过内网代理“意外”出境。

### 3. 建立合规决策流程
- 业务或产品需求出境时，先查内部《数据分类分级清单》，判断是否属于“重要数据”或触发安全评估阈值（处理100万人以上个人信息、年累计10万人普通或1万人敏感个人信息）。
- 若属于一般个人信息且未触发阈值，可签标准合同（SCC）或走认证（PIP认证）。
- 若属于自贸区负面清单内场景（如部分汽车数据、航运数据），必须走安全评估；清单外则适用简易程序。
- 若数据同时涉及GDPR（如涉及欧盟数据主体），需同时满足中国出境路径和GDPR充分性认定/BCR/SCC要求。

### 4. 定期复评与演练
- 安全评估结果有效期为2年，到期前6个月启动复评申请；期间发生接收方变更、数据规模超预估、法律环境重大变化等，需立即重新申报。
- 每年至少做一次数据出境风险自评估，模拟监管检查（材料完备性、技术措施有效性、合同条款落地情况）。

## 中国数据监管重点

- **重要数据识别**：目前仍未出台统一“重要数据目录”，各行业监管部门（工业、交通、汽车、医疗、金融、自然资源）正逐一发布本领域目录。企业必须对标所属行业征求意见稿，即使未被正式公布也应参照进行内部预识别。
- **个人信息保护影响评估（PIA）**：所有数据出境场景（不论走哪条路径）均须完成PIA，且应保存评估报告至少3年。
- **单独同意**：向境外接收方提供个人信息，需取得个人单独同意，且同意内容需明确境外接收方名称、联系方式、处理目的、方式、数据种类、保存期限。默示拒绝机制（如勾选框默认未勾选）。
- **CIIO义务加重**：关键信息基础设施运营者即使未触发阈值，也必须通过安全评估才能出境个人信息和重要数据。
- **自贸区负面清单的适用条件**：企业需在自贸区内注册或实际经营，且数据出境完全服务于清单所列业务场景（如国际物流、生物医药临床、跨境支付等），否则仍需走普适路径。

## 国际规则对照

| 维度 | 中国规则 | 对应国际规则 |
|------|----------|-------------|
| 出境前提 | 安全评估/标准合同/认证 | GDPR：充分性认定/BCR/SCC（标准合同条款1.0/2.0） |
| 数据本地化 | CIIO及特定行业强制 | 俄罗斯、印度、越南也有类似，GDPR不强制但鼓励 |
| 影响评估 | PIA必做，且需留档 | GDPR DPIA（数据保护影响评估）要求类似 |
| 个人权利 | 单独同意、撤回权、删除权 | GDPR知情权、删除权、数据可携权等 |
| 执法力度 | 2024年以来加大行政罚款和责令整改 | EU最高2000万欧元/4%全球营收 |
| 国际传输工具 | SCC（网信办模板）、NQI认证 | SCC（EU 2021/914）、BCR、CBPR（APEC） |
| 重要数据保护 | 《数据安全法》专项制度 | 无直接对应，NIS2要求关键基础设施强化安全，SOC 2关注保密性/可用性 |

跨国企业的实用策略：同时满足中国SCC + EU SCC，在一份合同中嵌入双方条款；采用部署地隔离 + 合规审批 + 持续监控的“三明治”架构。

## 可以提前准备的检查清单

- [ ] 1. 数据分类分级：完成全量数据资产盘点，标记出境字段，建立“重要数据”预识别清单。
- [ ] 2. 出境链路梳理：绘制数据流向图（包括第三方API、SDK、云计算平台），标注每一条出境的起始点和终结点。
- [ ] 3. 安全评估材料包初稿：包括数据出境风险自评估报告、数据处理者与接收方之间的合同、个人信息保护影响评估报告、数据安全能力证明（等级保护、等保测评等）。
- [ ] 4. 技术控制检查：加密传输、脱敏处理、访问控制、日志审计、最小化原则（仅传输必需字段）。
- [ ] 5. 同意机制更新：在用户注册/授权界面补充单独的“数据出境同意”选项，明确接收方信息。
- [ ] 6. 合同版本核对：使用最新版网信办标准合同模板（2023版已更新），确认接收方义务和责任分配。
- [ ] 7. 自贸区政策审查：如公司在自贸区内，评估是否适用负面清单并简化路径。
- [ ] 8. 复评预警：记录安全评估到期日、重大变更触发条件，提前6个月启动工作。
- [ ] 9. 内外部培训：数据合规负责人、业务PM、研发负责人了解出境判定标准和操作流程。
- [ ] 10. 应急预案：一旦接到监管通知要求暂停出境，需有技术方案（切断跨境连接、启动本地备份、切换国内镜像实例）并能在24小时内执行。

## 风险和不确定性

- **重要数据目录未完整覆盖**：部分行业（如教育、生物技术、人工智能训练数据）尚未发布正式目录，存在“灰色区”——企业自评为非重要数据，监管后续认定为重要数据，可能导致违规处罚。
- **跨境执法协调难度**：当境外接收方所在国法律（如美国FISA 702）要求提交数据时，合同约定的“配合中国法”条款可能无法实际执行，企业面临两难。
- **标准合同的更新频率**：网信办SCC模板可能与欧盟SCC冲突，需不断调整。2025年曾因中国SCC中“接收方应向网信办提供例行数据报告”条款引发国际争议，目前还有企业搁置签署。
- **“访问即出境”的认定边界模糊**：境外人员通过VPN或专线访问境内系统，是否构成数据出境？目前监管倾向于“实质性访问（如能导出、下载、查询到明细数据）视为出境”，但存有解释空间。工程上建议对境外访问严格权限分离：只提供脱敏视图或经同意的聚合数据。
- **自贸区政策落地不一致**：各地负面清单细节不同（如上海自贸区与海南自贸港对“汽车数据”的豁免条件不同），集团型企业需按注册地逐一核对，增加合规成本。

## 我的判断

中国数据出境合规不再是“做不做”的问题，而是“怎么做精”的问题。2024年的简化政策并非放宽监管，而是将资源集中于高危害场景（重要数据、海量个人信息、CIIO），对于低风险一般个人信息出境给予路径便利。因此：

- **对工程团队**：核心投入不是等法务通知，而是提前落地数据分类分级和出境映射。一个自动化标注+实时阻断的工具链，比事后补救有效十倍。
- **对CIIO和海量数据处理者**：安全评估是不可绕过的硬门槛，且复评风险持续存在。建议建立“永续合规”团队，每季度review一次数据出境全景。
- **对跨境SaaS和AI产品**：最稳妥的方案是“数据不出境”或“匿名化 + 低颗粒度聚合”。如果必须出境，应选择走标准合同（成本最低、效率最高），但需预留充足时间——SCC备案或认证通常需要3-6个月。
- **对国际企业**：中国SCC与欧盟SCC的融合是现实选择，但务必增加“法律冲突时的适用优先级”条款，并准备备份存储拓扑。

一句话总结：**合规不等于不变通，但变通的底线是“能自证”**。所有决策（是否出境、走哪条路径、用什么技术措施）都应记录在案，形成一封能从容应对监管质询的“合规档案”。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## China's Data Export Compliance: New Rules for Cross-Border Transfers

# China's Data Export Compliance: New Rules for Cross-Border Transfers

## What It Is

China's cross-border data transfer framework is anchored by the Cybersecurity Law (CSL), Data Security Law (DSL), and Personal Information Protection Law (PIPL). These laws require data processors to meet specific conditions before transferring personal information or “important data” outside mainland China. The primary compliance paths are: (1) passing a CAC-led security assessment (for CIIOs or those exceeding volume thresholds), (2) executing standard contracts (SCC) with the overseas recipient, or (3) obtaining personal information protection certification. Recent updates include negative lists for free trade zones, which exempt certain data types from restrictions, and expanded guidance from regulators.

## Why It Matters Now

Regulatory enforcement is intensifying. The CAC has published detailed assessment procedures, and provincial-level cyberspace offices are conducting completeness checks before submission. New free trade zone negative lists (e.g., in Shanghai, Beijing, Tianjin) explicitly map which data categories still require security assessment, SCC, or certification — and which are permitted to flow freely. Meanwhile, industries such as automotive, shipping, and human resources face sector-specific rules. Any company with cross-border operations involving Chinese‑originated data must reassess its compliance posture, as non‑compliance can lead to fines up to 5% of annual revenue, suspension of data transfers, or even criminal liability.

## Practical Next Steps for Engineering Teams

1. **Map data flows and classify data.** Identify whether data leaving China includes “important data” (defined by industry regulators) or personal information. For personal information, calculate cumulative volumes over the past year (100,000 persons for personal info, 10,000 for sensitive personal info are thresholds triggering mandatory security assessment).
2. **Conduct a risk self-assessment.** For each cross-border scenario (including remote access by overseas staff), document the purpose, scope, recipient’s protection measures, and impact on individual rights. Update annually.
3. **Choose the right compliance path.** If thresholds are met, prepare for CAC security assessment (submission through provincial cyberspace office). If below thresholds, use SCC filing or certification. For free trade zone entities, check the latest negative list — many routine data transfers (e.g., international trade, logistics, certain HR data) may now be exempt.
4. **Update contracts and consent mechanisms.** Ensure data processing agreements with overseas recipients include PIPL‑required clauses. Obtain separate consent from individuals (not buried in general terms).
5. **Monitor regulatory changes.** The framework is still evolving — follow CAC announcements and industry-specific guidelines (e.g., from MIIT for automotive data).

## Risks to Watch

- **Data localization requirements:** Certain “important data” and CIIO‑related data must remain in China unless security assessment is passed. Free trade zone exemptions do not apply to national security‑related data.
- **Evolving definitions:** “Important data” lists vary by industry and are being finalized — a conservative approach is recommended until clear guidance is published.
- **Audit and enforcement risk:** Regulators can order audits or suspend transfers even after initial approval. Any change in data volume, purpose, or recipient triggers a re‑assessment.

## Take

China’s cross‑border data rules are not static — they are a layered system with paths that depend on data type, volume, entity status, and location (free trade zone or not). Engineering and compliance teams should run a data flow audit now, classify every data field, and map each transfer to the corresponding CAC pathway. For most outbound SaaS and tech companies, the default next step is to prepare an SCC filing while monitoring whether upcoming “important data” catalogs push you into mandatory security assessment territory. Proactive mapping and contract updates are the cheapest insurance against a sudden enforcement action.

</div>

---

### 参考来源 / Sources

- [[PDF] 数据出境安全评估: 背景和要点 - PCPD](https://www.pcpd.org.hk/english/whatsnew/files/professor_hong.pdf)
- [[PDF] 数据出境安全评估管理建议](https://assets.kpmg.com/content/dam/kpmg/cn/pdf/zh/2022/07/practical-guidelines-for-managing-cross-border-data-transfer-in-china.pdf)
- [三尺之律四海之人——数据出境监管政策体系结构及实务操作指南（含自贸区数据出境负面清单全量梳理），兼解读《个人信息出境认证办法》 - 金杜律师事务所](https://www.kingandwood.com/cn/zh/insights/latest-thinking/china-s-cross-border-data-transfer-supervision-system-and-the-measures-for-certification-of-personal-information-export.html)
- [数据主权和中国法规 | Microsoft Learn](https://learn.microsoft.com/zh-cn/azure/china/overview-sovereignty-and-regulations)
- [嘉源研究 | 《网络安全法》、《数据安全法》和《个人信息保护法》：三法联动开启企业新一轮数据合规浪潮 | 嘉源律师事务所 Jia Yuan Law Offices](https://www.jiayuan-law.com/cn/news_content.aspx?Lan=CN&MenuID=00000000000000000006&KeyID=00000000000000002065&Type=00000000000000000081)
