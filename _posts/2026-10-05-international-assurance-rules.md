---
layout: post
title_en: "EU AI Act, DORA, NIS2: Engineering Compliance for AI & Cyber-Resilience"
title_cn: "国际AI与网络韧性法规：工程合规行动指南"
date: 2026-10-05 03:22:53 +0800
category: infosec
content_type: regulation_watch
content_type_cn: "法规追踪"
content_type_en: "Regulation Watch"
tags:
  - "EU AI Act"
  - "DORA"
  - "NIS2"
  - "China data regulation"
  - "engineering compliance"
summary_en: "The EU AI Act, DORA, and NIS2 impose binding compliance deadlines from 2025 to 2028, requiring engineering teams to build AI inventories, risk management, and incident reporting into product delivery. For outbound SaaS and AI products, these rules intersect with China's PIPL and generative AI regulations, creating a dual-compliance landscape for cross-border data and algorithm governance."
summary_cn: "欧盟AI法案、DORA和NIS2设定了2025至2028年的强制合规时间表，工程团队需将AI清单、风险管理和事件报告嵌入产品交付流程。对于出海SaaS和AI产品，这些规则与中国PIPL和生成式AI法规交叉，形成跨境数据与算法治理的双重合规格局。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 国际AI与网络韧性法规：工程合规行动指南

# 国际AI与网络韧性法规：工程合规行动指南

## 发生了什么

2026年8月2日，欧盟《人工智能法案》（EU AI Act）的核心条款正式生效：透明度规则（第50条）开始执行，通用人工智能模型（GPAI）义务已自2025年8月2日起适用，而高风险AI系统的大部分要求则被推迟至2027年12月2日（独立系统）和2028年8月2日（嵌入式系统）。与此同时，欧盟《数字运营韧性法案》（DORA）自2025年1月全面实施，NIS2指令的成员国转化期限已于2024年10月截止，目前各成员国正在密集执法。这些法规共同构成了欧洲数字韧性（cyber resilience）与AI治理的“三驾马车”，直接影响所有面向欧盟市场的技术产品。

在中国，2026年也是监管深化之年：《个人信息保护法》（PIPL）执法力度持续加强，《数据出境安全评估办法》修订版于2025年底发布，生成式人工智能服务备案要求进一步细化，算法推荐与深度合成管理规定进入常态化检查。跨境数据流动方面，中国与欧盟、东盟等地区的“数据安全出境”互认机制仍在谈判中，但企业自评估义务已不可回避。

## 为什么现在重要

对于技术团队而言，合规不再是法务部门的“纸面作业”，而是必须嵌入CI/CD流水线、模型训练流程、数据治理框架和第三方供应商管理的工程实践。EU AI Act的“AI素养”义务（第4条）自2025年2月已生效，要求所有使用AI系统的员工具备基本理解能力；而2026年8月生效的透明度规则要求生成式AI系统必须提供机器可读的标记（如水印），且已上市系统有至2026年12月2日的宽限期。这意味着工程团队现在就必须修改模型输出接口、添加元数据字段，并建立可审计的日志。

DORA要求金融机构在2025年1月前完成ICT风险管理框架、测试和报告能力建设，但2026年进入常态化监管——监管机构开始检查第三方ICT供应商的韧性。NIS2则要求“重要实体”和“基本实体”实施事件响应、供应链安全、加密和访问控制等具体措施，且管理层可被追究个人责任。

中国方面，2026年《数据出境安全评估办法》修订版明确将“重要数据”目录扩展至汽车、医疗、金融、AI训练数据等领域，且要求企业每年进行自评估。生成式AI服务的“双备案”（算法备案+服务备案）已覆盖文本、图像、音视频生成，未备案产品面临下架风险。

## 影响谁

