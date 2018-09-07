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

from keras.utils import plot_model
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

# Classifiers used
from sklearn import neighbors
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from plot_conf_matrix import plot_conf_matrix

from tools import calc_error_n_plot

import time

elapsed_t={}
clasf_report={}
prefijo=''
path_datos=('../data'+prefijo+'/')
path_results=('../results'+prefijo+'/')

random_st=42 
seed = 7 
np.random.seed(seed)

#X_df=pd.read_csv(path_datos+'XTrn.txt',usecols=['NALLParticlesTiotal','MUTotal','ELTotal','Zenith','Energy'])
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

#Train Val split

X_train,X_val,Y_train,Y_val=train_test_split(X_norm,
                                            Y_df.values,
                                            test_size=0.20,
                                            random_state=45)

""" 
KNN
"""

start_t = time.time()

n_neighbors = 3
clf = neighbors.KNeighborsClassifier(n_neighbors)
clf.fit(X_train, np.ravel(Y_train))

elapsed_t['knn'] = time.time() - start_t

Y_pred_train=clf.predict(X_train)
Y_pred_train=Y_pred_train.reshape(-1,1)
Y_pred_val=clf.predict(X_val)
Y_pred_val=Y_pred_val.reshape(-1,1)
Y_pred_test=clf.predict(X_test_norm)
Y_pred_test=Y_pred_test.reshape(-1,1)

calc_error_n_plot(Y_train,Y_pred_train,'TRAIN')
calc_error_n_plot(Y_val,Y_pred_val,'VALIDATION')
clasf_report['KNN']=calc_error_n_plot(Y_test_df.values,Y_pred_test,'TEST')


print('Time elapsed for kNN %f' % elapsed_t['knn'])


"""
SVM
"""

start_t = time.time()

C=0.75
clf = SVC(C)

clf.fit(X_train, np.ravel(Y_train))

elapsed_t['SVM'] = time.time() - start_t

Y_pred_train=clf.predict(X_train)
Y_pred_train=Y_pred_train.reshape(-1,1)
Y_pred_val=clf.predict(X_val)
Y_pred_val=Y_pred_val.reshape(-1,1)
Y_pred_test=clf.predict(X_test_norm)
Y_pred_test=Y_pred_test.reshape(-1,1)

calc_error_n_plot(Y_train,Y_pred_train,'TRAIN')
calc_error_n_plot(Y_val,Y_pred_val,'VALIDATION')
clasf_report['SVM']=calc_error_n_plot(Y_test_df.values,Y_pred_test,'TEST')

"""
Random Forest
"""
clf = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)
clf.fit(X_train, np.ravel(Y_train))

elapsed_t['RandForest'] = time.time() - start_t

Y_pred_train=clf.predict(X_train)
Y_pred_train=Y_pred_train.reshape(-1,1)
Y_pred_val=clf.predict(X_val)
Y_pred_val=Y_pred_val.reshape(-1,1)
Y_pred_test=clf.predict(X_test_norm)
Y_pred_test=Y_pred_test.reshape(-1,1)

calc_error_n_plot(Y_train,Y_pred_train,'TRAIN')
calc_error_n_plot(Y_val,Y_pred_val,'VALIDATION')
clasf_report['RandForest']=calc_error_n_plot(Y_test_df.values,Y_pred_test,'TEST')

"""
XGBoost
https://xgboost.ai/about
"""

import xgboost as xgb

#dtrain = xgb.DMatrix(np.concatenate((X_train,Y_train),axis=1))
#dtest = xgb.DMatrix(np.concatenate((X_test_norm,Y_test_df.values),axis=1))

dtrain = xgb.DMatrix(X_train, label=Y_train)
dtest = xgb.DMatrix(X_test_norm,label=Y_test_df.values)

# specify parameters via map
param = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'multi:softmax', 'num_class':5 }
num_round = 2
bst = xgb.train(param, dtrain, num_round)
# make prediction
Y_pred_test = bst.predict(dtest)

clasf_report['XGB']=calc_error_n_plot(Y_test_df.values,Y_pred_test,'TEST')

"""
DNN
"""
