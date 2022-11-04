import requests
import json
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import time


class age_transformator:
    '''
    Attributes
    ----------
    aws_lambda_url : string
        URL to the API Gateway of the AWS Lambda function that performs the prediciton
    ages : list of lists
        The ages for which the prediction is performed [[10], [20, 30, 40], ...]. Note that not
        more than three ages can be predicted at the same time due to timeout reasons. The first
        call is only one age due to cold-start reasons.
    
    Methods
    -------
    base64_to_img (staticmethod)
        Decodes a base64 string to an image.
    img_to_base64json (staticmethod)
        Encodes an image to a base64 json
    resize_image (staticmethod)
        Resizes the image to a size where the smaller side is no larger than 1024 px.
    predict
        Calls the API Gateway that performs the prediction.
    '''

    def __init__(self):
        self.aws_lambda_url = 'https://0i164xnbug.execute-api.eu-central-1.amazonaws.com/default/agePrediction'
        self.ages = [[10], [20, 30, 40], [50, 60, 70], [80]]

    @staticmethod
    def base64_to_img(data):
        '''
        Decodes a base64 string to an image.
        '''
        imdata = base64.b64decode(data)
        decoded_image = Image.open(BytesIO(imdata))
        decoded_image_cv2 = np.array(decoded_image)
        rgb_image = cv2.cvtColor(decoded_image_cv2,cv2.COLOR_BGR2RGB)
        
        return rgb_image
    
    
    @staticmethod
    def img_to_base64json(img):
        '''
        Encodes an image to a base64 json
        '''
        _, imdata = cv2.imencode('.JPG',img)
        jstr = base64.b64encode(imdata).decode('ascii')
        return jstr
    
    
    @staticmethod
    def resize_image(img):
        '''
        Resizes the image to a size where the smaller side is no larger than 1024 px.

        Args:
        -----
        img : Numpy array [w, h, c]
            The image that has to be resized

        Returns:
        --------
        Numpy array [w, h, c]
            The resized image
        '''
        
        if img.shape[0] > 1024 or img.shape[1] > 1024:
            if img.shape[0] > img.shape[1]:
                scale_percent = 1024/img.shape[1] 
                width = int(img.shape[1] * scale_percent)
                height = int(img.shape[0] * scale_percent)
                dim = (width, height)
                # resize image
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            else:
                scale_percent = 1024/img.shape[0] 
                width = int(img.shape[1] * scale_percent)
                height = int(img.shape[0] * scale_percent)
                dim = (width, height)
                # resize image
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            
            return resized
        else:
            return img


    def predict(self, img_path):
        '''
        Reads the profile image from the temporarily directory, encoded the image into base64
        and calls the API that performs the prediction. 

        The base64 encoded images that are returned form this API are then converted to cv2 images and
        stored in a temporarily directory. 

        Args:
        -----
        img_path : string
            Path (including filename) to the profile picture

        Returns:
        --------
        Bool
            True if the prediction process was successful, False if some error occured
        '''

        try:
            img = cv2.imread(img_path)
            print(img_path)
            encoded_image = self.img_to_base64json(self.resize_image(img))
            
            # Perform the prediction for each group of ages
            for idx, ag in enumerate(self.ages):
                print(f'Predicting ages {ag}')
                
                request_object = {'age': ag,
                                  'image': encoded_image}
                
                # The first prediction attempt might fail becuase the lambda function might run from a cold start
                # and the max. api response time (from the aws side) is 29 seconds.
                attempts = 0
                while attempts < 2:
                    try:
                        start = time.time()
                        response = requests.post(self.aws_lambda_url, 
                                                 data=json.dumps(request_object), 
                                                 headers={'Content-type': 'application/json'}, 
                                                 timeout=120
                                                 ).json()

                        # The images base64 encoded in the image object of the response json
                        response_images = response['image']
                        print(f'Time elapsed: {time.time()-start}')
                        break
                        
                    except:
                            attempts += 1
                            print(f'Prediction failed after {time.time()-start} seconds')
                            response_images = None
                            time.sleep(2)
                        
                for age, aged_image in response_images.items():
                    print(age)
                    cv2.imwrite('static/predicted_image/' + age + '.jpg', self.base64_to_img(aged_image))

            return True

        except Exception as e: 
            print(e)
            return False