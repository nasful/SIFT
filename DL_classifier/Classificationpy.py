"""
@author: Md Nasful Huda Prince
PhD student, OSE,UNM
PI: Professor Tonmoy Chakraborty
Lab: Light-sheet microscopy and Imaging Laboratory
"""
import tensorflow as tf
import keras
from keras.models import Model
from keras.layers import Input, Conv3D, MaxPooling3D, UpSampling3D, concatenate, Conv3DTranspose, BatchNormalization, Dropout, Lambda
from keras.optimizers import Adam
from keras.layers import Activation, MaxPool2D, Concatenate
import numpy as np
from matplotlib import pyplot as plt
from keras import backend as K
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import os
import random
from glob import glob
import tifffile
from keras.callbacks import ModelCheckpoint, EarlyStopping, CSVLogger

os.chdir('/Directory from where the software is running')
os.getcwd()
from model_Class import *
from data_generator import *
from keras.models import Sequential

# Input training parameters
Initial_LR = 0.0001
optim = keras.optimizers.Adam(Initial_LR)
img_shape = 1024
input_shape = (img_shape, img_shape, 1)
batch_size = 32 # Specify the batch size depending on the GPU memory
dataset = []
label = []
epoch = 100 # Specify number of epoch
kernel_initializer = 'he_uniform'
seed = 24
drop = 0.3

# Specify the training image directory
img_path = '/Informative image path/'
noise_path = '/Non-informative image path/'


# Check the GPU availability
if tf.test.is_gpu_available() ! = bool(True):
    print('Training with CPU')
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    model = model_build_sq(input_shape = input_shape, drop=drop, kernel_initializer = kernel_initializer)

else:
    print('Training with GPU')
    model = model_build_sq(input_shape = input_shape, drop = drop, kernel_initializer = kernel_initializer)
    
#model=model_build(input_shape=input_shape,drop=drop)
model=model_build_sq(input_shape = input_shape, drop = drop, kernel_initializer = kernel_initializer)
print(model.summary())
print(model.input_shape)

model.compile(loss = 'binary_crossentropy', optimizer = optim, metrics = ['accuracy'])

img_names = glob(img_path + '*.tif')
num_img = int(len(img_names)) * 2
steps_per_epoch = num_img // batch_size

dataset, label = image_generator(img_path, dataset, label, img_shape)
dataset, label = noise_generator(noise_path, dataset, label, img_shape)

dataset = np.array(dataset)
label = np.array(label)
print(dataset.shape)
print(label.shape)


# View few images
# Assign a random number within the range of 0 and (len(dataset)-1)
#image_number=random.randint(0,len(dataset)-1)
#plt.imshow(dataset[image_number])
#print('Label for this image is: ',label[image_number])

X_train, X_test, y_train, y_test = train_test_split(dataset, label, test_size = 0.2, random_state = 20)

filepath = '/Directory and file name in .hdf5 format where we want to save our trained checkpoints'
checkpoint = ModelCheckpoint(filepath, monitor = 'accuracy', verbose = 1, save_best_only = True, mode = 'max')

early_stop = EarlyStopping(monitor = 'accuracy', patience = 10, verbose = 1)
log_csv = CSVLogger('/Directory and file name in .csv format where we want to save our data log to observe the training performance',
                    separator = ',', append = False)
callbacks_list = [checkpoint, early_stop, log_csv]

#steps_per_epoch=num_train_imgs//batch_size
# Fit the model
history=model.fit(X_train, y_train, batch_size = batch_size, verbose = 1, epochs = epoch,
                  validation_data = (X_test, y_test), callbacks = callbacks_list, shuffle = False)

