"""
Step 6: the backtest trap: 1,000 random trading rules (Episode 13).
第 6 步：回测陷阱：一千条随机交易规则（第 13 集）。

Each rule: be in the S&P 500 only when a short moving average is above a long one,
and only in some randomly chosen months and weekdays. Otherwise hold cash (earning 0%, to keep it simple).
每条规则：只有当短期均线高于长期均线时才持有标普 500，而且只在随机选中的月份和星期几持有；其余时间持有现金（为简单起见，收益记为 0）。

We pick the best rule on 2000-2012, then test it on 2013-2025, data it has never seen.
在 2000-2012 年挑出最好的规则，再用它从没见过的 2013-2025 年数据检验。

Run / 运行:   python 6_backtest_trap.py      (takes a few seconds / 几秒钟)
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
price = pd.read_csv(HERE / "data" / "sp500_daily_1928_2026.csv", index_col="date", parse_dates=True)["close"]
price = price.loc["1999-01-01":"2025-12-31"]      # 1999 gives the moving averages a warm-up year / 1999 年用来 “预热” 均线
daily = price.pct_change().fillna(0)

train = (price.index >= "2000-01-01") & (price.index <= "2012-12-31")   # where we choose / 用来挑选规则
test = price.index >= "2013-01-01"                                     # never seen / 从没见过的数据


def per_year(returns, period):
    """Average growth per year over the days in `period`. / 该时段内的年均增长率。"""
    r = returns[period]
    years = period.sum() / 252          # about 252 trading days a year / 每年约 252 个交易日
    return (1 + r).prod() ** (1 / years) - 1


hold_train, hold_test = per_year(daily, train), per_year(daily, test)
print(f"Buy and hold / 买入持有:  2000-2012 {hold_train:+.1%}/yr   2013-2025 {hold_test:+.1%}/yr")

rng = np.random.default_rng(7)          # fixed seed, so you get the same rules as the video / 固定随机种子，和视频一样
months, weekdays = price.index.month.values, price.index.dayofweek.values
results = []
for k in range(1000):
    short = int(rng.integers(3, 60))                     # short moving average, days / 短期均线天数
    long = int(rng.integers(short + 5, 260))             # long moving average, days / 长期均线天数
    signal = (price.rolling(short).mean() > price.rolling(long).mean()).astype(float).values
    use_month = rng.random(12) < 0.75                    # e.g. "never hold in March" / 比如 “三月不持有”
    use_day = rng.random(5) < 0.8                        # e.g. "never hold on Fridays" / 比如 “周五不持有”
    signal = signal * use_month[months - 1] * use_day[weekdays]
    position = pd.Series(signal, index=price.index).shift(1).fillna(0)   # decide today, hold tomorrow / 今天决定，明天持有
    returns = position * daily
    results.append((per_year(returns, train), per_year(returns, test), short, long))

res = pd.DataFrame(results, columns=["train", "test", "short", "long"])
best = res.loc[res["train"].idxmax()]
print(f"Best rule / 最好的规则 (MA {best.short:.0f} vs {best.long:.0f}):  "
      f"2000-2012 {best.train:+.1%}/yr  →  2013-2025 {best.test:+.1%}/yr")
print(f"Rules beating buy & hold / 跑赢买入持有的规则:  2000-2012: {(res.train > hold_train).sum()} of 1,000   "
      f"2013-2025: {(res.test > hold_test).sum()} of 1,000")

plt.figure(figsize=(8, 6))
plt.scatter(res.train * 100, res.test * 100, s=8, alpha=0.5, label="1,000 random rules")
plt.scatter([best.train * 100], [best.test * 100], s=120, color="red", label="best on 2000-2012")
plt.axvline(hold_train * 100, color="orange", ls="--", label="buy & hold")
plt.axhline(hold_test * 100, color="orange", ls="--")
plt.xlabel("yearly return 2000-2012 (%)  ← where the rule was chosen")
plt.ylabel("yearly return 2013-2025 (%)  ← never seen")
plt.title("Looks great in the past ≠ works in the future")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
out = HERE / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "6_backtest_trap.png", dpi=120)
print("Saved / 已保存: results/6_backtest_trap.png")
plt.show()

# 🧪 Try it / 试一试:
#   1. Change the seed from 7 to another number. Does any rule beat buy & hold in 2013-2025? / 换一个随机种子试试。
#   2. Swap the periods: choose on 2013-2025, test on 2000-2012. / 把两个时段对调。
#   3. Add a trading cost: returns = position * daily - 0.0005 * position.diff().abs() / 加上交易成本。