- **AI产品团队**：直接受EU AI Act风险分类影响——高风险系统（如招聘、信贷、生物识别）需做符合性评估；GPAI模型需提供训练数据摘要、能源消耗报告；生成式AI需标记。
- **SaaS/云服务团队**：若服务欧洲金融机构，需满足DORA的ICT韧性测试和第三方风险管理；若服务欧盟公共部门或关键基础设施，需符合NIS2。
- **出海企业（尤其是中国公司）**：面临EU AI Act + 中国数据出境法规的双重约束。模型训练数据若包含中国个人信息，出境需通过安全评估或标准合同；模型部署在欧盟需满足EU AI Act透明度与文档要求。
- **安全/数据团队**：需建立AI系统清单、风险分类、数据治理日志、事件响应流程，并确保供应链合规。
- **合规/法务团队**：需将法规要求转化为工程需求，并参与设计评审。

## 工程/安全/数据团队要做什么

### 1. 建立AI系统清单与风险分类
- 扫描所有生产环境中的AI/ML模型，记录用途、训练数据来源、部署地区、输出类型。
- 对照EU AI Act附件III判断是否属于高风险（如用于就业、教育、执法、移民等）。若不确定，按高风险处理。
- 对于GPAI模型（如基础模型），记录训练算力（FLOPs）、数据来源、是否开源，并准备技术文档。

### 2. 实现透明度与可解释性
- 生成式AI输出必须包含机器可读标记：在API响应中添加`model_id`、`generation_timestamp`、`watermark`字段。对于图像/视频，使用不可见水印或元数据。
- 高风险系统需提供“解释性说明”：输出结果的关键因素、模型置信度、训练数据分布摘要。
- 建立用户投诉与人工审核接口。

### 3. 数据治理与隐私
- 训练数据中若包含中国个人信息，需确认出境合规路径（安全评估、标准合同、认证）。2026年建议使用“数据本地化+匿名化”方案，避免直接出境。
- 实施数据最小化：只收集模型训练和推理必需的数据，并设置自动删除策略。
- 记录数据来源、清洗过程、偏差评估报告（EU AI Act要求）。

### 4. 韧性测试与事件响应（DORA/NIS2）
- 金融机构需每两年进行一次ICT韧性测试（包括渗透测试、压力测试）。
- 所有受NIS2覆盖的实体需在24小时内报告重大安全事件，并保留事件日志至少2年。
- 建立第三方供应商评估机制：要求供应商提供SOC 2、ISO 27001或同等认证，并定期审查其韧性能力。

### 5. 自动化合规检查
- 在CI/CD流水线中加入合规检查步骤：例如，模型发布前自动检查是否包含水印、是否记录训练数据来源、是否触发高风险分类。
- 使用工具（如OpenSCA、SBOM生成器）管理AI组件依赖，生成AI系统物料清单（AI-BOM）。

## 中国数据监管重点

在中国，2026年以下法规直接关联AI产品与数据出境：

- **《个人信息保护法》（PIPL）**：处理个人信息需告知同意，敏感个人信息需单独同意。AI训练数据若包含生物识别、医疗健康、行踪轨迹等，属于敏感信息，出境需通过安全评估。
- **《数据安全法》（DSL）**：重要数据目录持续更新。AI训练语料若涉及“重要数据”（如大规模地理信息、经济统计、行业核心数据），出境前需进行数据出境安全评估。
- **《数据出境安全评估办法》（2025修订版）**：明确了“重要数据”的定义范围，并引入“标准合同”与“认证”两种补充路径。但实际执行中，监管机构倾向于要求安全评估，尤其是涉及CIIO（关键信息基础设施运营者）或100万人以上个人信息时。
- **生成式AI监管**：算法备案（《互联网信息服务算法推荐管理规定》）与深度合成备案（《深度合成管理规定》）已合并为“生成式AI服务备案”。2026年要求所有面向公众的生成式AI服务（包括API）在提供服务前完成备案，否则不得上线。备案材料需包括训练数据来源、模型安全评估报告、内容过滤机制说明。
- **跨境数据流动新规**：中国与欧盟正在推进“数据安全出境互认”框架，但尚未落地。目前企业仍需按现行法规操作。建议：将中国用户数据存储在中国境内，仅将匿名化后的模型参数或聚合统计信息出境。

