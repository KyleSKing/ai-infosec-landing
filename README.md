# AI Infosec Landing

每周 AI / 安全 / 合规中英双语实用情报 / Weekly bilingual practical intelligence for AI, security, and compliance

主页 / Landing Page: https://kylesking.github.io/ai-infosec-landing/

## 功能特性

- 每周自动发布 1 篇文章，四种内容类型轮换
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

进入 **Actions → Weekly Article Publisher → Run workflow**

等待约2分钟，文章自动生成并部署。

## 站点地址

```
https://YOUR_USERNAME.github.io/ai-infosec-landing
```

## 自定义发布时间

编辑 `.github/workflows/daily-publish.yml`：

```yaml
- cron: '0 16 * * 0'  # 每周日UTC 16:00 = 北京时间周一00:00
```

按需修改 cron 时间。周值：0=周日、1=周一等。

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
- Supabase（访问统计 / 点赞 / JSON-LD SEO 元数据）
- GitHub Pages 托管

## 可选：Supabase 接入（访问统计 + 点赞）

跳过也能用，但所有"浏览数 / 点赞 / 热门榜单"会显示"—"占位。

### 1. 创建 Supabase 项目

1. 打开 https://supabase.com → New project，命名如 `ai-infosec-landing`
2. Settings → API，记下 `Project URL` 和 `service_role` key

### 2. 跑 schema

在 SQL Editor 粘贴并执行 [supabase/migrations/0001_init.sql](supabase/migrations/0001_init.sql)。

### 3. 部署 Edge Functions

```bash
# 本地或 GitHub Actions 容器内
supabase link --project-ref <your-ref>
supabase secrets set SUPABASE_URL=https://<your-ref>.supabase.co
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
supabase secrets set SUPABASE_IP_SALT=<32-char-random>
supabase functions deploy like view stats
```

### 4. GitHub Secrets 新增

| Secret | 说明 |
|---|---|
| `SUPABASE_URL` | `https://<your-ref>.supabase.co` |
| `SUPABASE_ANON_KEY` | 浏览器公开 key（仅 SELECT 权限） |
| `SUPABASE_SERVICE_ROLE_KEY` | **仅 CI 用**，调 Edge Function + sync stats |
| `SUPABASE_IP_SALT` | 32 字符随机串，加盐用 |

跑一次 workflow → 首页 sidebar 应出现 PV/UV/点赞数；点文章页点赞按钮可写入。

## SEO 自检

- `robots.txt` + `sitemap.xml` 已生成
- 每篇文章注入 JSON-LD `Article` schema
- 首页注入 `WebSite` schema
- `<link rel="canonical">` + hreflang `zh-CN` / `en` / `x-default`
- Open Graph + Twitter Card（`jekyll-seo-tag` 增强）

部署后到以下工具校验：
- https://search.google.com/test/rich-results
- https://www.opengraph.xyz/
- Chrome DevTools → Lighthouse → SEO 审计
