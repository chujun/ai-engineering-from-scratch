# GPU 学习与测试方法

## 选项 1：本地 NVIDIA 显卡

### 检查是否拥有显卡

```bash
nvidia-smi
```

### 安装带有 CUDA 功能的 PyTorch

```bash
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 验证 PyTorch CUDA

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

---

## 选项 2：Google Colab（推荐无本地 GPU 时使用）

1. 访问 [colab.research.google.com](https://colab.research.google.com)
2. Runtime > Change runtime type > **T4 GPU**（免费）
3. 运行 `!nvidia-smi` 验证 GPU
4. 将本课程笔记本直接上传到 Colab

---

## CUDA 问题排查

### 问题 1：nvidia-smi 命令找不到

```bash
# 检查 NVIDIA 驱动是否安装
ls /usr/bin/nvidia-smi

# 重新安装驱动（Ubuntu）
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

### 问题 2：CUDA available 为 False，但 nvidia-smi 正常

常见原因：PyTorch CUDA 版本与驱动版本不匹配

```python
# 检查驱动支持的 CUDA 版本
nvidia-smi

# 检查 PyTorch 编译时使用的 CUDA 版本
python -c "import torch; print(torch.version.cuda)"

# 规则：PyTorch CUDA 版本必须 <= 驱动 CUDA 版本
```

**解决方法：**

```bash
# 重新安装匹配驱动版本的 PyTorch
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121  # CUDA 12.1
```

### 问题 3：GPU 显存不足（OOM）

```python
# 清理缓存
import torch
torch.cuda.empty_cache()

# 或减少 batch size
```

### 问题 4：Google Colab GPU 不可用

- 检查 Runtime > Change runtime type 是否设置为 GPU
- 免费版 Colab 有使用时限（约 90 分钟）
- 切换到 Kaggle Notebooks 作为替代（免费 P100，每周 30 小时）

### 问题 5：WINDOWS WSL2 环境 GPU 问题

```powershell
# 在 PowerShell（管理员）中安装 Windows NVIDIA 驱动（不是 Linux 驱动）
# WSL2 会自动共享 Windows 侧的 GPU
wsl --install -d Ubuntu-24.04
```

### 快速检查清单

```python
# 一行检查所有关键信息
import torch
print(f"Driver CUDA: {torch.version.cuda}")
print(f"PyTorch CUDA: {torch.version.cuda}")
print(f"GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

---

## Jupyter Lab 服务启动

Jupyter Lab 是进行 AI 实验的交互式开发环境。

### 启动 Jupyter Lab 服务

```bash
# 使用服务脚本管理
./my-shells/start-jupyter-lab-service.sh start

# 或直接启动（适用于临时使用）
jupyter lab --no-browser --port=8888 --ip=0.0.0.0 --allow-root
```

### 服务管理命令

```bash
./my-shells/start-jupyter-lab-service.sh start    # 启动服务
./my-shells/start-jupyter-lab-service.sh stop     # 停止服务
./my-shells/start-jupyter-lab-service.sh restart  # 重启服务
./my-shells/start-jupyter-lab-service.sh status  # 查看状态
```

### 访问方式

- **本地访问**: http://localhost:8888
- **远程访问**: http://<服务器IP>:8888
- 首次登录需要输入终端输出的 token

### 获取 Token（如果需要重新获取）

```bash
jupyter server list
```

### 日志位置

- 服务日志: `/tmp/jupyter-logs/jupyter-lab.log`
- PID 文件: `/tmp/jupyter-lab.pid`
