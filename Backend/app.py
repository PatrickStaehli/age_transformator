import os
import os.path
import sys
import cv2
import json
import numpy as np

from scripts import inference 
from utils.common import json2im, im2json

def lambda_handler(event, context):
    '''
    Lambda handler that takes input images and ages, performs the prediction and returns
    the resulting images.

    Args
    ----
        event : json
            event['body']['image'] : base64 encoded image of a person
            event['body']['age'] : List of ages to predict. These values must be provided as int between 1 and 100.

    Returns
    -------
        json 
            age : image (base64)
    '''

    # Body is a string -> encode it to json
    try:
        content = json.loads(event['body'])
        img = json2im(content['image'])
        ages = content['age']
    except Exception as e:
        return {
        "statusCode": 500,
        "headers": {
            "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": e.message
            })
        }
    

    # Perform the age transformation
    try:
        results = inference.predict_age(img, ages)

        # Encode the result
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
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": e.message
            })
        }
