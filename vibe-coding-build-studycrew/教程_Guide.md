# Hands-On: Build and Ship StudyCrew with an AI Agent
# 动手篇：和 AI 智能体一起把 StudyCrew 做出来并上线

Vibe Coding Explained · 第 12 集配套教程 · Sept 2026

This guide walks you through building StudyCrew, the product planned in the Product series (episode 17), and putting it online for real. Each step lists **what to ask your agent**, **what to check yourself**, and **which episode explains it**. A finished version is in [`studycrew/`](studycrew/), so you can compare your result or start from it.
这份教程带你把产品系列第 17 集规划的 StudyCrew 真正做出来并上线。每一步都写明：**对智能体说什么**、**你自己要检查什么**、**对应哪一集**。完整的参考版本在 [`studycrew/`](studycrew/) 文件夹里，你可以对照，也可以直接从它开始。

---

## 0 · What you're building 你要做的是什么

A link that opens inside the class group chat. A student enters first name, class, subject, chapter and free times, and gets: **"Your crew: Tue 4 pm · Library 2F, with Leo and Sara."** Groups have 3–4 people on the same chapter with a shared free time.
一个在班级群里直接打开的链接。学生填写名字、班级、科目、章节和空闲时间，就会收到：**"你的小组：周二下午 4 点 · 图书馆 2 楼，和 Leo、Sara 一起。"** 每组 3 到 4 人，复习同一章，时间都有空。

| Part 部分 | Choice 选择 | Episode 集 |
|---|---|---|
| Page 页面 | plain HTML, CSS, JavaScript (static files) | 07 |
| Server code 服务器代码 | one Cloudflare Worker | 07, 08 |
| Data 数据 | Cloudflare D1 (a small SQL database) | 07 |
| Bot check 机器人检查 | Cloudflare Turnstile, verified on the server | 09 |
| Tests 测试 | Node's built-in test runner | 11 |
| CI/CD | GitHub Actions: test every change, deploy main | 10 |

Why Workers and not Pages? In 2026 Cloudflare recommends Workers (with static assets) for new projects; Pages still works, but new features go to Workers (episode 07).
为什么用 Workers 而不是 Pages？2026 年，Cloudflare 推荐新项目使用 Workers（带静态资源）；Pages 依然能用，但新功能都放在 Workers 上（第 7 集）。

**Cost 花费:** free for a class-sized project (Workers Free: static files free and unlimited, 100,000 server requests a day; D1 and Turnstile have free tiers). A custom domain is optional, about $10–20 a year. Check current limits before you start.
一个班级规模的项目是免费的（Workers 免费版：静态文件免费不限量，每天 10 万次服务器请求；D1 和 Turnstile 都有免费额度）。自定义域名可选，每年约 10–20 美元。开始之前先查一下最新的额度。

---

## 1 · Get ready 准备（episodes 02, 04, 05）

You need 你需要:
- a computer with **Node.js 22+** and **Git** 装好 Node.js 22 以上版本和 Git 的电脑
- a **GitHub** account (turn on two-factor sign-in) GitHub 账号（打开双重验证）
- a free **Cloudflare** account 免费的 Cloudflare 账号
- a coding agent, e.g. **Claude Code**, **Codex**, or another you like 一个编程智能体，比如 Claude Code、Codex 或你喜欢的其他工具

```
mkdir studycrew && cd studycrew
git init
```

