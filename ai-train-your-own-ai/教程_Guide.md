# 动手篇：在自己的电脑上训练 AI
# Hands-on: Train Your Own AI

这是视频系列 **AI Explained**（英文配音，中英双语字幕）的第 22 集“动手篇”的配套教程。看了 21 集，现在轮到你自己动手了。跟着这份教程，你会在自己的电脑上从零训练两个 AI：

1. **认手写数字的神经网络**（对应第 2 集），训练大约 30 秒。
2. **会写英文小故事的迷你 GPT**（对应第 1、3 集），训练大约 3 分钟。

全程大约 1 小时。不需要什么新知识：会 Python 基础语法就够了，不懂的地方教程里都会解释。

> **给第一次真正写代码的你：** 出错是正常的，每个程序员每天都在出错。遇到红色的报错信息，先别慌，**读最后一行**，它通常会告诉你哪里出了问题。再对照本教程最后的“常见问题”。

---

## 文件夹里有什么

| 文件 | 作用 |
|---|---|
| `0_check_setup.py` | 第 0 步：检查环境装好没有 |
| `1_train_digits.py` | 第 1 步：训练认手写数字的网络 |
| `2_draw_digit.py` | 第 2 步：用鼠标写数字，让模型猜 |
| `gpt_model.py` | 迷你 GPT 的“大脑”：就是第 1 集讲的 Transformer，大约 80 行 |
| `3_train_storyteller.py` | 第 3 步：训练会讲故事的迷你 GPT |
| `4_write_stories.py` | 第 4 步：和你的模型一起写故事 |
| `参考结果_reference/` | 我们在同一台电脑上跑出来的结果，可以和你的对比 |

---

## 第 0 步：准备环境（约 10 分钟）

### 0.1 下载代码，打开终端

在本仓库的 GitHub 页面点绿色的 **Code → Download ZIP**，解压到任意位置（会的话也可以用 `git clone`）。
在文件资源管理器里打开解压后的 `ai-train-your-own-ai` 文件夹，在空白处**右键 → 在终端中打开**。
会出现一个黑色（或蓝色）窗口，这就是终端（PowerShell）。下面所有命令都在这里输入，输完按回车。

先确认 Python 装好了：

```powershell
python --version
```

应该看到 `Python 3.14.0` 之类的版本号（3.10 以上都可以）。

### 0.2 创建“虚拟环境”

虚拟环境（virtual environment）就是给这个项目单独准备的一个 Python 工具箱，装的东西不会影响电脑上的其他程序。

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

成功后，命令行最前面会出现 `(.venv)`。**以后每次重新打开终端，都要先运行第二行**来激活它。

> 如果第二行报错 “running scripts is disabled on this system”（禁止运行脚本），先运行下面这行，再重试：
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

### 0.3 安装 PyTorch

PyTorch 是全世界最常用的 AI 框架之一，ChatGPT 这类模型的研究也常用它。

```powershell
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
pip install matplotlib
```

第一行要下载大约 3 GB（其中大部分是让 PyTorch 使用 NVIDIA 显卡的 CUDA 库，第 9 集讲过），我们测试时用了大约 2 分钟。

### 0.4 检查

```powershell
python 0_check_setup.py
```

你应该看到类似这样的结果（这是我们在这台电脑上的实际输出）：

```
Python version / Python 版本: 3.14.0
PyTorch version / PyTorch 版本: 2.11.0+cu128
✅ GPU found / 找到显卡: NVIDIA GeForce RTX 5070 Ti
One 4096×4096 matrix multiply: 4.2 ms  (≈ 32 trillion operations per second)
✅ torchvision OK
✅ matplotlib OK
```

每秒 32 万亿次运算，这就是第 9 集讲的 GPU 的威力。

---

## 第 1 步：训练认手写数字的网络（约 10 分钟）

```powershell
python 1_train_digits.py
```

第一次运行会自动下载 MNIST 数据集（6 万张训练图 + 1 万张测试图，约 11 MB）。然后你会看到：

```
Parameters (weights + biases) / 参数个数: 109,386

Before training, it's just guessing / 训练前只是瞎猜: accuracy 10.0%
Epoch 1/5:  loss 0.346   test accuracy / 测试准确率 94.0%   (3.9 s)
Epoch 2/5:  loss 0.145   test accuracy / 测试准确率 96.2%   (3.8 s)
Epoch 3/5:  loss 0.100   test accuracy / 测试准确率 97.3%   (3.8 s)
Epoch 4/5:  loss 0.075   test accuracy / 测试准确率 97.4%   (3.9 s)
Epoch 5/5:  loss 0.062   test accuracy / 测试准确率 97.6%   (3.8 s)
```

