# 动手篇：用 Python 分析真实的市场历史
# Hands-on: Analyze Real Market History with Python

这是视频系列 **Investing Explained**（英文配音，中英双语字幕）的第 18 集“动手篇”的配套教程。看了 17 集，你已经听过很多数字：复利让艾玛赢了本，持有 20 年从没亏过钱，错过最好的 10 天收益少一半，一千条规则没有一条跑赢买入持有……
**这些数字都是真的吗？** 现在，你可以自己用 Python 和真实数据把它们算出来。

跟着这份教程，你会运行 7 个小程序（外加 1 个附加题），每个都对应前面的某一集。全程大约 1 到 1.5 小时。

> **给第一次真正写代码的你：** 出错是正常的。遇到红色的报错信息，先别慌，**读最后一行**，它通常会告诉你哪里出了问题。再对照本教程最后的“常见问题”。

> **声明：** 这是学习用的历史数据分析，不是投资建议。过去的回报不代表未来。

---

## 文件夹里有什么

| 文件 | 作用 | 对应视频 |
|---|---|---|
| `0_check_setup.py` | 检查环境，看一眼数据 | |
| `1_compound.py` | 复利：双胞胎艾玛和本 | 第 1 集 |
| `2_a_century_of_returns.py` | 近百年的股票、债券、国库券、黄金 | 第 1、4 集 |
| `3_patience.py` | 持有越久，亏钱的概率越低 | 第 4 集 |
| `4_three_markets.py` | 美国 vs 中国 vs 日本 | 第 5 集 |
| `5_best_days.py` | 错过最好的几天 | 第 10 集 |
| `6_backtest_trap.py` | 一千条随机规则的回测陷阱 | 第 13 集 |
| `7_roth_simulator.py` | 青少年罗斯 IRA 的一万种未来 | 第 17 集 |
| `8_bonus_any_stock.py` | 附加题：下载任意股票的最新数据 | 第 6 集 |
| `data/` | 年度收益率数据（已附带）；每日价格由第 0 步自动下载（截至 2026 年 9 月 25 日） | |
| `参考结果_reference/` | 我们在这台电脑上跑出来的结果，可以和你的对比 | |

**数据从哪来：**

| 文件 | 内容 | 来源 |
|---|---|---|
| `us_annual_returns_1928_2025.csv` | 每年的股票（标普 500，含分红）、10 年期国债、3 个月国库券、黄金收益率和通胀率 | 纽约大学 Aswath Damodaran 教授 |
| `sp500_daily_1928_2026.csv` | 标普 500 每日收盘价（不含分红） | 雅虎财经 ^GSPC（第 0 步下载） |
| `sp500_total_return_daily_1988_2026.csv` | 标普 500 全收益指数（分红再投资） | 雅虎财经 ^SP500TR |
| `world_markets_daily_1997_2026.csv` | 标普 500、上证综指、日经 225 每日收盘价 | 雅虎财经 |
| `nikkei_daily_1965_2026.csv` | 日经 225 每日收盘价 | 雅虎财经 ^N225 |

雅虎财经的数据不能随仓库一起分享，所以由第 0 步用 yfinance 下载，并且截止到 2026 年 9 月 25 日，保证你的结果和教程完全一样。

CSV 就是用逗号分隔的表格，可以直接用 Excel 或记事本打开看看。

---

## 第 0 步：准备环境（约 10 分钟）

### 0.1 下载代码，打开终端

在本仓库的 GitHub 页面点绿色的 **Code → Download ZIP**，解压到任意位置（会的话也可以用 `git clone`）。
在文件资源管理器里打开解压后的 `investing-check-the-numbers` 文件夹，在空白处**右键 → 在终端中打开**。下面所有命令都在这里输入，输完按回车。

```powershell
python --version
```

应该看到 `Python 3.14.0` 之类的版本号（3.10 以上都可以）。

### 0.2 创建虚拟环境并安装工具包

