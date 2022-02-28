#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 10:30:42 2022

@author: ymonjid
"""

import Glassdoor_scraper as gs
import pandas as pd

path = "/home/ymonjid/Desktop/Project_Data_science/Sahibinden_Flat_price/chromedriver_linux64_2/chromedriver"

df = gs.get_jobs('Data-Scientist-Jobs', 1000, False, path)

df.to_csv('Glassdoor_Datascientist_Jobs_France.csv', index=False)

# df = pd.read_csv('Glassdoor_Datascientist_Jobs.csv')