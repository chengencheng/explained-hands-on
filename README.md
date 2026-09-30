# Cheng Academy · 程氏学堂 — Hands-on / 动手篇

Code and step-by-step guides for the hands-on episodes of four bilingual video series from **Cheng Academy · 程氏学堂** (English narration, English + Chinese subtitles):

**程氏学堂**四个双语视频系列（英文配音，中英双语字幕）“动手篇”的代码和分步教程：

| Folder / 文件夹 | Series / 系列 | What you do / 你会做什么 | Time / 时间 |
|---|---|---|---|
| [`ai-train-your-own-ai/`](ai-train-your-own-ai/) | **AI Explained** #22 | Train a digit-reading neural network and a tiny story-writing GPT on your own computer. 在自己的电脑上训练认手写数字的神经网络，和会写英文小故事的迷你 GPT。 | ~1 hour |
| [`investing-check-the-numbers/`](investing-check-the-numbers/) | **Investing Explained** #18 | Use pandas and real market history to check the numbers from the investing videos yourself. 用 pandas 和真实的市场历史，亲手验证投资系列里的数字。 | ~1-1.5 hours |
| [`product-idea-to-plan/`](product-idea-to-plan/) | **Product Explained** #17 | Turn one idea into a one-page product plan (template + worked example). No coding. 把一个想法变成一页纸产品方案（模板 + 完整示例），不需要写代码。 | ~1-2 hours |
| [`vibe-coding-build-studycrew/`](vibe-coding-build-studycrew/) | **Vibe Coding Explained** #12 | Build that plan (StudyCrew) with an AI coding agent and put it online on Cloudflare. 和 AI 编程智能体一起把这个方案（StudyCrew）做出来，放到 Cloudflare 上线。 | ~2-3 hours |

**Start here / 从这里开始:** open the folder, then its `教程_Guide.md` (guides in Chinese or bilingual, code comments in English and Chinese).
打开文件夹，然后看里面的 `教程_Guide.md`（教程为中文或中英双语，代码注释中英双语）。

## Quick start / 快速开始

For the AI and Investing folders / AI 和投资两个文件夹：

1. Install [Python](https://www.python.org/downloads/) 3.10 or newer. 安装 Python 3.10 或更高版本。
2. Click **Code → Download ZIP** on this page and unzip it (or `git clone`). 点本页的 **Code → Download ZIP** 并解压。
3. Open a terminal in one of those folders and follow `教程_Guide.md`. 在其中一个文件夹里打开终端，按 `教程_Guide.md` 操作。

The guides were written for Windows (PowerShell). On macOS or Linux, activate the virtual environment with `source .venv/bin/activate` instead.
教程以 Windows（PowerShell）为例；在 macOS 或 Linux 上，用 `source .venv/bin/activate` 激活虚拟环境。

The Product folder needs nothing to install. The Vibe Coding folder needs [Node.js](https://nodejs.org/) 22+, Git and a free Cloudflare account; see its README.
产品文件夹不需要安装任何东西；编程文件夹需要 Node.js 22+、Git 和免费的 Cloudflare 账号，详见其 README。

Every script was run end to end in September 2026 (Python 3.14; StudyCrew: Node 24, Wrangler 4). Real outputs are in each folder's `参考结果_reference/`, so you can compare your results.
所有程序都在 2026 年 9 月完整运行过（Python 3.14），真实输出放在各自的 `参考结果_reference/` 里，可以和你的结果对比。

## Data / 数据

- **AI:** MNIST (downloaded by torchvision), [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories) (Eldan & Li, 2023) and [Tiny Shakespeare](https://github.com/karpathy/char-rnn) are downloaded when you run the scripts. The mini GPT follows the design of [nanoGPT](https://github.com/karpathy/nanoGPT).
- **Investing:** yearly U.S. returns 1928-2025 from [Prof. Aswath Damodaran](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html) (NYU Stern) are included. Daily index prices (S&P 500, S&P 500 total return, Shanghai Composite, Nikkei 225) are downloaded from Yahoo Finance by `0_check_setup.py`, up to Sept 25 2026 so your numbers match the guide exactly.

## License / 许可

Code: [MIT](LICENSE). Data belongs to its original sources listed above.

Education only, not investment, tax or legal advice. Past returns do not guarantee future returns.
仅供学习，不构成投资、税务或法律建议。过去的回报不代表未来。
