import os
from threading import get_ident
import time
from datetime import timedelta
import torch
import numpy as np
from PIL import Image
from taming.models import vqgan

import sys
sys.path.append("latent-diffusion-main")

from notebook_helpers import get_model, run

def upscaleImage(input):
    model = get_model('superresolution')

    #input.save('input_image.jpg')
    input_path = "result_image.jpg"
    steps = 10 #@param {type:"integer"}
    img_out = "output_image.jpg"

    logs = run(model["model"], input_path, 'superresolution', steps)
    print("Bitti")
    sample = logs["sample"]
    sample = sample.detach().cpu()
    sample = torch.clamp(sample, -1., 1.)
    sample = (sample + 1.) / 2. * 255
    sample = sample.numpy().astype(np.uint8)
    sample = np.transpose(sample, (0, 2, 3, 1))
    a = Image.fromarray(sample[0])
    a.save(img_out)

    if os.path.isfile(img_out):
        print('Upscaled image saved as:', img_out)
    else:
        print('Error occurred while saving the upscaled image.')


