# AI Infosec Landing

每日 AI / 安全 / 合规中英双语实用情报 / Daily bilingual practical intelligence for AI, security, and compliance

主页 / Landing Page: https://kylesking.github.io/ai-infosec-landing/

## 功能特性

- 每天自动发布 1 篇文章，四种内容类型轮换
- 中英双语，聚焦趋势追踪、教程实操、工具分享、法规合规分析
- 内容类型：工具攻略、趋势分析、防御实操、法规追踪
- DeepSeek V4 Flash 驱动写作
- Tavily 搜索最新热点
- GitHub Actions 全自动运行，无需服务器

## 快速部署

### 1. Fork 或 Clone 仓库

```bash
git clone https://github.com/YOUR_USERNAME/ai-infosec-landing.git
cd ai-infosec-landing
```

### 2. 修改配置

编辑 `_config.yml`，把 `YOUR_GITHUB_USERNAME` 替换成你的 GitHub 用户名：

```yaml
url: "https://YOUR_GITHUB_USERNAME.github.io"
```

### 3. 设置 GitHub Secrets

进入仓库 **Settings → Secrets and variables → Actions → New repository secret**，添加：

| Secret 名称 | 说明 |
|------------|------|
| `OPENROUTER_API_KEY` | OpenRouter API Key |
| `TAVILY_API_KEY` | Tavily Search API Key |

### 4. 开启 GitHub Pages

进入仓库 **Settings → Pages**：
- Source 选择 `GitHub Actions`

### 5. 手动触发第一次

进入 **Actions → Daily Article Publisher → Run workflow**

等待约2分钟，文章自动生成并部署。

## 站点地址

```
https://YOUR_USERNAME.github.io/ai-infosec-landing
```

## 自定义发布时间

编辑 `.github/workflows/daily-publish.yml`：

```yaml
- cron: '0 0 * * *'  # UTC 00:00 = 北京时间 08:00
```

按需修改 cron 时间。

## 本地预览

```bash
gem install bundler
bundle install
bundle exec jekyll serve
# 访问 http://localhost:4000
```

## 技术栈

- Jekyll 4.3 静态站点
- GitHub Actions 自动化
- DeepSeek V4 Flash via OpenRouter
- Tavily Search API
- GitHub Pages 托管
