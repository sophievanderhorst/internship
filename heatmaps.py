#!/usr/bin/env python

"""
I use this script to make heatmaps that show the ratio of Qle, Qh and NEE
for each site. I look at three different temperature distributions: 
overall, upper extreme and lower extreme for Qle, Qh and NEE. DData generatred by 
method2.py script.
"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.backends.backend_pdf #import PdfPages
import os
import matplotlib

#Function for heatmap (table-like)    
def heatmap(ax, data, sites, label, cmap, norm):
    im = ax.imshow(data, cmap = cmap, norm = norm, interpolation = 'nearest', 
                   aspect = 'auto')
    font = {'family': 'Arial Narrow', 'color':  'black','weight': 'normal', 
            'size': 8,}
    ax.set_xticklabels(label, fontdict = font)
    ax.set_yticklabels(sites, fontdict = font)
    ax.set_xticks(np.arange(len(label)))
    ax.set_yticks(np.arange(len(sites)))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    return im

#Function to format heatmaps (make certain text white and don't show the 0)   
def annotate_heatmap(im, data = None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=0.9, **textkw):    
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()
    kw = dict(horizontalalignment="center", verticalalignment="center")
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i,j]>=0 or data[i,j]<=0:
                kw.update(color=textcolors[(data[i, j]) >= threshold])
                kw.update (size = 8)
                kw.update (family = 'Arial Narrow')
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)
    return texts

#Function for formatting the tables 
def func(x, pos):
    return "{:.2f}".format(x).replace("0.", ".").replace("1.00", "1.0")

#open the data 
with open("../data/processed/results_LH.csv", newline='') as myFile:  
    df_results_LH = pd.read_csv(myFile)
    for row in df_results_LH:
        print(row) 
        
with open("../data/processed/results_SH.csv", newline='') as myFile:  
    df_results_SH = pd.read_csv(myFile)
    for row in df_results_SH:
        print(row) 

with open("../data/processed/results_NEE.csv", newline='') as myFile:  
    df_results_NEE = pd.read_csv(myFile)
    for row in df_results_NEE:
        print(row) 

df_data_LH = df_results_LH[['overall', 'smallerthan2stdev', 'largerthan2stdev']]
duplicated =  df_data_LH.duplicated()


sites = np.array(df_results_LH['site'])
label = ["All temps", "Lower extreme", "Higher extreme"]
data_LH = np.array(df_results_LH[['overall', 'smallerthan2stdev', 'largerthan2stdev']])
data_SH = np.array(df_results_SH[['overall', 'smallerthan2stdev', 'largerthan2stdev']])
data_NEE = np.array(df_results_NEE[['overall', 'smallerthan2stdev', 'largerthan2stdev']])
cmap = matplotlib.colors.ListedColormap(['#d73027', '#fc8d59', '#fee090', 
                                            '#e0f3f8', '#91bfdb', '#4575b4'])
norm = matplotlib.colors.BoundaryNorm([0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0], cmap.N)

#Qle
fig, ax = plt.subplots(nrows = 1, ncols = 7, figsize = (11,9))
plt.suptitle("Measurement ratios of Qle", x =0.5, y = 0.94)
im =heatmap(ax[0], data_LH[0:29][:], sites[0:29][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[1], data_LH[29:58][:], sites[29:58][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[2], data_LH[58:87][:], sites[58:87][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[3], data_LH[87:116][:], sites[87:116][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[4], data_LH[116:145][:], sites[116:145][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[5], data_LH[145:174][:], sites[145:174][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[6], data_LH[174:203][:], sites[174:203][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
fig.subplots_adjust( bottom=0.1, right=0.9, top=0.9, wspace=1, hspace=0)
cax = plt.axes([0.92, 0.1, 0.01, 0.8]) 
plt.colorbar(im, cax=cax, spacing = 'proportional')
plt.show()

plot_dir = "../plots"
ofname = "heatmap_LH.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1, dpi = 300)

#Qh
fig, ax = plt.subplots(nrows = 1, ncols = 7, figsize = (11,9))
plt.suptitle("Measurement ratios of Qh ", x =0.5, y = 0.94)
im = heatmap(ax[0], data_SH[0:29][:], sites[0:29][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[1], data_SH[29:58][:], sites[29:58][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[2], data_SH[58:87][:], sites[58:87][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[3], data_SH[87:116][:], sites[87:116][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[4], data_SH[116:145][:], sites[116:145][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[5], data_SH[145:174][:], sites[145:174][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[6], data_SH[174:203][:], sites[174:203][:], label, cmap, norm) 
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
fig.subplots_adjust( bottom=0.1, right=0.9, top=0.9, wspace=1, hspace=0)
cax = plt.axes([0.92, 0.1, 0.01, 0.8]) 
plt.colorbar(im, cax=cax, spacing = 'proportional')  
plt.show()

plot_dir = "../plots"
ofname = "heatmap_SH.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)

#NEE
fig, ax = plt.subplots(nrows = 1, ncols = 7, figsize = (11,9))
plt.suptitle("Measurement ratios of NEE", x =0.5, y = 0.94)
im = heatmap(ax[0], data_NEE[0:29][:], sites[0:29][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[1], data_NEE[29:58][:], sites[29:58][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[2], data_NEE[58:87][:], sites[58:87][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[3], data_NEE[87:116][:], sites[87:116][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[4], data_NEE[116:145][:], sites[116:145][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[5], data_NEE[145:174][:], sites[145:174][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
im = heatmap(ax[6], data_NEE[174:203][:], sites[174:203][:], label, cmap, norm)
annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func))
fig.subplots_adjust( bottom=0.1, right=0.9, top=0.9, wspace=1, hspace=0)
cax = plt.axes([0.92, 0.1, 0.01, 0.8]) 
plt.colorbar(im, cax=cax, spacing = 'proportional')
plt.show()

plot_dir = "../plots"
ofname = "heatmap_NEE.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)














       
        
        
        
        
        
        
        
        