import os
import argparse

import PIL
import albumentations
import pandas as pd
from albumentations import Normalize

from detection.utils import Xception
from utils import FolderDataset
from utils import Runner



def get_opts():
    arg = argparse.ArgumentParser()
    arg.add_argument(
        "--your-team-name",
        type=str,
    )
    arg.add_argument(
        "--data-folder",
        type=str,
    )
    arg.add_argument(
        "--model-weights",
        type=str,
    )
    arg.add_argument(
        "--result-path",
        type=str,
    )
    opts = arg.parse_args()
    return opts


def get_dataset(opts):
    ### tips: customize your transforms
    import torchvision.transforms as Transforms
    import cv2
    size = 224
    """ For CrossEfficientNetViT:
            Transforms.Resize((size, size)),
            Transforms.ToTensor(),
            Transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    """
    # for RFM
    transforms = Transforms.Compose([
        Transforms.Resize((256, 256)),
        Transforms.CenterCrop((size, size)),
        Transforms.ToTensor(),
        Transforms.Normalize([0.5, 0.5, 0.5], [0.25, 0.25, 0.25])
    ])

    # DO NOT change FolderDataset
    return FolderDataset(opts.data_folder, transforms) 


def get_model_runner(opts, dataset):
    ### tips: customize your model
    import yaml
    import torch
    from cross_efficient_vit import CrossEfficientViT

    # with open('configs/architecture.yaml', 'r') as ymlfile:
    #     config = yaml.safe_load(ymlfile)

    # model = CrossEfficientViT(config=config)

    #model.fc = torch.nn.Linear(2048, 1)
    model = Xception(2)
    model.load_state_dict(
        torch.load('./pretrained_on_celebdf.pth')
    )

    # DO NOT change Runner
    runner = Runner(model, dataset)
    return runner


if __name__ == "__main__":
    opts = get_opts()
    dataset = get_dataset(opts)
    runner = get_model_runner(opts, dataset)
    results = runner.run()

    os.makedirs(opts.result_path, exist_ok=True)
    writer = pd.ExcelWriter(os.path.join(opts.result_path, opts.your_team_name + ".xlsx"))
    prediction_frame = pd.DataFrame(
        data = {
            "img_names": results["predictions"].keys(),
            "predictions": results["predictions"].values(),
        }
    )
    time_frame = pd.DataFrame(
        data = {
            "Data Volume": [len(results["predictions"].keys())],
            "Time": [results["time"]],
        }
    )
    prediction_frame.to_excel(writer, sheet_name="predictions", index=False)
    time_frame.to_excel(writer, sheet_name="time", index=False)
    writer.close()