## 国际规则对照

| 法规 | 核心要求 | 适用对象 | 与中国法规的交叉点 |
|------|---------|---------|------------------|
| EU AI Act | 风险分类、透明度、文档、人类监督 | AI系统提供者/部署者 | 中国出海企业需同时满足；训练数据出境需符合PIPL |
| DORA | ICT韧性测试、第三方风险管理、事件报告 | 欧盟金融机构 | 中国金融科技公司若服务欧盟客户，需遵守；数据本地化要求可能与PIPL冲突 |
| NIS2 | 安全措施、事件报告、供应链安全 | 关键/重要实体（能源、交通、医疗等） | 中国云服务商若为欧盟关键基础设施提供ICT服务，需满足；供应链审计需覆盖中国供应商 |
| GDPR | 数据保护、跨境传输、DPIA | 所有处理欧盟个人数据的企业 | 与PIPL并行，需同时满足；数据出境需通过“充分性认定”或SCC |
| 中国PIPL/DSL | 个人信息保护、重要数据出境评估 | 中国境内数据处理者 | 出海企业需在境内完成合规后再出境 |

## 可以提前准备的检查清单

1. **AI系统清单**：列出所有模型，标注风险等级、部署地区、训练数据来源、是否涉及个人信息/重要数据。
2. **透明度标记**：生成式AI输出添加`model_id`、`watermark`、`timestamp`，并确保机器可读（如JSON-LD）。
3. **数据治理文档**：训练数据来源、清洗日志、偏差分析、数据保留策略。
4. **合规自动化**：在CI/CD中加入模型发布合规检查（风险分类、标记、文档完整性）。
5. **事件响应计划**：建立AI安全事件（如模型投毒、数据泄露）的响应流程，包括24小时报告机制（NIS2/DORA）。
6. **第三方供应商评估**：要求AI组件供应商提供合规声明（EU AI Act符合性、SOC 2、ISO 27001）。
7. **中国数据出境评估**：若涉及中国个人数据或重要数据出境，完成安全评估或签订标准合同。
8. **生成式AI备案**：检查是否完成算法备案与服务备案，确保内容过滤机制符合要求。

## 风险和不确定性

- **EU AI Act高风险分类的模糊性**：附件III中的“高风险”定义存在解释空间，监管机构可能通过后续指南扩大范围。建议对边缘案例按高风险处理。
- **DORA与NIS2的执法力度**：不同成员国转化速度不一，2026年可能出现执法差异。企业应以最严格标准准备。
- **中国数据出境互认进展缓慢**：与欧盟的互认框架尚未落地，企业需同时满足两套要求，增加合规成本。
- **生成式AI备案的审核周期**：备案材料可能被要求补充，导致产品上线延迟。建议提前3个月提交。
- **AI素养义务的落地**：EU AI Act要求员工培训，但具体内容无明确标准。建议参考ISO/IEC 42001（AI管理体系）设计培训方案。

## 我的判断

2026年是全球AI与网络韧性法规从“制定”转向“执行”的关键年份。EU AI Act、DORA、NIS2与中国数据出境、生成式AI监管形成了事实上的“双轨制”——任何面向欧盟或中国市场的技术产品都必须同时满足两套标准。对于工程团队而言，合规不再是法务的“翻译工作”，而是必须内化为代码逻辑、流水线检查和运维流程。建议企业立即启动以下三项行动：

1. **建立跨职能合规小组**：工程、安全、数据、法务每周同步，将法规要求拆解为具体的技术任务。
2. **投资合规自动化工具**：手动合规不可持续，应引入AI系统清单管理、水印生成、数据溯源等工具。
3. **优先处理中国数据出境**：由于中国监管执法力度强、周期长，建议先完成国内合规，再适配国际要求。

**适合人群**：AI产品经理、安全工程师、数据工程师、DevOps团队、合规经理、出海企业CTO。

