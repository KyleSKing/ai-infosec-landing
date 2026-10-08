// supabase/functions/like/index.ts
// Toggles like on a post. Requires anon JWT (browser sends it).
// IP-hash dedup via x-forwarded-for.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
const IP_SALT = Deno.env.get("SUPABASE_IP_SALT");

const SLUG_RE = /^[a-z0-9][a-z0-9-]{0,80}$/i;

const CORS_HEADERS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers":
    "authorization, content-type, apikey, x-client-info",
  "access-control-max-age": "86400",
};

async function hashIp(ip: string, salt: string): Promise<string> {
  const data = new TextEncoder().encode(ip + salt);
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
  if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY || !IP_SALT) {
    return jsonResponse({ error: "server configuration missing" }, 500);
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

  const ipHash = await hashIp(getClientIp(req), IP_SALT);

  const { data, error } = await supabase.rpc("toggle_like", {
    p_slug: slug,
    p_ip_hash: ipHash,
    p_action: action,
  }).single();
  if (error) return jsonResponse({ error: error.message }, 500);

  return jsonResponse({
    slug,
    liked: data.liked,
    count: data.count,
  });
});
