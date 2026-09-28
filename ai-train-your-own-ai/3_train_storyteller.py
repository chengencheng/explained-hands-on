"""
Step 3: train your own tiny GPT from scratch, so it learns to write short stories.
第 3 步：从零训练你自己的迷你 GPT，让它学会写英文小故事。

Training text: TinyStories (Eldan & Li, Microsoft Research, 2023) -- 27,000 simple stories
written for small language models to learn from. The first run downloads about 22 MB.
训练文本：TinyStories（微软研究院，2023）——两万七千个专门给小模型学习的简单小故事。
第一次运行会下载约 22 MB。

Run / 运行:
    python 3_train_storyteller.py               # short stories / 小故事
    python 3_train_storyteller.py shakespeare   # Shakespeare's plays instead / 换成莎士比亚的剧本
    python 3_train_storyteller.py my_text.txt   # any text file of your own (1 MB or more works best) / 用你自己的文本文件
"""
import json
import math
import os
import sys
import time
import urllib.request

import torch

from gpt_model import TinyGPT

CUSTOM = next((a for a in sys.argv[1:] if a.endswith(".txt")), None)
DATASET = "shakespeare" if "shakespeare" in sys.argv else os.path.basename(CUSTOM)[:-4] if CUSTOM else "stories"
device = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(1337)
os.makedirs("data", exist_ok=True)

# ===================================================================
# 1. The data / 数据
# ===================================================================
STORIES_URL = "https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-valid.txt"
SHAKESPEARE_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
END = "~"   # a character that marks "the story is over" / 表示“故事结束”的记号


def load_stories():
    path = "data/TinyStoriesV2-GPT4-valid.txt"
    if not os.path.exists(path):
        print("  downloading TinyStories (22 MB) / 下载 TinyStories（22 MB）...")
        urllib.request.urlretrieve(STORIES_URL, path)
    raw = open(path, encoding="utf-8").read()
    fancy = {"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "…": "..."}
    stories = []
    for s in raw.split("<|endoftext|>"):
        for a, b in fancy.items():
            s = s.replace(a, b)
        s = s.strip()
        if s and s.isascii():            # keep plain English text only / 只保留普通英文字符
            stories.append(s)
    return "".join(s + "\n" + END + "\n" for s in stories)


def load_shakespeare():
    path = "data/shakespeare.txt"
    if not os.path.exists(path):
        urllib.request.urlretrieve(SHAKESPEARE_URL, path)
    return open(path, encoding="utf-8").read()


if DATASET == "stories":
    text = load_stories()
elif DATASET == "shakespeare":
    text = load_shakespeare()
else:
    text = open(CUSTOM, encoding="utf-8").read()
chars = sorted(set(text))                      # every different character = our vocabulary / 所有不同的字符 = 词表
stoi = {c: i for i, c in enumerate(chars)}     # character -> number / 字符 → 编号
itos = {i: c for c, i in stoi.items()}         # number -> character / 编号 → 字符
encode = lambda s: [stoi[c] for c in s]
decode = lambda ids: "".join(itos[i] for i in ids)

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data, val_data = data[:n], data[n:]      # 90% to learn from, 10% kept aside to test / 90% 学习，10% 留作测试
print(f"Dataset / 数据集: {DATASET}   characters / 总字符数: {len(data):,}   vocabulary / 不同的字符: {len(chars)}")
if DATASET == "stories":
    print(f"Stories / 故事数量: {text.count(END):,}")

# ===================================================================
# 2. The model / 模型
# ===================================================================
BLOCK = 256        # how many characters it can look back at (its context window) / 最多往回看多少个字符（上下文窗口）
BATCH = 64         # how many text snippets per training step / 每一步训练看几段文字
STEPS = 5000       # training steps / 训练步数
LR = 1e-3          # learning rate / 学习率

model = TinyGPT(len(chars), block_size=BLOCK).to(device)
print(f"Parameters / 参数个数: {sum(p.numel() for p in model.parameters()):,}")
optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.1)


def get_batch(split):
    """Pick BATCH random snippets. The answers are the same snippets shifted by one character.
    随机取 BATCH 段文字。答案就是同一段文字往后错一个字符。"""
    d = train_data if split == "train" else val_data
    ix = torch.randint(len(d) - BLOCK - 1, (BATCH,))
    x = torch.stack([d[i:i + BLOCK] for i in ix])
    y = torch.stack([d[i + 1:i + BLOCK + 1] for i in ix])
    return x.to(device), y.to(device)


