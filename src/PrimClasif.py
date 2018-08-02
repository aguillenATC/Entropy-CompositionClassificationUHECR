#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 09:55:10 2018

@author: alberto
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_absolute_error, r2_score

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD,Adam
from keras.metrics import  categorical_accuracy
from keras.wrappers.scikit_learn import KerasRegressor
from keras import initializers
from keras import callbacks
from keras.utils.np_utils import to_categorical

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from keras.utils import plot_model
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

from sklearn import neighbors

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from plot_conf_matrix import plot_conf_matrix

import time

prefijo=''
path_datos=('../data'+prefijo+'/')
path_results=('../results'+prefijo+'/')

random_st=42 
seed = 7 
np.random.seed(seed)

#X_df=pd.read_csv(path_datos+'XTrn.txt',usecols=['NALLParticlesTotal','MUTotal','ELTotal','Zenith','Energy'])
X_df=pd.read_csv(path_datos+'XTrn.txt',sep='  ',header=None)
Y_df=pd.read_csv(path_datos+'YTrn.txt',sep='  ',header=None)
X_test_df=pd.read_csv(path_datos+'XTest.txt',sep='  ',header=None)
Y_test_df=pd.read_csv(path_datos+'YTest.txt',sep='  ',header=None)

scalerX = StandardScaler()  
scalerX.fit(X_df)  

#scalerY = StandardScaler()  
#scalerY.fit(Y_df) 

X_norm = scalerX.transform(X_df)  
X_test_norm = scalerX.transform(X_test_df)  

#Y_norm = scalerY.transform(Y_df)  
#Y_test_norm = scalerY.transform(Y_test_df)  


#TODO Train Val split

""" 
KNN
"""

start_t_knn = time.time()

n_neighbors = 15
clf = neighbors.KNeighborsClassifier(n_neighbors)
clf.fit(X_norm, Y_df)

elapsed_t_knn = time.time() - start_t_knn

Y_pred_train=clf.predict(X_norm)
Y_pred_train=Y_pred_train.reshape(-1,1)
Y_pred_test=clf.predict(X_test_norm)
Y_pred_test=Y_pred_test.reshape(-1,1)

print(classification_report(np.argmax(Y_df.values,axis=1), np.argmax(Y_pred_train,axis=1)))
    
# Compute confusion matrix
cnf_matrix = confusion_matrix(np.argmax(Y_df.values,axis=1),np.argmax(Y_pred_train,axis=1) )
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_conf_matrix(cnf_matrix, classes=['photon','proton', 'helium','nitrogen','iron' ],
                        title='Confusion matrix TRAIN')
plt.show()
# Plot normalized confusion matrix
plt.figure()
plot_conf_matrix(cnf_matrix, classes=['photon','proton', 'helium','nitrogen','iron' ], normalize=True,
                        title='Normalized confusion matrix TRAIN')
#
plt.show()
    
print(classification_report(np.argmax(Y_test_df,axis=1), np.argmax(Y_pred_test,axis=1)))

# Compute confusion matrix
cnf_matrix = confusion_matrix(np.argmax(Y_test_df,axis=1),np.argmax(Y_pred_test,axis=1) )
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_conf_matrix(cnf_matrix, classes=['photon','proton', 'helium','nitrogen','iron' ],
                        title='Confusion matrix TEST')
plt.show()
# Plot normalized confusion matrix
plt.figure()
plot_conf_matrix(cnf_matrix, classes=['photon','proton', 'helium','nitrogen','iron' ], normalize=True,
                        title='Normalized confusion matrix TEST')
#
plt.show()


print('Time elapsed for kNN %f', elapsed_t_knn)