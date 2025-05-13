# Deepfake Detection in DeepfakesAdvTrack - Spring 2025

### 实现

本项目的换脸检测使用[Cross EfficientNet ViT](https://github.com/davide-coccomini/Combining-EfficientNet-and-Vision-Transformers-for-Video-Deepfake-Detection)基于DFDC和FaceForensics++的预训练模型，图片Patch Extractor使用EfficientNet-B0。
将原项目基于albumentations和openCV的预处理简化为了基于pytorch的Transforms，并增加了归一化。

### 运行
1. 从原项目地址下载预训练权重 cross_efficient_vit.pth 置于本目录下；
2. 将Celeb-DF数据集的 /test 或 /val 文件夹置于本目录下，执行 run.sh，生成每张人脸的预测得分 test.xlsx 文件（接近1代表伪造，接近0代表真实）； 
3. 由于模型使用 BCEWithLogitsLoss，因此输出得分需要经sigmoid函数转化为正例概率。

### 更新（5.13）
1. 尝试了FF++的预训练模型[CADDM](https://github.com/megvii-research/CADDM)，效果与论文所述在Celeb-DF的迁移性能相差甚远，验证集AUC约0.56，且大多数图片都以0.75左右概率分类为“真实”，准确率很低；
2. 使用Celeb-DF的预训练模型[RFM](https://github.com/crywang/RFM)，auc改善至0.75，但从混淆矩阵看整体性能不佳。

|     | 标签0  | 标签1  |
|:---:|:----:|:----:|
| 预测0 | 808  | 192  |
| 预测1 | 7608 | 9392 |
