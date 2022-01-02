from PIL import Image, ImageOps
import os

def save_picture(image_form):
    '''
    Saves an profile picture that is uploaded via the picture form to the
    profile picture folder

    Args:
    -----
    image_form : FlaskForm
        FlaskForm that contains the properties filename and an image

    Returns:
    --------
    Bool
        True if the image is saved, False if the image has the wrong format

    '''
    
    _, f_ext = os.path.splitext(image_form.filename)
    if f_ext in ['.jpeg', '.jpg', '.png']:
        picture_path = 'static/profile_pics/original_image' + f_ext

        img = Image.open(image_form)
        img = ImageOps.exif_transpose(img)
        img.save(picture_path)

        return picture_path
    else:
        return False


def delete_images():
    '''
    Deletes the images that are in the folders 
        - static/predicted_image/
        - static/profile_pics/

    Returns:
    --------
    Bool
        True if the images were deleted, False if some error occured.
    '''
    
    try:
        for file in os.listdir('static/predicted_image/'):
            os.remove('static/predicted_image/' + file)
        for file in os.listdir('static/profile_pics/'):
            os.remove('static/profile_pics/' + file)
        return True
    
    except:
        return False