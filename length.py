#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
I use this script to make plots that show the relationship between the first half 
of the data collection and the second half of the data collection. Also, I 
show the relationship between the length of the dataset and the measurements ratios
of the fluxes. These are used for Supplementary figure 1. 

"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.backends.backend_pdf #import PdfPages
import os



with open("../data/processed/results_LH.csv", newline='') as myFile:  
    df_results_LH = pd.read_csv(myFile)
 
        
with open("../data/processed/results_SH.csv", newline='') as myFile:  
    df_results_SH = pd.read_csv(myFile)


with open("../data/processed/results_NEE.csv", newline='') as myFile:  
    df_results_NEE = pd.read_csv(myFile)
    
    
with open("../data/processed/results_LH_first.csv", newline='') as myFile:  
    df_results_LH_first = pd.read_csv(myFile)
    print(len(df_results_LH_first))
 
        
with open("../data/processed/results_SH_first.csv", newline='') as myFile:  
    df_results_SH_first = pd.read_csv(myFile)


with open("../data/processed/results_NEE_first.csv", newline='') as myFile:  
    df_results_NEE_first = pd.read_csv(myFile)
    
with open("../data/processed/results_LH_second.csv", newline='') as myFile:  
    df_results_LH_second = pd.read_csv(myFile)
    
    print(len(df_results_LH_second))
         
with open("../data/processed/results_SH_second.csv", newline='') as myFile:  
    df_results_SH_second = pd.read_csv(myFile)

with open("../data/processed/results_NEE_second.csv", newline='') as myFile:  
    df_results_NEE_second = pd.read_csv(myFile)

fig, ax = plt.subplots(ncols = 2, nrows = 3, figsize = (10,14))

ax[0,1].scatter(df_results_LH.length, df_results_LH.overall, s = 20)
ax[0,1].scatter(df_results_LH.length, df_results_LH.smallerthan2stdev, s = 20)
ax[0,1].scatter(df_results_LH.length, df_results_LH.largerthan2stdev, s = 20)
ax[0,1].set_ylabel("Measurement ratio")
ax[0,1].set_title("Qle")

ax[1,1].scatter(df_results_SH.length, df_results_SH.overall, s = 20)
ax[1,1].scatter(df_results_SH.length, df_results_SH.smallerthan2stdev, s = 20)
ax[1,1].scatter(df_results_SH.length, df_results_SH.largerthan2stdev, s = 20)
ax[1,1].set_ylabel("Measurement ratio")
ax[1,1].set_title("Qh")

ax[2,1].scatter(df_results_NEE.length, df_results_NEE.overall, s = 20)
ax[2,1].scatter(df_results_NEE.length, df_results_NEE.smallerthan2stdev, s = 20)
ax[2,1].scatter(df_results_NEE.length, df_results_NEE.largerthan2stdev, s = 20)
ax[2,1].set_xlabel("Number of temperature measurements")
ax[2,1].set_ylabel("Measurement ratio")
ax[2,1].set_title("NEE")


ax[0,0].scatter(df_results_LH_first.overall, df_results_LH_second.overall, s = 20)
ax[0,0].scatter(df_results_LH_first.smallerthan2stdev, df_results_LH_second.smallerthan2stdev, s = 20)
ax[0,0].scatter(df_results_LH_first.largerthan2stdev, df_results_LH_second.largerthan2stdev, s = 20)
ax[0,0].set_ylabel("Measurement ratio second half")
ax[0,1].legend(['Overall', 'Lower tail', 'Upper tail'])
ax[0,0].set_title("Qle")

ax[1,0].scatter(df_results_SH_first.overall, df_results_SH_second.overall, s = 20)
ax[1,0].scatter(df_results_SH_first.smallerthan2stdev, df_results_SH_second.smallerthan2stdev, s = 20)
ax[1,0].scatter(df_results_SH_first.largerthan2stdev, df_results_SH_second.largerthan2stdev, s = 20)
ax[1,0].set_ylabel("Measurement ratio second half")
ax[1,0].set_title("Qh")

ax[2,0].scatter(df_results_NEE_first.overall, df_results_NEE_second.overall, s = 20)
ax[2,0].scatter(df_results_NEE_first.smallerthan2stdev, df_results_NEE_second.smallerthan2stdev, s = 20)
ax[2,0].scatter(df_results_NEE_first.largerthan2stdev, df_results_NEE_second.largerthan2stdev, s = 20)
ax[2,0].set_xlabel("Measurement ratio first half")
ax[2,0].set_ylabel("Measurement ratio second half")
ax[2,0].set_title("NEE")



for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation = 30, ha="center", size = 10, alpha = 0.85)  
plt.tight_layout()

plot_dir = "../plots"
ofname = "datalength.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)

