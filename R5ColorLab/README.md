# R5 Color Lab · v4.5 色卡版（BIN v4）

使用当前Python环境在本地浏览器拟合CC1、block13、Gamma和5×9×9网格。无需原研究工作区、Edit或RawAlchemy安装；不执行相机刷写。

## 2026-11-02 当前训练实现

默认网格响应采用无专家共享 C1：`r5-paired-20261102-shared-c1-c50`，固定模型 SHA256 `e794ece2fe8f4114eb241e376918bffbc4c182e9fadf0f6fa21d99fdd7a1b552`。采用81×3共享分段权重，曲率50%、一阶结构与稀疏残差收缩，不使用色相专家；沿用原生 5×9×9 三线性查询和 1215 个整数系数。CPU、Metal、整数微调、连续性与照片预览共用同一模型。它仍是本次 PT 实拍条件下的经验预测器，不代表已恢复相机 ISP。

平滑现在按各原生算子的作用约束：CC1 的分支雅可比、block13 的实际扇区插值及线性／二次 RGB 作用、Gamma 的真实非均匀横坐标斜率／曲率。最终网格在固定亮度、色相、饱和度和中性直线路径上约束实际 preclip 修正的一、二阶变化，不直接惩罚相邻裸系数。原完整输出的暗部／色相／饱和度连续性约束继续保留。算法允许合理局部变化，不强制色相角单调，也不保证全域 C1。

新结果绑定模型、注册表与实际 CPU／GPU 推理源码指纹；历史 v2 和非线性结果仅经已知源码白名单及原类逐值对照兼容，不改历史参数或 BIN。自由 PC tone-tint 教师仍是原生参数搜索的辅助模型；最终 `fuji-target` 网格直接拟合富士目标。正式训练预算、平滑30／连续性30及压缩后不交替、不做灰阶微调保持，详见 [TRAINING.md](TRAINING.md)。

当前十二款正式滤镜已全部完成，批次 `c29ff1d3ef314d718ab370cf6ed2bfb6`。下载 [R5NATIVE.BIN、可编辑配置与训练／数值回执](../filters/FUJ_12_v45_shared_c1_20261104/)；BIN SHA256 为 `2e9c60c1f7858940e366aa1b0f2c0c089347445c9c286c0c938a40a35610caee`。兼容4.48声音版及支持本项目BIN v4的固件。旧批次保留其独立模型身份。

## 启动

推荐Python 3.12，在本目录安装依赖：

```sh
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Windows使用`py -3`替代`python3`，或运行启动BAT；macOS可双击启动command。浏览器打开`http://127.0.0.1:4180`，仅监听本机。端口冲突可加`--port 4181`。关闭终端或Ctrl+C停止。

CPU为默认后端；Apple Silicon可安装`requirements-gpu.txt`并设置`R5_GPU_TRAINING=1`启用Metal/MPS。最终配置仍经过整数参数及CPU数值校验；本包不自动安装PyTorch。AMD专用包是独立工具，本包未验证AMD设备。

## 色卡与目标图

默认使用 **v4.5 · 5300K · 一亿像素** 色卡，完整有效11648×8736，共99,372个32×32色块。Web提供Sony ARW、标准Sony DNG及GFX100S II RAF下载；[三格式色卡包与独立训练台下载](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware/releases/tag/colorlab-v4.5)。三种RAW在源码包内以gzip无损存储，下载时恢复原始字节并核验SHA256。

Sony RGGB白平衡为2606:1024:1024:1789，Bayer码值已反向补偿，以保持原色卡的Sony PT颜色标准；DNG保留同一码值、电平和WB，RAF经IED方案转换，未另加增益。在各软件保留拍摄白平衡；富士显示的Kelvin可能不同，不要据显示值强改5300K。14位信号、16位DNG容器不等于16位有效传感器精度。

从v4.5重新导出同尺寸RGB TIFF（推荐16位）或JPG，保留方向，不缩放、裁切或做几何修正。Adobe RGB等RGB ICC目标使用64位浮点ICC转换，先逐采样点转为sRGB、再取中心横向5点均值，无RGB8中间量化；超出sRGB的值裁切到有效范围。训练、压缩及评估统一使用中心5点均值。

ITP/拍摄WB→SSCS的纯模拟输入已与新版Edit PT实采核对：全部99,372块×9探针RGB逐值一致。实采最终输出与TIFF编码逐值一致；完整PT颜色模拟99,371块一致，仅第59,361块（从0编号）G差11个原生码值，约0.17/255。实采仅作独立验证，不回填训练输入、不增加颜色补偿。任意照片的空间处理前端仍近似。

Web保留v4历史色卡选择，上传及任务按版本绑定；同尺寸旧目标不能直接切换为v4.5。历史v4与v4.5结果按各自目录及审计身份区分，不能混用输入版本。生成源码及依赖边界见[chart_sources/v4.5](chart_sources/v4.5/README.md)，验证摘要见[发布记录](../publication/colorlab-v4.5/edit-runtime-validation.json)。

## 训练与导出

导入目标TIFF/JPG或cube，设置独立配置序号、简称/全称、权重和平滑，进行原生参数拟合。支持文件夹批量训练，简称使用实际文件名stem，全称独立保存；批次完成后合并BIN。最新12滤镜正式训练使用精度预算2000、12起点、8动态轮、压缩前Gamma/色彩交替3轮及量化3轮、参数平滑30、输出连续性30。详见[正式训练方案](TRAINING.md)。

自动压缩训练默认`fuji-target`：最终405节点整数网格直接拟合目标图，仅使用训练集优化；`pc-teacher`保留为显式可选研究目标。压缩后原生参数/网格交替以及灰阶微调关闭，压缩前交替保留。必要的3×5×9×9系数与原生参数一起写入BIN v4，旧BIN格式不兼容。导出前必须选择来源固定的原厂网格或完成网格拟合，服务端校验参数/目标/模型绑定。

历史 `r5-paired-20261024-v2` 和 `r5-paired-20261102-nonlinear` 继续按保存身份回放；它们不是当前新任务默认。BIN只含整数网格系数，不把PC响应模型写入固件。任意照片RAW前端与空间处理预览仍为近似，不声称完整恢复相机ISP。

运行`python3 launcher.py --check`核对数据与模型，`--test`运行回归。标定文件由`data_manifest.json`校验；合成capture报告仅脱敏本地路径，数值缓冲原样保留，manifest同时记录原报告与公开报告SHA256。`web/runs`、`web/batches`、上传/预览目录保存用户数据，不属于发布内容。

## 来源与许可

项目代码使用[GNU AGPL v3](LICENSE)。[致谢](ACKNOWLEDGEMENTS.md)、[数值来源](PROVENANCE.md)及`third_party/`记录QAQ MIT参考和其它第三方来源。Sony数值/合成色卡容器的来源不构成额外再许可。没有发布Sony完整应用、原机镜像、密钥或用户目标照片。离线拟合和格式校验通过不等于实际机内颜色验收。
