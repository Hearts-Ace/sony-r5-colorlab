# R5 Color Lab · v4.5 色卡版（BIN v4）

使用当前Python环境在本地浏览器拟合CC1、block13、Gamma和5×9×9网格。无需原研究工作区、Edit或RawAlchemy安装；不执行相机刷写。

## 2026-11-08 当前双平台正式实现

默认响应为 Hybrid 三专家 `r5-paired-20261107-nonlinear-he3`，固定模型 SHA256 `936af0b27f3c5f1ff422c20dd7c1436f92458407d1dd492a4edca2e5ef45e677`。正式入口固定十二起点原生基准、五轮目标网格和三轮叠加优化，两平台使用同一份训练约束。详情见 [TRAINING.md](TRAINING.md)。旧共享 C1 滤镜包保留独立历史身份，本次发布源码不代表新批次训练结果已全部完成。

CPU 与 Metal 已修复 PT 色相半索引边界精度：保留实采的全部 99,372 个色块中心五点输出一致。任意照片前端仍近似；这些验证只覆盖本次 PT 条件，未证明跨光源、所有创意外观或完整机内 ISP 等价。

## 启动

推荐Python 3.12，在本目录安装依赖：

```sh
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Windows使用`py -3`替代`python3`，或运行启动BAT；macOS可双击启动command。浏览器打开`http://127.0.0.1:4180`，仅监听本机。端口冲突可加`--port 4181`。关闭终端或Ctrl+C停止。

正式启动默认启用 GPU：macOS 使用 Metal/MPS（安装 `requirements-gpu.txt`），Windows AMD 使用 ROCm（安装说明见 [AMD.md](AMD.md)）。可显式指定 `--backend mac` 或 `--backend amd`。Mac 为 8 CPU线程／2并发，AMD 为 10 CPU线程／3并发；整数验收继续走 CPU。两平台共享 `web/data`，运行产物分别保存在各自目录。

## 色卡与目标图

默认使用 **v4.5 · 5300K · 一亿像素** 色卡，完整有效11648×8736，共99,372个32×32色块。Web提供Sony ARW、标准Sony DNG及GFX100S II RAF下载；[三格式色卡包与独立训练台下载](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware/releases/tag/colorlab-v4.5)。三种RAW在源码包内以gzip无损存储，下载时恢复原始字节并核验SHA256。

Sony RGGB白平衡为2606:1024:1024:1789，Bayer码值已反向补偿，以保持原色卡的Sony PT颜色标准；DNG保留同一码值、电平和WB，RAF经IED方案转换，未另加增益。在各软件保留拍摄白平衡；富士显示的Kelvin可能不同，不要据显示值强改5300K。14位信号、16位DNG容器不等于16位有效传感器精度。

从v4.5重新导出同尺寸RGB TIFF（推荐16位）或JPG，保留方向，不缩放、裁切或做几何修正。Adobe RGB等RGB ICC目标使用64位浮点ICC转换，先逐采样点转为sRGB、再取中心横向5点均值，无RGB8中间量化；超出sRGB的值裁切到有效范围。训练、压缩及评估统一使用中心5点均值。

ITP/拍摄WB→SSCS 模拟输入与保留 Edit PT 实采的 99,372块×9探针逐值一致。修复色相半索引计算后，全部色块中心五点输出一致；CPU 两平台全探针输出 SHA256 为 `e1149c1991bc6135b952a7dc48b9f45d3763e8a08f0472e4154049f8085b6a3b`。本次只修复颜色数值，不扩展空间处理或跨光源结论。

Web保留v4历史色卡选择，上传及任务按版本绑定；同尺寸旧目标不能直接切换为v4.5。历史v4与v4.5结果按各自目录及审计身份区分，不能混用输入版本。生成源码及依赖边界见[chart_sources/v4.5](chart_sources/v4.5/README.md)，验证摘要见[发布记录](../publication/colorlab-v4.5/edit-runtime-validation.json)。

## 训练与导出

导入目标TIFF/JPG或cube，设置独立配置序号、简称/全称、权重和平滑，进行原生参数拟合。支持文件夹批量训练，简称使用实际文件名stem，全称独立保存；批次完成后合并BIN。当前正式预算和叠加约束见 [正式训练方案](TRAINING.md)。

最终 405 节点整数网格直接拟合目标；BIN v4 写入原生 CC1、block13、Gamma 与 3×5×9×9 网格系数。导出前检查参数、目标与模型绑定；PC 响应模型不写入固件。

本次正式入口只接受固定 Hybrid 模型；历史结果需使用其对应提交回放。BIN只含整数网格系数，不把PC响应模型写入固件。任意照片RAW前端与空间处理预览仍为近似，不声称完整恢复相机ISP。

运行`python3 self_check.py`核对数据与模型，`python3 launcher.py --check`检查所选GPU与色相边界，`--test`运行回归。标定文件由`data_manifest.json`校验；合成capture报告仅脱敏本地路径，数值缓冲原样保留，manifest同时记录原报告与公开报告SHA256。`web/runs`、`web/batches`、上传/预览目录保存用户数据，不属于发布内容。

## 来源与许可

项目代码使用[GNU AGPL v3](LICENSE)。[致谢](ACKNOWLEDGEMENTS.md)、[数值来源](PROVENANCE.md)及`third_party/`记录QAQ MIT参考和其它第三方来源。Sony数值/合成色卡容器的来源不构成额外再许可。没有发布Sony完整应用、原机镜像、密钥或用户目标照片。离线拟合和格式校验通过不等于实际机内颜色验收。