最后会弹出一张图：绿色是答对的，最下面一排红色是答错的。看看那些错题，有些连人都会认错！关掉图片窗口，程序就结束了。

### 读懂代码

用 VS Code 或记事本打开 `1_train_digits.py`，对照下面的说明看。代码分成 4 块：

1. **数据**：`transforms.ToTensor()` 把图片变成 0 到 1 之间的数字（第 5 集：图片就是一堆数字）。`DataLoader` 每次拿 64 张图出来。
2. **模型**：`nn.Sequential(...)` 就是第 2 集那种网络：784 个输入 → 128 个神经元 → 64 个神经元 → 10 个输出。`nn.Linear` 是加权求和，`nn.ReLU` 是第 13 集讲的激活函数。
3. **训练**：最核心的就是循环里这 5 行，和第 2、13 集讲的一模一样：
   ```python
   scores = model(x)              # 猜一猜
   loss = loss_fn(scores, y)      # 错得有多离谱
   optimizer.zero_grad()
   loss.backward()                # 反向传播：每个权重该往哪边调
   optimizer.step()               # 把每个权重微调一点点
   ```
4. **看结果**：画出一些测试图和它的答案。

**为什么要分“训练集”和“测试集”？** 测试用的 1 万张图，模型在训练时从来没见过。在没见过的题上考得好，才说明它真的学会了，而不是背下了答案（第 20 集讲的“考前看到试卷”问题）。

### ✏️ 动手改一改

每次改完保存，再运行一次，看结果怎么变：

1. 把 `EPOCHS = 5` 改成 `EPOCHS = 10`。准确率还能涨多少？
2. 把两处 `128` 都改成 `16`（网络变小了）。准确率会怎样？
3. 把 `lr=0.001` 改成 `lr=0.5`（学习率太大）。发生了什么？想想第 13 集梯度下降里“步子迈太大”的比喻。

改完记得改回来，第 2 步要用训练好的模型。

---

## 第 2 步：自己写数字给它认（约 5 分钟）

```powershell
python 2_draw_digit.py
```

会弹出一个窗口。在黑色画板上用鼠标写一个数字，点 **Guess / 猜一猜**，右边会显示它对 0 到 9 每个数字的把握有多大。点 **Clear / 清除** 重来。

**试试看：**
- 写得很小、很歪、只写一半，它还认得出吗？
- 写一个“欧洲式”的 7（中间加一横），或者带底座的 1？
- 它什么时候“很有把握地答错”？（第 3 集：AI 可能自信满满地犯错。）

**一个重要的小秘密：** 你写的数字，在交给模型之前，会先被缩小到 28×28，并**按“重心”放到正中间**，因为 MNIST 的训练图就是这样处理的。我们测试时发现，少了“按重心居中”这一步，50 个测试数字只认对 36 个；加上以后能认对 47 个。

这说明：**模型只擅长处理和训练数据“长得像”的东西。** 这也是自动驾驶（第 14 集）和各种 AI 都要面对的难题。

---

## 第 3 步：训练你自己的迷你 GPT（约 3 分钟）

这是最酷的一步。你要从零训练一个会写英文小故事的 GPT。

```powershell
python 3_train_storyteller.py
```

### 它学什么？

训练文本是 **TinyStories**：微软研究院 2023 年发布的数据集，里面是专门写给小模型学习的简单英文小故事，我们用了其中 27,626 个。第一次运行会下载约 22 MB。

模型的任务只有一个：**看前面的字符，预测下一个字符。** 就像第 3 集讲的，ChatGPT 本质上也是在做这件事，只不过它预测的是词（token），而我们为了简单，一个字母一个字母地来。

### 它长什么样？

打开 `gpt_model.py`，你会认出第 1 集的所有零件：

| 代码 | 第 1 集里的概念 |
|---|---|
| `tok_emb = nn.Embedding(...)` | 每个字符变成一个向量（嵌入，也见第 13 集） |
| `pos_emb` | 位置信息：这个字符在第几个位置 |
| `SelfAttention` | 注意力：每个字符回头看前面的字符，决定哪些重要 |
| `is_causal=True` | 遮罩：不许偷看后面的字 |
| `n_head=6` | 多头注意力：6 个“头”各自关注不同的东西 |
| `Block` × 6 | 6 层 Transformer 叠在一起 |
| `head` + `softmax` | 给每个可能的下一个字符打分，变成概率 |

整个模型有 10,805,069 个参数（约 1100 万）。GPT-3 有 1750 亿个，是它的一万六千多倍（第 20 集）。

