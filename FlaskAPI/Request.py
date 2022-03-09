#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 18:15:14 2022

@author: ymonjid
"""

import requests
from data_input import data_in

URL = 'http://127.0.0.1:5000/predict'
PARAMS = {'Content-Type': 'application/json'}
data = {'input': data_in}

r = requests.get(URL, headers=PARAMS, json=data)

r.json()