# pip install torch torchvision

from torch import nn
import torch
from PIL import Image
from torchvision import transforms
import os
import random


recipes_list = [
    "American",
    "Chinese",
    "Korean",
    "Japanese",
    "Mexican",
    "Middle East",
    "Indian",
    "Others"
]


def predict(picture_path):
    """
    Temporary fake AI prediction.
    现在先不训练模型，只用来跑通 Flask 上传图片流程。
    """

    # 固定返回一个分类
    return "Chinese"
    # return random.choice(recipes_list)