和 AI 系列的动手篇一样，先创建一个虚拟环境（这个项目专用的工具箱）：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pandas matplotlib yfinance
```

成功后，命令行最前面会出现 `(.venv)`。**以后每次重新打开终端，都要先运行第二行**来激活它。
这次只需要三个工具包，下载大约 30 MB，比 AI 篇的 PyTorch 小得多：

- **pandas**：处理表格数据的工具，全世界的数据分析师、量化研究员（第 13 集）每天都在用。
- **matplotlib**：画图。
- **yfinance**：从雅虎财经下载股价数据。

> 如果第二行报错 “running scripts is disabled on this system”，先运行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，再重试。

### 0.3 检查并下载数据

```powershell
python 0_check_setup.py
```

第一次运行会下载每日价格（需要联网，几秒到一分钟）。你应该看到（这是我们的实际输出）：

```
Python version / Python 版本: 3.14.0
numpy 2.5.3 · pandas 3.0.6 · matplotlib 3.11.2

Downloading daily prices from Yahoo Finance (about 1 minute) ...
  ✅ sp500_daily_1928_2026.csv
  ✅ sp500_total_return_daily_1988_2026.csv
  ✅ nikkei_daily_1965_2026.csv
  ✅ world_markets_daily_1997_2026.csv

✅ nikkei_daily_1965_2026.csv                    15,173 rows / 行   1965-01-05 → 2026-09-25
✅ sp500_daily_1928_2026.csv                     24,800 rows / 行   1928-01-03 → 2026-09-25
✅ sp500_total_return_daily_1988_2026.csv         9,756 rows / 行   1988-01-04 → 2026-09-25
✅ us_annual_returns_1928_2025.csv                   98 rows / 行   1928 → 2025
✅ world_markets_daily_1997_2026.csv              7,602 rows / 行   1997-07-02 → 2026-09-25
```

两万四千八百行：这是标普 500 近一百年里的每一个交易日。

### 0.4 pandas 五分钟入门

后面的程序会反复用到这几招。不用背，用到的时候回来看：

```python
import pandas as pd
df = pd.read_csv("data/us_annual_returns_1928_2025.csv", index_col="year")  # 读表格，用年份当行名

df["stocks"]            # 取一列：每年的股票收益率，比如 0.2488 表示 +24.88%
df.loc[2008]            # 取一行：2008 年的所有数据
df.loc[1966:]           # 取 1966 年以后的所有行
(df["stocks"] < 0).sum()   # 有多少年是亏的（True 算 1，False 算 0）

(1 + df["stocks"]).cumprod()    # 累积连乘：1 美元一年年滚下来变成多少，这就是复利！
s.pct_change()                  # 每天比前一天涨跌了百分之几
s.rolling(10).mean()            # 滑动窗口：每个位置往前 10 个数的平均（第 13 集的“均线”）
s.nlargest(10)                  # 最大的 10 个值
s.cummax()                      # 到目前为止的最高值，用来算“从高点跌了多少”
```

最重要的一招是 `cumprod()`（累积连乘）。如果某年涨 10%、第二年跌 5%，钱就变成 1 × 1.10 × 0.95 = 1.045 倍。这就是第 1 集的复利，写成代码只有一行。

---

## 第 1 步：复利，艾玛和本（第 1 集）

```powershell
python 1_compound.py
```

```
Emma put in / 艾玛存入      $   12,000  → at 65 / 65 岁时 $   240,737
Ben put in  / 本存入        $   46,800  → at 65 / 65 岁时 $   231,128
Emma, 16-65 / 艾玛坚持到 65 $   58,800  → at 65 / 65 岁时 $   471,865
At 7%: rule of 72 says 10.3 years, exact answer 10.24 years
```

和第 1 集的数字**一模一样**。还会弹出一张图，关掉窗口程序就结束了（图也保存在 `results/` 文件夹里）。

### 读懂代码

核心就是 `balances()` 函数里的循环：每个月先存 100 美元，再让余额增长一个月。

```python
monthly_rate = (1 + rate) ** (1 / 12) - 1   # 每年 7% 换算成每月约 0.565%
for month in range(16 * 12, end_age * 12):
    if start_age <= age < stop_age:
        balance += monthly          # 存钱
    balance *= 1 + monthly_rate     # 增长一个月
```

为什么每月利率不是 7% ÷ 12？因为每月的增长也会复利。(1.00565)¹² 才正好等于 1.07。

### ✏️ 动手改一改

1. 把 `RATE = 0.07` 改成 `0.04` 或 `0.10`，现在谁赢？（提示：利率越高，早开始的优势越大。）
2. 本每月存 200 美元：把 `ben = balances(26, 65)` 改成 `balances(26, 65, monthly=200)`。
3. 本最晚几岁开始，才能赢过艾玛？写个循环试试 `for start in range(16, 27):`。

---

## 第 2 步：近百年的回报（第 1、4 集）

```powershell
python 2_a_century_of_returns.py
```

```
$100 at the start of 1928 → end of 2025 (98 years):
             nominal 名义   after inflation 实际     real %/yr 实际年化
