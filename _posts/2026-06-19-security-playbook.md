---
layout: post
title_en: "DevSecOps Playbook: Detect and Fix SBOM & CI/CD Security Gaps"
title_cn: "DevSecOps防御实操：SBOM与CI/CD安全缺口排查"
date: 2026-06-19 11:29:32 +0800
category: infosec
content_type: defensive_playbook
content_type_cn: "防御实操"
content_type_en: "Defensive Playbook"
tags:
  - "DevSecOps"
  - "SBOM"
  - "CI/CD"
  - "GitHub Actions"
  - "supply chain security"
  - "vulnerability scanning"
  - "defensive playbook"
summary_en: "A practical guide for teams to detect and fix common security gaps in CI/CD pipelines, focusing on SBOM generation, vulnerability scanning, and supply chain risks using GitHub Actions and open-source tools."
summary_cn: "面向团队的CI/CD安全防御实操指南，聚焦SBOM生成、漏洞扫描与供应链风险，结合GitHub Actions与开源工具给出可落地的检测与修复步骤。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## DevSecOps防御实操：SBOM与CI/CD安全缺口排查

# DevSecOps防御实操：SBOM与CI/CD安全缺口排查

## 风险是什么

2026年6月的今天，软件供应链攻击已经不是“会不会发生”的问题，而是“什么时候轮到你的CI/CD管道被投毒”。SBOM（软件物料清单）和CI/CD安全扫描是当前最被低估的两个防御环节。

**核心风险**：
- 你的CI/CD管道里跑着大量第三方依赖，但没人知道这些依赖里藏着什么。
- 依赖的版本锁定、签名验证、来源追溯几乎为零。
- 攻击者通过投毒上游包（如PyPI、npm、GitHub Actions的第三方action）就能直接进入你的生产环境。

**真实案例**：2024-2026年间，多个开源项目被通过依赖混淆和恶意commit投毒，受害者包括金融科技公司和SaaS平台。这些攻击的共性：CI/CD管道没有SBOM，没有依赖签名验证。

## 谁会受影响

- **任何使用第三方依赖的团队**：Python、JavaScript、Go、Java、Rust项目都中招。
- **CI/CD管道中有GitHub Actions、自建Jenkins、GitLab CI的团队**：尤其是那些直接拉取第三方action或镜像的。
- **SaaS和B2B团队**：客户要求你提供SBOM和供应链安全报告，你拿不出来。
- **合规团队**：PIPL、EU AI Act、SOC 2、ISO 27001都开始要求软件供应链透明度。

## 怎么检查

### 检查清单（可立即执行）

**1. 你的CI/CD管道有SBOM吗？**

- 检查方式：在CI/CD中加入SBOM生成步骤。
- 工具：CycloneDX插件、SPDX工具、Trivy、Syft。
- 命令示例（GitHub Actions）：

```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    path: ./
    format: cyclonedx-json
```

**2. 你的依赖有签名验证吗？**

- 检查方式：看你的`npm install`或`pip install`是否用了`--verify`或`--require-hashes`。
- 大多数团队没有。这是缺口。
- 修复：在CI中加入`pip install --require-hashes`或`npm audit`。

**3. 你的CI/CD安全扫描覆盖了哪些层？**

- SAST（静态分析）：CodeQL、Semgrep、SonarQube。
- SCA（软件组成分析）：Dependabot、Trivy、Snyk。
- DAST（动态分析）：OWASP ZAP。
- 容器扫描：Docker Scout、Trivy镜像扫描。
- 基础设施即代码扫描：Checkov、tfsec。

**4. 你的第三方Actions有审计吗？**

- 检查：`actions/checkout`、`actions/setup-python`这些官方action没问题。
- 风险：第三方action如`docker/login-action`、`aws-actions/configure-aws-credentials`。
- 修复：只使用经过GitHub验证的action，或自建镜像。

## 怎么修 / 怎么接入流程

### 立即行动：三步修复

