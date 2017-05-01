# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 09:19:40 2016

@author: Jack
"""
#%%
import pandas as pd
import matplotlib.pyplot as plt

#%% Read data
df = pd.read_csv(r'C:\Users\Jack\Desktop\file.dmp',
                 index_col=0)
    
#%% Outliers
df['mean'] = df['measure'].mean()
df['+1 StD'] = df['mean'] + df['measure'].std()
df['-1 StD'] = df['mean'] - df['measure'].std()
df['+3 StD'] = df['mean'] + (df['measure'].std() * 3)
df['-3 StD'] = df['mean'] - (df['measure'].std() * 3)
df['measure'] = df['measure'].rolling(2).mean()

df = df[df['measure'] < df['+3 StD']]
df = df[df['measure'] > df['-3 StD']]
df.plot(legend=False)

#%% Loop it bitch
crossStd = False
cycles = []

for index, row in df.iterrows():
    if (not(crossStd) and (row['measure'] > row['+1 StD'])):
        crossStd = True
        cycles.append(index)
        
    if ((crossStd) and (row['measure'] < row['mean'])):
        crossStd = False
        
#%% Visualize
df2 = pd.concat([df, df['measure'].ix[cycles]],axis=1)
df2.columns = ['measure', 'mean', '+1 StD', '-1 StD', '+3 Std', '-3 StD', 'peak']
df2.plot(legend=False)
df2['peak'].plot(style='rd', markersize=10)
