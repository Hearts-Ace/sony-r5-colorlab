# Sony R5 Color Lab

Independent public color training, calibration and technical documentation project.

- [Color training workbench and launch instructions](R5ColorLab/README.md)
- [Training algorithm and settings](R5ColorLab/TRAINING.md)
- [Grid calibration workbench](R5GridCalibrator/README.md)
- [Technical research](analysis/)
- [Firmware and macOS flash workbench](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)
- [Existing v4.5 application and synthetic charts download](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware/releases/tag/colorlab-v4.5)
- [Current FUJ/v4.5 shared C1 filters, editable configuration and export audit](filters/FUJ_12_v45_shared_c1_20261104/)
- [Download the complete workbench source](https://github.com/Hearts-Ace/sony-r5-colorlab/archive/refs/heads/main.zip)

Current source (2026-11-08): portable formal **Mac Metal/MPS and Windows AMD ROCm** workbenches. Both use the pinned Hybrid three-expert response and the same native twelve-start → five grid rounds → three stacked rounds recipe. AMD defaults to **10 CPU threads / 3 concurrent jobs**; Mac uses 8 / 2. See [training settings](R5ColorLab/TRAINING.md) and [AMD setup](R5ColorLab/AMD.md).

The PT hue half-index precision fix is included in CPU and Metal inference. Retained PT chart validation covers all 99,372 center-five samples; this is not a cross-illuminant or full camera ISP validation. Previously published shared-C1 filter exports retain their historical model identity; this source update does not replace them with new training results.

Migrated from firmware repository commit bf71d789262d53ff5fcd23d87aea5bdc07a46f19. Historical release assets stay at their original URLs; current training source and documentation are maintained here. Install each workbench using its own requirements.txt. No firmware build scripts or flash operations are part of this project.

Source licenses remain per directory: R5ColorLab/LICENSE and notices govern the training workbench; root MIT does not replace third-party or AGPL terms. See THIRD_PARTY_NOTICES.md and licenses/.
