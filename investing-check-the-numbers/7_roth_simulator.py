"""
Step 7: a teen Roth IRA, with real ups and downs (Episode 17).
第 7 步：青少年的罗斯 IRA，加入真实的涨跌（第 17 集）。

In Episode 17 we assumed a smooth 6.8% a year. Real markets don't move smoothly.
Here we build 10,000 possible futures by drawing random years from real history (1928-2025), after inflation.
第 17 集假设每年平稳增长 6.8%，但真实的市场不会这么平稳。
这里我们从真实历史（1928-2025）中随机抽取年份，拼出一万种可能的未来（扣除通胀后）。

Run / 运行:   python 7_roth_simulator.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

YEARLY = 3000               # put in each year / 每年存入
START_AGE, STOP_AGE = 16, 20   # contribute at ages 16, 17, 18, 19 / 在 16、17、18、19 岁存入
END_AGE = 65
FUTURES = 10_000

HERE = Path(__file__).parent
df = pd.read_csv(HERE / "data" / "us_annual_returns_1928_2025.csv", index_col="year")
real = ((1 + df["stocks"]) / (1 + df["inflation"]) - 1).values     # 98 real yearly returns / 98 个实际年收益率

rng = np.random.default_rng(2026)
years = END_AGE - START_AGE
finals = np.empty(FUTURES)
paths = []
for i in range(FUTURES):
    draws = rng.choice(real, size=years, replace=True)     # a random future made of real past years / 用真实年份拼出的随机未来
    balance = 0.0
    path = []
    for k, r in enumerate(draws):
        age = START_AGE + k
        if age < STOP_AGE:
            balance += YEARLY           # add at the start of the year / 年初存入
        balance *= 1 + r                # one year of real ups and downs / 一年真实的涨跌
        path.append(balance)
    finals[i] = balance
    if i < 200:
        paths.append(path)

smooth = sum(YEARLY * 1.068 ** (END_AGE - a) for a in range(START_AGE, STOP_AGE))
put_in = YEARLY * (STOP_AGE - START_AGE)
p10, p50, p90 = np.percentile(finals, [10, 50, 90])
print(f"You put in / 你存入: ${put_in:,}  (ages / 年龄 {START_AGE}-{STOP_AGE - 1})")
print(f"Smooth 6.8%/yr (Episode 17) / 平稳 6.8%（第 17 集）:        ${smooth:>12,.0f}")
print(f"Random real history, middle result / 随机真实历史，中间结果: ${p50:>12,.0f}")
print(f"  unlucky 10% end below / 最差的 10% 低于:                 ${p10:>12,.0f}")
print(f"  lucky 10% end above / 最好的 10% 高于:                   ${p90:>12,.0f}")
print(f"Futures that ended below what you put in / 最后低于本金的未来: {(finals < put_in).mean():.1%}")
print("(all in today's dollars, after inflation, before any fees / 均为扣除通胀后的今天美元，未计费用)")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
ages = np.arange(START_AGE + 1, END_AGE + 1)
for p in paths:
    ax1.plot(ages, p, color="steelblue", alpha=0.08)
ax1.set_yscale("log")
ax1.set_title("200 of the 10,000 possible futures")
ax1.set_xlabel("age")
ax1.set_ylabel("balance ($, today's money, log scale)")
ax1.grid(alpha=0.3, which="both")

ax2.hist(finals / 1000, bins=np.logspace(np.log10(max(finals.min(), 1000) / 1000), np.log10(finals.max() / 1000), 60))
ax2.set_xscale("log")
for v, name in [(p10, "10%"), (p50, "middle"), (p90, "90%")]:
    ax2.axvline(v / 1000, color="red", ls="--")
    ax2.text(v / 1000, ax2.get_ylim()[1] * 0.9, f" {name}\n ${v / 1000:,.0f}K", color="red")
ax2.set_title(f"Balance at {END_AGE} ($ thousands, log scale)")
plt.tight_layout()
out = HERE / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "7_roth_futures.png", dpi=120)
print("Saved / 已保存: results/7_roth_futures.png")
plt.show()

# 🧪 Try it / 试一试:
#   1. Keep investing every year until 65: set STOP_AGE = 65. / 一直存到 65 岁。
#   2. A 60/40 mix: use 0.6 * df["stocks"] + 0.4 * df["bonds"]. The middle falls, but so do the bad cases? / 股债 60/40。
#   3. Start at 30 instead of 16. / 从 30 岁开始。
