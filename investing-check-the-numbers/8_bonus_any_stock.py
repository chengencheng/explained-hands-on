"""
Bonus: download fresh data for any stocks or funds, and compare them.
附加题：下载任意股票或基金的最新数据，并进行比较。

Needs the internet and one more package / 需要联网，并多装一个工具包:
    pip install yfinance

Run / 运行:   python 8_bonus_any_stock.py
       or / 或者:   python 8_bonus_any_stock.py AAPL MSFT KO SPY
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt

try:
    import yfinance as yf
except ImportError:
    print("Please run / 请先运行:  pip install yfinance")
    sys.exit(1)

TICKERS = sys.argv[1:] or ["SPY", "AAPL", "KO", "GE"]    # SPY = an S&P 500 index fund / SPY 是标普 500 指数基金
START = "2006-01-01"

# auto_adjust=True: prices include dividends and splits, like a "total return" / 价格已包含分红和拆股的调整
data = yf.download(TICKERS, start=START, auto_adjust=True, progress=False)["Close"]
if data.empty:
    print("No data downloaded. Check the internet and the ticker symbols. / 没有下载到数据，请检查网络和股票代码。")
    sys.exit(1)

print(f"$10,000 invested on {data.index[0]:%Y-%m-%d} → {data.index[-1]:%Y-%m-%d} / 投入 1 万美元:")
plt.figure(figsize=(10, 5.5))
for t in data.columns:
    s = data[t].dropna()
    value = 10_000 * s / s.iloc[0]
    worst = (s / s.cummax() - 1).min()          # biggest fall from a high / 从高点的最大跌幅
    print(f"  {t:6s} ${value.iloc[-1]:>10,.0f}    biggest fall / 最大跌幅 {worst:.0%}")
    plt.plot(value.index, value, label=t, lw=2)

plt.yscale("log")
plt.title(f"$10,000 invested in {START[:4]} (dividends reinvested, log scale)")
plt.grid(alpha=0.3, which="both")
plt.legend()
plt.tight_layout()
out = Path(__file__).parent / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "8_any_stock.png", dpi=120)
print("Saved / 已保存: results/8_any_stock.png")
plt.show()

# 🧪 Try it / 试一试:
#   python 8_bonus_any_stock.py SPY QQQ GLD TLT      (stocks, tech, gold, long bonds / 股票、科技、黄金、长期债券)
#   Chinese A-shares use .SS or .SZ, e.g. 600519.SS; Hong Kong uses .HK, e.g. 0700.HK / A 股加 .SS 或 .SZ，港股加 .HK
#   Remember Episode 6: picking the one winner in advance is the hard part! / 记住第 6 集：事先挑中赢家才是最难的！