stocks   $    1,157,591 $             61,799              6.8%
bonds    $        7,714 $                412              1.5%
tbills   $        2,579 $                138              0.3%
gold     $       21,021 $              1,122              2.5%

Stocks fell in 26 of 98 years
Worst year: 1931 (-43.8%)    Best year: 1954 (+52.6%)
```

这就是第 4 集那张表的来源。注意看左图：纵轴是**对数坐标**，每往上一格就是 10 倍。在普通坐标上，1990 年以前的曲线会被压成一条贴地的线，看不出任何起伏。

右图是每年收益率的分布：大多数年份在 0% 到 +30% 之间，但左边那几根柱子（-44%、-37%、-35%）就是 1931、2008、1937 年。

### ✏️ 动手改一改

1. 在读数据后面加一行 `df = df.loc[1966:]`，从 1966 年开始算。股票的实际年化收益变了多少？
2. 用 `s.nlargest(5)` 打印最好的五年。
3. 第 6 集的“分散投资”：加一列 60% 股票 + 40% 债券的组合，`df["mix"] = 0.6 * df["stocks"] + 0.4 * df["bonds"]`，再把 `"mix"` 加进 `assets` 列表。它的最差年份是哪年？

---

## 第 3 步：耐心的力量（第 4 集）

```powershell
python 3_patience.py
```

```
hold  1 yrs:  98 periods, lost money  31.6%,  worst -38.1%/yr,  best +53.7%/yr
hold  5 yrs:  94 periods, lost money  23.4%,  worst -10.3%/yr,  best +25.3%/yr
hold 10 yrs:  89 periods, lost money  12.4%,  worst  -3.8%/yr,  best +17.9%/yr
hold 15 yrs:  84 periods, lost money   6.0%,  worst  -0.5%/yr,  best +15.1%/yr
hold 20 yrs:  79 periods, lost money   0.0%,  worst  +0.6%/yr,  best +13.2%/yr
```

程序把每一个可能的起点都试了一遍：1928 年开始持有 5 年、1929 年开始持有 5 年……一直到 2021 年开始持有 5 年，一共 94 个区间，其中 23.4% 扣除通胀后是亏的。
关键代码是 `real.rolling(hold).apply(...)`：一个“滑动窗口”，每次框住连续 `hold` 年，把它们的增长倍数乘起来。

**注意：** 20 年 0% 亏损，是美国过去近百年的结果。第 5 集讲过，同样的规律在日本和中国并不成立。

### ✏️ 动手改一改

1. 换成债券：把 `df["stocks"]` 改成 `df["bonds"]`。持有 20 年的债券，亏钱的概率是多少？（答案可能让你惊讶，想想第 4 集的通胀。）
2. 在 `[1, 5, 10, 15, 20]` 里加上 `30`。
3. 不考虑通胀：`real = 1 + df["stocks"]`。概率变了多少？

---

## 第 4 步：选择市场（第 5 集）

```powershell
python 4_three_markets.py
```

```
Start at 100 on 1997-07-02:
  S&P 500 (price)            →     857   (+7.6% a year)
  S&P 500 (with dividends)   →   1,447   (+9.6% a year)
  Shanghai Composite         →     324   (+4.1% a year)
  Nikkei 225                 →     329   (+4.2% a year)

Biggest falls:
  Shanghai: peak 6,092 on 2007-10-16 → bottom 1,707 (-72%) → back: not yet
  Nikkei (since 1965): peak 38,916 on 1989-12-29 → bottom 7,055 (-82%) → back: 2024-02-22 (34.1 years later)
  S&P 500: peak 1,565 on 2007-10-09 → bottom 677 (-57%) → back: 2013-03-28 (5.5 years later)
