from argparse import Namespace
import os
import time
import sys
os.environ['CUDA_VISIBLE_DEVICES'] = ''

import numpy as np
from PIL import Image

import torch
import torchvision.transforms.functional as TF

from datasets.alignment import run_alignment
from datasets.augmentations import AgeTransformer
from utils.common import tensor2im
from models.psp import pSp


def load_model():
	'''
	Loads the pre-trained age_transformation torch model

	Returns
	-------
		torch_model : The pre-trained torch model for the age_transformation

	'''


	# Options
	options = {'checkpoint_path':'pretrained_models/sam_ffhq_aging.pt',
				'resize_outputs':False,
				'device': 'cpu'
				}
	
	# Load the pretrained model	(to cpu)		
	ckpt = torch.load(options['checkpoint_path'], map_location=torch.device("cpu"))
	
	# update test options with options used during training
	opts = ckpt['opts']
	opts.update(options)
	opts = Namespace(**opts)
	
	net = pSp(opts)
	net.to('cpu')
	net.eval()

	return net

def predict_age(img, target_age):
	'''
	Transforms the input image to the target age

	Args
    ----
        img (cv2) : Profile image
		target_age (list of int) : Target ages 

    Returns
    -------
        list
			List of predicted images for the target age
	'''
	
	# Load the pre-trained model
	net = load_model()

	# Create AgeTransformer
	age_transformers = [AgeTransformer(target_age=age) for age in target_age]

	# Align the face in the image
	aligned_image = run_alignment(img)
	aligned_image = torch.tensor(aligned_image)

	# Normalize the image so that it matches the training cases
	normalized_image = TF.normalize(aligned_image, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

	# Predict the target images
	generated_images = []
	for age_transformer in age_transformers:

		print(f"Running on target age: {age_transformer.target_age}")
		
		with torch.no_grad():
			input_age_batch = [age_transformer(normalized_image.cpu())]
			input_age_batch = torch.stack(input_age_batch)
			result_batch = net(input_age_batch.float(), 
							   randomize_noise=False, 
							   resize=opts.resize_outputs)
			result = tensor2im(result_batch[0])
			generated_images.append({'age': age_transformer.target_age,
									 'img': result})

	return generated_images		