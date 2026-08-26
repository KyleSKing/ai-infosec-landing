// supabase/functions/like/index.ts
// Toggles like on a post. Requires anon JWT (browser sends it).
// IP-hash dedup via x-forwarded-for.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("PROJECT_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SERVICE_ROLE_KEY")!;
const IP_SALT = Deno.env.get("IP_SALT") ?? "fallback-salt";

const SLUG_RE = /^[a-z0-9][a-z0-9-]{0,80}$/i;

const CORS_HEADERS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers":
    "authorization, content-type, apikey, x-client-info",
  "access-control-max-age": "86400",
};

async function hashIp(ip: string): Promise<string> {
  const data = new TextEncoder().encode(ip + IP_SALT);
  const buf = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function getClientIp(req: Request): string {
  const xff = req.headers.get("x-forwarded-for");
  if (xff) return xff.split(",")[0].trim();
  return req.headers.get("x-real-ip") ?? "0.0.0.0";
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...CORS_HEADERS },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  if (req.method !== "POST") {
    return jsonResponse({ error: "method not allowed" }, 405);
  }

  let body: { slug?: string; action?: string };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "invalid json" }, 400);
  }

  const slug = (body.slug ?? "").trim();
  const action = body.action === "remove" ? "remove" : "add";

  if (!SLUG_RE.test(slug)) {
    return jsonResponse({ error: "invalid slug" }, 400);
  }

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, {
    auth: { persistSession: false },
  });

  const ipHash = await hashIp(getClientIp(req));

  // Check current vote state
  const { data: existing } = await supabase
    .from("like_voters")
    .select("ip_hash")
    .eq("ip_hash", ipHash)
    .eq("slug", slug)
    .maybeSingle();

  const hasVote = !!existing;
  let delta = 0;
  let liked: boolean;

  if (action === "add") {
    if (!hasVote) {
      const { error } = await supabase
        .from("like_voters")
        .insert({ ip_hash: ipHash, slug });
      if (error) return jsonResponse({ error: error.message }, 500);
      delta = 1;
      liked = true;
    } else {
      liked = true;
      delta = 0;
    }
  } else {
    if (hasVote) {
      const { error } = await supabase
        .from("like_voters")
        .delete()
        .eq("ip_hash", ipHash)
        .eq("slug", slug);
      if (error) return jsonResponse({ error: error.message }, 500);
      delta = -1;
      liked = false;
    } else {
      liked = false;
      delta = 0;
    }
  }

  if (delta !== 0) {
    // Atomic upsert with increment
    const { data: current } = await supabase
      .from("likes")
      .select("count")
      .eq("slug", slug)
      .maybeSingle();
    const next = Math.max(0, (current?.count ?? 0) + delta);
    const { error: upsertErr } = await supabase
      .from("likes")
      .upsert(
        { slug, count: next, updated_at: new Date().toISOString() },
        { onConflict: "slug" },
      );
    if (upsertErr) return jsonResponse({ error: upsertErr.message }, 500);
  }

  // Read final count
  const { data: final } = await supabase
    .from("likes")
    .select("count")
    .eq("slug", slug)
    .maybeSingle();

  return jsonResponse({
    slug,
    liked,
    count: final?.count ?? 0,
  });
});
