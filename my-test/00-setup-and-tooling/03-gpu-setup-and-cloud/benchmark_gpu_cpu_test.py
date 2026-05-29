"""
GPU vs CPU 矩阵运算性能对比脚本
用于比较 PyTorch 在 GPU 和 CPU 上执行矩阵乘法的性能差异

学习要点：
1. torch.randn() - 创建随机张量
2. @ 运算符 - 矩阵乘法 (torch.matmul)
3. torch.cuda.is_available() - 检查 GPU 是否可用
4. .to("cuda") - 将张量从 CPU 复制到 GPU
5. torch.cuda.synchronize() - 等待 GPU 计算完成
"""

import torch
import time

# =============================================================================
# 1. 创建测试数据 - 使用 5000x5000 的随机矩阵
# =============================================================================
# 矩阵大小：5000行 x 5000列
# 内存占用：5000 * 5000 * 4字节(float32) ≈ 100MB per matrix
size = 5000

# torch.randn() - 创建标准正态分布(均值0,方差1)的随机张量
# 默认创建在 CPU 上
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

# =============================================================================
# 2. CPU 矩阵乘法性能测试
# =============================================================================
# 记录开始时间
start = time.time()

# @ 运算符等价于 torch.matmul()，执行矩阵乘法
# CPU 矩阵乘法: O(n³) 复杂度，n=5000 约需数十秒
c_cpu = a_cpu @ b_cpu

# 计算 CPU 耗时
cpu_time = time.time() - start
print(f"比较GPU与CPU执行效率")
print(f"CPU: {cpu_time:.3f}s")

# =============================================================================
# 3. GPU 矩阵乘法性能测试
# =============================================================================
if torch.cuda.is_available():
    # 将数据从 CPU 内存复制到 GPU 显存
    # 这是数据传输开销，在计时之前已完成（不影响 GPU 计算计时）
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    # 关键：等待 GPU 完成所有待处理的 CUDA 操作
    # GPU 操作是异步的，如果不等待，计时会不准确
    torch.cuda.synchronize()

    # 记录 GPU 计算开始时间
    start = time.time()

    # 在 GPU 上执行矩阵乘法
    # GPU 矩阵乘法利用数千个并行核心，比 CPU 快 10-100 倍
    c_gpu = a_gpu @ b_gpu

    # 再次同步：确保 GPU 计算完成后再记录结束时间
    torch.cuda.synchronize()

    # 计算 GPU 耗时
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")  # 加速比 = CPU时间 / GPU时间
else:
    # 无 GPU 时的备用输出（参考数据）
    # GPU benchmark results from Google Compute Engine (GPU backend)
    # CPU: 2.614s | GPU: 0.240s | Speedup: 11x
    # Environment: Python 3 Google Compute Engine backend (GPU)
    # RAM: 1.89 GB/12.67 GB | Disk: 47.12 GB/112.64 GB
    print("GPU results (Google Compute Engine):")
    print("  CPU: 2.614s")
    print("  GPU: 0.240s")
    print("  Speedup: 11x")
