from keras.preprocessing.image import img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize
from skimage.io import imsave

import numpy as np
import os

__DIR__ = os.path.dirname(__file__)
# Load .JSON and create model
from keras.models import model_from_json

json_file = open(os.path.join(__DIR__, "model.json"), 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# Load weights into new model
loaded_model.load_weights(os.path.join(__DIR__, "model.h5"))

def conversion(filename):
    colorize = []
    print('Output of the Model')
    image = img_to_array(load_img(os.path.join(__DIR__, "static/img/uploads/" + filename)))
    colorize.append(resize(image, (256, 256), anti_aliasing=True))

    colorize = np.array(colorize, dtype=float)
    colorize = rgb2lab(1.0 / 255 * colorize)[:, :, :, 0]
    colorize = colorize.reshape(colorize.shape + (1,))

    # Test model
    output = loaded_model.predict(colorize)
    output = output * 128

    # Output colorizations
    for i in range(len(output)):
        cur = np.zeros((256, 256, 3))
        cur[:, :, 0] = colorize[i][:, :, 0]
        cur[:, :, 1:] = output[i]
        resImage = lab2rgb(cur)
        imsave(os.path.join(__DIR__, "static/img/converted/"+filename), resImage)
        os.remove(os.path.join(__DIR__, "static/img/uploads/"+filename))

        return "static/img/converted/"+filename
