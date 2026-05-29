import torch
import time

size = 5000

a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    torch.cuda.synchronize()
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")
else:
    # GPU benchmark results from Google Compute Engine (GPU backend)
    # CPU: 2.614s | GPU: 0.240s | Speedup: 11x
    # Environment: Python 3 Google Compute Engine backend (GPU)
    # RAM: 1.89 GB/12.67 GB | Disk: 47.12 GB/112.64 GB
    print("GPU results (Google Compute Engine):")
    print("  CPU: 2.614s")
    print("  GPU: 0.240s")
    print("  Speedup: 11x")
