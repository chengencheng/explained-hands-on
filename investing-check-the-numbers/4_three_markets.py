"""
Step 4: choosing the market: America vs China vs Japan (Episode 5).
第 4 步：选择市场：美国 vs 中国 vs 日本（第 5 集）。

Data: daily closing prices from Yahoo Finance (^GSPC, ^SP500TR, 000001.SS, ^N225).
数据：雅虎财经的每日收盘价（标普 500、标普 500 全收益、上证综指、日经 225）。

Run / 运行:   python 4_three_markets.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
w = pd.read_csv(HERE / "data" / "world_markets_daily_1997_2026.csv", index_col="date", parse_dates=True)

names = {"sp500": "S&P 500 (price)", "sp500_total_return": "S&P 500 (with dividends)",
         "shanghai": "Shanghai Composite", "nikkei": "Nikkei 225"}

print(f"Start at 100 on {w.index[0]:%Y-%m-%d} / {w.index[0]:%Y-%m-%d} 起点设为 100:")
plt.figure(figsize=(10, 5.5))
for col, name in names.items():
    s = w[col].dropna()                    # each market has its own holidays / 各市场假日不同
    s = 100 * s / s.iloc[0]                # rescale so the start = 100 / 把起点换算成 100
    years = (s.index[-1] - s.index[0]).days / 365.25
    per_year = (s.iloc[-1] / 100) ** (1 / years) - 1
    print(f"  {name:26s} → {s.iloc[-1]:7,.0f}   ({per_year:+.1%} a year / 每年)")
    plt.plot(s.index, s, label=name, lw=2)

plt.title("Three markets, all starting at 100 in July 1997 (price indexes, local currency)")
plt.ylabel("value (start = 100)")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
out = HERE / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "4_three_markets.png", dpi=120)
print("Saved / 已保存: results/4_three_markets.png")


def peak_and_recovery(s, label):
    """Find the highest point before the worst fall, the bottom, and when it got back.
    找出最大跌幅前的最高点、最低点，以及何时回到最高点。"""
    running_peak = s.cummax()                 # highest price so far / 到目前为止的最高价
    drawdown = s / running_peak - 1           # how far below that peak / 比最高点低多少
    bottom_day = drawdown.idxmin()
    peak_day = s.loc[:bottom_day].idxmax()
    after = s.loc[bottom_day:]
    back = after[after >= s[peak_day]]
    got_back = f"{back.index[0]:%Y-%m-%d} ({(back.index[0] - peak_day).days / 365.25:.1f} years later / 年后)" \
        if len(back) else "not yet / 尚未回到"
    print(f"  {label}: peak / 高点 {s[peak_day]:,.0f} on {peak_day:%Y-%m-%d} → "
          f"bottom / 低点 {s[bottom_day]:,.0f} ({drawdown.min():.0%}) → back / 回到高点: {got_back}")


print()
print("Biggest falls / 最大跌幅:")
peak_and_recovery(w["shanghai"].dropna(), "Shanghai 上证")
nk = pd.read_csv(HERE / "data" / "nikkei_daily_1965_2026.csv", index_col="date", parse_dates=True)["close"]
peak_and_recovery(nk, "Nikkei 日经 (since 1965)")
peak_and_recovery(w["sp500"].dropna(), "S&P 500 标普")
plt.show()

# 🧪 Try it / 试一试:
#   1. Start in 2009 instead:  w = w.loc["2009-03-09":]   Does the ranking change? / 从 2009 年开始，排名会变吗？
#   2. Find Shanghai's highest close ever: w["shanghai"].max() and .idxmax() / 找上证历史最高收盘价
#   3. Why is "with dividends" so much higher? (Episode 2) / 为什么 “含分红” 高这么多？
