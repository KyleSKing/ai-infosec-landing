---
layout: post
title_en: "Hardening Service Accounts and Secrets: A Defensive Playbook for Engineering Teams"
title_cn: "服务账户与密钥防御实操指南"
date: 2026-09-28 03:42:00 +0800
category: infosec
content_type: defensive_playbook
content_type_cn: "防御实操"
content_type_en: "Defensive Playbook"
tags:
  - "least privilege"
  - "service accounts"
  - "secret scanning"
  - "IAM"
  - "DevSecOps"
summary_en: "Service accounts and secrets are prime attack targets due to excessive permissions and poor rotation. This playbook covers least-privilege enforcement, automated secret scanning, and rotation workflows to reduce blast radius."
summary_cn: "服务账户和密钥因权限过大、轮换不足成为主要攻击目标。本文提供最小权限强制、自动密钥扫描和轮换流程的防御实操方案，缩小爆炸半径。"
view_count_seed: 0
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## 服务账户与密钥防御实操指南

# 服务账户与密钥防御实操指南

## 风险是什么

服务账户（Service Account）和密钥（API Key、Token、证书）是云原生和CI/CD流水线中最容易被忽视的“隐形身份”。它们没有密码过期提醒，没有MFA，通常被硬编码在代码仓库、环境变量或配置文件中。一旦泄露，攻击者可以：

- 利用过大的权限横向移动（例如一个只读的CI服务账户被赋予`*:*`权限）
- 持续访问资源（密钥不轮换，泄露后长期有效）
- 绕过人工审计（服务账户通常不在常规访问审查范围内）

最小权限原则（PoLP）是限制爆炸半径的核心手段。但现实是：超过60%的服务账户拥有比实际需要更多的权限，且超过40%的密钥从未被轮换。

## 谁会受影响

- **开发团队**：在本地开发、测试中硬编码密钥，或在Docker镜像中嵌入凭据。
- **DevOps/SRE**：在CI/CD流水线（GitHub Actions、Jenkins、GitLab CI）中直接使用长期密钥，而非临时令牌。
- **安全团队**：缺乏对服务账户权限的自动审查和密钥泄露的实时检测。
- **云平台管理员**：跨AWS、Azure、GCP管理多个服务账户，权限分散，难以统一治理。
- **合规团队**：需要满足SOC 2、ISO 27001、PIPL等对访问控制和密钥管理的审计要求。

## 怎么检查

以下检查清单可直接用于日常巡检或自动化扫描：

### 1. 服务账户权限审计

- [ ] 列出所有服务账户（IAM角色/用户），标记其关联的资源（云服务、API、数据库）。
- [ ] 检查每个服务账户是否遵循“一个应用一个账户”原则，避免共享。
- [ ] 使用云厂商的IAM Access Analyzer（AWS）、IAM Recommender（GCP）、Entra ID Access Reviews（Azure）生成权限使用报告。
- [ ] 识别“未使用权限”：例如某服务账户被授予`ec2:*`但从未调用过`RunInstances`。
- [ ] 检查信任策略：是否允许跨账户AssumeRole？是否允许匿名主体访问？

### 2. 密钥泄露检测

- [ ] 扫描所有代码仓库（包括私有仓库、历史提交）中的硬编码密钥。工具：GitHub Secret Scanning、GitLeaks、TruffleHog、Cycode。
- [ ] 检查环境变量、Dockerfile、Kubernetes ConfigMap/Secret中是否明文存储密钥。
- [ ] 检查CI/CD日志输出是否意外打印了密钥（例如`echo $API_KEY`）。
- [ ] 检查云平台密钥轮换策略：AWS IAM Access Key、GCP Service Account Key、Azure AD Client Secret的创建时间和上次使用时间。

### 3. 密钥轮换与生命周期

- [ ] 确认所有长期密钥设置了自动轮换（例如AWS IAM密钥每90天轮换）。
- [ ] 检查是否有密钥超过180天未轮换。
- [ ] 确认轮换流程是否自动化（而非手动修改）。
- [ ] 检查密钥删除后是否仍有依赖该密钥的服务在运行（导致中断）。

## 怎么修 / 怎么接入流程

### 1. 最小权限落地

- **按应用拆分服务账户**：每个微服务/工作负载使用独立服务账户，不要复用。
- **使用预定义角色**：优先使用云厂商预定义的最小权限角色（如`roles/storage.objectViewer`），而非自定义角色（容易过度授权）。
- **定期权限回收**：每季度运行一次权限使用报告，撤销90天内未使用的权限。
- **实施Just-In-Time（JIT）访问**：对敏感操作（如删除资源、修改IAM策略）使用临时提升权限，而非长期持有。
- **使用条件键**：在IAM策略中限制来源IP、VPC端点、MFA要求等。

