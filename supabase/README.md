# Supabase backend

## Setup

```bash
# 1. Install supabase CLI: https://supabase.com/docs/guides/cli
# 2. Link to your project
supabase link --project-ref <your-ref>

# 3. Apply schema
supabase db push

# 4. Set function secrets
supabase secrets set SUPABASE_URL=https://<your-ref>.supabase.co
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
supabase secrets set SUPABASE_IP_SALT=<32-char-random-string>

# 5. Deploy functions
supabase functions deploy like view stats
```

## Tables

- `views` — one row per (deduped) page view, with IP-hash + slug + ts
- `likes` — counter per article slug
- `like_voters` — IP-hash × slug dedup table

## RPC functions

- `top_articles(days, lim)` — top articles by views
- `daily_stats(days)` — daily PV/UV time series
- `site_totals()` — global counters (total PV/UV/likes/articles)

## Edge functions

- `POST /functions/v1/like`  body: `{slug, action: "add"|"remove"}`  →  `{slug, liked, count}`
- `POST /functions/v1/view`  body: `{slug, lang}`  →  204
- `GET  /functions/v1/stats?type=top|daily|site`  →  JSON

## Security

- Anon key: SELECT on `likes` only. No write access.
- Service role key: used by edge functions only. Never browser-exposed.
- IP-hash: `sha256(ip + IP_SALT)`, computed server-side in edge function.
