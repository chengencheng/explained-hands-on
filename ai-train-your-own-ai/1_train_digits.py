"""
Step 1: teach a small neural network to read handwritten digits.
第 1 步：训练一个能认手写数字的小神经网络。

This is exactly the kind of network from Episode 2.
这就是第 2 集里讲的那种神经网络。

Run / 运行:   python 1_train_digits.py
"""
import sys
import time

import matplotlib.pyplot as plt
import torch
from torch import nn
from torchvision import datasets, transforms

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using / 使用:", device)
torch.manual_seed(0)  # same random start every time, so results are repeatable / 固定随机数，结果可重复

# ---------------------------------------------------------------
# 1. The data / 数据
# MNIST: 60,000 training pictures + 10,000 test pictures of handwritten digits, 28 x 28 pixels each.
# MNIST：6 万张训练图 + 1 万张测试图，每张是 28×28 像素的手写数字。
# The first run downloads about 11 MB into the "data" folder.
# 第一次运行会下载约 11 MB 到 data 文件夹。
# ---------------------------------------------------------------
to_numbers = transforms.ToTensor()  # picture -> numbers between 0 (black) and 1 (white) / 图片 → 0 到 1 之间的数字
train_set = datasets.MNIST("data", train=True, download=True, transform=to_numbers)
test_set = datasets.MNIST("data", train=False, download=True, transform=to_numbers)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)  # 64 pictures at a time / 每次 64 张
test_loader = torch.utils.data.DataLoader(test_set, batch_size=1000)
print(f"Training pictures / 训练图片: {len(train_set):,}    Test pictures / 测试图片: {len(test_set):,}")

# ---------------------------------------------------------------
# 2. The model / 模型
# 784 inputs (one per pixel) -> 128 neurons -> 64 neurons -> 10 outputs (one score per digit 0-9)
# 784 个输入（每个像素一个）→ 128 个神经元 → 64 个神经元 → 10 个输出（0 到 9 每个数字一个分数）
# ---------------------------------------------------------------
model = nn.Sequential(
    nn.Flatten(),                      # 28 x 28 picture -> a list of 784 numbers / 把图片拉成一串 784 个数字
    nn.Linear(784, 128), nn.ReLU(),    # weighted sums + ReLU (Episodes 2 and 13) / 加权求和 + ReLU
    nn.Linear(128, 64), nn.ReLU(),
    nn.Linear(64, 10),                 # 10 scores / 10 个分数
).to(device)
print(f"Parameters (weights + biases) / 参数个数: {sum(p.numel() for p in model.parameters()):,}")

loss_fn = nn.CrossEntropyLoss()        # softmax + -log(probability of the right answer) (Episode 13)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # a smarter version of gradient descent / 更聪明的梯度下降


def test_accuracy():
    """What fraction of the 10,000 test pictures does the model get right? / 1 万张测试图答对了多少？"""
    model.eval()
    correct = 0
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            correct += (model(x).argmax(dim=1) == y).sum().item()
    model.train()
    return correct / len(test_set)


# ---------------------------------------------------------------
# 3. Training / 训练
# ---------------------------------------------------------------
print(f"\nBefore training, it's just guessing / 训练前只是瞎猜: accuracy {test_accuracy():.1%}")
EPOCHS = 5  # an "epoch" = one pass through all 60,000 pictures / 一个 epoch = 把 6 万张图全部看一遍
for epoch in range(1, EPOCHS + 1):
    t0 = time.time()
    total_loss = 0.0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        scores = model(x)              # forward: make a guess / 前向：猜一猜
        loss = loss_fn(scores, y)      # how wrong was it? / 错得有多离谱？
        optimizer.zero_grad()
        loss.backward()                # backpropagation: which way should each weight move? / 反向传播：每个权重该往哪边调？
        optimizer.step()               # nudge every weight a little / 把每个权重微调一点点
        total_loss += loss.item() * len(x)
    print(f"Epoch {epoch}/{EPOCHS}:  loss {total_loss / len(train_set):.3f}   "
          f"test accuracy / 测试准确率 {test_accuracy():.1%}   ({time.time() - t0:.1f} s)")

torch.save(model.state_dict(), "digits_model.pt")
print("\nSaved the trained model to digits_model.pt / 训练好的模型已保存到 digits_model.pt")

# ---------------------------------------------------------------
# 4. Look at some answers, including mistakes / 看看它的答案，包括答错的
# ---------------------------------------------------------------
model.eval()
x, y = next(iter(test_loader))
with torch.no_grad():
    guess = model(x.to(device)).argmax(dim=1).cpu()
wrong = (guess != y).nonzero().flatten()[:8].tolist()
show = list(range(16)) + wrong
fig, axes = plt.subplots(3, 8, figsize=(12, 5))
for ax, i in zip(axes.flat, show):
    ax.imshow(x[i, 0], cmap="gray")
    ok = guess[i] == y[i]
    ax.set_title(f"guess {guess[i].item()}" + ("" if ok else f" (is {y[i].item()})"), color="green" if ok else "red")
    ax.axis("off")
fig.suptitle("Top two rows: first 16 test pictures.  Bottom row: mistakes (red).")
plt.tight_layout()
plt.savefig("digits_results.png", dpi=100)
print("Saved a picture of its answers to digits_results.png / 答案图片已保存到 digits_results.png")
if "--no-show" not in sys.argv:
    plt.show()  # close the window to finish / 关掉窗口程序就结束
