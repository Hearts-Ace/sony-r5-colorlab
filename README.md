# Sony R5 Color Lab

Independent public color training, calibration and technical documentation project.

- [Color training workbench and launch instructions](R5ColorLab/README.md)
- [Training algorithm and settings](R5ColorLab/TRAINING.md)
- [Grid calibration workbench](R5GridCalibrator/README.md)
- [Technical research](analysis/)
- [Firmware and macOS flash workbench](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware)
- [Existing v4.5 application and synthetic charts download](https://github.com/Hearts-Ace/sony-a7r5-custom-firmware/releases/tag/colorlab-v4.5)
- [Historical FUJ/v4.5 three-expert filters and export audit](filters/FUJ_12_v45_three_experts_20261102/)

Current standard: **no-expert shared C1 + native-operator constraints**. New color-training jobs use the pinned `r5-paired-20261102-shared-c1-c50` response. Grid inference defaults to nonlinear coordinates, C1 structure, 50% curvature penalty, sparse residual shrinkage, and joint RGB/perceptual loss; hue experts are off. See [training settings](R5ColorLab/TRAINING.md) and [grid inference](R5GridCalibrator/README.md). Historical results retain their recorded model identities.

Migrated from firmware repository commit bf71d789262d53ff5fcd23d87aea5bdc07a46f19. Historical release assets stay at their original URLs; current training source and documentation are maintained here. Install each workbench using its own requirements.txt. No firmware build scripts or flash operations are part of this project.

Source licenses remain per directory: R5ColorLab/LICENSE and notices govern the training workbench; root MIT does not replace third-party or AGPL terms. See THIRD_PARTY_NOTICES.md and licenses/.
