---
layout: post
title_en: "DevSecOps Defensive Playbook: Automate Security Scanning in CI/CD with GitHub Actions & SBOM"
title_cn: "DevSecOps防御实操：在CI/CD中集成自动化安全扫描与SBOM"
date: 2026-07-13 01:06:10 +0800
category: infosec
content_type: defensive_playbook
content_type_cn: "防御实操"
content_type_en: "Defensive Playbook"
tags:
  - "DevSecOps"
  - "GitHub Actions"
  - "SBOM"
  - "OWASP ZAP"
  - "CI/CD Security"
summary_en: "A practical guide to embedding OWASP ZAP DAST, SAST, and SBOM scanning into GitHub Actions for early detection of vulnerabilities. Covers setup, remediation workflow, and operational caveats for engineering teams."
summary_cn: "一份实操指南，教你如何在GitHub Actions中集成OWASP ZAP动态扫描、静态分析及SBOM扫描，实现漏洞早期发现。涵盖配置、修复流程及工程团队需要注意的操作陷阱。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## DevSecOps防御实操：在CI/CD中集成自动化安全扫描与SBOM

# DevSecOps防御实操：在CI/CD中集成自动化安全扫描与SBOM

## 风险是什么

现代软件交付高度依赖开源组件和第三方依赖。一次供应链攻击（如SolarWinds、Log4j）就能让整个组织暴露。常见的风险包括：

- **已知漏洞依赖**：项目引用了带CVE的库，未及时更新。
- **配置错误**：Git仓库权限过宽、Actions工作流未限制触发条件、密钥硬编码。
- **API安全缺陷**：REST API未做输入验证、认证缺失。
- **SBOM缺失**：无法快速响应新漏洞，因为不知道用了哪些组件及其版本。
- **CI/CD管道自身被攻击**：未签名的第三方Action、未锁定的依赖版本。

这些风险在每次代码提交和合并时都可能被引入。传统“上线前再安全测试”的模式已经失效，必须左移——在CI/CD管道中自动执行安全扫描。

## 谁会受影响

- **开发团队**：直接编写代码、引入依赖、配置CI/CD的人。
- **安全工程师**：需要制定策略、选择工具、分析结果。
- **DevOps/SRE**：维护CI/CD基础设施，负责扫描任务的稳定运行。
- **合规/法务**：需要SBOM满足供应链安全法规（如美国EO 14028、中国关键信息基础设施安全保护要求）。
- **技术管理者**：决定安全投入优先级，评估风险。

## 怎么检查

建议在CI/CD中建立以下检查点（按执行顺序）：

### 1. 静态代码分析（SAST）
- 使用 **CodeQL**（GitHub原生）或 **Semgrep**。
- 检查SQL注入、XSS、硬编码密钥等。
- 在push和pull_request触发。

### 2. 依赖扫描（SCA）与SBOM生成
- 使用 **Syft** 生成SBOM（支持CycloneDX/SPDX格式），**Grype** 扫描漏洞。
- 或使用 **Trivy** 同时完成SBOM生成和漏洞扫描。
- 将SBOM上传到 **Dependency-Track** 进行持续监控。

### 3. 密钥/凭证扫描
- 使用 **GitLeaks** 或 **TruffleHog** 扫描提交历史中的密钥。
- 在pre-commit hook和CI中均执行。

### 4. 基础设施即代码（IaC）扫描
- 使用 **Checkov** 或 **tfsec** 扫描Terraform、CloudFormation等模板的安全配置。

### 5. 动态应用安全测试（DAST）
- 对已部署的API或Web应用使用 **OWASP ZAP** 进行主动扫描。
- 适合在staging环境或PR部署预览中执行。

### 6. 仓库配置安全扫描
- 使用 **Legitify** 检查Git仓库设置（如分支保护、Actions权限、密钥轮换）。

## 怎么修 / 怎么接入流程

以下是一个完整的GitHub Actions工作流示例，集成SAST、SCA、SBOM、密钥扫描和DAST。将文件保存为 `.github/workflows/security.yml`：

```yaml
name: DevSecOps Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript, python  # 根据项目调整
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: GitLeaks Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  sbom-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM with Syft
        uses: anchore/sbom-action@v0
        with:
          path: ./
          format: cyclonedx-json
      - name: Scan vulnerabilities with Grype
        uses: anchore/scan-action@v3
        with:
          path: ./
          fail-build: true
          severity-cutoff: high
      - name: Upload SBOM to Dependency-Track
        env:
          DTRACK_URL: ${{ secrets.DTRACK_URL }}
          DTRACK_API_KEY: ${{ secrets.DTRACK_API_KEY }}
        run: |
          curl -X POST "$DTRACK_URL/api/v1/bom" \
            -H "X-Api-Key: $DTRACK_API_KEY" \
            -H "Content-Type: multipart/form-data" \
            -F "project=my-app" \
            -F "bom=@sbom.cyclonedx.json"

  dast:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    needs: [sast, sbom-scan]
    steps:
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          docker_name: owasp/zap2docker-stable
          target: https://staging.example.com/api/openapi.json  # 替换为实际API文档URL
          fail_on_alert: high
```

