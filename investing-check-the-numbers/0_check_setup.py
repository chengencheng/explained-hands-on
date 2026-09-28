"""
Step 0: check that everything is installed, download the market data, and look at it.
第 0 步：检查环境是否装好，下载市场数据，并看一眼。

Run / 运行:   python 0_check_setup.py

The yearly returns file (from Prof. Aswath Damodaran, NYU Stern) is included in data/.
The daily index prices come from Yahoo Finance, so they are downloaded here instead of being shared in this repository.
年度收益率文件（来自纽约大学达摩达兰教授）已经放在 data/ 里。
每日指数价格来自雅虎财经，所以不直接放在仓库里，而是由这个程序下载。
"""
import sys
from pathlib import Path

# Stop at the same day as the guide and the videos, so your numbers match exactly.
# Set END = None to download everything up to today (your numbers will then differ a little).
# 截止到和教程、视频相同的日期，这样你的结果会完全一样。改成 END = None 可以下载到今天的最新数据（结果会略有不同）。
END = "2026-09-26"

print("Python version / Python 版本:", sys.version.split()[0])
try:
    import numpy
    import pandas as pd
    import matplotlib
except ImportError as e:
    print("❌ Missing package / 缺少工具包:", e.name)
    print("   Run / 请运行:  pip install pandas matplotlib yfinance")
    sys.exit(1)
print("numpy", numpy.__version__, "· pandas", pd.__version__, "· matplotlib", matplotlib.__version__)
print()

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

# file name → (Yahoo tickers, start date) / 文件名 → （雅虎代码，起始日期）
FILES = {
    "sp500_daily_1928_2026.csv": (["^GSPC"], "1928-01-01"),
    "sp500_total_return_daily_1988_2026.csv": (["^SP500TR"], "1988-01-01"),
    "nikkei_daily_1965_2026.csv": (["^N225"], "1965-01-01"),
    "world_markets_daily_1997_2026.csv": (["^GSPC", "^SP500TR", "000001.SS", "^N225"], "1997-07-02"),
}
COLUMNS = {"^GSPC": "sp500", "^SP500TR": "sp500_total_return", "000001.SS": "shanghai", "^N225": "nikkei"}

missing = [f for f in FILES if not (DATA / f).exists()]
if missing:
    try:
        import yfinance as yf
    except ImportError:
        print("❌ Please install yfinance first / 请先安装 yfinance:  pip install yfinance")
        sys.exit(1)
    print("Downloading daily prices from Yahoo Finance (about 1 minute) / 正在从雅虎财经下载每日价格（约 1 分钟）...")
    for name in missing:
        tickers, start = FILES[name]
        raw = yf.download(tickers, start=start, end=END, auto_adjust=False, progress=False)["Close"]
        if raw.empty:
            print(f"❌ Download failed for {name}. Check the internet, then try  pip install -U yfinance")
            print(f"   {name} 下载失败。请检查网络，然后试试 pip install -U yfinance")
            sys.exit(1)
        if len(tickers) == 1:
            table = raw[tickers[0]].dropna().rename("close").to_frame()
        else:
            table = raw[tickers].rename(columns=COLUMNS).dropna(how="all")
        if table.index.tz is not None:
            table.index = table.index.tz_localize(None)
        table.round(2).rename_axis("date").to_csv(DATA / name, date_format="%Y-%m-%d")
        print(f"  ✅ {name}")
    print()

for f in sorted(DATA.glob("*.csv")):
    df = pd.read_csv(f)
    first, last = df.iloc[0, 0], df.iloc[-1, 0]
    print(f"✅ {f.name:45s} {len(df):6,d} rows / 行   {first} → {last}")

print()
print("A peek at the yearly returns / 看一眼年度收益率数据:")
print(pd.read_csv(DATA / "us_annual_returns_1928_2025.csv").tail(5).to_string(index=False))
print()
print("All good! Next / 一切就绪！下一步:  python 1_compound.py")
