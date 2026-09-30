# StudyCrew (reference version) · StudyCrew 参考版本

The finished example for Vibe Coding Explained, episode 12. It matches high school students studying the same chapter into crews of 3–4 with a shared free time. Planned in Product Explained, episode 17.
Vibe Coding 系列第 12 集的完整示例：把复习同一章、时间都有空的高中生分成 3–4 人的小组。产品方案见产品系列第 17 集。

**Step-by-step guide 分步教程:** [`../教程_Guide.md`](../教程_Guide.md)

## Files 文件
| Path | What |
|---|---|
| `public/` | the page: `index.html`, `style.css`, `app.js` (static, served free by Workers) |
| `src/match.js` | pure matching + input validation (tested) |
| `src/worker.js` | Cloudflare Worker: `/api/join`, `/api/crew`, `/api/config`, daily cleanup cron |
| `schema.sql` | D1 tables |
| `test/match.test.js` | 10 unit tests, including edge cases |
| `wrangler.jsonc` | Workers config (static assets + D1 + cron) |
| `.github/workflows/ci.yml` | CI: tests on every PR/push; CD: deploy main |
| `CLAUDE.md` | memory file for coding agents |

## Run 运行
```
npm test                       # unit tests, no install needed
npm install
cp .dev.vars.example .dev.vars
npm run db:init:local
npm run dev                    # http://localhost:8787
```
Deploy: see the guide, section 5. 部署步骤见教程第 5 节。

## Verified 已验证 (2026-09-30)
- `npm test`: 10/10 passing (Node 24).
- Local end-to-end with `wrangler dev` 4.x and Turnstile test keys: four sign-ups with the same chapter and time form one crew; the fifth starts a new crew; `<script>` names are rejected; missing Turnstile token → 403; unknown key → 404.
- Not deployed to a real Cloudflare account (that needs your own account, keys and D1 database ID).

## Known limits 已知局限
- Two sign-ups at the same instant could both join a group with 3 members, making 5. Fine for a class; a later version could use a transaction or Durable Object.
- The place is one fixed setting (`PLACE`); groups don't pick rooms.
- English/Chinese labels only.

Education only. 仅供学习。
