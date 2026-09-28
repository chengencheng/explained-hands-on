"""
Step 0: check that everything is installed.
第 0 步：检查环境是否装好。

Run / 运行:   python 0_check_setup.py
"""
import sys
import time

print("Python version / Python 版本:", sys.version.split()[0])

try:
    import torch
except ImportError:
    print("❌ PyTorch is not installed. See step 0 in the guide. / 没有装 PyTorch，请看教程第 0 步。")
    sys.exit(1)

print("PyTorch version / PyTorch 版本:", torch.__version__)

if torch.cuda.is_available():
    print("✅ GPU found / 找到显卡:", torch.cuda.get_device_name(0))
    device = "cuda"
else:
    print("⚠️  No GPU found, will use the CPU (slower, but it still works). / 没找到显卡，会用 CPU（慢一些，但也能跑）。")
    device = "cpu"

# A quick speed test: multiply two big 4096 x 4096 matrices (remember Episode 9?)
# 小测速：两个 4096×4096 的大矩阵相乘（还记得第 9 集吗？）
a = torch.randn(4096, 4096, device=device)
b = torch.randn(4096, 4096, device=device)
a @ b  # warm-up / 热身
if device == "cuda":
    torch.cuda.synchronize()
t0 = time.time()
for _ in range(10):
    c = a @ b
if device == "cuda":
    torch.cuda.synchronize()
seconds = (time.time() - t0) / 10
tflops = 2 * 4096**3 / seconds / 1e12
print(f"One 4096×4096 matrix multiply: {seconds * 1000:.1f} ms  (≈ {tflops:.0f} trillion operations per second)")
print(f"一次 4096×4096 矩阵乘法：{seconds * 1000:.1f} 毫秒（约每秒 {tflops:.0f} 万亿次运算）")

for name in ["torchvision", "matplotlib"]:
    try:
        __import__(name)
        print(f"✅ {name} OK")
    except ImportError:
        print(f"❌ {name} is missing / 没有装 {name}")

print("\nAll set! Next: python 1_train_digits.py   / 准备好了！下一步：python 1_train_digits.py")
