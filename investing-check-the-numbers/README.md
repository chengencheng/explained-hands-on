# Investing Explained #18 · Hands-on: Check the Numbers Yourself / 动手篇：用 Python 亲手验证这些数字

Start here / 从这里开始: **[教程_Guide.md](教程_Guide.md)** (step-by-step guide / 分步教程)

| Step | Script | Reproduces | Key output |
|---|---|---|---|
| 0 | `0_check_setup.py` | | checks pandas / matplotlib, downloads the daily prices |
| 1 | `1_compound.py` | Ep 1 | Emma $240,737 vs Ben $231,128 |
| 2 | `2_a_century_of_returns.py` | Ep 1, 4 | $100 (1928) → $61,799 after inflation in stocks; 26 of 98 years down |
| 3 | `3_patience.py` | Ep 4 | chance of a real loss, 1/5/10/15/20 yrs: 31.6 / 23.4 / 12.4 / 6.0 / 0% |
| 4 | `4_three_markets.py` | Ep 5 | 1997 = 100: S&P 857 (1,447 with dividends), Shanghai 324, Nikkei 329 |
| 5 | `5_best_days.py` | Ep 10 | $79,316 → $35,286 if you miss the 10 best days |
| 6 | `6_backtest_trap.py` | Ep 13 | best of 1,000 rules +6.4% → +7.8%; 0 of 1,000 beat buy & hold later |
| 7 | `7_roth_simulator.py` | Ep 17 | 10,000 futures: median $278K, 10th percentile $51K, 90th $1.45M |
| bonus | `8_bonus_any_stock.py` | Ep 6 | fresh data for any ticker (needs internet) |

Setup: `python -m venv .venv`, `.venv\Scripts\Activate.ps1`, `pip install pandas matplotlib yfinance`, `python 0_check_setup.py`.
Every script runs in a second or two. Real outputs and charts are in `参考结果_reference/`.

Data: `data/us_annual_returns_1928_2025.csv` from Aswath Damodaran (NYU Stern): S&P 500 with dividends, 10-yr Treasury bonds,
3-month T-bills, gold, CPI inflation. Daily closes (^GSPC, ^SP500TR, 000001.SS, ^N225) are downloaded from Yahoo Finance by step 0,
ending Sept 25 2026. Downloaded files were checked byte-for-byte against the ones used for the videos.

Education only, not investment advice. Past returns do not guarantee future returns.