### 关键配置说明

- **fail-build: true**：当发现高危以上漏洞时，阻止合并。
- **severity-cutoff: high**：只对高严重性漏洞失败，避免误报阻塞开发。
- **Dependency-Track**：需要自建服务，用于长期监控SBOM变化和新增漏洞。
- **DAST**：仅对PR执行，且需要staging环境可用。如果无API文档，可使用 `zaproxy/action-full-scan` 进行爬虫扫描。

### 本地开发阶段（Shift Left 更早）

- 安装pre-commit钩子，在commit前运行密钥扫描和lint。
- 使用IDE插件（如Snyk、Trivy）在编写代码时提示依赖漏洞。

## 注意事项

### 工具局限性

| 工具 | 局限 |
|------|------|
| CodeQL | 需要编译型语言配置复杂；规则覆盖不全，可能漏报逻辑漏洞。 |
| Syft/Grype | 仅扫描已知CVE，无法检测0day；依赖NVD数据源更新延迟。 |
| OWASP ZAP | 对单页应用（SPA）扫描效果差；可能产生大量误报；需要目标环境稳定。 |
| GitLeaks | 只能检测已知模式的密钥，自定义规则需维护。 |
| Legitify | 仅检查仓库设置，不检查代码逻辑。 |

### 误报与漏报

- 依赖扫描中，很多CVE标记为“不受影响”但工具仍报错，需要人工研判。
- SAST可能将安全编码模式误判为漏洞（例如参数化查询被误报为SQL注入）。
- 建议设置“警告但不阻断”的阈值，并建立安全团队定期审核机制。

### 性能与成本

- 每次push都运行全量扫描会显著增加构建时间（尤其CodeQL和DAST）。
- 优化策略：SAST和SCA在PR时运行，DAST仅在合并到主分支前运行一次。
- SBOM生成和上传是轻量操作，建议每次构建都执行。

### 合规与SBOM消费

- 生成SBOM只是第一步，必须持续监控（如Dependency-Track）并建立响应流程。
- 中国法规（如《网络数据安全管理条例》《关键信息基础设施安全保护条例》）要求采购软件时提供SBOM，CIIO需评估供应链风险。
- 建议将SBOM作为交付物，与客户或监管共享（仅包含组件列表，不包含内部元数据）。

## 我的判断

**DevSecOps不是工具堆砌，而是流程文化。** 当前大多数团队已经用GitHub Actions做CI，但安全扫描往往缺失或流于形式。我的建议：

1. **从SCA+SBOM开始**：这是投入产出比最高的环节。使用Syft+Grype或Trivy，几分钟就能集成，立即发现已知漏洞。
2. **SAST必选CodeQL**：GitHub原生集成，免费，覆盖主流语言。缺点是扫描慢，但可以只对关键分支运行。
3. **DAST按需启用**：如果项目有REST API，用ZAP做API扫描；如果没有API，DAST的收益较低，可暂缓。
4. **密钥扫描必须前置**：在pre-commit和CI中都跑GitLeaks，防止密钥泄露到远程。
5. **SBOM消费比生成更重要**：很多团队生成SBOM后就不管了。必须接入Dependency-Track或类似平台，设置告警，定期复核。

**适合人群**：已有GitHub CI基础、希望快速提升安全水平的开发团队；需要满足供应链安全合规的组织。

**不适合人群**：没有专职安全人员的小团队（建议先使用Snyk等托管服务）；项目不依赖外部代码（纯自研）可跳过SCA。

**风险警告**：自动化扫描不能替代人工渗透测试。误报会导致开发疲劳，漏报会带来虚假安全感。务必建立安全评审闭环。

---

## English Brief

**Risk**: Software supply chain attacks, vulnerable dependencies, misconfigured CI/CD, hardcoded secrets, and lack of SBOM for incident response.

**Affected teams**: Developers, security engineers, DevOps, compliance, and technical managers.

**Checks**:
- SAST (CodeQL)
- Secret scanning (GitLeaks)
- SCA + SBOM generation (Syft + Grype or Trivy)
- DAST (OWASP ZAP for APIs)
- Repo config audit (Legitify)

**Remediation workflow**:
1. Add a security workflow in `.github/workflows/security.yml` that runs on push/PR.
2. Use CodeQL for static analysis, GitLeaks for secrets, Syft+Grype for SBOM/vulnerabilities.
3. Upload SBOM to Dependency-Track for continuous monitoring.
4. Run ZAP API scan on PRs against staging environment.
5. Set `fail-build: true` for high-severity findings, but allow warnings for medium/low.

**Caveats**:
- Tools have false positives/negatives; require human review.
- DAST is only effective if staging environment is stable.
- SBOM consumption (monitoring) is more important than generation.
- Performance impact: full scans can slow CI; optimize by running DAST only on PRs to main.

