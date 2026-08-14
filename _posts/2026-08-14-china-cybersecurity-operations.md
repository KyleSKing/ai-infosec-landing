---
layout: post
title_en: "China CIIO & MLPS Compliance: New Enforcement Signals for Important Data and Cross-Border Ops"
title_cn: "关基与等保合规新信号：重要数据与跨境运维实操要点"
date: 2026-08-14 14:43:39 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "CIIO"
  - "MLPS"
  - "important data"
  - "data export"
  - "China compliance"
summary_en: "Recent regulatory signals tighten CIIO obligations on procurement, domestic maintenance, and data export security assessments. MLPS 2.0 compliance remains a five-stage process with mandatory third-party evaluation, affecting all SaaS, AI, and outbound businesses handling important data."
summary_cn: "近期监管信号强化关基运营者在采购、境内运维及数据出境安全评估上的义务。等保2.0合规仍为五阶段流程，须由有资质机构测评，影响所有涉及重要数据的SaaS、AI及出海企业。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 关基与等保合规新信号：重要数据与跨境运维实操要点

# 关基与等保合规新信号：重要数据与跨境运维实操要点

## 发生了什么

2026年以来，中国关键信息基础设施（CII）和数据安全监管进入精细化执行阶段。核心变化集中在三个方向：

1. **CIIO采购与外包安全审查**：根据《网络安全法》第三十五条及《关键信息基础设施安全保护条例》（以下简称《关保条例》）第三十一、三十二条，CIIO采购网络产品和服务若可能影响国家安全，必须通过国家网络安全审查。外包开发的系统上线前必须进行安全检测，并签订安全保密协议。

2. **数据境内存储与跨境运维收紧**：《网安法》第三十七条要求CIIO在境内运营中收集和产生的个人信息和重要数据存储在境内。确需向境外提供的，须按《数据出境安全评估办法》进行安全评估。更关键的是，《关保条例》第三十四条明确：**关键信息基础设施的运行维护应当在境内实施；因业务需要确需境外远程维护的，应事先报国家行业主管或监管部门和国务院公安部门**。这意味着跨境运维不再是“内部审批”即可，而是需要向两个政府部门报批。

3. **等保2.0全流程闭环**：等保2.0的定级、备案、建设整改、等级测评、监督检查五阶段已形成完整闭环。评估只能由有资质的评估机构进行，报告提交公安部网络安全办公室审核。阿里云等云服务商已推出合规解决方案，但企业自身仍需承担定级和整改的主体责任。

## 为什么现在重要

2025-2026年是中国数据安全法规的“执行深化期”。此前很多企业将关基认定、重要数据目录、跨境运维报批视为“理论要求”，但近期监管动作表明：

- 行业主管/监管部门正在加速制定本行业关基认定规则，并组织认定工作。
- 数据出境安全评估的申报量激增，未申报即跨境传输的处罚案例开始公开。
- 跨境运维报批的“事先”要求被执法部门强调，已有企业因未报批被约谈。

对于使用海外云服务、跨国运维、外包开发、采购海外网络产品的企业，合规窗口正在关闭。

## 影响谁

- **CIIO（关键信息基础设施运营者）**：直接受《关保条例》约束，采购、运维、数据出境均需合规。
- **AI产品与SaaS企业**：若被认定为CII或处理重要数据，需满足数据本地化、安全评估、算法备案等要求。跨境提供AI服务需额外关注。
- **出海企业（Outbound SaaS）**：在境内运营中收集数据，即使面向海外客户，仍受中国数据法管辖。跨境运维团队需报批。
- **安全团队与数据团队**：需建立重要数据识别、分类分级、风险评估、应急响应机制。
- **法律/合规团队**：需跟踪行业关基认定规则、数据出境安全评估指南、跨境运维报批流程。
- **产品团队**：涉及外包开发、第三方SDK、海外运维工具的产品，需重新设计数据流和运维架构。

## 工程/安全/数据团队要做什么

### 1. 重要数据识别与分类分级
- 依据《数据安全法》第二十一条，建立数据分类分级制度，确定重要数据目录。
- 参考行业标准（如金融、能源、交通等已出台的指南），识别本企业是否处理重要数据。
- 重要数据的处理者需明确数据安全负责人和管理机构，定期开展风险评估并上报。

### 2. 数据本地化与跨境合规
- 检查所有CII系统：个人信息和重要数据是否存储在境内？若否，立即制定迁移计划。
- 对确需出境的场景，启动数据出境安全评估流程。先完成自我评估，再向省级网信办申报。
- 跨境运维报批：梳理所有境外远程维护场景（包括VPN、堡垒机、远程桌面等），准备报批材料（业务必要性、安全方案、数据保护措施），向行业主管/监管部门和公安部提交申请。

### 3. 采购与外包安全审查
- 建立采购审批流程：对可能影响国家安全的网络产品和服务，启动国家安全审查（参考《网络产品和服务安全审查办法》）。
- 与供应商签订安全保密协议，明确安全义务。
- 外包开发的系统，上线前必须进行安全检测（渗透测试、代码审计、配置核查）。