**示例（GCP）：**  
```bash
# 为审计员创建只读角色
gcloud projects add-iam-policy-binding my-project \
  --member="group:[email protected]" \
  --role="roles/iam.securityReviewer"
gcloud projects add-iam-policy-binding my-project \
  --member="group:[email protected]" \
  --role="roles/logging.viewer"
```

### 2. 密钥管理自动化

- **使用密钥管理服务**：AWS Secrets Manager、GCP Secret Manager、Azure Key Vault。应用运行时从KMS读取，不硬编码。
- **CI/CD中使用临时凭据**：GitHub Actions使用OIDC获取云平台临时令牌，避免存储长期密钥。AWS、GCP、Azure均支持。
- **自动轮换**：设置Lambda/Cloud Function定期轮换密钥，并更新依赖该密钥的服务（如数据库密码）。
- **预提交钩子**：在`pre-commit`阶段运行密钥扫描，阻止包含密钥的提交。工具：`pre-commit` + `detect-secrets`。

**示例（GitHub Actions + OIDC）：**  
```yaml
jobs:
  deploy:
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
```

### 3. 泄露响应流程

- **自动撤销**：一旦检测到密钥泄露，立即在云平台撤销该密钥（通过API或预置的自动化工作流）。
- **通知开发者**：在开发者IDE或工单系统中提供修复指引（例如“请删除该密钥，并使用Secret Manager重新生成”）。
- **验证修复**：自动扫描确认密钥已从仓库移除，且云平台中已轮换。
- **记录事件**：将泄露事件纳入安全事件管理，分析根因（是开发者误操作还是CI日志泄露？）。

## 注意事项

### 工具限制

- **密钥扫描的误报**：Base64编码的随机字符串可能被误判为密钥。需要配置白名单（如测试密钥、示例代码）。
- **漏报**：扫描工具无法检测到通过加密、分段存储或动态生成的密钥。需要结合运行时监控（如异常API调用）。
- **权限审计的假阴性**：云厂商的“未使用权限”报告基于最近访问记录，如果服务账户仅在特定条件下使用（如每月一次），可能被误判为未使用。建议设置合理的时间窗口（90天以上）。

### 操作风险

- **过度收紧权限导致服务中断**：在回收权限前，务必确认该权限确实未被使用。建议先在测试环境验证。
- **自动轮换导致依赖失效**：如果密钥被多个服务共享，轮换后所有依赖方必须同步更新。建议使用密钥管理服务的自动更新回调，或采用临时凭据避免依赖。
- **OIDC配置错误**：GitHub Actions的OIDC信任策略如果过于宽松（允许任何仓库AssumeRole），反而引入风险。必须限制`sub`和`aud`声明。

### 团队流程

- **开发者抵触**：强制密钥扫描和权限审查可能降低开发效率。建议在CI中设置“警告”而非“阻断”，逐步过渡到“阻断”。
- **审计疲劳**：权限审查报告如果太长，团队会忽略。建议只关注高风险项（如管理员权限、跨账户信任）。

## 我的判断

服务账户和密钥管理是云安全中最容易被低估但回报最高的投入。**最小权限 + 自动轮换 + 泄露检测**三者缺一不可。当前云厂商和开源工具已经提供了足够成熟的方案（OIDC、Secret Manager、IAM Access Analyzer），但落地难点在于团队习惯和流程设计。

- **优先做**：立即启用GitHub Secret Scanning（免费），并为所有CI/CD流水线切换到OIDC临时凭据。
- **中期做**：每季度执行一次服务账户权限审计，撤销未使用权限。
- **长期做**：建立密钥泄露自动化响应流程，并与事件管理平台集成。

不要试图一次性“完美”治理，先解决最痛的泄露问题，再逐步收紧权限。对于合规要求高的团队（如金融、医疗），建议将服务账户纳入季度访问审查范围，并保留密钥轮换日志以应对审计。

**适合人群**：开发团队、DevOps/SRE、安全工程师、云平台管理员、合规负责人。

**不适合人群**：完全使用本地部署且无API密钥的小团队（但仍有数据库密码等凭据需要管理）。

---

## English Brief

**Risk**: Service accounts and API keys are often over-privileged, never rotated, and hardcoded in code or CI/CD pipelines. A leaked key can lead to lateral movement, data exfiltration, or resource hijacking.

**Affected Teams**: Developers, DevOps, SRE, security, cloud admins, compliance.