**Take**: Start with SCA+SBOM (highest ROI), add SAST (CodeQL) for critical branches, and enforce secret scanning pre-commit. Do not treat automation as a replacement for manual pentesting. For compliance (e.g., CIIO, EU AI Act), SBOM is mandatory but must be actively monitored.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## DevSecOps Defensive Playbook: Automate Security Scanning in CI/CD with GitHub Actions & SBOM

# DevSecOps Defensive Playbook: Automate Security Scanning in CI/CD with GitHub Actions & SBOM

Modern CI/CD pipelines must embed security checks as automated gates, not manual afterthoughts. This playbook covers how to integrate SAST, DAST, SCA, and SBOM generation directly into GitHub Actions workflows, enabling teams to catch vulnerabilities before they reach production.

## What It Is

A DevSecOps defensive pipeline combines static analysis (CodeQL, ESLint), dynamic scanning (OWASP ZAP), dependency vulnerability scanning (Trivy, Grype), and Software Bill of Materials (SBOM) generation (Syft, OX Security). GitHub Actions orchestrates these tools as steps in your CI workflow, triggered on every push or pull request. The goal: shift security left without slowing development.

## Why It Matters Now

Supply chain attacks and regulatory mandates (CISA’s Secure Software Development Attestation, OMB M-22-18) require organizations to know what goes into their software. Automated SBOM generation and vulnerability scanning are no longer optional—they are prerequisites for government contracts and enterprise sales. Meanwhile, OWASP Top 10 and CWE vulnerabilities continue to plague web applications. Automating detection in CI/CD reduces the mean time to remediation and prevents regressions.

## Practical Next Steps

1. **Add static analysis** – In your `.github/workflows/ci.yml`, include a CodeQL step (source [2]):
   ```yaml
   - name: Run security scan
     uses: github/codeql-action/init@v2
     with:
       languages: javascript
   - name: Perform CodeQL Analysis
     uses: github/codeql-action/analyze@v2
   ```

2. **Enable DAST for APIs** – Use the OWASP ZAP GitHub Action for API scanning (source [1]):
   ```yaml
   - name: ZAP Scan
     uses: zaproxy/action-api-scan@v0.1.0
     with:
       token: ${{ secrets.GITHUB_TOKEN }}
       target: 'https://your-staging-app/api/openapi.json'
   ```

3. **Generate and scan SBOM** – Add Syft and Grype to generate a CycloneDX SBOM and scan for known vulnerabilities (source [5]):
   ```yaml
   - name: Generate SBOM
     uses: anchore/sbom-action@v0
     with:
       format: cyclonedx-json
   - name: Scan SBOM
     uses: anchore/scan-action@v3
     with:
       sbom: sbom.json
   ```

4. **Audit Git repository security** – Include Legitify to detect misconfigured repo settings and risky GitHub Actions (source [3]).

5. **Monitor continuously** – Feed SBOMs into Dependency-Track for long-term tracking of component vulnerabilities (source [5]).

## Risks & Operational Notes

- **False positives** – Static and dependency scanners can flag benign issues. Tune ignore rules early and triage results weekly.
- **Performance** – Adding multiple scans can increase pipeline duration. Use caching for dependency scanners and run time-consuming jobs in parallel.
- **Credential leakage** – Never embed secrets in workflow files; use GitHub Secrets. ZAP and other tools may expose tokens in logs if not configured carefully.
- **SBOM accuracy** – Generated SBOMs may miss transitive dependencies or include stale versions. Pair generation with continuous monitoring.
- **Attack surface** – The CI/CD pipeline itself is a target. Lock down runner permissions, pin action versions, and audit third-party actions regularly.

## Take

Start small: add SAST and SBOM generation to your most critical repo within one sprint. Gate merges on critical and high-severity vulnerabilities. As confidence grows, layer in DAST for external endpoints and continuous SBOM monitoring. Automation doesn’t eliminate risk—it makes it visible and actionable. The goal is not zero vulnerabilities, but a reproducible process that prevents known bad patterns from reaching production.

</div>

---

### 参考来源 / Sources

- [DevSecOps with GitHub Action and SaaS Tools | cicd-github-action-example](https://judebantony.github.io/cicd-github-action-example)
- [GitHub Actions in DevSecOps: A Comprehensive Tutorial - DevSecOps School](https://devsecopsschool.com/blog/github-actions-in-devsecops-a-comprehensive-tutorial)
- [Top 13 Open-Source DevSecOps Tools for 2025](https://www.upwind.io/glossary/13-best-devsecops-tools-2025s-best-open-source-options-sorted-by-use-case)
- [[PDF] Recommended Practices for Software Bill of Materials Consumption](https://www.cisa.gov/sites/default/files/2024-08/SECURING_THE_SOFTWARE_SUPPLY_CHAIN_RECOMMENDED_PRACTICES_FOR_SOFTWARE_BILL_OF_MATERIALS_CONSUMPTION-508.pdf)
- [Top 5 SBOM Tools for Securing the Software Supply Chain](https://www.ox.security/blog/sbom-tools)
