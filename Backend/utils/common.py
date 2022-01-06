from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import cv2

def im2json(im):
    '''
    Converts an cv2 image to a base64 string in a valid json format

    Args
    ----
        img : cv2 image
    
    Returns
    -------
        str : base64 string of the image
    '''

    _, imdata = cv2.imencode('.JPG',im)
    jstr = base64.b64encode(imdata).decode('ascii')
    return jstr


def json2im(img_jsoncode):
    '''
    Converts an base64 string in a valid json format to a cv2 image

    Args
    ----
        str : base64 string of the image
    
    Returns
    -------
        img : cv2 image
    '''

    imdata = base64.b64decode(img_jsoncode)
    decoded_image = Image.open(BytesIO(imdata))
    decoded_image_cv2 = np.array(decoded_image)
    rgb_image = cv2.cvtColor(decoded_image_cv2,cv2.COLOR_BGR2RGB)
    
    return rgb_image


def tensor2im(var):
	var = var.cpu().detach().transpose(0, 2).transpose(0, 1).numpy()
	var = ((var + 1) / 2)
	var[var < 0] = 0
	var[var > 1] = 1
	var = var * 255
	return Image.fromarray(var.astype('uint8'))