**第一步：在CI/CD中嵌入SBOM生成**

- 每个构建都生成SBOM。
- 存储SBOM到制品库（如GitHub Releases、Artifactory）。
- 示例工作流：

```yaml
name: CI with SBOM
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          path: ./
          format: cyclonedx-json
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.json
```

**第二步：加入依赖签名验证**

- 使用`pip install --require-hashes`或`npm ci --only=production`。
- 对GitHub Actions的第三方action，使用`actions/checkout`的`ref`参数锁定版本。

**第三步：加入安全扫描**

- 加入CodeQL、Dependabot、Trivy。
- 加入OWASP ZAP做DAST。
- 加入Checkov扫描IaC。

### 适合人群

- **DevOps/DevSecOps工程师**：直接操作CI/CD。
- **安全工程师**：需要审计和报告。
- **SaaS团队**：需要向客户提供SBOM。
- **合规团队**：需要满足PIPL、SOC 2、ISO 27001。

### 不适合人群

- **纯前端团队**：如果项目不涉及后端依赖，SBOM价值有限。
- **没有CI/CD的团队**：先搭CI/CD再谈。

## 注意事项

### 工具限制

- **Trivy**：基础扫描，但缺乏可达性分析（reachability analysis）。无法告诉你“这个漏洞是否真的被代码调用”。
- **Dependabot**：只做版本更新，不做漏洞优先级排序。容易产生大量噪音。
- **CodeQL**：需要配置语言，对Python和JavaScript支持好，但对Rust和Go支持有限。
- **OWASP ZAP**：DAST扫描只对API有效，对前端SPA效果差。

### 误报和漏报

- **误报**：SBOM中的依赖版本和实际运行版本可能不一致。依赖树解析错误会导致SBOM不准确。
- **漏报**：SBOM只覆盖直接依赖，不覆盖间接依赖（transitive dependency）。这是最大的缺口。
- **操作风险**：SBOM生成过程本身可能被篡改。需要签名SBOM。

### 我的判断

**SBOM是2026年最被低估的防御工具**。不是因为SBOM能解决所有问题，而是因为：

1. **合规要求**：PIPL、EU AI Act、SOC 2都开始要求SBOM。没有SBOM，审计过不去。
2. **攻击面**：2024-2026年供应链攻击集中在“依赖投毒”。没有SBOM，你根本不知道你用了什么。
3. **成本**：SBOM生成是免费的（CycloneDX、SPDX）。不做的成本是审计失败和客户流失。

**但SBOM不是银弹**。它需要配合：
- 依赖签名验证（`require-hashes`）
- 可达性分析（Snyk、Endor Labs）
- 运行时监控（Falco、Tetragon）

**建议**：先做SBOM生成和上传，再做依赖签名验证，最后加入安全扫描。顺序不能错。

## English Brief

**Risk**: CI/CD pipelines without SBOM and dependency verification are the primary attack surface for software supply chain attacks in 2026. Most teams have no visibility into their third-party dependencies.

**Affected Teams**: DevOps, security, SaaS, compliance, and B2B teams using GitHub Actions, Jenkins, or GitLab CI.

**Checks**:
1. Does your pipeline generate SBOM (CycloneDX/SPDX)?
2. Are dependencies verified with `--require-hashes` or `--verify`?
3. Are security scans (SAST, SCA, DAST, container) in place?
4. Are third-party GitHub Actions audited?

**Remediation Workflow**:
1. Add SBOM generation to every build.
2. Add dependency signature verification.
3. Add security scans (CodeQL, Trivy, OWASP ZAP).

**Caveats**:
- SBOM only covers direct dependencies, not transitive ones.
- Tools like Trivy lack reachability analysis.
- SBOM generation itself must be signed.

**Take**: SBOM is the most underrated defense in 2026. It's free, required by regulations (PIPL, SOC 2, EU AI Act), and directly addresses the supply chain attack vector. Start with SBOM generation, then add verification and scanning.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## DevSecOps Playbook: Detect and Fix SBOM & CI/CD Security Gaps

