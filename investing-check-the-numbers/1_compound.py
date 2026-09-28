"""
Step 1: compound interest, the twins Emma and Ben (Episode 1).
第 1 步：复利，双胞胎艾玛和本（第 1 集）。

Run / 运行:   python 1_compound.py
"""
import math
from pathlib import Path
import matplotlib.pyplot as plt

RATE = 0.07        # growth per year, after inflation / 每年增长率（扣除通胀后）
MONTHLY = 100      # dollars added each month / 每月存入的美元


def balances(start_age, stop_age, rate=RATE, monthly=MONTHLY, end_age=65):
    """Balance at each age (16 to 65). Money is added at the start of each month.
    每个年龄（16 到 65 岁）时的余额。每月月初存钱。"""
    monthly_rate = (1 + rate) ** (1 / 12) - 1      # 7% a year ≈ 0.565% a month / 年 7% ≈ 月 0.565%
    balance = 0.0
    by_age = {16: 0.0}
    for month in range(16 * 12, end_age * 12):
        age = month / 12
        if start_age <= age < stop_age:
            balance += monthly                      # add money / 存钱
        balance *= 1 + monthly_rate                 # grow for one month / 增长一个月
        if (month + 1) % 12 == 0:
            by_age[(month + 1) // 12] = balance
    return by_age


emma = balances(16, 26)        # Emma: 16 to 26, then stops / 艾玛：16 到 26 岁，然后停止
ben = balances(26, 65)         # Ben: 26 to 65 / 本：26 到 65 岁
emma_all = balances(16, 65)    # Emma keeps going / 艾玛一直坚持

print(f"Emma put in / 艾玛存入      ${10 * 12 * MONTHLY:>9,}  → at 65 / 65 岁时 ${emma[65]:>10,.0f}")
print(f"Ben put in  / 本存入        ${39 * 12 * MONTHLY:>9,}  → at 65 / 65 岁时 ${ben[65]:>10,.0f}")
print(f"Emma, 16-65 / 艾玛坚持到 65 ${49 * 12 * MONTHLY:>9,}  → at 65 / 65 岁时 ${emma_all[65]:>10,.0f}")

# The rule of 72: money doubles in about 72 / rate years. / 72 法则：翻倍大约需要 72 ÷ 利率 年。
for r in [0.04, 0.07, 0.10]:
    exact = math.log(2) / math.log(1 + r)      # solve (1 + r) ** years = 2 / 解方程 (1+r)^years = 2
    print(f"At {r:.0%}: rule of 72 says {72 / (r * 100):.1f} years, exact answer {exact:.2f} years "
          f"/ 利率 {r:.0%}：72 法则估计 {72 / (r * 100):.1f} 年，精确答案 {exact:.2f} 年")

# Draw it / 画图
ages = list(emma.keys())
plt.figure(figsize=(9, 5))
plt.plot(ages, [emma[a] for a in ages], label="Emma: $100/month, age 16-26", lw=3)
plt.plot(ages, [ben[a] for a in ages], label="Ben: $100/month, age 26-65", lw=3)
plt.plot(ages, [emma_all[a] for a in ages], label="Emma if she kept going", ls="--")
plt.xlabel("age")
plt.ylabel("balance ($, today's money)")
plt.title(f"The twins, growing {RATE:.0%} a year after inflation")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

out = Path(__file__).parent / "results"
out.mkdir(exist_ok=True)
plt.savefig(out / "1_twins.png", dpi=120)
print("Saved / 已保存: results/1_twins.png")
plt.show()

# 🧪 Try it / 试一试:
#   1. Change RATE to 0.04 or 0.10. Who wins now? / 把 RATE 改成 0.04 或 0.10，现在谁赢？
#   2. What if Ben invests $200 a month? / 如果本每月存 200 美元呢？  balances(26, 65, monthly=200)
#   3. At what age would Ben need to start to beat Emma with $100 a month? / 本最晚几岁开始，才能赢过艾玛？