```

这就是第 5 集的核心数据：同样从 1997 年开始，标普 500 涨到 857（含分红 1,447），上证和日经只有三百多。上证 2007 年的高点 6,092，到今天还没回去；日经花了整整 34 年才回到 1989 年的高点。

### 读懂代码

`peak_and_recovery()` 这个函数值得仔细看，它用三行找出“最惨的一次下跌”：

```python
running_peak = s.cummax()        # 到每一天为止的最高价
drawdown = s / running_peak - 1  # 每一天比之前的最高点低了多少（回撤）
bottom_day = drawdown.idxmin()   # 回撤最大的那一天
```

**注意：** 这里比较的是各自货币的价格指数。上证和日经的数字不含分红，所以对它们稍微不公平；但即使加上每年 2% 左右的分红，差距依然巨大。

### ✏️ 动手改一改

1. 从 2009 年 3 月（金融危机最低点）开始：在读数据后加 `w = w.loc["2009-03-09":]`。排名变了吗？起点有多重要？
2. 用 `w["shanghai"].idxmax()` 找出上证历史最高收盘价是哪一天。
3. 为什么“含分红”的标普比不含分红的高出这么多？（第 2 集）

---

## 第 5 步：错过最好的几天（第 10 集）

```powershell
python 5_best_days.py
```

```
5,030 trading days from 2006-01-04 to 2025-12-31
miss the  0 best days: $   79,316
miss the 10 best days: $   35,286
miss the 20 best days: $   20,834
miss the 30 best days: $   13,603

The 10 best days:
  2008-10-13  +11.6%  ← within 2 weeks of a worst day (2008-10-15)
  2008-10-28  +10.8%  ← within 2 weeks of a worst day (2008-10-15)
  2025-04-09  +9.5%
  ...
```

和第 10 集一模一样。五千多个交易日里，只要错过最好的 10 天，结果就少了一半多。再看下面的列表：最好的日子，大多紧挨着最差的日子，都在 2008 年和 2020 年的恐慌里。恐慌时卖出的人，几乎一定会错过反弹。

代码只有一个技巧：`daily.drop(best)` 把最好的那几天从表里删掉，假装那几天你不在市场里。

### ✏️ 动手改一改

1. 如果你**同时**错过了最好的 10 天和最差的 10 天呢？`daily.drop(daily.nlargest(10).index).drop(daily.nsmallest(10).index)`
2. 把 `START` 改成 `"1990-01-01"`。
3. 想一想：为什么现实中几乎不可能只躲开最差的日子？

---

## 第 6 步：回测陷阱（第 13 集）

```powershell
python 6_backtest_trap.py
```

```
Buy and hold / 买入持有:  2000-2012 -0.2%/yr   2013-2025 +12.8%/yr
Best rule / 最好的规则 (MA 45 vs 254):  2000-2012 +6.4%/yr  →  2013-2025 +7.8%/yr
Rules beating buy & hold:  2000-2012: 792 of 1,000   2013-2025: 0 of 1,000
```

这就是第 13 集的实验，而且用的是同一个随机种子（`default_rng(7)`），所以你会得到完全相同的一千条规则。（视频里写的 12.9% 是四舍五入的差别，实际是 12.85%。）

看看散点图：横轴是规则在 2000-2012 年的表现（用来挑选的数据），纵轴是在 2013-2025 年的表现（从没见过的数据）。
- 2000-2012 年，一千条规则里有 792 条跑赢了买入持有，那段时间市场本身几乎没涨，躲开下跌就显得很聪明。
- 最好的那条（红点）看起来像天才：每年 +6.4%，而市场是 -0.2%。
- 可是到了 2013-2025 年，**一千条规则没有一条**跑赢简单的持有。

点云基本上是一团没有方向的云：过去表现好的规则，未来并不更好。这就是 AI 系列里讲的**过拟合**，只不过这次发生在钱上。

### ✏️ 动手改一改

1. 把 `default_rng(7)` 里的 7 换成别的数字。有没有哪条规则在 2013-2025 年跑赢？
2. 把两个时段对调：在 2013-2025 年挑规则，在 2000-2012 年检验。
3. 加上交易成本（每次买卖付 0.05%）：把 `returns = position * daily` 改成
   `returns = position * daily - 0.0005 * position.diff().abs().fillna(0)`。

---

## 第 7 步：罗斯 IRA 的一万种未来（第 17 集）

```powershell
python 7_roth_simulator.py
```

```
You put in / 你存入: $12,000  (ages / 年龄 16-19)
Smooth 6.8%/yr (Episode 17):                    $     273,836
Random real history, middle result:            $     278,154
  unlucky 10% end below:                       $      51,242
  lucky 10% end above:                         $   1,452,757
