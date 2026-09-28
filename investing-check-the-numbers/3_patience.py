"""
Step 3: how patience changes the odds of losing money (Episode 4).
第 3 步：耐心怎样改变亏钱的概率（第 4 集）。

For every possible starting year, we hold stocks for N years and check: did we lose money after inflation?
对每一个可能的起始年份，持有股票 N 年，然后检查：扣除通胀后亏钱了吗？

Run / 运行:   python 3_patience.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
df = pd.read_csv(HERE / "data" / "us_annual_returns_1928_2025.csv", index_col="year")
real = (1 + df["stocks"]) / (1 + df["inflation"])      # real growth factor each year / 每年的实际增长倍数

rows = []
for hold in [1, 5, 10, 15, 20]:
    # .rolling(hold).apply(prod) multiplies each window of `hold` years / 把每 hold 年的倍数连乘起来
    windows = real.rolling(hold).apply(lambda x: x.prod(), raw=True).dropna()
    per_year = windows ** (1 / hold) - 1
    lost = (windows < 1).mean()
    rows.append((hold, len(windows), lost, per_year.min(), per_year.max()))
    print(f"hold {hold:2d} yrs / 持有 {hold:2d} 年: {len(windows):3d} periods / 个区间, "
          f"lost money / 亏钱 {lost:6.1%},  worst / 最差 {per_year.min():+6.1%}/yr,  best / 最好 {per_year.max():+6.1%}/yr")

holds = [f"{r[0]} yr" for r in rows]
plt.figure(figsize=(8, 5))
bars = plt.bar(holds, [r[2] * 100 for r in rows], color="tomato")
for b, r in zip(bars, rows):
    plt.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.5, f"{r[2]:.1%}", ha="center")
plt.title("Chance of losing money after inflation, S&P 500, 1928-2025")
plt.xlabel("holding period")
plt.ylabel("% of periods that lost money")
plt.tight_layout()

out = HERE / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "3_patience.png", dpi=120)
print("Saved / 已保存: results/3_patience.png")
plt.show()

# 🧪 Try it / 试一试:
#   1. Do the same for bonds: replace df["stocks"] with df["bonds"]. / 换成债券试试。
#   2. Add a 30-year holding period. / 加一个 30 年的持有期。
#   3. Ignore inflation: real = 1 + df["stocks"]. How do the odds change? / 不考虑通胀，概率怎样变化？
