"""
@author: Md Nasful Huda Prince
PhD student, OSE,UNM
PI: Professor Tonmoy Chakraborty
Lab: Light-sheet microscopy and Imaging Laboratory
"""
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
import tifffile
from PIL import Image
from glob import glob
import numpy as np
from skimage.transform import resize

# Define a function to scale images, to convert masks into categorical etc
def preprocess_data(img, img_shape):
    img = resize(img, (img_shape, img_shape))
    img = img/img.max()
    return (img)

def image_generator(img_path, dataset, label, img_shape):
    img_names = glob(img_path + '*.tif')
    for i in (img_names):
        img = tifffile.imread(i)
        #img = np.max(img, axis = 0)
        img = preprocess_data(img, img_shape)
        img = np.reshape(img, (img.shape[0], img.shape[1], 1))
        dataset.append(np.array(img))
        label.append(1)
    return (dataset, label)
        
def noise_generator(noise_path, dataset, label, img_shape):
    noise_names = glob(noise_path + '*.tif')
    for i in (noise_names):
        noise = tifffile.imread(i)
        #noise = np.max(noise, axis = 0)
        noise = preprocess_data(noise, img_shape)
        noise = np.reshape(noise, (noise.shape[0], noise.shape[1], 1))
        dataset.append(np.array(noise))
        label.append(0)
    return (dataset,label)        



