# Deepfake Generation in DeepfakesAdvTrack - Spring 2025

### 实现
本项目的换脸生成使用[SimSwap](https://github.com/neuralchen/SimSwap)基于VGGFace2的预训练模型。
简单修改了TestOptions。

1. img_extract.ipynb 文件根据 img_list.txt 截取Celeb-DF视频中相应的源和目标人脸对，其中源人脸直接使用对应id的第1个视频第1帧。
2. bat.ipynb 根据 img_list.txt 生成换脸脚本 swap.sh，即1000条调用SimSwap的命令。

### 运行
1. 从原项目地址下载模型权重
   1. 下载 arcface_checkpoint.tar 置于 arcface_model/；
   2. 下载并解压 checkpoints.zip 于 checkpoints/;
   3. 下载 parsing_model 权重置于 parsing_model/checkpoint/;
   4. 下载 insightface 权重 /antelope 置于 insightface_func/models/；
2. 将Celeb-DF数据集的 /Celeb-real 文件夹置于上级目录下，运行 img_extract.ipynb，将在本目录生成 ./source-face 和 ./target-frames 文件夹，分别包含源和目标；
3. 运行 swap.sh 生成换脸结果，保存于 ./output 中。