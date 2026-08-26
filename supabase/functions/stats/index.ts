// supabase/functions/stats/index.ts
// Aggregated stats for the homepage sidebar. GET-only.
// type=top | daily | site

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("PROJECT_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SERVICE_ROLE_KEY")!;

const CORS_HEADERS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, OPTIONS",
  "access-control-allow-headers":
    "authorization, content-type, apikey, x-client-info",
  "access-control-max-age": "86400",
};

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "cache-control": "public, max-age=300",
      ...CORS_HEADERS,
    },
  });
}

function clampInt(v: string | null, def: number, min: number, max: number) {
  const n = parseInt(v ?? "", 10);
  if (Number.isNaN(n)) return def;
  return Math.min(max, Math.max(min, n));
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  if (req.method !== "GET") {
    return jsonResponse({ error: "method not allowed" }, 405);
  }

  const url = new URL(req.url);
  const type = url.searchParams.get("type") ?? "site";

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, {
    auth: { persistSession: false },
  });

  if (type === "top") {
    const days = clampInt(url.searchParams.get("days"), 7, 1, 90);
    const lim = clampInt(url.searchParams.get("limit"), 5, 1, 20);
    const { data, error } = await supabase.rpc("top_articles", {
      days,
      lim,
    });
    if (error) return jsonResponse({ error: error.message }, 500);
    return jsonResponse({ type: "top", days, items: data ?? [] });
  }

  if (type === "daily") {
    const days = clampInt(url.searchParams.get("days"), 30, 1, 365);
    const { data, error } = await supabase.rpc("daily_stats", { days });
    if (error) return jsonResponse({ error: error.message }, 500);
    return jsonResponse({ type: "daily", days, items: data ?? [] });
  }

  if (type === "site") {
    const { data, error } = await supabase.rpc("site_totals");
    if (error) return jsonResponse({ error: error.message }, 500);
    return jsonResponse({ type: "site", totals: data?.[0] ?? {} });
  }

  return jsonResponse({ error: "unknown type" }, 400);
});
