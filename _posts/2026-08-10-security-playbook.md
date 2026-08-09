---
layout: post
title_en: "Practical DevSecOps in CI/CD: Detecting SBOM, SAST, SCA & Secrets Risks with GitHub Actions"
title_cn: "CI/CD中实战DevSecOps：用GitHub Actions检测SBOM、SAST、SCA与密钥风险"
date: 2026-08-10 00:42:42 +0800
category: infosec
content_type: defensive_playbook
content_type_cn: "防御实操"
content_type_en: "Defensive Playbook"
tags:
  - "DevSecOps"
  - "GitHub Actions"
  - "SBOM"
  - "SAST"
  - "SCA"
  - "secret scanning"
  - "supply chain security"
  - "CI/CD security"
summary_en: "A defensive playbook for teams to embed SBOM generation, SAST, SCA, secret scanning, and container signing into GitHub Actions pipelines using open-source tools. Includes detection steps, remediation workflows, and operational caveats for false positives and CI overhead."
summary_cn: "面向开发和安全团队的操作手册，讲解如何在GitHub Actions中集成SBOM生成、静态分析、依赖扫描、密钥检测和容器签名。包含检测步骤、修复流程，以及误报和CI性能开销的注意事项。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## CI/CD中实战DevSecOps：用GitHub Actions检测SBOM、SAST、SCA与密钥风险

# CI/CD中实战DevSecOps：用GitHub Actions检测SBOM、SAST、SCA与密钥风险

## 风险是什么

现代软件交付依赖于大量开源组件和第三方依赖，攻击者可以渗透依赖链、植入恶意包、窃取构建密钥，或者利用未发现的漏洞。常见的 DevSecOps 风险包括：

- **SBOM（软件物料清单）缺失**：不知道应用中用了哪些组件、版本，无法快速响应新披露的漏洞。
- **SAST（静态应用安全测试）缺失**：源代码中的安全缺陷（SQL 注入、XSS、硬编码密码等）直接流入生产。
- **SCA（软件组成分析）缺失**：使用的开源库存在已知 CVE（通用漏洞披露），且未及时更新。
- **密钥/凭据泄露**：硬编码的 API 密钥、令牌、数据库密码被提交到仓库，导致外部攻击者直接访问内部系统。
- **镜像和构建环境不安全**：基础镜像存在漏洞，或构建过程中使用的缓存、第三方 action 未验证完整性。

这些问题在 CI/CD 流水线中如果未被自动化检测和阻断，最终都会暴露在生产环境中，带来数据泄露、服务中断、合规处罚等严重后果。

## 谁会受影响

- **开发团队**：直接将不安全代码推送到仓库。
- **DevOps / SRE 团队**：维护 CI/CD 流水线，但安全扫描配置不完整或未绑定为阻断条件。
- **安全团队**：依赖事后人工审计，效率低且覆盖不全。
- **合规团队**：需要证明软件供应链的安全性和可追溯性（如 SOC 2、ISO 27001、PIPL 等对第三方组件管理的要求）。
- **管理层 / 甲方**：如果供应链攻击发生，将面临业务停摆和法律责任。

## 怎么检查

