from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray
from skimage.io import imsave
from random import randint
import numpy as np
import os

import tensorflow as tf
from keras.layers import Conv2D, Conv2DTranspose, UpSampling2D
from keras.layers import Activation, Dense, Dropout, Flatten, InputLayer
from keras.layers.normalization import BatchNormalization
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.models import Sequential

# Load .JSON and create model
from keras.models import model_from_json

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# Load weights into new model
loaded_model.load_weights("model.h5")

def conversion(filename):
    colorize = []
    print('Output of the Model')
    for filename in os.listdir('static/img/uploads/'):
        colorize.append(img_to_array(load_img('static/img/uploads/' + filename)))

    colorize = np.array(colorize, dtype=float)
    colorize = rgb2lab(1.0 / 255 * colorize)[:, :, :, 0]
    colorize = colorize.reshape(colorize.shape + (1,))

    # Test model
    output = loaded_model.predict(colorize)
    output = output * 128

    row = 0

    # Output colorizations
    for i in range(len(output)):
        cur = np.zeros((256, 256, 3))
        cur[:, :, 0] = colorize[i][:, :, 0]
        cur[:, :, 1:] = output[i]
        resImage = lab2rgb(cur)
        imsave("static/img/converted/"+filename, resImage)
