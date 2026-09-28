# AI Explained #22 · Hands-on: Train Your Own AI / 动手篇：训练你自己的 AI

Start here / 从这里开始: **[教程_Guide.md](教程_Guide.md)** (step-by-step guide / 分步教程)

| Step | Script | What it does | Time on an RTX 5070 Ti |
|---|---|---|---|
| 0 | `0_check_setup.py` | check Python, PyTorch, GPU | seconds |
| 1 | `1_train_digits.py` | train a digit-reading network on MNIST (97.6%) | ~30 s |
| 2 | `2_draw_digit.py` | draw digits with the mouse, the model guesses | — |
| 3 | `3_train_storyteller.py` | train a 10.8M-parameter character-level GPT on TinyStories | ~3 min |
| 4 | `4_write_stories.py` | write stories, change temperature, peek at next-character probabilities | — |

`gpt_model.py` is the Transformer itself (~80 lines). `参考结果_reference/` holds real outputs from our test run.
No NVIDIA GPU? Everything still runs on the CPU, just slower (step 3 takes much longer; the guide explains how to shorten it).

All scripts were run end to end in Sept 2026 (Python 3.14, torch 2.11.0+cu128), including the Shakespeare, custom-text and CNN challenges.
Data: MNIST; TinyStories (Eldan & Li, 2023); Tiny Shakespeare (Karpathy). Model design follows nanoGPT.
