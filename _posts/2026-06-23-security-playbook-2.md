---
layout: post
title_en: "DevSecOps in GitHub Actions: Automating Security Scans for SBOM, SAST, and DAST"
title_cn: "GitHub Actions DevSecOps：自动化SBOM、SAST与DAST安全扫描"
date: 2026-06-23 17:56:16 +0800
category: infosec
content_type: defensive_playbook
content_type_cn: "防御实操"
content_type_en: "Defensive Playbook"
tags:
  - "DevSecOps"
  - "GitHub Actions"
  - "SBOM"
  - "SAST"
  - "DAST"
summary_en: "This playbook covers how to integrate SBOM generation (Syft), SAST (CodeQL), and DAST (OWASP ZAP) into GitHub Actions for early vulnerability detection. It provides actionable workflows and addresses false positives, performance overhead, and compliance risks."
summary_cn: "本文介绍如何在GitHub Actions中集成SBOM生成（Syft）、SAST（CodeQL）和DAST（OWASP ZAP），实现早期漏洞检测。提供可落地的CI/CD工作流，并讨论误报、性能开销与合规风险。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## GitHub Actions DevSecOps：自动化SBOM、SAST与DAST安全扫描

# GitHub Actions DevSecOps：自动化SBOM、SAST与DAST安全扫描

## 风险是什么

现代软件供应链攻击正在快速上升。2025年，超过70%的企业代码库包含至少一个已知漏洞的开源依赖，而供应链攻击（如依赖混淆、恶意包投毒、CI/CD管道劫持）已成为攻击者最青睐的入口之一。

核心风险有三层：

1. **依赖层**：你不知道你的代码里用了什么，更不知道这些依赖有没有已知漏洞。没有SBOM（软件物料清单），你连“用了什么”都说不清。
2. **代码层**：开发者在代码中引入的安全缺陷（SQL注入、XSS、硬编码密钥）在合并前未被发现，直接流入生产。
3. **运行时层**：应用上线后，攻击面暴露在互联网上，但团队从未对运行中的应用做过动态扫描。

这三个风险叠加，意味着你的CI/CD管道可能正在安全地交付不安全的软件。

## 谁会受影响

- **开发团队**：每天提交代码，但缺乏自动化安全检测手段。
- **DevOps/SRE团队**：维护CI/CD管道，需要在不拖慢交付的前提下嵌入安全扫描。
- **安全工程师**：需要从海量告警中筛选真正需要修复的漏洞。
- **合规团队**：需要满足PIPL、CSL、MLPS 2.0、EU AI Act、SOC 2等对软件供应链透明度的要求。
- **独立开发者/小团队**：没有专职安全人员，但同样面临供应链攻击风险。

**不适合谁**：已经拥有成熟商业级AST平台（如Snyk、Checkmarx、Veracode）且管道集成完善的团队。本文方案是开源/低成本替代方案，适合从零搭建或补充现有流程。

## 怎么检查

### 第一步：生成SBOM

SBOM是供应链安全的基础。没有SBOM，你无法知道依赖树的全貌。

**推荐工具：Syft（Anchore开源项目）**

在GitHub Actions中集成：

```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    path: ./
    format: cyclonedx-json
    output-file: sbom.cdx.json
```

检查要点：
- 生成的SBOM是否包含所有直接和传递依赖？
- 格式是否为CycloneDX或SPDX（行业标准）？
- 是否包含版本号和许可证信息？

### 第二步：SAST静态扫描

SAST在代码编写阶段发现安全缺陷，实现“左移”。

**推荐工具：CodeQL（GitHub原生）**

```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: python, javascript
- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v3
```

检查要点：
- 是否覆盖了所有主要语言？
- 是否配置了`security-and-quality`查询套件（比默认更全面）？
- 是否在PR级别设置了门禁（阻断含Critical漏洞的PR合并）？

### 第三步：DAST动态扫描

DAST在应用运行后扫描，发现运行时安全问题。

**推荐工具：OWASP ZAP**

```yaml
- name: ZAP Scan
  uses: zaproxy/action-full-scan@v0.10.0
  with:
    target: 'https://staging.example.com'
    rules_file_name: '.zap/rules.tsv'
    cmd_options: '-a'
```

检查要点：
- 是否有可访问的staging环境？
- 是否配置了排除规则（避免扫描注销/删除功能）？
- 是否设置了告警阈值（避免因低危告警阻塞管道）？

## 怎么修 / 怎么接入流程

### 完整工作流示例

在`.github/workflows/security-scan.yml`中：

