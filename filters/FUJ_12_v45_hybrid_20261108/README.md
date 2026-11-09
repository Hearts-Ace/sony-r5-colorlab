# Hybrid 十二款滤镜（Windows AMD，2026-11-08 批次）

[下载 R5NATIVE.BIN](R5NATIVE.BIN) · [可编辑配置](native_config.json)

最新完成批次：`8911457906ba4538b682dee98485a151`，12 款全部完成，Windows AMD ROCm，CPU 15 线程、6 并发。2026-11-09 发布。

顺序：AS / CC / EBB / ET / NC / NH / PV / RA / VN / 正片 / 负片 / Portra400。

使用固定 Hybrid 三专家模型 `r5-paired-20261107-nonlinear-he3`（SHA256 `936af0b27f3c5f1ff422c20dd7c1436f92458407d1dd492a4edca2e5ef45e677`），包含 PT 色相精度修复；原生 12 起点、五轮网格、三轮叠加，同向约束 30、目标导数 0.02、叠加阶段 Gamma 冻结，validation 选优。

BIN 为 v4 格式，29552 字节，包含整套十二项。导入会替换整套自定义滤镜，需要支持 BIN v4 的固件。电脑端 Hybrid 响应用于拟合，文件保存原生参数及最终整数网格；本次发布不代表新的实机或跨光源验收。

`export_audit.json` 记录每项最终网格与模型来源；`delivery-verification.json` 是上次交付时保留的重编译核验回执，本次直接发布该既有交付件，没有重新训练。

BIN SHA256：`f1e3b1a0120ce3022dfdc811630ce3763fc33889418ece113f4b32c75c2d1eb4`。
