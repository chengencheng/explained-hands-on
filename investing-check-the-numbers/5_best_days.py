"""
Step 5: what if you missed the market's best days? (Episode 10)
第 5 步：如果错过了市场最好的几天，会怎样？（第 10 集）

Data: S&P 500 total return index (dividends reinvested), daily, from Yahoo Finance (^SP500TR).
数据：标普 500 全收益指数（分红再投资）的每日数据，来自雅虎财经。

Run / 运行:   python 5_best_days.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

START, END = "2006-01-01", "2025-12-31"     # 20 years / 20 年
MONEY = 10_000

HERE = Path(__file__).parent
tr = pd.read_csv(HERE / "data" / "sp500_total_return_daily_1988_2026.csv", index_col="date", parse_dates=True)["close"]
tr = tr.loc[START:END]                       # we buy at the close of the first day / 在第一天收盘时买入
daily = tr.pct_change().dropna()             # each day's % change / 每天的涨跌幅
print(f"{len(daily):,} trading days from {daily.index[0]:%Y-%m-%d} to {daily.index[-1]:%Y-%m-%d} / 个交易日")

results = {}
for missed in [0, 10, 20, 30]:
    best = daily.nlargest(missed).index              # the N best days / 最好的 N 天
    kept = daily.drop(best)                          # pretend we were out of the market / 假装那几天不在市场里
    results[missed] = MONEY * (1 + kept).prod()
    print(f"miss the {missed:2d} best days / 错过最好的 {missed:2d} 天: ${results[missed]:>9,.0f}")

# Where were the best days? Right next to the worst ones! / 最好的日子在哪？就在最差的日子旁边！
best10, worst10 = daily.nlargest(10), daily.nsmallest(10)
print()
print("The 10 best days / 最好的 10 天:")
for day, r in best10.items():
    near = [w for w in worst10.index if abs((w - day).days) <= 14]
    note = f"  ← within 2 weeks of a worst day ({near[0]:%Y-%m-%d}) / 与最差的一天相隔两周内" if near else ""
    print(f"  {day:%Y-%m-%d}  {r:+.1%}{note}")

plt.figure(figsize=(8, 5))
labels = ["stayed in", "missed 10 best", "missed 20 best", "missed 30 best"]
bars = plt.bar(labels, list(results.values()), color=["seagreen", "orange", "tomato", "firebrick"])
for b, v in zip(bars, results.values()):
    plt.text(b.get_x() + b.get_width() / 2, v + 800, f"${v:,.0f}", ha="center")
plt.title(f"${MONEY:,} in the S&P 500 (with dividends), 2006-2025")
plt.ylabel("final value ($)")
plt.tight_layout()
out = HERE / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "5_best_days.png", dpi=120)
print("Saved / 已保存: results/5_best_days.png")
plt.show()

# 🧪 Try it / 试一试:
#   1. What if you also missed the 10 WORST days? daily.drop(daily.nsmallest(10).index) / 如果同时错过最差的 10 天呢？
#   2. Change START to "1990-01-01". / 把起点改成 1990 年。
#   3. Why is it almost impossible to miss only the worst days? / 为什么几乎不可能只躲开最差的日子？
