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

Current standard: **no-expert shared C1 + native-operator constraints**. New color-training jobs use the pinned `r5-paired-20261102-shared-c1-c50` response. Grid inference defaults to nonlinear coordinates, C1 structure, 50% curvature penalty, sparse residual shrinkage, and joint RGB/perceptual loss; hue experts are off. See [training settings](R5ColorLab/TRAINING.md) and [grid inference](R5GridCalibrator/README.md). Historical results retain their recorded model identities. The current twelve-filter batch is complete (`c29ff1d3ef314d718ab370cf6ed2bfb6`); its BIN SHA256 is `2e9c60c1f7858940e366aa1b0f2c0c089347445c9c286c0c938a40a35610caee`. The operator and workbench implementation are the same reviewed shared C1 source; this publication adds the completed filter exports and current documentation.

Migrated from firmware repository commit bf71d789262d53ff5fcd23d87aea5bdc07a46f19. Historical release assets stay at their original URLs; current training source and documentation are maintained here. Install each workbench using its own requirements.txt. No firmware build scripts or flash operations are part of this project.

Source licenses remain per directory: R5ColorLab/LICENSE and notices govern the training workbench; root MIT does not replace third-party or AGPL terms. See THIRD_PARTY_NOTICES.md and licenses/.
