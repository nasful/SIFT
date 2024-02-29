"""
@author: Md Nasful Huda Prince
PhD student, OSE,UNM
PI: Professor Tonmoy Chakraborty
Lab: Light-sheet microscopy and Imaging Laboratory
"""
import tensorflow as tf
import keras
from keras.models import Model
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, BatchNormalization, Activation, Dropout, Flatten
from keras.optimizers import Adam
from keras.layers import Activation, MaxPool2D
import numpy as np
from matplotlib import pyplot as plt
from keras import backend as K
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential

# Sequential model
def model_block_init(model, input_shape, num_filter):
    model.add(Conv2D(num_filter, (3, 3), input_shape = input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (2,2)))
    return model

def model_block(model, num_filter, kernel_initializer):
    model.add(Conv2D(num_filter, (3, 3), kernel_initializer = kernel_initializer))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    return model

def model_build_sq(input_shape, drop, kernel_initializer):

    model=Sequential()
    model_block_init(model, input_shape = input_shape, num_filter = 64)
    model_block(model, 128, kernel_initializer = kernel_initializer)
    model_block(model, 256, kernel_initializer = kernel_initializer)
    model_block(model, 512, kernel_initializer = kernel_initializer)
    #model_block(model, 1024, kernel_initializer = kernel_initializer)
        
    # Creates 1D vector. Dense layer doesn't accept 2D array rather accepts 1D vector
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(drop))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    return model