```yaml
name: DevSecOps Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          path: ./
          format: cyclonedx-json
          output-file: sbom.cdx.json
      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.cdx.json

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-and-quality
      - name: Autobuild
        uses: github/codeql-action/autobuild@v3
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

  dast:
    needs: [sbom, sast]
    runs-on: ubuntu-latest
    steps:
      - name: ZAP Scan
        uses: zaproxy/action-full-scan@v0.10.0
        with:
          target: 'https://staging-${{ github.sha }}.example.com'
          allow_issue_writing: false
```

### 修复优先级

1. **SBOM告警**：使用`grype`（与Syft同属Anchore生态）扫描SBOM中的漏洞，按CVSS评分排序修复。
2. **SAST告警**：CodeQL结果按`error`/`warning`分级，Critical和High必须阻断PR合并。
3. **DAST告警**：ZAP结果中，仅High和Critical阻断管道，Medium和Low作为工单跟踪。

### 中国合规特别要求

- **PIPL/CSL**：SBOM中需记录个人信息处理模块的依赖关系，确保不引入未经安全评估的第三方SDK。
- **MLPS 2.0**：SAST和DAST结果需作为等保测评的“安全开发”证据留存。
- **CAC数据出境**：如果SBOM显示使用了跨境数据处理的依赖（如海外日志SDK），需触发数据出境安全评估流程。

## 注意事项

### 工具限制

| 工具 | 已知限制 | 误报/漏报 |
|------|----------|-----------|
| Syft | 不扫描运行时依赖，仅分析文件系统 | 低误报，但可能漏掉动态加载的包 |
| CodeQL | 对动态语言（Python/JS）覆盖较好，对C++/Go的复杂模板可能漏报 | 中等误报率，需要人工确认 |
| ZAP | 仅扫描HTTP接口，不覆盖gRPC/WebSocket | 高误报率，需要配置排除规则 |

### 运营风险

- **管道时间膨胀**：全量SAST扫描可能增加5-15分钟构建时间。建议SAST在PR级别运行，DAST在合并后运行。
- **告警疲劳**：ZAP默认规则集会产生大量Low/Info告警。必须配置`rules_file_name.tsv`排除噪音。
- **假阳性处理**：不要直接忽略，应创建`.codeql/codeql-config.yml`定义suppression规则并附上理由。

### 安全风险

- **DAST扫描目标**：绝不要对生产环境运行ZAP全量扫描，可能导致数据污染或服务中断。
- **凭证管理**：扫描工具中不要硬编码API密钥，使用GitHub Secrets注入。
- **SBOM泄露**：SBOM文件可能暴露内部包名和版本号，上传到公开仓库前需确认。

## 我的判断

**GitHub Actions + 开源工具链（Syft + CodeQL + ZAP）是目前中小团队性价比最高的DevSecOps入门方案。** 它不需要额外预算，不需要专用服务器，完全在GitHub生态内运行。

但必须清醒认识到：这套方案是“安全基线”而非“安全终点”。

- 如果你处理的是重要数据（CIIO、重要数据、跨境数据），这套方案远远不够——你需要商业级SCA工具、IAST运行时监控、以及定期的渗透测试。
- 如果你在合规审计场景下，开源工具的告警报告可能不被审计师接受——需要额外整理和解释。
- 如果你团队超过50人，建议评估Snyk、Checkmarx或Semgrep的商业版，它们提供更好的策略管理和告警去重。

**我的建议**：今天就开始。在现有CI管道中加一个SBOM生成步骤，只需要5分钟。然后逐步加入SAST和DAST。不要追求完美，先跑起来，再优化。

---

## English Brief

**Risk**: Modern software supply chain attacks exploit unknown dependencies, code-level vulnerabilities, and runtime exposure. Without automated SBOM, SAST, and DAST in CI/CD, teams ship insecure software blindly.

**Affected Teams**: Developers, DevOps/SRE, security engineers, compliance teams, and indie hackers. Not for teams already using enterprise AST platforms (Snyk, Checkmarx).

**Checklist**:
1. **SBOM**: Use `anchore/sbom-action` to generate CycloneDX JSON.
2. **SAST**: Use `github/codeql-action` with `security-and-quality` queries.
3. **DAST**: Use `zaproxy/action-full-scan` on staging environment.

**Remediation Workflow**:
- Block PR merge on CodeQL Critical/High findings.
- Use `grype` to scan SBOM for CVSS-scored vulnerabilities.
- Configure ZAP rule exclusions to reduce noise.
- For China compliance (PIPL/CSL/MLPS 2.0): retain scan artifacts as audit evidence; trigger data export assessment if SBOM reveals cross-border dependencies.