# DevSecOps Playbook: Detect and Fix SBOM & CI/CD Security Gaps

## What It Is

This playbook addresses two interconnected security gaps in modern software delivery: **SBOM (Software Bill of Materials) management** and **CI/CD pipeline security**. SBOMs provide a machine-readable inventory of all software components—names, versions, suppliers, licenses, and dependency relationships—typically in SPDX 2.3 or CycloneDX 1.5 formats. CI/CD security gaps arise when pipelines lack automated scanning for vulnerabilities, misconfigurations, or supply chain risks. Tools like GitHub Actions, CodeQL, Dependabot, OWASP ZAP, and Docker Scout can be integrated to detect these issues early.

## Why It Matters Now

Software supply chain attacks are escalating. A single vulnerable dependency can compromise an entire organization. Regulatory pressure is mounting: U.S. Executive Order 14028 mandates SBOMs for federal software, and frameworks like SOC 2 and ISO 27001 increasingly expect supply chain visibility. Without automated detection in CI/CD, teams ship vulnerabilities unknowingly. The shift-left approach—catching issues during development rather than post-deployment—reduces remediation costs and breach risk.

## Practical Next Steps

1. **Generate SBOMs automatically** in your CI pipeline. Use tools like `syft` or `trivy` to produce CycloneDX or SPDX files on every build. Store them alongside artifacts.

2. **Integrate static analysis (SAST)** with GitHub CodeQL or ESLint security plugins. Add a workflow step that runs on every push and pull request.

3. **Add dependency scanning** via Dependabot or Trivy. Configure alerts for critical vulnerabilities and auto-create pull requests for fixes.

4. **Run dynamic analysis (DAST)** on staging environments using OWASP ZAP. Focus on API endpoints—use the `zaproxy/action-api-scan` GitHub Action for REST APIs.

5. **Enforce policy gates**: Fail builds if SBOM reveals components with known critical CVEs or license violations. Use tools like Docker Scout for containerized apps.

6. **Audit pipeline secrets**: Scan for hardcoded credentials using `truffleHog` or `git-secrets` in a pre-commit hook or CI step.

## Risks & Limitations

- **False positives** from SAST/DAST tools can desensitize teams—tune rulesets and prioritize reachable vulnerabilities.
- **SBOM completeness** depends on accurate dependency resolution; transitive dependencies may be missed.
- **Open-source scanners** (Trivy, Grype) lack reachability analysis and automated remediation guidance found in commercial platforms (Snyk, Checkmarx).
- **Pipeline complexity** increases maintenance burden; start with critical paths (e.g., production builds) before expanding.
- **No tool catches everything**—combine SAST, DAST, SCA, and manual review for defense in depth.

## Take

Start with SBOM generation and dependency scanning—they provide the highest visibility-to-effort ratio. Add SAST and DAST incrementally. For most teams, open-source tools cover 80% of needs; invest in commercial platforms only when policy management, SSO, or advanced remediation become bottlenecks. The goal is not zero vulnerabilities but a repeatable process that catches critical issues before production.

</div>

---

### 参考来源 / Sources

- [DevSecOps Tutorial for Beginners | CI Pipeline with GitHub Actions and Docker Scout](https://www.youtube.com/watch?v=gLJdrXPn0ns)
- [DevSecOps with GitHub Action and SaaS Tools | cicd-github-action-example](https://judebantony.github.io/cicd-github-action-example)
- [GitHub Actions in DevSecOps: A Comprehensive Tutorial - DevSecOps School](https://devsecopsschool.com/blog/github-actions-in-devsecops-a-comprehensive-tutorial)
- [Software Supply Chain Security Ultimate Guide](https://checkmarx.com/learn/supply-chain-security/software-supply-chain-security-guide)
- [Best Software Supply Chain Security Tools for AppSec Teams](https://www.endorlabs.com/learn/best-software-supply-chain-security-tools-a816d)