Futures that ended below what you put in:      1.0%
```

第 17 集假设每年平稳增长 6.8%，结果是约 27.4 万美元。但真实的市场不会平稳。这个程序做了一件量化研究员常做的事，叫**蒙特卡洛模拟**：从 1928-2025 年的真实年份里随机抽 49 次，拼成一种可能的未来，重复一万次。

结果很有意思：
- **中间的结果**（27.8 万）和平稳假设差不多。
- 但**范围非常宽**：运气差的 10% 不到 5.2 万，运气好的 10% 超过 145 万。
- 一万种未来里，只有 1% 最后低于你存进去的 1.2 万美元。

这就是投资的真相：长期来看大概率会增长，但具体多少，没有人能提前知道。

**注意：** 随机抽年份会打乱真实历史的顺序（比如大跌后往往有反弹），这是一个简化。而且美国过去近百年的回报，本身就是全世界最好的之一（第 5 集）。

### ✏️ 动手改一改

1. 一直存到 65 岁：`STOP_AGE = 65`。
2. 股债 60/40 组合：把 `df["stocks"]` 换成 `0.6 * df["stocks"] + 0.4 * df["bonds"]`。中间结果降了多少？最差的 10% 呢？
3. 从 30 岁开始：`START_AGE, STOP_AGE = 30, 34`。

---

## 🚀 附加题：下载任意股票的数据（第 6 集）

这一步需要联网（yfinance 在第 0 步已经装好了）：

```powershell
python 8_bonus_any_stock.py
python 8_bonus_any_stock.py SPY QQQ GLD TLT
```

它会下载 2006 年至今的每日数据（含分红调整），告诉你 1 万美元变成了多少、中途最大跌了多少。默认比较 SPY（标普 500 指数基金）、苹果、可口可乐和通用电气（第 6 集的 GE）。

A 股代码加 `.SS`（上海）或 `.SZ`（深圳），比如贵州茅台是 `600519.SS`；港股加 `.HK`，比如腾讯是 `0700.HK`。

**记住第 6 集：** 事后看，挑出苹果当然很容易。难的是在 2006 年就知道该挑哪一只。

> yfinance 是非官方的工具，雅虎偶尔会改变网站，导致下载失败。如果报错，先运行 `pip install -U yfinance` 更新一下；第 1 到 7 步用的是第 0 步已经下载好的数据，不受影响。

---

## 🔧 常见问题

| 问题 | 解决办法 |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | 没激活虚拟环境。先运行 `.venv\Scripts\Activate.ps1`，看到 `(.venv)` 再运行。 |
| `FileNotFoundError: ... data\...csv` | 还没运行第 0 步，或者终端不在 `investing-check-the-numbers` 文件夹里。先 `cd` 进入这个文件夹，再运行 `python 0_check_setup.py`。 |
| 第 0 步下载失败 | 检查网络，然后运行 `pip install -U yfinance` 更新后重试。 |
| 中文显示成乱码 | 在 Windows Terminal 里运行；或者先运行 `$env:PYTHONUTF8=1`。 |
| 图片窗口弹出后程序“卡住” | 这是正常的：关掉图片窗口，程序就会结束。 |
| 改了代码后报 `IndentationError` | Python 靠缩进（行首空格）分块，检查新加的那行和上下行是否对齐。 |
| 我的结果和参考结果不一样 | 第 0-7 步用的是同样的数据和随机种子，结果应该完全一样。先检查是不是改过代码。 |

---

## 你刚刚做了什么

你用大约 350 行 Python 代码（不算注释），把整个系列最重要的几个结论，从原始数据里亲手算了一遍：

- 复利：早开始比多存钱更重要（第 1 集）。
- 股票长期回报最高，但每 3 年左右就有 1 年下跌（第 1、4 集）。
- 持有越久，亏钱的概率越低；但前提是选对了市场（第 4、5 集）。
- 择时的代价：错过最好的几天，收益少一半（第 10 集）。
- 过去表现好的规则，未来不一定好（第 13 集）。
- 未来是一个范围，而不是一个数字（第 17 集）。

以后再看到任何人说“这个策略过去十年赚了 300%”，你知道该怎么做了：**拿数据，自己算一遍，然后在它没见过的数据上检验。**

投资愉快！Invest wisely!
