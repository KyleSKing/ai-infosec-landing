<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  exclude-result-prefixes="atom content">

  <xsl:output method="html" encoding="UTF-8" doctype-system="about:legacy-compat" />

  <xsl:template match="/">
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title><xsl:value-of select="rss/channel/title" /> RSS Feed</title>
        <style>
          :root{color-scheme:dark;--bg:#05070a;--panel:#0b1017;--text:#f7f8f8;--muted:#8a8f98;--line:rgba(255,255,255,.1);--cyan:#00e5ff;--amber:#ffb020}
          *{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,rgba(0,229,255,.14),transparent 32%),var(--bg);color:var(--text);font-family:Inter,"Noto Sans SC",system-ui,sans-serif;line-height:1.65}.wrap{max-width:960px;margin:0 auto;padding:48px 20px 72px}.kicker{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--cyan);font-size:12px;letter-spacing:.14em}.head{border:1px solid var(--line);border-radius:20px;padding:28px;background:rgba(255,255,255,.04);margin-bottom:22px}.head h1{margin:.2rem 0 .5rem;font-size:clamp(2rem,6vw,4rem);line-height:1}.head p{margin:0;color:var(--muted)}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}.btn{border:1px solid rgba(0,229,255,.36);border-radius:999px;color:var(--cyan);text-decoration:none;padding:9px 14px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}.note{border-left:3px solid var(--amber);background:rgba(255,176,32,.1);padding:12px 14px;color:#d8d2c7;margin-bottom:22px}.item{display:block;border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:12px 0;text-decoration:none;color:inherit;background:rgba(255,255,255,.035)}.item:hover{border-color:rgba(0,229,255,.45);background:rgba(0,229,255,.06)}.meta{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--muted);font-size:12px;margin-bottom:8px}.title{font-size:20px;font-weight:800;line-height:1.35;margin-bottom:8px}.desc{color:#d0d6e0;font-size:14px}.raw{margin-top:26px;color:var(--muted);font-size:13px}code{color:var(--cyan)}
        </style>
      </head>
      <body>
        <main class="wrap">
          <section class="head">
            <div class="kicker">RSS FEED · SUBSCRIBE ENDPOINT</div>
            <h1><xsl:value-of select="rss/channel/title" /></h1>
            <p><xsl:value-of select="rss/channel/description" /></p>
            <div class="actions">
              <a class="btn" href="{rss/channel/link}">OPEN SITE</a>
              <a class="btn" href="{rss/channel/atom:link/@href}">RAW RSS XML</a>
            </div>
          </section>

          <div class="note">
            这是 RSS 订阅地址。复制当前 URL 到 RSS 阅读器即可订阅；浏览器中显示的是可读预览。
          </div>

          <xsl:for-each select="rss/channel/item">
            <a class="item" href="{link}">
              <div class="meta"><xsl:value-of select="pubDate" /></div>
              <div class="title"><xsl:value-of select="title" /></div>
              <div class="desc"><xsl:value-of select="description" /></div>
            </a>
          </xsl:for-each>

          <p class="raw">订阅地址：<code><xsl:value-of select="rss/channel/atom:link/@href" /></code></p>
        </main>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
