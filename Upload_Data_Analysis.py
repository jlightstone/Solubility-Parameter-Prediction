# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 04:35:28 2019

@author: Jordan
"""
import Upload_Model_Predition
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np


reg_train_set,reg_test_set,pca_test_set, pca_train_set,lasso_train_set,lasso_test_set = Upload_Model_Predition.test_train_set()
      
for count in [0,1,2]:
    if count == 0:
        file_name = ['Solubility_Prediction_Train_Parity_Overlay.jpg','Solubility_Prediction_Train_Parity_Test.jpg','Solubility_Prediction_Train_Parity.jpg']
        title = 'Linear_Regression/Solubility_Parameter'
        train_set = reg_train_set
        test_set = reg_test_set
    elif count == 1:
        file_name = ['PCA_Solubility_Prediction_Train_Parity_Overlay.jpg','PCA_Solubility_Prediction_Train_Parity_Test.jpg','PCA_Solubility_Prediction_Train_Parity.jpg']
        title = 'Linear_Regression/PCA/Solubility_Parameter'
        train_set = pca_train_set
        test_set = pca_test_set
    else:
        file_name = ['Lasso_Solubility_Prediction_Train_Parity_Overlay.jpg','Lasso_Solubility_Prediction_Train_Parity_Test.jpg','Lasso_Solubility_Prediction_Train_Parity.jpg']
        title = 'Linear_Regression/Lasso/Solubility_Parameter'
        train_set = lasso_train_set
        test_set = lasso_test_set


    train_data_actual = train_set.iloc[:,2:3].values.tolist()
    train_data_predicted = train_set.iloc[:,3:4].values.tolist()
    test_data_actual = test_set.iloc[:,2:3].values.tolist()
    test_data_predicted = test_set.iloc[:,3:4].values.tolist()
    
    test_error = np.std(test_data_predicted)
    train_error = np.std(train_data_predicted)
    
    test_lim_low = min(min(test_data_actual),min(test_data_predicted))[0]
    test_lim_max = max(max(test_data_actual),max(test_data_predicted))[0]
    train_lim_low = min(min(train_data_predicted),min(train_data_predicted))[0]
    train_lim_max = max(max(train_data_predicted),max(train_data_predicted))[0]
    
    lim_min = float(str(min(test_lim_low, train_lim_low)))
    lower_lim = lim_min - lim_min*.1
    lim_max = float(str(min(test_lim_max,train_lim_max)))
    upper_lim = lim_max + lim_max*.1 
    lim = [lower_lim,upper_lim]
    
    train_size = len(train_set)
    test_size = len(test_set)
    
    RMSE_train_set = metrics.mean_squared_error(train_data_actual,train_data_predicted)
    r2_train_set = metrics.r2_score(train_data_actual,train_data_predicted)
    RMSE_test_set = metrics.mean_squared_error(test_data_actual,test_data_predicted)
    r2_test_set = metrics.r2_score(test_data_actual,test_data_predicted)
    
    label_test = 'Test set (' + str('%.0f points,' % int(test_size))+ 'R2=' + str('%.3f' % r2_test_set) + '\nRMSE=' + str('%.3f' % RMSE_test_set) + ')'
    label_train= 'Train set (' + str('%.0f points,' % int(train_size))+ 'R2=' + str('%.3f' % r2_train_set) + '\nRMSE=' + str('%.3f' % RMSE_train_set) + ')'
      
    plt.figure(figsize=(7, 6.5))
    plt.axis((lower_lim,upper_lim,lower_lim,upper_lim))
    plt.xlabel('Solubility_Parameter (M/Pa)')
    plt.ylabel('Predicted_Solubility_Parameter (M/Pa)')
    plt.legend(loc = 'upper left')
    plt.rc('font', family='Arial narrow')
    plt.rc('xtick', labelsize=17)
    plt.rc('ytick', labelsize=17)

    plt.xlim(lim)
    plt.ylim(lim)
    plt.title(title, fontsize=15, fontweight='bold')

    dashed_layer = plt.plot(lim, lim, dashes=[5, 3], c='k', lw=2, zorder=0)

    train_err = plt.errorbar(train_data_actual, train_data_predicted, yerr= train_error, fmt ='s',c= 'b', lw=8, alpha=0.3, zorder=1)
    test_err = plt.errorbar(test_data_actual, test_data_predicted, yerr=test_error, fmt= 's', c='g', lw=8, alpha=0.3, zorder=2)
    train_scatter= plt.scatter(train_data_actual,train_data_predicted,s=30, c='b', edgecolor='k', marker='o', label=label_train, zorder=3)
    test_scatter = plt.scatter(test_data_actual,test_data_predicted,s=30, c='g', edgecolor='k', alpha=0.6, marker='s', label=label_test, zorder=4)
    plt.axis((lower_lim,upper_lim,lower_lim,upper_lim))
    plt.xlabel('Solubility_Parameter (M/Pa)')
    plt.ylabel('Predicted_Solubility_Parameter (M/Pa)')
    plt.legend(loc = 'upper left')
    plt.savefig(file_name[0], dpi=450)
    plt.show()
    plt.close()
 
    plt.figure(figsize=(7, 6.5))
    plt.axis((lower_lim,upper_lim,lower_lim,upper_lim))
    plt.xlabel('Solubility_Parameter (M/Pa)')
    plt.ylabel('Predicted_Solubility_Parameter (M/Pa)')
    plt.legend(loc = 'upper left')
    plt.rc('font', family='Arial narrow')
    plt.rc('xtick', labelsize=17)
    plt.rc('ytick', labelsize=17)
    
    plt.xlim(lim)
    plt.ylim(lim)
    plt.title(title, fontsize=15, fontweight='bold')
    
    dashed_layer = plt.plot(lim, lim, dashes=[5, 3], c='k', lw=2, zorder=0)
    
    test_err = plt.errorbar(test_data_actual, test_data_predicted, yerr= test_error, fmt= 's', c='g', lw=8, alpha=0.3, zorder=1)
    test_scatter = plt.scatter(test_data_actual,test_data_predicted,s=30, c='g', edgecolor='k', alpha=0.6, marker='s', label=label_test, zorder=2)
    plt.axis((lower_lim,upper_lim,lower_lim,upper_lim))
    plt.xlabel('Solubility_Parameter (M/Pa)')
    plt.ylabel('Predicted_Solubility_Parameter (M/Pa)')
    plt.legend(loc = 'upper left')
    plt.savefig(file_name[1], dpi=450)
    plt.show()
    plt.close() 
       
    plt.figure(figsize=(7, 6.5))
    plt.axis((lower_lim,upper_lim,lower_lim,upper_lim))
    plt.xlabel('Solubility_Parameter (M/Pa)')
    plt.ylabel('Predicted_Solubility_Parameter (M/Pa)')
    plt.legend(loc = 'upper left')
    plt.rc('font', family='Arial narrow')
    plt.rc('xtick', labelsize=17)
    plt.rc('ytick', labelsize=17)
    
    plt.xlim(lim)
    plt.ylim(lim)
    plt.title(title, fontsize=15, fontweight='bold')
    
    dashed_layer = plt.plot(lim, lim, dashes=[5, 3], c='k', lw=2, zorder=0)
    
    train_err = plt.errorbar(train_data_actual, train_data_predicted, yerr= train_error, fmt ='s',c= 'b', lw=8, alpha=0.3, zorder=1)
    train_scatter= plt.scatter(train_data_actual,train_data_predicted,s=30, c='b', edgecolor='k', marker='o', label=label_train, zorder=2)
    plt.axis((lower_lim,upper_lim,lower_lim,upper_lim))
    plt.xlabel('Solubility_Parameter (M/Pa)')
    plt.ylabel('Predicted_Solubility_Parameter (M/Pa)')
    plt.legend(loc = 'upper left')
    plt.savefig(file_name[2], dpi=450)
    plt.show()
    plt.close()
    
