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



# df = pd.read_csv('EDA_Glassdoor_DS_jobs.csv')
df = pd.read_csv('Glassdoor_ds_jobs_cleaned.csv')

#df = df.drop('Unnamed: 0', axis=1)

# 1) Choose relevant columnsa
df.columns
df_model = df[['avg salary', 'Rating', 'Founded', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
               'hourly', 'Employer Provided', 'State', 'Age', 'Python', 'Machine Learning',
               'Deep Learning', 'Big Data', 'Statistic', 'Math', 'Job simplified', 'Seniority', 'job desc len']]
# df_model = df[['avg salary', 'Rating', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
#                 'hourly', 'Employer Provided', 'State', 'Age', 'Python', 'Machine Learning',
#               'Math','Seniority']]

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
    alpha.append(i/100)
    lm_L = Lasso(alpha=(i/100))
    cr = cross_val_score(lm_L, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
    scores_L.append(cr.mean())
    
plt.plot(alpha, scores_L)

## c) Random Forest
rf = RandomForestRegressor()
cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)
### Tune the rf model using GridsearchCV
parameters = {'n_estimators': range(10,200,20), 'criterion':('mae', 'mse'), 'max_features':('auto', 'sqrt', 'log2')}
clf = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
clf.fit(X_train, y_train)


## d) Gradient Boosting Tree
reg = GradientBoostingRegressor()
cross_val_score(reg, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)

R = np.arange(0.01, 1, 0.05)
parameters = {'learning_rate': R, 'n_estimators': range(10,200,20)}
clf_GB = GridSearchCV(reg, parameters, scoring='neg_mean_absolute_error', cv=3)
clf_GB.fit(X_train, y_train)

# 6) Test ensembles