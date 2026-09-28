"""
Step 4: play with the storyteller you trained in step 3.
第 4 步：和你在第 3 步训练好的“讲故事模型”一起玩。

Run / 运行:   python 4_write_stories.py      (or: python 4_write_stories.py shakespeare / my_text)

What you can type / 可以输入：
    Tom found a magic box       -> it continues your story / 接着你的开头写故事
    (just press Enter)          -> starts with "Once upon a time" / 直接回车，从 "Once upon a time" 开始
    t=1.5                       -> change the temperature / 修改温度
    ? The cat sat on the m      -> show its top guesses for the NEXT character / 看它对下一个字符的前几个猜测
    q                           -> quit / 退出
"""
import sys

import torch
from torch.nn import functional as F

from gpt_model import TinyGPT

DATASET = sys.argv[1].removesuffix(".txt") if len(sys.argv) > 1 else "stories"
device = "cuda" if torch.cuda.is_available() else "cpu"
ckpt = torch.load(f"storyteller_{DATASET}.pt", map_location=device)
chars = ckpt["chars"]
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
model = TinyGPT(len(chars), block_size=ckpt["block"]).to(device)
model.load_state_dict(ckpt["model"])
model.eval()
END = ckpt.get("end", "~")
temperature = 0.8


def encode(s):
    unknown = sorted({c for c in s if c not in stoi})
    if unknown:
        print(f"  (skipping characters it never saw / 跳过它没见过的字符: {''.join(unknown)})")
    return [stoi[c] for c in s if c in stoi]


def write(start, length=600):
    ids = encode(start) or [stoi["\n"]]
    out = model.generate(torch.tensor([ids], device=device), length, temperature=temperature, stop=stoi.get(END))
    return "".join(itos[i] for i in out[0].tolist()).replace(END, "").strip()


def next_char_guesses(start):
    """The model's probabilities for the very next character (Episode 3: it's all next-word prediction!).
    模型对下一个字符的概率（第 3 集：一切都是在预测下一个词！）"""
    ids = encode(start)
    with torch.no_grad():
        logits, _ = model(torch.tensor([ids[-ckpt['block']:]], device=device))
    probs = F.softmax(logits[0, -1] / temperature, dim=-1)
    top = torch.topk(probs, 5)
    for p, i in zip(top.values.tolist(), top.indices.tolist()):
        c = {" ": "(space)", "\n": "(new line)"}.get(itos[i], itos[i])
        print(f"   {c:<11} {'█' * round(p * 40):<40} {p:6.1%}")


print("What you can type" + __doc__.split("What you can type")[1])
while True:
    try:
        cmd = input(f"\n[temperature {temperature}] Your start / 你的开头 > ")
    except (EOFError, KeyboardInterrupt):
        break
    if cmd.strip().lower() == "q":
        break
    if cmd.startswith("t="):
        temperature = max(0.1, float(cmd[2:]))
        print(f"   temperature is now {temperature} / 温度现在是 {temperature}")
        continue
    if cmd.startswith("?"):
        next_char_guesses(cmd[1:].lstrip())
        continue
    print()
    default_start = {"stories": "Once upon a time", "shakespeare": "ROMEO:"}.get(DATASET, "")
    print(write(cmd if cmd.strip() else default_start))
