-- Keep like voter and aggregate updates in one serialized transaction per slug.
create or replace function public.toggle_like(p_slug text, p_ip_hash text, p_action text)
returns table (liked boolean, count int)
language plpgsql
security definer
set search_path = ''
as $$
declare
  vote_exists boolean;
  delta int := 0;
  result_liked boolean;
  result_count int;
begin
  perform pg_advisory_xact_lock(hashtextextended(p_slug, 0));
  select exists (
    select 1 from public.like_voters where ip_hash = p_ip_hash and slug = p_slug
  ) into vote_exists;

  if p_action = 'add' then
    result_liked := true;
    if not vote_exists then
      insert into public.like_voters (ip_hash, slug) values (p_ip_hash, p_slug);
      delta := 1;
    end if;
  elsif p_action = 'remove' then
    result_liked := false;
    if vote_exists then
      delete from public.like_voters where ip_hash = p_ip_hash and slug = p_slug;
      delta := -1;
    end if;
  else
    raise exception 'invalid action';
  end if;

  if delta <> 0 then
    insert into public.likes (slug, count, updated_at)
    values (p_slug, greatest(0, delta), now())
    on conflict (slug) do update
      set count = greatest(0, public.likes.count + delta), updated_at = now();
  end if;

  select coalesce(l.count, 0) into result_count from (select 1) as seed
  left join public.likes l on l.slug = p_slug;
  return query select result_liked, result_count;
end;
$$;

revoke all on function public.toggle_like(text, text, text) from public, anon, authenticated;
grant execute on function public.toggle_like(text, text, text) to service_role;

-- Homepage traffic is tracked separately and should not displace articles in rankings.
create or replace function public.top_articles(days int default 7, lim int default 5)
returns table (slug text, views bigint, likes int)
language sql stable
as $$
  select v.slug, count(*)::bigint as views, coalesce(l.count, 0) as likes
  from public.views v
  left join public.likes l on l.slug = v.slug
  where v.ts > now() - make_interval(days => days)
    and v.slug <> '_index'
  group by v.slug, l.count
  order by views desc, likes desc
  limit lim;
$$;
