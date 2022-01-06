import time
import dlib
from scripts.align_all_parallel import align_face
import numpy as np

def run_alignment(img):
    '''
    Align the images using face landmarks
    
    '''

    start = time.time()
    predictor = dlib.shape_predictor('pretrained_models/shape_predictor_68_face_landmarks.dat')
    aligned_image = align_face(img, predictor)
    print(f'Aligned image has shape: {aligned_image.size}. Elapsed time: {time.time()-start}')

    return np.moveaxis(np.array(aligned_image)/255.0, -1, 0)
