import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import argparse
import os
import tqdm
import scipy.ndimage as nd
from torchvision import transforms
import matplotlib.pyplot as plt
from tqdm import tqdm 
import cv2 

from torch_dreams import *

mode = "vgg"

image_main = cv2.imread("sample_images/cloudy-mountains.jpg")
image_sample = cv2.cvtColor(image_main, cv2.COLOR_BGR2RGB)
image_sample = cv2.resize(image_sample, (1024,1024))

plt.imshow(image_sample)
plt.show()

if mode == "vgg":
    model= models.vgg19(pretrained=True)
    layers = list(model.features.children())
    model.eval()

    preprocess = preprocess_func_vgg
    deprocess = deprocess_func_vgg

else:
    model = models.resnet18(pretrained=True)
    layers = list(model.children())
    model.eval()

    preprocess = preprocess_func
    deprocess = None


layer = layers[8]

dreamed = deep_dream(
                    image_sample, 
                    model,
                    layer = layer, 
                    octave_scale = 1.5, 
                    num_octaves = 7, 
                    iterations = 5, 
                    lr = 0.09,
                    preprocess_func = preprocess,
                    deprocess_func = deprocess
                    )

plt.imshow(dreamed)
plt.show()

cv2.imwrite('dream.jpg', dreamed)