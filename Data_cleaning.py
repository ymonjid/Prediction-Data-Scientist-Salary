#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 12:06:36 2022

@author: ymonjid
"""

import pandas as pd

df = pd.read_csv('Glassdoor_Datascientist_Jobs.csv')

# 1) salary parsing (removing the "K", the "$", the "(Glassdoor est.)", "Employer...", 
# and converting the hourly to annually)
# Removing the rows with salaries = -1
df = df[df['Salary Estimate'] != '-1']
# Removing the "Glassdoor est. text
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]) 
# Removing the "K"'s and $ sign
minus_ks = salary.apply(lambda x: x.replace('K','').replace('$',''))
# Create a column to 'per hour' and 'Employer provided salary'
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['Employer Provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)
# Removing  'Per hour' and 'Employer Provided Salary'
min_per_hr = minus_ks.apply(lambda x: x.lower().replace('per hour', ''))
min_employer = min_per_hr.apply(lambda x: x.lower().replace('employer provided salary:', ''))
# A column for min and max salary
df['min salary'] = min_employer.apply(lambda x: int(x.split('-')[0])) 
df['max salary'] = min_employer.apply(lambda x: int(x.split('-')[1]) if (len(x.split('-'))==2)  else  int(x.split('-')[0]))
# Converting hourly salary to annually
df.loc[df['hourly'] == 1, 'min salary'] = 2*df['min salary']
df.loc[df['hourly'] == 1, 'max salary'] = 2*df['max salary']
# Computing the average salary
df['avg salary'] = (df['min salary'] + df['max salary'])/2
# Removing the column of Salary Estimate
del(df['Salary Estimate'])

# 2) Remove the rating from the company name
# Keep the company name if the rating < 0
comp = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)
# Restore teh company name when the rating is not added in the company name field
comp = df.apply(lambda x: x['Company Name'][:-3] if x['Company Name'][-3:]==str(x['Rating']) else x['Company Name'], axis=1)
# Remove the ratings in some rows where the values of the rating in the company name are different
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.3)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.8)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.9)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(4.1)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(4.2)) else x)
df['Company Name'] = comp

# 3) State field
df['State'] = df['Location'].apply(lambda x: x.split(',')[0])

# 4) Replacing the 'Unkniwn' in 'Type of ownership' by Company-Private or -Public
df.loc[(df['Founded'] == 'Company - Private')&(df['Type of ownership']=='Unknown / Non-Applicable'), 'Type of ownership'] = 'Company - Private'
df.loc[(df['Founded'] == 'Company - Public')&(df['Type of ownership']=='Unknown / Non-Applicable'), 'Type of ownership'] = 'Company - Pubic'

# 5) Determining the age of the company
## Changing the 'Company - Private' in 'Founded' by the real incorporation year
df.loc[df['Founded']=='Company - Private', 'Company Name'].value_counts()
dict_Private = {'UTOFUN\n' : 2016, 'InspiHER Tech' : 1995, 'ClimateAI\n' : 2008, 'IT Consulting Services\n' : 2005, 
        'Acorn Analytics' : 2016, 'FocusKPI Inc.\n' : 2010, 'Avila Trading\n' : 2017, 'Nexintech Inc.' : 2020, 
        'Myticas Consulting\n' : 2016, 'zb.io\n' : -1, 'Kattech Systems Inc\n' : 2016
        }
df['Founded'] = df.apply(lambda x: dict_Private[x['Company Name']] if (x['Company Name'] in dict_Private) else x['Founded'], axis=1)

## Changing the 'Company - Public' in 'Founded' by the real incorporation year
df.loc[df['Founded']=='Company - Public', 'Company Name'].value_counts()
dict_Public = {'IntelliGen Technologies\n' : 1996, 'Dynamic Placement Services, LLC' : 2020}
df['Founded'] = df.apply(lambda x: dict_Public[x['Company Name']] if (x['Company Name'] in dict_Public) else x['Founded'], axis=1)

## Calculating the age of the company
df['Age'] =  df.apply(lambda x: 2022 - int(x['Founded']) if int(x['Founded']) != -1 else -1, axis=1)

# 5) Parsing of the job desription (python ...)
df['Python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['R'] = df['Job Description'].apply(lambda x: 1 if 'R' in x else 0)
df['SQL'] = df['Job Description'].apply(lambda x: 1 if 'SQL' in x else 0)
df['Machine Learning'] = df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
df['Deep Learning'] = df['Job Description'].apply(lambda x: 1 if 'deep learning' in x.lower() else 0)
df['Big Data'] = df['Job Description'].apply(lambda x: 1 if 'big data' in x.lower() else 0)
df['Statistic'] = df['Job Description'].apply(lambda x: 1 if 'statistic' in x.lower() else 0)
df['Math'] = df['Job Description'].apply(lambda x: 1 if 'math' in x.lower() else 0)
df['Master'] = df['Job Description'].apply(lambda x: 1 if 'master' in x.lower() else 0)
df['AWS'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['SPARK'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