### 4. 等保2.0合规落地
- 完成定级：确定对象等级，准备定级报告。
- 备案：将报告提交当地公安机关。
- 建设整改：依据等保2.0基本要求进行差距分析，部署安全产品（防火墙、IDS/IPS、日志审计、堡垒机等）。
- 等级测评：委托有资质评估机构进行测评，获取报告。
- 监督检查：配合公安机关和行业主管部门检查。

### 5. 持续监控与应急
- 建立数据安全风险监测机制，对缺陷、漏洞及时补救。
- 制定数据安全应急处置预案，发生事件后立即处置并上报。
- 定期开展数据安全风险评估，形成报告存档。

## 中国数据监管重点

- **重要数据保护**：国家建立重要数据目录，CIIO和重要数据处理者承担更高义务（本地存储、安全评估、负责人、定期风评）。
- **跨境数据传输**：数据出境安全评估、标准合同、认证三条路径并行。CIIO仅适用安全评估路径。
- **跨境运维报批**：这是《关保条例》第三十四条的独特要求，与一般数据出境不同，需额外报批。
- **等保2.0与关基保护联动**：等保是基础，关基是重点。CIIO必须在等保三级以上基础上满足关基专项要求。
- **生成式AI与算法合规**：若AI产品涉及算法推荐、深度合成、生成式AI，需履行算法备案、安全评估、内容审核等义务。

## 国际规则对照

| 中国要求 | 国际对应规则 | 差异点 |
|---------|------------|--------|
| 重要数据本地存储 | GDPR第44-49条（数据跨境限制） | 中国对重要数据定义更宽泛，且无“充分性认定”替代路径 |
| 数据出境安全评估 | GDPR SCCs + 影响评估 | 中国安全评估是前置审批，而非事后备案 |
| 跨境运维报批 | 无直接对应 | 欧盟NIS2要求事件报告，但未要求运维地点 |
| 等保2.0 | ISO 27001、SOC 2 | 等保是强制等级制度，ISO/SOC是自愿认证 |
| 关基保护 | NIS2（欧盟）、DORA（金融） | 中国监管更强调境内运维和采购审查 |

对于同时受GDPR管辖的企业，需注意中国数据出境安全评估与GDPR SCCs的衔接——同一数据流可能需同时满足两套规则。

## 可以提前准备的检查清单

- [ ] 是否已识别本企业是否属于CIIO？是否收到行业主管部门的认定通知？
- [ ] 是否已建立重要数据目录？是否明确数据安全负责人？
- [ ] 所有CII系统的数据是否存储在境内？若否，是否已启动迁移或申报？
- [ ] 是否存在境外远程运维场景？是否已向行业主管和公安部报批？
- [ ] 采购的网络产品和服务是否经过安全审查？外包系统是否上线前检测？
- [ ] 等保定级是否完成？是否已备案？等级测评是否在有效期内？
- [ ] 是否建立了数据安全风险评估和应急响应机制？最近一次风评时间？
- [ ] 是否与供应商签订了安全保密协议？
- [ ] 是否跟踪了本行业关基认定规则的最新动态？

## 风险和不确定性

- **重要数据范围不明确**：虽然国家层面有目录，但行业目录仍在制定中，企业可能误判。
- **跨境运维报批流程不透明**：目前缺乏公开的报批指南，不同行业主管部门要求可能不同。
- **执法力度差异**：部分地区执法宽松，但一线城市和重点行业已开始严格检查。
- **与GDPR的冲突**：例如，GDPR要求数据可跨境传输，中国要求本地存储，企业可能陷入两难。
- **技术实现成本**：数据本地化、安全评估、运维架构改造需要大量投入，中小企业压力大。

## 我的判断

2026年是中国关基与数据合规的“执行元年”。此前法规框架已基本完善，现在进入“查漏补缺”阶段。对于CIIO和重要数据处理者，合规不再是可选项，而是生存条件。

**核心建议**：
1. **立即启动重要数据识别**，不要等行业目录出台后再行动。
2. **跨境运维报批是当前最大盲区**，建议主动向行业主管部门咨询流程，不要等到被检查。
3. **将等保2.0与关基保护整合推进**，避免重复建设。
4. **建立合规-安全-工程联动机制**，避免法务团队孤军奋战。

**适合人群**：CIIO安全负责人、数据合规负责人、出海SaaS CTO、云服务商合规团队。

**限制/风险**：本文不构成法律意见。具体操作需咨询专业律师，并关注最新法规更新。部分行业（如金融、能源）可能有更严格的专项要求。

---

**English Brief**

**What happened**: China's CII and data security regulations entered an enforcement phase in 2026. Key changes include: (1) CIIOs must undergo national security review for procurement of network products/services; (2) data must be stored locally, and cross-border O&M requires prior approval from both industry regulator and Ministry of Public Security; (3) MLPS 2.0 five-stage process is now fully enforced.

