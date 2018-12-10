#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:10:43 2018

@author: z5228341
"""

import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.backends.backend_pdf #import PdfPages
import os
import matplotlib
from statsmodels.regression.linear_model import OLSResults


with open("../data/processed/results_LH.csv", newline='') as myFile:  
    df_results_LH = pd.read_csv(myFile)
 
        
with open("../data/processed/results_SH.csv", newline='') as myFile:  
    df_results_SH = pd.read_csv(myFile)


with open("../data/processed/results_NEE.csv", newline='') as myFile:  
    df_results_NEE = pd.read_csv(myFile)


pdf = matplotlib.backends.backend_pdf.PdfPages("regression_LH.pdf")

print("Regression LH -- overall")
#LH
#Overall
df = pd.DataFrame(df_results_LH[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_LH.overall, columns= ['overall'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['overall']
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
predictions = model.predict(x) 

print(model.summary())
print("")
print("Regression LH -- lower tail")
#Lower tail
df = pd.DataFrame(df_results_LH[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_LH.smallerthan2stdev, columns= ['smallerthan2stdev'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['smallerthan2stdev']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())
print("")
print("Regression LH -- upper tail")
#upper tail
df = pd.DataFrame(df_results_LH[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_LH.largerthan2stdev, columns= ['largerthan2stdev'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['largerthan2stdev']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())
print("")
#SH
print("Regression SH -- overall")
#Overall
df = pd.DataFrame(df_results_SH[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_SH.overall, columns= ['overall'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['overall']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())
print("")
print("Regression SH -- lower tail")
#lower tail
df = pd.DataFrame(df_results_SH[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_SH.smallerthan2stdev, columns= ['smallerthan2stdev'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['smallerthan2stdev']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())
print("")
print("Regression SH -- upper tail")
#upper tail
df = pd.DataFrame(df_results_SH[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_SH.largerthan2stdev, columns= ['largerthan2stdev'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['largerthan2stdev']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())

#NEE
print("")
print("Regression NEE -- overall")

#Overall
df = pd.DataFrame(df_results_NEE[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_NEE.overall, columns= ['overall'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['overall']
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
predictions = model.predict(x) 
print(model.summary())
print("")
print("Regression NEE -- lower tail")

#lower tail
df = pd.DataFrame(df_results_NEE[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_NEE.smallerthan2stdev, columns= ['smallerthan2stdev'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['smallerthan2stdev']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())
print("")
print("Regression NEE -- upper tail")
#upper tail
df = pd.DataFrame(df_results_NEE[['length', 'meantemp', 'meanprec', 'lon', 'lat']], columns= ['length', 'meantemp', 'meanprec', 'lon', 'lat'])
target = pd.DataFrame(df_results_NEE.largerthan2stdev, columns= ['largerthan2stdev'])
x = df[['length', 'meantemp', 'meanprec', 'lon', 'lat']]
y = target['largerthan2stdev']
x = sm.add_constant(x)
model = sm.OLS(y, x, missing='drop').fit()
predictions = model.predict(x) 
print(model.summary())
