# StudyCrew

Link-based web app that matches high school students studying the same chapter into groups of 3–4. The one-page plan: `../../product-idea-to-plan/示例方案_Example_StudyCrew.md` (copy it into your repo as PLAN.md).

## Run
- `npm test`: unit tests (Node's built-in test runner, nothing to install)
- `npm install`, `cp .dev.vars.example .dev.vars`, `npm run db:init:local`, `npm run dev`: local site at http://localhost:8787
- Deploy: push to main (CI runs the tests, then deploys), or `npm run deploy`

## Rules
- Plain HTML/CSS/JS in `public/`; server code in `src/worker.js`; pure logic in `src/match.js` (keep it pure and tested).
- Validate every input on the server (`validateSignup`). Show user text with `textContent`, never `innerHTML`.
- Verify the Turnstile token on the server before accepting a sign-up.
- Collect only first name, class, subject, chapter and free times. No ratings, no feeds, no strangers.
- Secrets only via `wrangler secret put` or `.dev.vars` (never committed).

## Traps
- A failing test means the code is wrong: never weaken a test to make it pass.
- Replace `database_id` in `wrangler.jsonc` after `npx wrangler d1 create studycrew`.
