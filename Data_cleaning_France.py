#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 17:44:52 2022

@author: ymonjid
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 12:06:36 2022

@author: ymonjid
"""

import pandas as pd
import numpy as np

df = pd.read_csv('Glassdoor_Datascientist_Jobs_France.csv')

# 1) salary parsing (removing the "K", the "€", the "(Est. de Glassdoor)", "Salaire fourni ...", 
# and converting the hourly to annually)
# Removing the rows with salaries = -1
df = df[df['Salary Estimate'] != '-1']
# Removing the "Glassdoor est. text
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]) 
# Removing the "K"'s and $ sign
minus_ks = salary.apply(lambda x: x.replace('k','').replace('€',''))
# Create a column to 'per hour' and 'Employer provided salary'
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'par heure' in x.lower() else 0)
df['Employer Provided'] = df['Salary Estimate'].apply(lambda x: 1 if "salaire fourni par l'employeur:" in x.lower() else 0)
# Removing  'Par heure' and 'Salaire fourni par l'employeur:'
min_per_hr = minus_ks.apply(lambda x: x.lower().replace('par heure', ''))
min_employer = min_per_hr.apply(lambda x: x.lower().replace("salaire fourni par l'employeur:", ''))
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
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.5)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.7)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.8)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(3.9)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(4.0)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(4.1)) else x)
comp = comp.apply(lambda x: x[:-3] if (x[-3:] == str(4.2)) else x)
df['Company Name'] = comp

# 3) State field
df['State'] = df['Location'].apply(lambda x: x.split(',')[0])

# 4) Replacing the 'Unknown' in 'Type of ownership' by Company-Private or -Public
df.loc[(df['Founded'] == 'Entreprise non cotée en bourse')&(df['Type of ownership']=='Ne sait pas / non applicable'), 'Type of ownership'] = 'Entreprise non cotée en bourse'
df.loc[(df['Founded'] == 'Travailleur indépendant')&(df['Type of ownership']=='Ne sait pas / non applicable'), 'Type of ownership'] = 'Travailleur indépendant'
df.loc[(df['Founded'] == 'Entreprise cotée en bourse')&(df['Type of ownership']=='Ne sait pas / non applicable'), 'Type of ownership'] = 'Entreprise cotée en bourse'

# 5) Determining the age of the company
## Companies with non-year in 'Founded'
NameComp = df.apply(lambda x: x['Company Name'] if (x['Founded']=='Entreprise non cotée en bourse' or x['Founded']=='Entreprise cotée en bourse'
                                                     or x['Founded']=='Travailleur indépendant') else 'None', axis=1)
NameComp.value_counts()
Comp = pd.DataFrame(NameComp[NameComp != 'None'].unique())

## List of creation years of the companies in 'Companies'
y = [1929, 1938, 2007, 2014, 1963, 1994, 2013, 1996, 2012, 2017, 2007, 2011, 2017, 2020, 1979, 2020, 1991, 2016]
dic = {}
for i in range(0,len(y)):
    dic[Comp[0][i]] = y[i]
df['Founded'] = df.apply(lambda x: dic[x['Company Name']] if (x['Company Name'] in dic) else x['Founded'], axis=1)
df.loc[df['Founded'] == 'Cabinet / Société du secteur privé', 'Founded'] = 2015

## Calculating the age of the company
df['Age'] =  df.apply(lambda x: 2022 - int(x['Founded']) if int(x['Founded']) != -1 else -1, axis=1)

# Removing the exact same rows
df.drop_duplicates(subset = df.columns, keep = False, inplace = True)

# 5) Parsing of the job desription (python ...)
df['Python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['Python'].value_counts()
df['R'] = df['Job Description'].apply(lambda x: 1 if 'R' in x else 0)
df['R'].value_counts()
df['SQL'] = df['Job Description'].apply(lambda x: 1 if 'SQL' in x else 0)
df['SQL'].value_counts()
df['Machine Learning'] = df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
df['Machine Learning'].value_counts()
df['Big Data'] = df['Job Description'].apply(lambda x: 1 if 'big data' in x.lower() else 0)
df['Statistique'] = df['Job Description'].apply(lambda x: 1 if 'statisti' in x.lower() else 0)
df['Math'] = df['Job Description'].apply(lambda x: 1 if 'math' in x.lower() else 0)
df['Master'] = df['Job Description'].apply(lambda x: 1 if 'master' in x.lower() else 0)
df['AWS'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

# 6) Saving the cleaned data to CSV file
df.to_csv('Glassdoor_ds_jobs_France_cleaned.csv', index=False)