### 训练时你会看到什么

每 250 步，程序会打印一次损失（loss），并让模型用 “Once upon a time” 开头写一小段。如果这次的 val 损失是目前最好的，就把模型存下来，并标上 `<- best so far, saved`。**仔细看它是怎么一点点学会写字的！** 下面是我们这次训练的真实输出（你的会有些不同，因为有随机性）：

```
step     0   loss: train 4.493  val 4.494   (    2 s)   <- best so far, saved / 目前最好，已保存
   sample / 样例: Once upon a timerfzxmq7`HP,DwS,lV-Pr-E.tJVn6iA R;YFtx`C5Rq4"sUNQIkWE.0wbC593WQJQ XN9OLN:ieN9Djlf`sswk/ivx9 TNa!9PQqUtulqN;uvHM`vV7hPcOomo"sbsN OdH'"BC

step   250   loss: train 1.441  val 1.450   (   12 s)   <- best so far, saved / 目前最好，已保存
   sample / 样例: Once upon a time boall named Sur. One day, A a playing with tree.

step  1000   loss: train 0.825  val 0.842   (   42 s)   <- best so far, saved / 目前最好，已保存
   sample / 样例: Once upon a time, there was an old norman. The turtle boy liked hopping treats of the people in the sun. The turtle cat was so proud of the streamble 

step  5000   loss: train 0.593  val 0.627   (  199 s)   <- best so far, saved / 目前最好，已保存
   sample / 样例: Once upon a time, there was a small squirrel named Tim. Tim loved to eat sweet near his house. One day, Tim saw a big closet on the sea. He wanted to 
```

- **第 0 步：** 完全是乱码。它还什么都不知道，每个字符都是随便猜的。
- **第 250 步（12 秒）：** 学会了空格、标点和一些短单词，但句子不通。
- **第 1000 步（42 秒）：** 学会了故事的套路（*Once upon a time, there was...*），句子结构基本对了，但用词还很奇怪（*The turtle cat*？）。
- **第 5000 步（3 分钟）：** 能写出像样的小故事了。不过仔细读会发现，情节常常说不通。这就是小模型的极限，也是第 20 集讲的规模定律：模型越大、数据越多，写得越好。

完整的输出在 `参考结果_reference/step3_training_output.txt` 里。

两个损失：`train` 是在学过的文字上的成绩，`val` 是在**从没学过**的 10% 文字上的成绩。两个一起下降，说明它是真学会了，不是死记硬背。

训练完会保存模型 `storyteller_stories.pt`、损失曲线图 `loss_stories.png`，最后再写两个完整的故事。

---

## 第 4 步：和你的模型一起写故事

```powershell
python 4_write_stories.py
```

然后就可以输入了：

| 输入 | 效果 |
|---|---|
| `Tom found a magic box` | 它接着你的开头写故事 |
| 直接回车 | 从 “Once upon a time” 开始 |
| `t=0.3` 或 `t=1.5` | 修改“温度”（第 3 集） |
| `? Once upon a ti` | 看它对**下一个字符**的前 5 个猜测和概率 |
| `q` | 退出 |

### ✏️ 实验

1. **温度：** 分别试 `t=0.3`、`t=0.8`、`t=1.5`，每次都直接回车。我们测试时，温度 0.3 的故事很“保守”，还原封不动地重复了一句 *They did not know what to do.*；温度 1.5 时开始胡言乱语，甚至拼错单词（*Frridged*、*automobis*）。想想为什么？（提示：温度决定了“掷骰子”时，不太可能的字符有多大机会被选中。）
2. **偷看它的想法：** 试试 `? Once upon a ti`，它会 100% 确定下一个是 `m`。再试试 `? Once upon a time, there was a little `（最后有个空格），我们的模型给出 `g` 51%、`b` 39%：它在犹豫接下来写 girl 还是 boy！这就是第 3 集讲的“按概率选下一个词”。
3. **考考它：** 给它一个它在小故事里很少见的开头，比如 `The spaceship landed on Mars`。它会怎么处理？
4. **它会编吗？** 它写的故事，是从训练数据里抄的，还是新编的？（提示：用记事本打开 `data` 文件夹里的 txt 文件，用 Ctrl+F 搜一句它写的话。）

---

## 🚀 挑战

做完以上四步，你已经完成了真正的 AI 工程师的核心流程。想继续玩，可以试试这些：