**限制/风险**：本文基于公开法规文本和行业实践，不构成法律意见。各企业应结合自身业务咨询专业律师。法规仍在演进，2027-2028年还有更多条款生效，需持续跟踪。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## EU AI Act, DORA, NIS2: Engineering Compliance for AI & Cyber-Resilience

# EU AI Act, DORA, NIS2: Engineering Compliance for AI & Cyber-Resilience

## What It Is

Three European regulatory frameworks are converging on technical teams: the **EU AI Act** (risk-based AI regulation), **DORA** (Digital Operational Resilience Act for financial sector), and **NIS2** (network and information security directive for essential services). Each mandates specific engineering controls, documentation, and incident reporting—not just legal policies.

## Why It Matters Now

The EU AI Act’s AI literacy duty has been enforceable since **February 2025**, with supervision starting August 2026. The heavy high-risk regime now applies **December 2027** (standalone systems) and **August 2028** (embedded systems). DORA and NIS2 are already in force for many organizations. Regulators will evaluate **technical artifacts and operational controls**, not intent.

## Practical Next Steps for Engineering Teams

1. **Create an AI system inventory** – Catalog every model, training dataset, and deployment. Classify risk per EU AI Act categories (prohibited, high-risk, GPAI, limited/minimal). This is the foundation for all compliance work.

2. **Implement risk management and data governance** – For high-risk systems: maintain technical documentation (model cards, data sheets), ensure human oversight mechanisms, and conduct conformity assessments. For GPAI: document training data sources, compute, and energy consumption.

3. **Map existing security controls to NIS2/DORA** – NIST and ISO 27001 controls can be mapped to NIS2 requirements. For DORA: focus on third-party ICT risk management, incident reporting (within defined timelines), and digital operational resilience testing.

4. **Embed compliance into CI/CD** – Add automated checks for AI system documentation, model versioning, and transparency markings. The machine-readable marking requirement for generative systems already on the market before August 2026 has a grace window until **2 December 2026**.

5. **Establish incident response and reporting** – Both DORA and NIS2 require formalized incident reporting to authorities. Define technical triggers, escalation paths, and documentation templates.

## Risks and Operational Notes

- **Phased deadlines are confusing** – Many teams assume the 2026/2027 dates are far off, but AI literacy and transparency rules are already active. Start with inventory and risk classification now.
- **Third-party risk is under-scoped** – DORA explicitly covers ICT providers; NIS2 extends to supply chains. Audit your AI vendors and cloud providers.
- **Documentation is not optional** – Regulators will ask for technical documentation, not policy PDFs. Use structured formats (e.g., model cards, system cards) that can be versioned and audited.
- **Cross-sector overlap** – If your organization is both a financial institution and an AI provider, you must comply with DORA *and* the EU AI Act. Map overlaps to avoid duplication.

## Take

These regulations are engineering problems, not legal abstractions. The teams that treat compliance as a product requirement—building AI inventories, automated documentation, and incident response playbooks into their workflows—will have a clear advantage. Start with the inventory and risk classification; everything else follows.

</div>

---

### 参考来源 / Sources

- [EU AI Act Compliance Checklist: 11 Steps for Teams](https://aioutlooks.com/eu-ai-act-compliance-checklist)
- [The Engineering Manager's EU AI Act Compliance Checklist (2026)](https://blog.codacy.com/the-engineering-managers-eu-ai-act-compliance-checklist-2026)
- [EU AI Act Compliance Checklist for Businesses in 2026](https://www.codebridge.tech/articles/the-eu-ai-act-compliance-checklist-ownership-evidence-and-release-control-for-businesses)
- [What is DORA? Purpose, Benefits & Compliance](https://www.kiteworks.com/risk-compliance-glossary/dora)
- [NIS2 Directive & DORA Cyber Resilience Framework](https://www.kelacyber.com/academy/cti/nis2-directive-and-dora-cyber-resilience-framework-benefits-and-alignment-explained)
