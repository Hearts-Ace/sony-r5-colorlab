# AMD Windows 正式训练工作台

与 Mac 最新正式方案使用相同目标、数学约束和选优规则。当前默认 **CPU 10线程、3个滤镜并发**；ROCm经PyTorch的`cuda`命名空间使用AMD显卡。`torch.set_num_threads(10)`控制CPU运算，不控制GPU线程数。原生整数验收、ICC转换和数值梯度使用CPU，浮点拟合和网格优化使用GPU。

使用Python 3.12及AMD支持的显卡/驱动组合。先按[AMD官方Windows PyTorch说明](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/windows/install-pytorch.html)安装匹配硬件的ROCm PyTorch；普通CPU或NVIDIA构建不能替代。已运行环境为RX7900XTX、PyTorch `2.9.0+rocmsdk20251116`、HIP `7.1.52802-561cc400e1`，这些是验证环境标识，不是对所有Windows硬件的兼容承诺。

在`R5ColorLab`目录运行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-amd.txt
# 在同一虚拟环境中安装AMD官方支持的ROCm PyTorch，然后自检：
.\.venv\Scripts\python.exe formal_launcher.py --backend amd --check
.\.venv\Scripts\python.exe formal_launcher.py --backend amd
```

浏览器打开`http://127.0.0.1:4180/`。默认仅监听本机；如需局域网访问，可显式加`--host 0.0.0.0 --lan-address 你的局域网IP`，并配置Windows防火墙。未内嵌作者的IP、账号或密码。

界面导入当前v4.5色卡导出的目标文件夹，按正式配方训练1–12项，完成后下载整批BIN。每个平台的`runs/`、`batches/`、`chart_uploads/`独立保存在平台目录，数据/数值表共用`web/data/`；请保留整个项目目录结构。Mac运行历史和Windows运行历史不会自动迁移，原有用户目标与训练结果不在源码发布中。

当前流程为原生12起点→五轮目标网格→三轮五项叠加，详见[TRAINING.md](TRAINING.md)。GPU不可用时正式训练停止并报错，不静默切CPU。20线程/6并发曾是中间运行设置，已按用户要求改为10线程/3并发；源码以当前值为准。

Ctrl+C停止服务；关闭服务会中断当前任务。长时间训练请在本机终端/服务管理器中持续运行，不将远程SSH会话当作持久任务管理器。当前发布包含可重用正式服务，不自动启动作者的批次或复用半成品。
