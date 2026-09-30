# Vibe Coding Explained #12 · Hands-On: Build and Ship StudyCrew
# AI 编程入门 第 12 集 · 动手篇：把 StudyCrew 做出来并上线

Build StudyCrew, the product planned in [`../product-idea-to-plan/`](../product-idea-to-plan/) (Product Explained #17), with an AI coding agent, and put it online on Cloudflare.
和 AI 编程智能体一起，把产品系列第 17 集规划的 StudyCrew 做出来，并放到 Cloudflare 上线。

| File / 文件 | What / 内容 |
|---|---|
| [`教程_Guide.md`](教程_Guide.md) | Step-by-step guide: what to ask your agent, what to check yourself, which episode explains it 分步教程 |
| [`studycrew/`](studycrew/) | The finished reference app: page, Cloudflare Worker, D1 database schema, Turnstile bot check, 10 tests, CI/CD workflow, CLAUDE.md 完整参考代码 |
| [`参考结果_reference/`](参考结果_reference/) | Screenshots of the app running locally (sign-up form and "Your crew") 本地运行截图 |

**You need / 你需要:** Node.js 22+, Git, a GitHub account, a free Cloudflare account, and a coding agent (e.g. Claude Code or Codex).

**Try the reference app / 试运行参考版本:**
```
cd studycrew
npm test                        # 10 unit tests, no install needed
npm install
cp .dev.vars.example .dev.vars  # Turnstile test secret for local use
npm run db:init:local
npm run dev                     # http://localhost:8787
```

Checked in September 2026 on Windows (Node 24, Wrangler 4): all 10 tests pass, and a local end-to-end run works (four students on the same chapter and time form one crew, the fifth starts a new one, `<script>` names are refused, a missing bot check is blocked). Deploying needs your own Cloudflare account, keys and D1 database: see section 5 of the guide.
2026 年 9 月在 Windows 上验证过（Node 24、Wrangler 4）：10 个测试全部通过，本地端到端运行正常。部署需要你自己的 Cloudflare 账号、密钥和 D1 数据库，见教程第 5 节。

Why Cloudflare Workers and not Pages? In 2026 Cloudflare recommends Workers (with static assets) for new projects; Pages still works, but new features go to Workers.
为什么用 Workers 而不是 Pages？2026 年 Cloudflare 推荐新项目使用 Workers；Pages 仍可用，但新功能都放在 Workers 上。

Note: `studycrew/.github/workflows/ci.yml` runs when `studycrew/` is the root of your own repository.
注：`studycrew/.github/workflows/ci.yml` 需要 `studycrew/` 作为你自己仓库的根目录时才会运行。

Free-plan limits and prices change; check them before you pay. Education only.
免费额度和价格会变，付费前先确认。仅供学习。
