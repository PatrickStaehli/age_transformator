from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class UploadImageFomr(FlaskForm):
    '''
    Flask form for uploading the profile image
    '''
    
    picture = FileField('', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Upload image')