**Caveats**:
- Syft misses runtime-loaded packages.
- CodeQL has moderate false positive rate.
- ZAP produces high noise; must configure exclusion rules.
- Never run DAST on production.
- SBOM files may leak internal package names.

**Take**: This open-source stack (Syft + CodeQL + ZAP) is the most cost-effective DevSecOps baseline for small-to-medium teams. It's a starting point, not a final solution. For critical data or compliance-heavy environments, upgrade to commercial tools. Start today: add SBOM generation to your pipeline in 5 minutes.

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## DevSecOps in GitHub Actions: Automating Security Scans for SBOM, SAST, and DAST

# DevSecOps in GitHub Actions: Automating Security Scans for SBOM, SAST, and DAST

## What It Is

DevSecOps in GitHub Actions means embedding security scanning directly into your CI/CD pipeline using GitHub's native automation. The three core scan types are:

- **SBOM (Software Bill of Materials)**: Generates an inventory of all open-source components and dependencies in your application. Tools like Syft, Trivy, and Docker Scout produce machine-readable lists (SPDX, CycloneDX) for vulnerability tracking and compliance.
- **SAST (Static Application Security Testing)**: Scans source code without executing it. GitHub's CodeQL is the primary option, with community alternatives like ESLint security plugins and Bandit for Python.
- **DAST (Dynamic Application Security Testing)**: Tests running applications for vulnerabilities. OWASP ZAP is the leading open-source tool, with GitHub Actions wrappers for API scanning and full web app testing.

## Why It Matters Now

Software supply chain attacks are accelerating. The US Executive Order 14028 and global regulations increasingly require SBOM generation. GitHub Actions makes these scans frictionless—triggering automatically on every push or pull request without separate infrastructure. Teams that skip automated security scanning in CI/CD are shipping blind, often discovering vulnerabilities only after production deployment or audit.

## Practical Next Steps

1. **Add SBOM generation** to your build workflow using `anchore/sbom-action` or `aquasecurity/trivy-action`. Output CycloneDX or SPDX format and store artifacts for audit trails.
2. **Enable CodeQL** via GitHub's built-in action. Configure it for your language (JavaScript, Python, Java, etc.) and set it to run on every push and pull request.
3. **Add a DAST scan** for web applications using `zaproxy/action-api-scan` for REST APIs or `zaproxy/action-full-scan` for full web apps. Run this after deployment to a staging environment.
4. **Use Dependabot** (GitHub-native) or Renovate to automate dependency updates and alert on known vulnerabilities.

Example minimal workflow snippet for a Node.js project:

```yaml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: javascript
- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
```

## Risks and Operational Notes

- **False positives** are common in SAST and DAST. Triage results and tune rules to avoid alert fatigue. Do not block builds on every finding—use severity thresholds.
- **SBOM tools produce flat lists** of vulnerabilities without cloud or runtime context. They are developer-level artifacts, not production security assessments. Pair with runtime scanners (e.g., Wiz, KubeClarity) for actionable insights.
- **DAST scans can break staging environments** or trigger rate limits. Run them against isolated test instances, not production.
- **Pipeline slowdown** is real. Run scans in parallel where possible and cache dependencies to avoid rebuilding SBOMs on every commit.
- **GitHub Actions minutes** are consumed by scans. For large repos, consider running full scans on schedule (nightly) and quick scans on PRs.

## Take

Every team shipping code on GitHub should implement at minimum SBOM generation and CodeQL scanning. These are free, built-in, and take less than an hour to configure. DAST is valuable but requires a running environment—start with API scanning if you have REST endpoints. The cost of not scanning is higher than the cost of false positives or pipeline delays. Automate now, tune later.

</div>

---

### 参考来源 / Sources

- [DevSecOps Tutorial for Beginners | CI Pipeline with GitHub Actions and Docker Scout](https://www.youtube.com/watch?v=gLJdrXPn0ns)
- [DevSecOps with GitHub Action and SaaS Tools | cicd-github-action-example](https://judebantony.github.io/cicd-github-action-example)
- [GitHub Actions in DevSecOps: A Comprehensive Tutorial - DevSecOps School](https://devsecopsschool.com/blog/github-actions-in-devsecops-a-comprehensive-tutorial)
- [Guide to SBOM Tools: 5 Picks for Enterprise Security Teams | Wiz](https://www.wiz.io/academy/application-security/top-open-source-sbom-tools)
- [bureado/awesome-software-supply-chain-security - GitHub](https://github.com/bureado/awesome-software-supply-chain-security)