**Checks**:
- Audit service account permissions (use IAM Access Analyzer, Recommender).
- Scan all repos and CI logs for hardcoded secrets (GitHub Secret Scanning, GitLeaks, TruffleHog).
- Verify key rotation policies (every 90 days recommended).
- Check for shared service accounts across applications.

**Remediation Workflow**:
1. Apply least privilege: one service account per app, use predefined roles, revoke unused permissions quarterly.
2. Use temporary credentials in CI/CD (OIDC with GitHub Actions, AWS/GCP/Azure).
3. Store secrets in Secret Manager (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault).
4. Automate rotation and revocation on leak detection.
5. Add pre-commit hooks to prevent secret commits.

**Caveats**:
- Secret scanners have false positives (test keys) and false negatives (encrypted secrets).
- Over-restricting permissions can break services; test in staging first.
- OIDC trust policies must be scoped to specific repos/roles.
- Team adoption requires gradual enforcement (warn first, then block).

**Take**: Start with secret scanning and OIDC for CI/CD. Then audit service account permissions quarterly. Automate rotation and incident response. This is the highest-ROI security investment for cloud-native teams.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## Hardening Service Accounts and Secrets: A Defensive Playbook for Engineering Teams

# Hardening Service Accounts and Secrets: A Defensive Playbook for Engineering Teams

## What It Is

This playbook focuses on two interconnected attack surfaces: over‑permissioned service accounts and leaked secrets. Service accounts (used by workloads, CI/CD pipelines, VMs, functions) often carry excessive permissions, run continuously, and are regularly omitted from access reviews – making them prime targets. Secrets (API keys, database passwords, tokens) stored in code, configs, or logs create instant compromise paths when exposed.

## Why It Matters Now

Credential theft is the fastest path to a cloud breach. A single leaked secret with broad IAM permissions can give an attacker full control over an environment. Traditional human‑centric access reviews miss service accounts, and secret scanning is still reactive in many orgs. With cloud‑native architectures multiplying identities, the blast radius of a compromised non‑human identity grows unless explicitly contained.

## Practical Next Steps

1. **Enforce least privilege for every identity** – Not just users. IAM roles, service accounts, access keys, and function execution roles should each get the minimum permissions required. Don’t share service accounts across applications; create one per workload (source [3]). Use predefined roles (like `roles/iam.securityReviewer`) instead of custom admin roles where possible.

2. **Treat service accounts as full‑scope identities** – Include them in quarterly access reviews, monitor their permissions drift, and apply the same zero‑trust assumptions as human identities. In multi‑cloud environments, centralise governance to maintain consistent visibility across AWS, Azure, and GCP (source [2]).

3. **Automate secret scanning end‑to‑end** – Scan code repositories, logs, CI/CD artifacts, and cloud storage for committed secrets. When a leak is detected:
   - Automatically revoke or rotate the secret in the target service (AWS, Azure, DB).
   - Provide developers with actionable remediation steps inside their IDE or ticketing system.
   - Verify removal from the repo **and** rotation in the target system – only then close the ticket (source [4]).

4. **Embed rotation into the workflow** – Don’t rely on manual rotation. Establish automated workflows that rotate secrets on a schedule **and** immediately after a detection. Monitor usage patterns to detect compromise early (source [5]).

## Risks to Watch

- Over‑permissioned service accounts that are never reviewed – they drift over time.
- Shared service accounts between applications – increases blast radius and audit complexity.
- Secret rotation without verification – a secret may be rotated but still present in old code or backups.
- Developers bypassing prevention due to friction – make security guidance part of their normal workflow, not a separate ceremony.

## The Take

The principle of least privilege is decades old, but its practical application to non‑human identities is still immature in many engineering orgs. The goal is to contain potential damage by design: every service account should be scoped to exactly what it needs, every secret should be short‑lived and automatically rotated, and scanning should be continuous, not periodic. Integrate these steps into your existing CI/CD and cloud governance – security that blocks delivery will be ignored; security that guides delivery gets adopted.

</div>

---

### 参考来源 / Sources

- [Cloud Least Privilege: Best Practices Guide](https://orca.security/resources/blog/cloud-least-privilege-principles-best-practices)
- [Least Privilege in AWS, Azure & GCP Environments](https://www.securends.com/blog/least-privilege-cloud-environments)
- [How to Use the Principle of Least Privilege with Predefined IAM Roles in GCP](https://oneuptime.com/blog/post/2026-02-17-how-to-implement-the-principle-of-least-privilege-with-predefined-iam-roles-in-gcp/view)
- [Secret Scanning: The definitive guide | Cycode](https://cycode.com/blog/secret-scanning-guide)
- [Configure secret scanning](https://docs.cloudbees.com/docs/cloudbees-unify/latest/application-security/how-to-guides/configure-secret-scanning)
