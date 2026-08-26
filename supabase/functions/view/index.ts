// supabase/functions/view/index.ts
// Records a page view. Dedupes by IP+slug within 30 min.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const IP_SALT = Deno.env.get("SUPABASE_IP_SALT") ?? "fallback-salt";

const SLUG_RE = /^[a-z0-9][a-z0-9-]{0,80}$/i;
const DEDUP_WINDOW_MIN = 30;

async function hashString(s: string): Promise<string> {
  const buf = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(s),
  );
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function getClientIp(req: Request): string {
  const xff = req.headers.get("x-forwarded-for");
  if (xff) return xff.split(",")[0].trim();
  return req.headers.get("x-real-ip") ?? "0.0.0.0";
}

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("method not allowed", { status: 405 });
  }

  let body: { slug?: string; lang?: string };
  try {
    body = await req.json();
  } catch {
    return new Response("invalid json", { status: 400 });
  }

  const slug = (body.slug ?? "").trim();
  const lang = body.lang ?? "bi";
  if (!SLUG_RE.test(slug)) {
    return new Response("invalid slug", { status: 400 });
  }
  if (!["zh", "en", "bi"].includes(lang)) {
    return new Response("invalid lang", { status: 400 });
  }

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, {
    auth: { persistSession: false },
  });

  const ip = getClientIp(req);
  const ipHash = await hashString(ip + IP_SALT);
  const ua = req.headers.get("user-agent") ?? "";
  const uaHash = ua ? await hashString(ua + IP_SALT) : null;

  // Dedup: most recent view from same ip+slug within window?
  const since = new Date(
    Date.now() - DEDUP_WINDOW_MIN * 60 * 1000,
  ).toISOString();
  const { data: recent } = await supabase
    .from("views")
    .select("id")
    .eq("slug", slug)
    .eq("ip_hash", ipHash)
    .gte("ts", since)
    .limit(1)
    .maybeSingle();

  if (recent) {
    return new Response(null, { status: 204 });
  }

  const { error } = await supabase.from("views").insert({
    slug,
    ip_hash: ipHash,
    ua_hash: uaHash,
    lang,
  });

  if (error) {
    return new Response(error.message, { status: 500 });
  }

  return new Response(null, { status: 204 });
});
