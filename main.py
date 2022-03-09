#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 10:30:42 2022

@author: ymonjid
"""

import pandas as pd

path = "/home/ymonjid/Desktop/Project_Data_science/Sahibinden_Flat_price/chromedriver_linux64_2/chromedriver"
keyword = 'Data-Scientist-Jobs'
num_jobs = 1000

# 1) Data scraping
import Glassdoor_scraper as gs
df = gs.get_jobs(keyword, num_jobs, False, path)
data = 'Glassdoor_ds_jobs_2.csv'
# df.to_csv('Glassdoor_ds_jobs_France.csv', index=False)
df.to_csv(data, index=False)
# df = pd.read_csv(data)

# 2) Data cleaning
import Data_cleaning as dc
clean_data = 'Glassdoor_ds_jobs_cleaned_2.csv'
df_clean = dc.Data_cleaning(data)
df_clean.to_csv(clean_data, index=False)

# 3) Model building
import Building_models as bm
lm, lm_L, clf_rf, clf_GB, X_test, y_test = bm.Building_models(clean_data)

# 4) Test ensembles
from sklearn.metrics import mean_absolute_error
Ypred_lm = lm.predict(X_test)
Ypred_lmL = lm_L.predict(X_test)
Ypred_rf = clf_rf.best_estimator_.predict(X_test)
Ypred_GB = clf_GB.best_estimator_.predict(X_test)
mae_lm = mean_absolute_error(Ypred_lm, y_test)
mae_lmL = mean_absolute_error(Ypred_lmL, y_test)
mae_rf = mean_absolute_error(Ypred_rf, y_test)
mae_GB = mean_absolute_error(Ypred_GB, y_test)

# 5) Predict a new output
for i in range(1,len(y_test)):
    print(Ypred_lm[i], Ypred_lmL[i], Ypred_rf[i], Ypred_GB[i], y_test[i])



