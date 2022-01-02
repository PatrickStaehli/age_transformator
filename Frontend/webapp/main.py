import os
import time
from flask import Flask, render_template, flash, jsonify, session

import logging
logging.basicConfig(filename='logs.log', level=logging.DEBUG)

from forms import UploadImageFomr
from utils import save_picture, delete_images
from job_handler import age_predictor

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = '0Af4ee3597Ias5//asft21A'


predictor = age_predictor()


@app.route("/age_predictor", methods=['GET', 'POST'])
def home():
    
    sessionID = 'j6uzp_fiKk1L0g'
    session['id'] = sessionID

    form = UploadImageFomr()
    
    if form.validate_on_submit():
        if form.picture.data:
            original_image_path = save_picture(form.picture.data)
            if original_image_path:
                session['original_image_path'] = original_image_path
                return render_template('index.html', title='Account',
                                    image_upload=True, image_filepath = 'age_predictor/' + original_image_path, 
                                    form=form)
            else:
                flash('Could not upload image', 'warning')
   
    
    return render_template('index.html', title='Account',
                           image_upload=False, form=form)


@app.route("/age_predictor/results", methods=['GET', 'POST'])
def results():
  
    # Count files in prediction
    list_prediction_files = os.listdir('static/predicted_image/') # dir is your directory path
    list_prediction_files.sort()
    prediction_filepath = ['/age_predictor/static/predicted_image/' + filename for filename in list_prediction_files]
    #prediction_filepath = ['/static/predicted_image/' + filename for filename in list_prediction_files] # Local Debugging
    number_files = len(prediction_filepath)
 
    ages = ['10', '20', '30', '40', '50', '60', '70', '80', '90'] 
    
    return render_template('results.html', title='Account',
                        num_prediction_files=number_files,
                        prediction_filepath=prediction_filepath,
                        ages = ages)


@app.route("/age_predictor/predict", methods=['GET', 'POST'])
def predict_age():
   
    status = predictor.predict(session['original_image_path'])

    if not status:
        flash('Something went wrong', 'warning')
        delete_images()
    
    response = jsonify({'prediction_status': status})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route("/age_predictor/remove_images", methods=['GET', 'POST'])
def remove_images():
    
    # Wait 5 seconds to be sure that the images are loaded.

    time.sleep(5)
    delete_status = delete_images()
    
    response = jsonify({'success': delete_status})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

if __name__ == "__main__":
    app.run(host='0.0.0.0')
        