// StudyCrew server code: a Cloudflare Worker. Static files in public/ are served for free by Workers static assets;
// this code only runs for /api/* requests (see "run_worker_first" in wrangler.jsonc).
import { validateSignup, chooseGroup, newGroupSlot } from "./match.js";

const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const DAY = 24 * 60 * 60 * 1000;

// Ask Cloudflare whether the Turnstile token from the page is real. The server check is the part people forget.
async function verifyTurnstile(token, secret, ip) {
  if (typeof token !== "string" || !token) return false;
  const body = new FormData();
  body.append("secret", secret);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  const out = await res.json();
  return out.success === true;
}

// Members of one group: first names only (the minimum a student needs).
async function crewFor(db, groupId) {
  const group = await db.prepare("SELECT id, subject, chapter, slot, place FROM groups WHERE id = ?").bind(groupId).first();
  const { results } = await db.prepare("SELECT first_name FROM students WHERE group_id = ? ORDER BY created_at").bind(groupId).all();
  return { subject: group.subject, chapter: group.chapter, slot: group.slot, place: group.place, members: results.map(r => r.first_name) };
}

async function join(request, env) {
  let input;
  try { input = await request.json(); } catch { return json({ error: "Invalid request." }, 400); }

  const human = await verifyTurnstile(input.turnstileToken, env.TURNSTILE_SECRET, request.headers.get("CF-Connecting-IP"));
  if (!human) return json({ error: "Bot check failed. Please try again." }, 403);

  const checked = validateSignup(input);
  if (!checked.ok) return json({ error: checked.error }, 400);
  const s = checked.value;

  // Optional class code, so only classmates can join (set CLASS_CODE as a secret to turn it on).
  if (env.CLASS_CODE && input.classCode !== env.CLASS_CODE) return json({ error: "Wrong class code. Ask your class group chat." }, 403);

  // Existing groups for the same subject and chapter, with how many members each has.
  const { results } = await env.DB.prepare(
    "SELECT g.id, g.slot, COUNT(s.id) AS members FROM groups g LEFT JOIN students s ON s.group_id = g.id WHERE g.subject = ? AND g.chapter = ? GROUP BY g.id"
  ).bind(s.subject, s.chapter).all();

  const now = Date.now();
  let group = chooseGroup(results, s.slots);
  if (!group) {
    group = { id: crypto.randomUUID(), slot: newGroupSlot(s.slots) };
    await env.DB.prepare("INSERT INTO groups (id, subject, chapter, slot, place, created_at) VALUES (?, ?, ?, ?, ?, ?)")
      .bind(group.id, s.subject, s.chapter, group.slot, env.PLACE || "Library 2F", now).run();
  }

  // A private key lets this student (and only this student) look up their crew later.
  const key = crypto.randomUUID();
  await env.DB.prepare("INSERT INTO students (id, key, first_name, class_name, subject, chapter, slots, group_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
    .bind(crypto.randomUUID(), key, s.firstName, s.className, s.subject, s.chapter, JSON.stringify(s.slots), group.id, now).run();

  return json({ key, crew: await crewFor(env.DB, group.id) });
}

async function myCrew(url, env) {
  const key = url.searchParams.get("key");
  if (!key) return json({ error: "Missing key." }, 400);
  // Access control: the key decides which crew you may see; there is no way to list other groups.
  const me = await env.DB.prepare("SELECT group_id FROM students WHERE key = ?").bind(key).first();
  if (!me) return json({ error: "Not found." }, 404);
  return json({ crew: await crewFor(env.DB, me.group_id) });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/join" && request.method === "POST") return join(request, env);
    if (url.pathname === "/api/crew" && request.method === "GET") return myCrew(url, env);
    if (url.pathname === "/api/config") return json({ turnstileSiteKey: env.TURNSTILE_SITE_KEY, classCode: !!env.CLASS_CODE });
    if (url.pathname.startsWith("/api/")) return json({ error: "Not found." }, 404);
    return env.ASSETS.fetch(request);
  },

  // Responsibility: keep data only for the test week. Runs daily (see "triggers" in wrangler.jsonc).
  async scheduled(event, env) {
    const cutoff = Date.now() - 14 * DAY;
    await env.DB.prepare("DELETE FROM students WHERE created_at < ?").bind(cutoff).run();
    await env.DB.prepare("DELETE FROM groups WHERE created_at < ? AND id NOT IN (SELECT group_id FROM students)").bind(cutoff).run();
  },
};
