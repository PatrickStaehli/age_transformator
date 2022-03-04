import os
import os.path
import sys
import cv2
import json
import numpy as np

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

from scripts import inference, load_model
from utils.common import json2im, im2json



def lambda_handler(event, context):
    '''
    Lambda handler that takes input images and ages, performs the prediction and returns
    the resulting images.

    Args
    ----
        event : json
            event['image'] : base64 encoded image of a person
            event['age'] : List of ages to predict. These values must be provided as int between 1 and 100.
            event['only_load_model'] : If true, the model is loaded but no inference is executed.
    Returns
    -------
        json 
            age : image (base64)
    '''

    only_load_model = event['only_load_model'] 

    if only_load_model == True:
        logging.debug('only_load_model flag is true')
        logging.debug('Start loading model')
        _ = load_model()
        logging.debug('Model loaded')
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": 'Model is loaded'
            })
        }

    else:   
        # Perform the age transformation
        logging.debug('only_load_model flag is false')
        
        logging.debug('Casting input parameters')
        img = json2im(event['image'])
        ages = event['age']
        
        logging.debug('Starting inference')
        results = inference.predict_age(img, ages)


        # Encode the result
        logging.debug('Encode Results')
        encoded_result = {}
        for result in results:
            cv_image = np.array(result['img'], dtype=np.uint8)
            image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
            encoded_result[result['age']] = im2json(image)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "image": encoded_result
            })
        }