1. **换成莎士比亚，亲眼看到“过拟合”：**
   ```powershell
   python 3_train_storyteller.py shakespeare
   python 4_write_stories.py shakespeare
   ```
   莎士比亚的全部文本只有 110 万个字符，是 TinyStories 的二十分之一。训练时盯着两个损失看：我们测试时，`val` 在第 1000 步左右降到最低（1.54），之后**不降反升**，一直涨到 4.2；而 `train` 却一路降到 0.09。

   这就是**过拟合（overfitting）**：数据太少，模型开始把训练文本**死记硬背**下来，而不是学规律。我们检查过：第 1000 步时，它写的内容和原文最长只重合 13 个字符，是自己“编”的；到第 5000 步，它写出的一段里有 104 个字符和原文一字不差，是“背”出来的。它背熟了学过的台词，碰到没见过的文字却一塌糊涂。就像只背答案、不懂方法的学生（第 20 集）。

   所以程序会自动保存 `val` 最低的那个版本（输出里标着 `<- best so far, saved`），而不是最后一步的版本。打开 `loss_shakespeare.png` 看看两条线是怎么分开的（我们的结果在 `参考结果_reference/loss_shakespeare.png`：一条线往下，一条线掉头往上，这是教科书式的过拟合曲线）。

2. **用你自己的文字训练：** 把一个很长的纯文本文件放进文件夹，比如在 gutenberg.org 下载的公版小说（选 “Plain Text UTF-8” 格式），改名为 `my_book.txt`：
   ```powershell
   python 3_train_storyteller.py my_book.txt
   python 4_write_stories.py my_book
   ```
   文字越多越好。一本小说通常只有几十万到一百多万个字符，一样会过拟合，但程序会保留最好的版本。
3. **改模型大小（第 20 集的规模定律）：** 在 `3_train_storyteller.py` 里找到 `TinyGPT(len(chars), block_size=BLOCK)`，改成 `TinyGPT(len(chars), block_size=BLOCK, n_layer=2, n_embd=128)`，模型会小很多。最后的 val 损失会变差多少？写出来的故事呢？
4. **训练更久：** 把 `STEPS = 5000` 改成 `10000`。TinyStories 的 val 损失还会降吗？会不会也开始过拟合？
5. **升级数字识别：** 第 6 集讲过，看图用卷积神经网络（CNN）更好。试着把第 1 步的模型换成：
   ```python
   model = nn.Sequential(
       nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 28×28 → 14×14
       nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 14×14 → 7×7
       nn.Flatten(),
       nn.Linear(32 * 7 * 7, 64), nn.ReLU(),
       nn.Linear(64, 10),
   ).to(device)
   ```
   准确率能到多少？我们测试时，参数个数差不多（105,866 对 109,386），准确率却从 97.6% 提高到 98.9%，错题少了一半多。这就是卷积“看局部图案”的威力。（`2_draw_digit.py` 里的模型也要改成一样的结构才能加载。）

---

## 🔧 常见问题

| 现象 | 解决办法 |
|---|---|
| `running scripts is disabled on this system` | 运行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，再激活 |
| `ModuleNotFoundError: No module named 'torch'` | 虚拟环境没激活。运行 `.venv\Scripts\Activate.ps1`，行首要有 `(.venv)` |
| `No GPU found` | 能用 CPU 跑，但第 3 步会很慢。可以把 `STEPS` 改成 `1000`、`BATCH` 改成 `16` |
| `CUDA out of memory`（显存不够） | 把 `BATCH = 64` 改小，比如 `32` 或 `16` |
| 下载失败（`URLError`、超时） | 检查网络后重试。下载好的文件在 `data` 文件夹里，只需要下载一次 |
| `FileNotFoundError: digits_model.pt` | 先运行第 1 步 |
| `FileNotFoundError: storyteller_stories.pt` | 先运行第 3 步 |
| 程序卡住不动 | 训练本来就需要时间，看看是否还在打印。想中途停止，按 `Ctrl + C` |

---

## 你刚刚做了什么

| 你做的事 | 大公司做的事 |
|---|---|
| 用 6 万张图训练 10 万个参数，30 秒 | 用几十亿张图训练几十亿个参数 |
| 用 2200 万个字符训练 1100 万个参数，3 分钟，一块显卡 | 用十几万亿个 token 训练几千亿个参数，几个月，几万块显卡（第 11、20 集） |
| 一个字符一个字符地预测 | 一个 token 一个 token 地预测：**原理完全一样** |

恭喜你，你已经亲手训练了一个 GPT！

---

*数据来源：MNIST（LeCun 等）；TinyStories（Eldan & Li, 2023, huggingface.co/datasets/roneneldan/TinyStories）；Tiny Shakespeare（Karpathy, char-rnn）。模型结构参考了 Andrej Karpathy 的 nanoGPT。*
