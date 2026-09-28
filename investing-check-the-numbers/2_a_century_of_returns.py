"""
Step 2: almost a century of American returns (Episodes 1 and 4).
第 2 步：美国近百年的投资回报（第 1、4 集）。

Data: yearly returns 1928-2025 from Prof. Aswath Damodaran (NYU Stern).
数据：纽约大学达摩达兰教授整理的 1928-2025 年年度收益率。

Run / 运行:   python 2_a_century_of_returns.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
df = pd.read_csv(HERE / "data" / "us_annual_returns_1928_2025.csv", index_col="year")
# Columns / 列: stocks (S&P 500 with dividends), bonds (10-year Treasury), tbills (3-month), gold, inflation

assets = ["stocks", "bonds", "tbills", "gold"]

# Growth of $100: multiply (1 + return) year after year. / 100 美元的增长：每年乘以 (1 + 收益率)。
growth = 100 * (1 + df[assets]).cumprod()
prices = (1 + df["inflation"]).cumprod()             # how much prices rose / 物价涨了多少倍
real = growth.div(prices, axis=0)                    # growth after inflation / 扣除通胀后的增长

years = len(df)
print(f"$100 at the start of 1928 → end of 2025 ({years} years) / 1928 年初的 100 美元 → 2025 年底:")
print(f"{'':8s} {'nominal 名义':>14s} {'after inflation 实际':>20s} {'real %/yr 实际年化':>18s}")
for a in assets:
    per_year = (real[a].iloc[-1] / 100) ** (1 / years) - 1
    print(f"{a:8s} ${growth[a].iloc[-1]:>13,.0f} ${real[a].iloc[-1]:>19,.0f} {per_year:>17.1%}")

s = df["stocks"]
print()
print(f"Stocks fell in {(s < 0).sum()} of {years} years / 股票在 {years} 年中有 {(s < 0).sum()} 年下跌")
print(f"Worst year / 最差年份: {s.idxmin()} ({s.min():+.1%})    Best year / 最好年份: {s.idxmax()} ({s.max():+.1%})")
print("Five worst years / 最差的五年:", ", ".join(f"{y} ({v:+.0%})" for y, v in s.nsmallest(5).items()))

# Chart 1: growth after inflation, log scale / 图 1：扣除通胀后的增长，对数坐标
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
for a in assets:
    ax1.plot(real.index, real[a], label=a, lw=2)
ax1.set_yscale("log")          # each gridline = 10x / 每条横线 = 10 倍
ax1.set_title("$100 in 1928, after inflation (log scale)")
ax1.grid(alpha=0.3, which="both")
ax1.legend()

# Chart 2: how often each yearly return happened / 图 2：各种年度收益率出现的次数
ax2.hist(s * 100, bins=range(-50, 60, 5), edgecolor="black")
ax2.axvline(0, color="red")
ax2.set_title("S&P 500 yearly returns, 1928-2025")
ax2.set_xlabel("return in one year (%)")
ax2.set_ylabel("number of years")
plt.tight_layout()

out = HERE / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "2_century.png", dpi=120)
print("Saved / 已保存: results/2_century.png")
plt.show()

# 🧪 Try it / 试一试:
#   1. Start in 1966 instead of 1928:  df = df.loc[1966:]   What changes? / 从 1966 年开始算，有什么变化？
#   2. Print the best five years with s.nlargest(5). / 用 s.nlargest(5) 打印最好的五年。
#   3. A 60% stocks / 40% bonds mix:  mix = 0.6 * df["stocks"] + 0.4 * df["bonds"]  (Episode 6)