@torch.no_grad()
def estimate_loss():
    model.eval()
    out = {}
    for split in ["train", "val"]:
        losses = [model(*get_batch(split))[1].item() for _ in range(40)]
        out[split] = sum(losses) / len(losses)
    model.train()
    return out


def sample(start, length=400, temperature=0.8):
    idx = torch.tensor([encode(start)], device=device)
    out = model.generate(idx, length, temperature=temperature, stop=stoi.get(END))
    return decode(out[0].tolist()).replace(END, "").strip()


START = {"stories": "Once upon a time", "shakespeare": "ROMEO:"}.get(DATASET, text[:12])
CKPT = f"storyteller_{DATASET}.pt"
best_val, best_step = float("inf"), 0
log = []
print(f"\nTraining for {STEPS} steps on {device} ... / 开始训练 {STEPS} 步 ...\n")
t0 = time.time()
for step in range(STEPS + 1):
    # learning rate: short warm-up, then slowly lower it (cosine schedule) / 学习率：先热身，再慢慢降低
    lr = LR * min(1, (step + 1) / 100) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / STEPS)))
    for g in optimizer.param_groups:
        g["lr"] = lr

    if step % 250 == 0:
        losses = estimate_loss()
        story = sample(START, length=200)
        log.append({"step": step, "train": losses["train"], "val": losses["val"], "seconds": time.time() - t0, "sample": story})
        note = ""
        if losses["val"] < best_val:   # keep the version that does best on text it has NEVER seen / 保存在“没见过的文字”上成绩最好的版本
            best_val, best_step = losses["val"], step
            torch.save({"model": model.state_dict(), "chars": chars, "block": BLOCK, "dataset": DATASET, "end": END}, CKPT)
            note = "   <- best so far, saved / 目前最好，已保存"
        print(f"step {step:5d}   loss: train {losses['train']:.3f}  val {losses['val']:.3f}   ({time.time() - t0:5.0f} s){note}")
        print("   sample / 样例: " + story.replace("\n", " ")[:150] + "\n")
    if step == STEPS:
        break

    x, y = get_batch("train")
    with torch.autocast(device_type=device, dtype=torch.bfloat16, enabled=(device == "cuda")):  # faster math on the GPU / 在显卡上算得更快
        _, loss = model(x, y)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()                                            # backpropagation / 反向传播
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()                                           # nudge all the weights / 微调所有权重

minutes = (time.time() - t0) / 60
print(f"Done in {minutes:.1f} minutes. / 训练完成，用时 {minutes:.1f} 分钟。")
json.dump(log, open(f"training_log_{DATASET}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"Best model: step {best_step}, val loss {best_val:.3f} -> saved in {CKPT} / 最好的模型在第 {best_step} 步，已保存到 {CKPT}")
if log[-1]["val"] > best_val * 1.05:   # clearly worse at the end than at its best / 结尾明显比最好时差
    print("  Note: val loss stopped improving, so the model started memorizing (overfitting). We kept the best version.")
    print("  注意：val 损失后来不降反升，说明模型开始死记硬背（过拟合）。我们保留了最好的那个版本。")
model.load_state_dict(torch.load(CKPT)["model"])

try:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(7, 4))
    plt.plot([r["step"] for r in log], [r["train"] for r in log], label="train")
    plt.plot([r["step"] for r in log], [r["val"] for r in log], label="val (never trained on)")
    plt.xlabel("training step")
    plt.ylabel("loss (lower = better)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"loss_{DATASET}.png", dpi=100)
    print(f"Saved the loss curve to loss_{DATASET}.png / 损失曲线已保存到 loss_{DATASET}.png")
except ImportError:
    pass

print("\nTwo stories from your model / 你的模型写的两个故事:\n")
for s in {"stories": [START, "Tom and his dog"], "shakespeare": ["ROMEO:", "JULIET:"]}.get(DATASET, [START]):
    print(sample(s, length=1000), "\n")
print(f"Next: python 4_write_stories.py {'' if DATASET == 'stories' else DATASET}   / 下一步：运行 4_write_stories.py")