在 GitHub Actions 中集成以下扫描，可以在每次 push 或 PR 时自动执行。以下基于一个已验证的持续集成安全流水线（如 [awesome-security-pipeline](https://github.com/rezmoss/awesome-security-pipeline)）列举关键步骤：

### 1. Secrets 扫描（密钥检测）

使用工具如 **TruffleHog** 或 **GitLeaks** 扫描提交历史中的高熵字符串和已知模式。

```yaml
- name: Secret scan
  uses: trufflesecurity/trufflehog@v3
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
    head: HEAD
    fail_on_error: true
```

### 2. SAST（静态代码分析）

使用 **Semgrep** 或 **CodeQL** 对代码库进行规则匹配，发现常见漏洞模式。

```yaml
- name: SAST with Semgrep
  uses: semgrep/semgrep-action@v1
  with:
    config: auto  # 或指定规则集
    failOn: high
```

### 3. SCA / 依赖项扫描

使用 **Trivy** 或 **Grype** 扫描 `requirements.txt`、`package-lock.json` 等清单文件，识别已知 CVE。

```yaml
- name: Scan dependencies with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: fs
    scan-ref: .
    format: sarif
    output: trivy-results.sarif
    severity: HIGH,CRITICAL
    exit-code: 1
```

### 4. SBOM 生成

使用 **Syft** 生成 CycloneDX 格式的 SBOM，并将其作为构建产物归档，便于下游审计。

```yaml
- name: Generate SBOM
  uses: anchore/syft-action@v0
  with:
    path: .
    output: cyclonedx-json
    file: sbom.cdx.json
```

### 5. 容器镜像扫描（如果构建 Docker 镜像）

使用 **Trivy** 或 **Docker Scout** 对生成的镜像进行漏洞扫描，并生成不可变摘要（digest）用于签名。

```yaml
- name: Build and scan image
  run: |
    docker build -t myapp:${{ github.sha }} .
    trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:${{ github.sha }}
```

### 6. （可选）DAST 动态扫描

如果已有测试环境，可用 OWASP ZAP 的 API 扫描模式执行动态安全测试，但注意 DAST 通常部署在预发布环境，不适合每次提交。

## 怎么修 / 怎么接入流程

1. **选取工具组合**：每个类别至少选一个成熟的开源工具（如 Semgrep + Trivy + TruffleHog + Syft）。
2. **编写统一 Workflow**：在一个 `.github/workflows/security.yml` 中定义所有步骤，按阶段串联（Secrets → SAST → SCA → SBOM → Build）。
3. **设置失败条件**：对 HIGH/CRITICAL 漏洞或有效密钥，使用 `exit-code: 1` 并让 job 失败，从而阻断合并。
4. **生成报告并归档**：将 SARIF 结果上传到 GitHub Security 选项卡（`github/codeql-action/upload-sarif`），并将 SBOM 和镜像摘要上传为 Artifacts。
5. **密钥轮换与修复**：当检测到密钥时，立即通知开发者撤销并替换，同时扫描历史提交删除痕迹。
6. **定期更新规则库**：工具依赖规则集，建议每周或每次工具版本更新时拉取最新规则。
7. **配置合规策略**：对于中国法规下的重要数据和跨境传输，需额外检查组件中的隐私库（如某些 SDK 是否违规收集数据），这一步需要手工审核配合。

## 注意事项

- **工具局限性**：SAST 可能漏报逻辑漏洞、误报大量低级问题；SCA 仅能扫描已知 CVE，对零日或供应链投毒风险无法检测；密钥扫描可能遗漏未匹配模式的 token。
- **性能开销**：全量扫描大型项目可能耗时 5-15 分钟，建议在 PR 上仅对变更文件执行 SAST，SCA 使用增量模式。
- **凭证保护**：在 workflow 中避免直接暴露 GitHub Token 或自定义密钥，使用 `secrets.GITHUB_TOKEN` 和环境变量加密。
- **SBOM 更新**：SBOM 不是静态文件，每次依赖变更后必须重新生成，并与版本标签关联。
- **合规落地**：国内法规（如《网络安全法》《数据安全法》《个人信息保护法》及算法备案要求）要求对跨境数据、重要数据处理进行安全评估，SBOM 可以帮助说明使用了哪些处理数据的组件，但还需配合数据处理清单和影响评估报告。

## 我的判断

**在 CI/CD 中自动集成 DevSecOps 扫描已是必选项，而非锦上添花。** 对于任何输出软件产品的团队，至少应完成“密钥扫描 + SCA 高/危阻断 + SBOM 生成”这三级安全基座。基于 GitHub Actions 的开源工具链已经足够成熟，无需昂贵商业工具即可应对大部分常见风险。

- **适合人群**：中小型开发团队、独立开发者、DevOps 工程师、安全工程师。
- **不适合人群**：对安全合规有极致要求（如医疗、军工）或需要动态模糊测试、IAST 深度分析的团队，这些仍需专业商业产品。
- **推荐顺序**：先跑通 key leak 和 SCA，再补充 SAST，最后完善 SBOM 和签名。

建议所有团队在本周内 fork 一个类似 [awesome-security-pipeline](https://github.com/rezmoss/awesome-security-pipeline) 的仓库跑通一次完整流程，然后根据自己语言和技术栈进行裁剪。

---

## English Brief

**Risk**: Missing SBOM, SAST, SCA, and secret detection in CI/CD pipelines allow vulnerabilities, leaked credentials, and unpatched dependencies to reach production, enabling supply chain attacks and compliance failures.

**Affected teams**: Dev, DevOps, security, compliance, and management.

**Checks**: Integrate GitHub Actions with:
- Secret scanning (TruffleHog / GitLeaks)
- SAST (Semgrep / CodeQL)
- SCA / dependency scan (Trivy / Grype)
- SBOM generation (Syft)
- Container image scan (Trivy / Docker Scout)

**Remediation workflow**: Define a unified workflow; break builds on HIGH/CRITICAL findings; upload SARIF reports to GitHub Security; archive SBOM and image digests as artifacts; rotate secrets immediately upon detection.

**Caveats**: Tools miss zero‑day attacks, produce false positives, and require rule updates; full scans increase pipeline duration; SBOM must be regenerated on every dependency change.

**Take**: Automating these five scanning categories is the minimum viable security baseline. Teams should implement secret scan + SCA + SBOM first, and then add SAST. An open‑source pipeline (e.g., awesome‑security‑pipeline) can serve as a practical starting point.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## Practical DevSecOps in CI/CD: Detecting SBOM, SAST, SCA & Secrets Risks with GitHub Actions

# Practical DevSecOps in CI/CD: Detecting SBOM, SAST, SCA & Secrets Risks with GitHub Actions

## What This Is

A practical, continuously verified open-source DevSecOps pipeline for GitHub Actions that integrates SBOM generation, SAST (Static Application Security Testing), SCA (Software Composition Analysis), secrets detection, container scanning, and artifact signing into a single CI/CD workflow. The reference implementation is the `awesome-security-pipeline` repository, which uses an intentionally vulnerable Python application from OWASP to demonstrate real vulnerability detection.

## Why It Matters Now

Software supply chain attacks have become the primary vector for breaches. The US Executive Order on Cybersecurity, EU Cyber Resilience Act, and China's MLPS 2.0 all mandate SBOMs and dependency visibility. Most teams still run security scans manually or not at all. Embedding these checks into CI/CD means every commit gets automatically validated before reaching production, reducing the window for exploitation from weeks to minutes.

## Practical Next Steps

1. **Fork and run the demo pipeline**: Fork `rezmoss/awesome-security-pipeline`, enable GitHub Actions, and trigger the Security Baseline workflow. It requires no cloud account or custom secrets.
2. **Inspect the artifacts**: After a successful run, examine the CycloneDX SBOM, SAST reports, dependency scan results, and the immutable container digest.
3. **Adapt for your stack**: The pipeline is language-agnostic but the demo uses Python. Replace the scanning tools with equivalents for your tech stack (e.g., Trivy for containers, Semgrep for SAST, Gitleaks for secrets).
4. **Add DAST for APIs**: Integrate OWASP ZAP API scan for REST endpoints, as demonstrated in the cicd-github-action-example repository.
5. **Sign your artifacts**: Enable keyless signing using Sigstore for container images and SBOMs to establish provenance.

## Risks and Operational Notes

- **False positives**: SAST and SCA tools generate noise. Triage and tune rules per project rather than blindly blocking builds.
- **Pipeline slowdown**: Full security scans can add 5-15 minutes to CI. Run fast checks (secrets, linting) on every commit and deeper scans (SAST, DAST) on pull requests or merges.
- **SBOM maintenance**: SBOMs must be regenerated on every build. Stale SBOMs are worse than none.
- **Tool selection**: Not all open-source scanners support all languages. Verify coverage for your dependencies.
- **Compliance alignment**: For Chinese regulations (CSL, DSL, PIPL), ensure SBOMs capture all third-party components and that scanning tools are deployed within China if processing sensitive data.

## The Take

This is not theoretical. A working, tested pipeline exists today that any team can fork and run in under 10 minutes. The barrier to entry is a GitHub account. The cost is zero. The risk of not doing it is a compromised supply chain. Start with the demo, then adapt. Security in CI/CD is no longer optional—it's the minimum viable practice for any team shipping software.

</div>

---

### 参考来源 / Sources

- [DevSecOps Tutorial for Beginners | CI Pipeline with GitHub Actions and Docker Scout](https://www.youtube.com/watch?v=gLJdrXPn0ns)
- [GitHub - rezmoss/awesome-security-pipeline: Practical, continuously verified open-source DevSecOps tools and a tested CI/CD security pipeline for GitHub Actions](https://github.com/rezmoss/awesome-security-pipeline)
- [DevSecOps with GitHub Action and SaaS Tools | cicd-github-action-example](https://judebantony.github.io/cicd-github-action-example)
- [Software Supply Chain Security Ultimate Guide](https://checkmarx.com/learn/supply-chain-security/software-supply-chain-security-guide)
- [Software Supply Chain Security: A Strategic Guide to SCA & SBOMs](https://www.armorcode.com/blog/software-supply-chain-security-guide-sca-sbom)
