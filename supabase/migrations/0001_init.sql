-- ai-infosec-landing — Supabase initial schema
-- Applied via `supabase db push` or dashboard SQL editor

-- views: one row per article visit, deduped server-side (30 min window per ip+slug)
create table if not exists public.views (
  id bigserial primary key,
  slug text not null,
  ip_hash text not null,
  ua_hash text,
  lang text check (lang in ('zh', 'en', 'bi')),
  ts timestamptz not null default now()
);

create index if not exists views_slug_ts_idx on public.views (slug, ts desc);
create index if not exists views_ip_slug_ts_idx on public.views (ip_hash, slug, ts desc);
create index if not exists views_ts_idx on public.views (ts desc);

-- likes: aggregate counter per article (one row per slug)
create table if not exists public.likes (
  slug text primary key,
  count int not null default 0,
  updated_at timestamptz not null default now()
);

-- like_voters: prevent double-like from same IP
create table if not exists public.like_voters (
  ip_hash text not null,
  slug text not null,
  ts timestamptz not null default now(),
  primary key (ip_hash, slug)
);

create index if not exists like_voters_slug_idx on public.like_voters (slug);

-- RLS: anon can SELECT likes (for initial render), nothing else directly
alter table public.views enable row level security;
alter table public.likes enable row level security;
alter table public.like_voters enable row level security;

-- likes: anon can read counts
drop policy if exists "anon read likes" on public.likes;
create policy "anon read likes" on public.likes
  for select to anon using (true);

-- views / like_voters: NO anon policy. All writes must go through edge functions (service_role).
-- This guarantees browsers can't bypass IP-hash validation.

-- Aggregations

create or replace function public.top_articles(days int default 7, lim int default 5)
returns table (slug text, views bigint, likes int)
language sql stable
as $$
  select v.slug, count(*)::bigint as views, coalesce(l.count, 0) as likes
  from public.views v
  left join public.likes l on l.slug = v.slug
  where v.ts > now() - make_interval(days => days)
  group by v.slug, l.count
  order by views desc, likes desc
  limit lim;
$$;

create or replace function public.daily_stats(days int default 30)
returns table (day date, pv bigint, uv bigint)
language sql stable
as $$
  select date_trunc('day', ts)::date as day,
         count(*)::bigint as pv,
         count(distinct ip_hash)::bigint as uv
  from public.views
  where ts > now() - make_interval(days => days)
  group by 1
  order by 1;
$$;

create or replace function public.site_totals()
returns table (total_pv bigint, total_uv bigint, total_likes bigint, total_articles bigint)
language sql stable
as $$
  select
    (select count(*) from public.views)::bigint as total_pv,
    (select count(distinct ip_hash) from public.views)::bigint as total_uv,
    (select coalesce(sum(count), 0) from public.likes)::bigint as total_likes,
    (select count(*) from public.likes)::bigint as total_articles;
$$;
