#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 08:33:27 2022

@author: ymonjid
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
import statsmodels.api as sm
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor

def Building_models(file_in):
    df = pd.read_csv(file_in)
    
    # df = pd.read_csv('EDA_Glassdoor_DS_jobs.csv')
    #df = pd.read_csv('Glassdoor_ds_jobs_cleaned.csv')
    # df = pd.read_csv('Glassdoor_ds_jobs_cleaned_test.csv')
    #df = df.append(df_test, ignore_index=True)
    
    #df = df.drop('Unnamed: 0', axis=1)
    
    # 1) Choose relevant columnsa
    df.columns
    df_model = df[['avg salary', 'Rating', 'Founded', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
                   'hourly', 'Employer Provided', 'State', 'Age', 'Python', 'Machine Learning',
                   'Deep Learning', 'Big Data', 'Statistic', 'Math', 'Job simplified', 'Seniority', 'job desc len']]
    
    # 2) Generate dummy variables
    df_dummy = pd.get_dummies(df_model)
    
    # 3) Train Test split
    X = df_dummy.drop('avg salary', axis=1)
    y = df_dummy['avg salary'].values
    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=42)
    
    # 4) Build models
    ## a) Multiple Linear Regression
    X_sm = sm.add_constant(X)
    model = sm.OLS(y, X_sm)
    model.fit().summary()
    
    lm = LinearRegression()
    lm.fit(X_train, y_train)
    scores = cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
    scores.mean(), scores.std()
    
    ## b) Lasso Rregression
    lm_L = Lasso()
    cross_val_score(lm_L, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
    ### Trying various values for alpha

    alpha = []
    scores_L = []
    for i in range(1,100):
        alpha.append(i/10)
        lm_L = Lasso(alpha=(i/100))
        cr = cross_val_score(lm_L, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
        scores_L.append(cr.mean())
        

    plt.plot(alpha, scores_L)
    error = tuple(zip(alpha, scores_L))
    df_err = pd.DataFrame(error, columns=['alpha', 'error'])
    alpha_best = df_err[df_err.error == max(df_err.error)]['alpha']
    
    lm_L = Lasso(alpha=float(alpha_best))      
    lm_L.fit(X_train, y_train)
 
    ## c) Random Forest
    rf = RandomForestRegressor()
    cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
    ### Tune the rf model using GridsearchCV
    parameters = {'n_estimators': range(10,200,20), 'criterion':('mae', 'mse'), 'max_features':('auto', 'sqrt', 'log2')}
    clf_rf = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
    clf_rf.fit(X_train, y_train)
    
    ## d) Gradient Boosting Tree
    GB = GradientBoostingRegressor()
    cross_val_score(GB, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
    
    R = np.arange(0.01, 1, 0.05)
    parameters = {'learning_rate': R, 'n_estimators': range(10,200,20)}
    clf_GB = GridSearchCV(GB, parameters, scoring='neg_mean_absolute_error', cv=3)
    clf_GB.fit(X_train, y_train)

    return lm, lm_L, clf_rf, clf_GB, X_test, y_test

# X_train.iloc[0]['Rating'] = 4.0
# X_train.iloc[0]['Age'] = 5
# X_train.iloc[0]['Founded'] = 2017

# # Predict a salary
# X_pred = pd.read_csv('X_to_predict.csv')
# X_pred = X_pred[['Rating', 'Founded', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
#                'hourly', 'Employer Provided', 'State', 'Age', 'Python', 'Machine Learning',
#                'Deep Learning', 'Big Data', 'Statistic', 'Math', 'Job simplified', 'Seniority', 'job desc len']]
# X_pred_dum = pd.get_dummies(X_pred)

# Ypred_lm = lm.predict(X_pred_dum)

# Ypred_lmL = lm_L.predict(X_pred_dum)

# Ypred_clf = clf_GB.best_estimator_.predict(X_pred_dum)

# X = X.drop(columns='State_Long Beach')
# X['State_Long Beach']
# i = 758
# print(y[i])
# X.iloc[i].shape
# Ypred_lm = lm.predict(np.array(X.iloc[i]).reshape(1,-1))
# print(Ypred_lm)
# Ypred_lmL = lm_L.predict(np.array(X.iloc[i]).reshape(1,-1))
# print(Ypred_lmL)
# Ypred_clf = clf_GB.best_estimator_.predict(np.array(X.iloc[i]).reshape(1,-1))
# print(Ypred_clf)

# for i in range(1,len(X.columns)):
#     if X.columns[i-1] in df_col:
#         pass
#     else:
#         print(X.columns[i-1])