**Who is affected**: CIIOs, AI/SaaS companies handling important data, outbound businesses with cross-border O&M, security/data teams, legal/compliance teams, product teams using outsourced development.

**Engineering/security actions**: 
- Identify important data and classify it.
- Ensure local storage; apply for data export security assessment if needed.
- Apply for cross-border O&M approval before any remote maintenance.
- Implement procurement security review and vendor security agreements.
- Complete MLPS grading, filing, remediation, and assessment.
- Establish risk monitoring and incident response.

**China data compliance angle**: Priority on important data protection, local storage, cross-border data transfer security assessment, and the unique requirement of cross-border O&M approval (Article 34 of CII Protection Regulation). MLPS 2.0 is mandatory baseline.

**Take**: 2026 is the enforcement year. CIIOs and important data processors must act now. The biggest blind spot is cross-border O&M approval—start consulting regulators proactively. Integrate MLPS and CII compliance to avoid duplication.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## China CIIO & MLPS Compliance: New Enforcement Signals for Important Data and Cross-Border Ops

# China CIIO & MLPS Compliance: New Enforcement Signals for Important Data and Cross-Border Ops

**What it is.** China is tightening the operational compliance burden on operators of critical information infrastructure (CIIO) and on any organization handling important data. Three interlocking regimes are now the baseline: the Cybersecurity Law (CSL), the Data Security Law (DSL), and MLPS 2.0 (网络安全等级保护 / Multi-Level Protection Scheme). The CIIO-specific rules were firmly established by the *Key Information Infrastructure Security Protection Regulations* (《关键信息基础设施安全保护条例》), which detail obligations in procurement, data location, and system operation.

**Why it matters now.** The legal framework has moved from draft guidance to enforced rules. CII identification is being defined sector-by-sector by industry regulators, so many organizations will only learn they are CIIO after designation. For everyone else, MLPS 2.0 filing and assessment is now a de facto prerequisite for operating regulated systems in China, and data cross-border rules are being enforced through the CAC security assessment process — not merely recommended.

**Key obligations to operationalize.**

- **Procurement and supply chain.** CIIOs purchasing network products or services that may affect national security must pass a national security review. Security and confidentiality agreements with suppliers are required. Outsourced or donated systems must undergo security testing before going live.
- **Data localization and cross-border transfer.** Personal information and important data collected in China by CIIOs must be stored domestically. If transfer abroad is necessary, a security assessment under CAC measures is required. For important data, the DSL adds classification-and-grading obligations and a national important data catalog.
- **Domestic operation and maintenance.** CII operation and maintenance must be performed inside China. Remote maintenance from overseas requires prior reporting to the industry regulator and the Ministry of Public Security — a clause often overlooked.
- **MLPS 2.0 process.** The five-stage lifecycle is: classification (定级), filing (备案), remediation (建设整改), assessment by a qualified Chinese third-party institution (等级测评), and supervision/inspection (监督检查). The assessment report must be submitted to local public security authorities.

**Practical next steps.** Determine whether you may fall under CII criteria by sector, and confirm your MLPS level (typically Level 2 or 3 for most commercial systems). Inventory your data assets and classify them against the important data catalog. If you transfer data overseas, audit whether you need a CAC security assessment or China SCC filings. Review procurement contracts for security review triggers and confidentiality clauses. Pre-test all outsourced code before production. Document any remote O&M involving overseas access and file the required notifications.

**Risks.** Enforcement exposure spans fines, suspension of operations, and criminal liability for responsible personnel. The main pitfalls: treating MLPS as a one-time paperwork exercise rather than continuous monitoring, failing to keep an up-to-date important data inventory, and unapproved cross-border data flows — including remote troubleshooting access from abroad.

**Take.** Compliance is now an engineering and operations program. Engineering teams should map MLPS controls to their infrastructure, data teams should operationalize classification and export assessments, and security teams should add CII inspection points to procurement, release, and remote-access workflows. Treat the legal texts as technical requirements, not legal formalities.

*This brief is informational, not legal advice.*

</div>

---

### 参考来源 / Sources

- [观韬视点 | 国家网络安全领域核心命脉：关键信息基础设施的合规要点解析-北京观韬律师事务所](https://www.guantao.com/page2082)
- [等保2.0安全合规解决方案- 阿里云](https://www.alibabacloud.com/zh/china-gateway/mlps2?_p_lc=1)
- [《关键信息基础设施安全保护条例》正式出台](https://www.junhe.com/legal-updates/1534?locale=zh)
- [[PDF] 网络安全与数据合规法律法规汇编 - 宁波市律师协会](http://www.nblawyer.com/FileUpload/ueditor/file/20240730/6385795123086712509588223.pdf)
- [深度解读｜数据安全法](https://www.dbappsecurity.com.cn/content/details284_6069.html)
