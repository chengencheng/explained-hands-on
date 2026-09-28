"""
Step 2: draw your own digit with the mouse and let your model guess it.
第 2 步：用鼠标写一个数字，让你刚训练好的模型来猜。

Needs digits_model.pt from step 1.  需要第 1 步生成的 digits_model.pt。
Run / 运行:   python 2_draw_digit.py
"""
import sys
import tkinter as tk

import torch
from PIL import Image, ImageDraw, ImageFilter
from torch import nn

SIZE = 280    # drawing area in screen pixels (10x the 28-pixel MNIST pictures) / 画板大小
BRUSH = 22    # brush thickness / 笔刷粗细

# The same network shape as in step 1, then load the trained weights.
# 和第 1 步一模一样的网络结构，再装上训练好的权重。
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 128), nn.ReLU(),
    nn.Linear(128, 64), nn.ReLU(),
    nn.Linear(64, 10),
)
model.load_state_dict(torch.load("digits_model.pt", map_location="cpu"))
model.eval()


def to_mnist(img):
    """Make a drawing look like an MNIST picture: 28x28, digit about 20x20, centered, a little blurry.
    把画的图变成 MNIST 的样子：28×28，数字约 20×20 居中，稍微模糊一点。"""
    box = img.getbbox()
    if box is None:
        return None
    digit = img.crop(box)
    w, h = digit.size
    scale = 20 / max(w, h)
    digit = digit.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    x = torch.frombuffer(bytearray(digit.tobytes()), dtype=torch.uint8).float().view(digit.height, digit.width) / 255
    # MNIST digits are centered by their "center of mass", so we do the same / MNIST 按“重心”居中，我们也一样
    ys, xs = torch.meshgrid(torch.arange(digit.height), torch.arange(digit.width), indexing="ij")
    cy, cx = (x * ys).sum() / x.sum(), (x * xs).sum() / x.sum()
    canvas = Image.new("L", (28, 28), 0)
    canvas.paste(digit, (round(14 - cx.item()), round(14 - cy.item())))
    canvas = canvas.filter(ImageFilter.GaussianBlur(0.5))
    return torch.frombuffer(bytearray(canvas.tobytes()), dtype=torch.uint8).float().view(1, 1, 28, 28) / 255


def guess(img):
    x = to_mnist(img)
    if x is None:
        return None
    with torch.no_grad():
        return torch.softmax(model(x), dim=1)[0]   # 10 probabilities that add up to 1 / 加起来等于 1 的 10 个概率


def self_test():
    """Draw a 1 and a 7 with code (no mouse) to check everything works. / 用代码画 1 和 7，检查能不能用。"""
    for name, lines in [("1", [(140, 40, 140, 240)]), ("7", [(70, 50, 210, 50), (210, 50, 110, 240)])]:
        img = Image.new("L", (SIZE, SIZE), 0)
        d = ImageDraw.Draw(img)
        for ln in lines:
            d.line(ln, fill=255, width=BRUSH)
        p = guess(img)
        print(f"drew a {name} -> model says {p.argmax().item()} ({p.max().item():.0%} sure)")


if "--selftest" in sys.argv:
    self_test()
    sys.exit()

# ---------------- the window / 窗口 ----------------
root = tk.Tk()
root.title("Draw a digit 0-9 / 写一个 0 到 9 的数字")
board = tk.Canvas(root, width=SIZE, height=SIZE, bg="black", cursor="pencil")
board.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
image = Image.new("L", (SIZE, SIZE), 0)       # an invisible copy of the drawing that we give to the model
pen = ImageDraw.Draw(image)
result = tk.Label(root, text="Draw with the mouse, then click Guess\n用鼠标写一个数字，再点“猜一猜”",
                  font=("Microsoft YaHei", 14), justify="left")
result.grid(row=0, column=2, padx=10, sticky="n")
last = [None]


def draw(event):
    x, y = event.x, event.y
    if last[0]:
        board.create_line(*last[0], x, y, fill="white", width=BRUSH, capstyle="round", smooth=True)
        pen.line([*last[0], x, y], fill=255, width=BRUSH)
    pen.ellipse([x - BRUSH / 2, y - BRUSH / 2, x + BRUSH / 2, y + BRUSH / 2], fill=255)
    last[0] = (x, y)


def lift(event):
    last[0] = None


def on_guess():
    p = guess(image)
    if p is None:
        result.config(text="Draw something first!\n先写一个数字！")
        return
    best = p.argmax().item()
    bars = "\n".join(f"{d}: {'█' * round(p[d].item() * 20):<20} {p[d].item():5.1%}" for d in range(10))
    result.config(text=f"I think it's a {best}  ({p[best].item():.0%} sure)\n我猜是 {best}\n\n{bars}", font=("Consolas", 13))


def on_clear():
    board.delete("all")
    pen.rectangle([0, 0, SIZE, SIZE], fill=0)
    result.config(text="Draw with the mouse, then click Guess\n用鼠标写一个数字，再点“猜一猜”", font=("Microsoft YaHei", 14))


board.bind("<B1-Motion>", draw)
board.bind("<Button-1>", draw)
board.bind("<ButtonRelease-1>", lift)
tk.Button(root, text="Guess / 猜一猜", font=("Microsoft YaHei", 14), command=on_guess).grid(row=1, column=0, pady=10)
tk.Button(root, text="Clear / 清除", font=("Microsoft YaHei", 14), command=on_clear).grid(row=1, column=1, pady=10)
if "--autoclose" in sys.argv:            # used only for automatic testing / 仅用于自动测试
    root.after(1500, root.destroy)
root.mainloop()