Copy the one-page plan ([`../product-idea-to-plan/示例方案_Example_StudyCrew.md`](../product-idea-to-plan/示例方案_Example_StudyCrew.md), from Product Explained #17) into the folder as `PLAN.md`.
把一页纸方案（产品系列第 17 集的示例方案，见上面的链接）复制进文件夹，命名为 `PLAN.md`。

---

## 2 · Plan with the agent 和智能体一起计划（episode 03）

**Ask 对智能体说:**
> Read PLAN.md. We're building version 1 of StudyCrew: a mobile web page plus a Cloudflare Worker with a D1 database and Turnstile. Interview me about anything unclear, then write SPEC.md: pages, API endpoints, database tables, matching rules, what data we keep and for how long, and what's out of scope (no accounts, no payments, no ratings). End the spec with how we'll test it.

**Check yourself 自己检查:**
- Does SPEC.md collect only first name, class, subject, chapter and free times? 规格里是否只收集名字、班级、科目、章节和空闲时间？
- Is "delete data after the test week" in it? 有没有写"考试周后删除数据"？
- Is anything out of scope written down? 有没有写清楚哪些不做？

Then ask it to write a short **CLAUDE.md** (or **AGENTS.md**): how to run, the rules, the traps. See [`studycrew/CLAUDE.md`](studycrew/CLAUDE.md). Commit. 然后让它写一个简短的记忆文件，提交一次。

---

## 3 · Build in small steps 小步来做（episodes 03, 04, 11）

Do one step per request. After each step: run the check, read the diff, **commit**.
一次只做一步。每一步之后：运行检查、读 diff、**提交**。

**Step A · the matching logic, tests first 先写测试**
> Write test/match.test.js for a pure function chooseGroup(groups, slots) and validateSignup(input), following SPEC.md. Include edge cases: empty name, a 500-character name, a script in the name, a full group of 4, no shared time, and 200 students at once. Then write src/match.js until `npm test` passes. Don't change the tests to make them pass.

Check: `npm test` is green, and no test was weakened. 检查：测试全绿，没有测试被削弱。

**Step B · the page 页面**
> Build public/index.html, style.css and app.js: a phone-first form (first name, class, subject, chapter, free-time checkboxes) and a "Your crew" view. Show user text with textContent, never innerHTML.

Check on a narrow window (or your phone). 用窄窗口或手机看一看。

**Step C · the server and database 服务器和数据库**
> Create src/worker.js for Cloudflare Workers with static assets: POST /api/join (validate on the server, match, store in D1, return the crew and a private key), GET /api/crew?key=… (only that student's crew), and a daily cron that deletes rows older than 14 days. Add schema.sql and wrangler.jsonc.

**Step D · the bot check 机器人检查（episode 09）**
> Add Cloudflare Turnstile: render the widget on the page, send the token with the form, and verify it on the server with the Siteverify API before accepting a sign-up. Use Turnstile's test keys for local development.

---

## 4 · Test it locally 在本地测试（episodes 06, 11）

```
npm install
cp .dev.vars.example .dev.vars      # Turnstile test secret, never committed
npx wrangler d1 create studycrew    # copy the database_id into wrangler.jsonc
npm run db:init:local
npm run dev                         # http://localhost:8787
```

Try 试一试:
- Sign up four people with the same chapter and time: they should land in one crew. 用同一章、同一时间报四个人：应该分在同一个小组。
- A fifth person gets a new crew. 第五个人会被分到新小组。
- A name like `<script>` is refused. 名字写成 `<script>` 会被拒绝。
- Open the browser's developer tools → Network: every request should be 200, or a clear error. 打开开发者工具 → Network：每个请求都应是 200，或者一个清楚的错误。

If something breaks, give the agent the exact error, the steps, and what you expected (episode 11).
出问题时，把确切的错误信息、重现步骤和期望结果交给智能体（第 11 集）。

---

## 5 · Ship it 上线（episodes 05, 07, 09, 10）

1. **GitHub:** create a private repo, `git push`. Turn on branch protection for main with the CI check required. 创建私有仓库并推送；为 main 打开分支保护，要求 CI 检查通过。
2. **Turnstile:** in the Cloudflare dashboard, create a Turnstile widget for your domain. Put the **site key** in `wrangler.jsonc`, and the **secret** as a secret: 在 Cloudflare 后台创建 Turnstile 组件；站点密钥写进配置，私密密钥存成机密：
   ```
   npx wrangler secret put TURNSTILE_SECRET
   ```
3. **Database:** `npm run db:init` (creates the tables in the real D1). 在正式的 D1 里建表。
4. **Deploy:** `npm run deploy`, and you get `https://studycrew.<your-account>.workers.dev`. 部署后得到一个 workers.dev 网址。
5. **CI/CD:** add two GitHub secrets, `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. The workflow in `.github/workflows/ci.yml` (it runs when `studycrew/` is the root of your own repo) then tests every pull request and deploys main automatically. 在 GitHub 添加两个机密后，工作流会测试每个拉取请求，并自动部署 main。
6. **Domain (optional):** buy one, add it in Cloudflare, attach it to the Worker. The certificate is automatic. 自定义域名（可选）：购买后在 Cloudflare 里添加并绑定到 Worker，证书自动申请。
7. **Open it on your phone.** Check the lock, try the form, look at the small screen (episode 07). 用手机打开：检查那把锁、试表单、看小屏幕效果。

---

## 6 · Before real students use it 真正给同学用之前（episodes 09, Product 16）

- Ask the agent for a **security review** (e.g. `/security-review` in Claude Code), and read what it finds. 让智能体做一次安全审查，并读一读它发现了什么。
- Optional **class code**: `npx wrangler secret put CLASS_CODE`, so only classmates can join. 可选的班级口令，只让同学加入。
- Share the link **only** in the class group chat. 只在班级群里分享链接。
- Tell students what you keep and when it's deleted (the page already says so). 告诉同学你保存什么、什么时候删除（页面上已经写了）。
- No public ratings, no feeds, no strangers. 不公开打分、不做信息流、不让陌生人加入。

---

## 7 · After launch 上线之后（Product episodes 06, 12）

Watch the North Star: **study sessions that actually happen each week**, not sign-ups. After each session ask: "Was it useful? Coming next time?" Write down repeated questions for version 2.
盯住北极星指标：**每周真正发生的复习次数**，而不是报名人数。每次复习后问一句："有用吗？下次还来吗？"把大家反复问的问题记下来，准备第二版。

---

## Checklist 检查清单

- [ ] SPEC.md and CLAUDE.md written, committed 规格说明和记忆文件已写好并提交
- [ ] `npm test` green; edge cases covered; no weakened tests 测试全绿，覆盖边界情况，没有削弱测试
- [ ] Input validated on the server; text shown with textContent 服务器校验输入；用 textContent 显示文字
- [ ] Turnstile token verified on the server 服务器核验 Turnstile 令牌
- [ ] Secrets only in `wrangler secret` / GitHub secrets / `.dev.vars` 机密只放在机密存储里
- [ ] CI required on main; deploy on merge main 分支要求 CI 通过；合并即部署
- [ ] Data deleted after 14 days (cron) 14 天后删除数据（定时任务）
- [ ] Tested on a real phone 在真实手机上测试过

*Education only. Prices and limits change: check before you pay. 仅供学习。价格和额度会变，付费前先确认。*
