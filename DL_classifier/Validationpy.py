"""
@author: Md Nasful Huda Prince
PhD student, OSE,UNM
PI: Professor Tonmoy Chakraborty
Lab: Light-sheet microscopy and Imaging Laboratory
"""
# Load the saved model
from keras.models import load_model
import tifffile
import glob
import os
import numpy as np
from skimage.transform import resize
import time

model_path = '/Directory where the best trained checkpoints are located/'
model = load_model(model_path + 'Best trained checkpoint.hdf5', compile = False)

img_path = '/Directory of the low resolution images/'
start_time = time.time()
f_acc = open('/Directory where we want to create the text file containing the coordinates of the informative images/'+'informative image coordinate file name.txt','w')
f_rej = open('/Directory where we want to create the text file containing the coordinates of the non-informative images/'+'non-informative image coordinate file name.txt','w')
num_fold = 0

for _,dir,fil in os.walk(img_path):
    num_fold += len(dir)

img_shape = 1024
threshold = 0.9 # Input the probability threhold to distinguish informative and non-informative images 

prob = []
num_acc = 0
num_rej = 0

# Indentify the XYZ coordinates from the low resolution image tiles
word_x = 'PositionX_mm' 
word_y = 'PositionY_mm'
word_z = 'PositionZ_mm'

for i in range(num_fold):
    path = img_path + 'position '+str(i+1)+'/'
    pos_img = path + '*.tif' # Direct the images
    img = tifffile.imread(pos_img)
    mip = np.max(img, axis = 0)
    mip_res = resize(mip, (img_shape, img_shape))
    maxm = mip_res.max()
    mip_norm = mip_res/maxm
    mip_resh = np.reshape(mip_norm, (mip_norm.shape[0], mip_norm.shape[1], 1))
    inp_img = np.expand_dims(mip_resh, axis = 0)
    pr = model.predict(inp_img)
    prob.append(pr)
    #img_acc = (model.predict(image)>threshold).astype(int)
    f_coord = open(path + 'AcqInfo.txt')
    
    if pr >= threshold:
        num_acc = num_acc + 1
        #f_acc.write(str(num_acc) + '\t' + str(num_acc) + '\t')
        f_acc.write(str(i+1) + '\t' + str(num_acc) + '\t')
        for line in f_coord:
            list_words = (line.rsplit('\n')[0]).rsplit(' ')
            if word_x in list_words:
                f_acc.write(list_words[2] + '\t')
            elif word_y in list_words:
                f_acc.write(list_words[2] + '\t')
            elif word_z in list_words:
                f_acc.write(list_words[2] + '\t' + 'NaN' + '\t' + 'NaN' + '\n')
    else:
        num_rej = num_rej + 1
        #f_rej.write(str(num_rej) + '\t' + str(num_rej) + '\t')
        f_rej.write(str(i + 1) + '\t' + str(num_rej) + '\t')
        for line in f_coord:
            list_words = (line.rsplit('\n')[0]).rsplit(' ')
            if word_x in list_words:
                f_rej.write(list_words[2] + '\t')
            elif word_y in list_words:
                f_rej.write(list_words[2] + '\t')
            elif word_z in list_words:
                f_rej.write(list_words[2] + '\t' + 'NaN' + '\t' + 'NaN' + '\n')
    f_coord.close()
    print('Finished checking image no. ', i + 1)
f_acc.close()
f_rej.close()

# Estimating the time required to distinguih the images
end_time = time.time()
print('Time required %s seconds' % (end_time - start_time))
print(prob)
