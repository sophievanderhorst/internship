

"""
I use this script to make zoommaps which show the ratio of measurements of
Qle, Qh and NEE for each FLUXNET and LaThuille site. 

"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.backends.backend_pdf #import PdfPages
import matplotlib
import os
import numpy as np

#fuction for making temperature-precipitation plots
def prectemp(tag, temp, precip, lat, lon, vals, title, ax, label):
    cmap = matplotlib.colors.ListedColormap(['#d73027', '#fc8d59', '#fee090', 
                                             '#e0f3f8', '#91bfdb', '#4575b4'])
    norm = matplotlib.colors.BoundaryNorm([0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0], cmap.N)
    ax.set_title(title, fontsize = 12)                                         
    ax.tick_params(axis = 'both', which = 'major', labelsize = 10)
    for tag, temp, precip, lat, lon, val in zip(tag, temp, precip, lat, lon, vals):
        if val >= 0 and val<0.3:
            color = '#d73027'
        elif val >= 0.3 and val <0.5:
            color= '#fc8d59'
        elif val >= 0.5 and val <0.7:
            color = '#fee090'
        elif val >= 0.7 and val <0.8:
            color =  '#e0f3f8'
        elif val >= 0.8 and val < 0.9:
            color = '#91bfdb'
        elif val >= 0.9:
            color = '#4575b4'
        else:
            color = "white"
    
        if lat < -10 and lat > -40 and lon >110  and lon <155:
                sc = ax.scatter(temp, precip, s= 30, c= color, cmap=cmap, norm=norm )
                if val >= 0 :
                    x = temp
                    y = precip
                    if tag == 'AU-Tum' or tag =='AU-Wom' or tag == 'AU-Rob'\
                    or tag == 'AU-How'or tag == 'AU-Cpr' or tag == 'AU-ASM' \
                    or tag == 'AU-Emr' or tag == 'AU-Whr' or tag == 'AU-Ync'\
                    or tag == 'AU-Rig' or tag == 'AU-Ade' or tag == 'AU-Fog'\
                    or tag == 'AU-DaP' or tag == 'AU-RDF':
                        ax.text(x-7.7, y-15, tag, fontsize=7)
                    else: 
                        ax.text(x+0.6, y-15, tag, fontsize=7)
                
                
                
                """
                ax.annotate(tag,
                xy=(temp, precip), xytext=(-20, 20),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', alpha=0.5),
                arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
                """
        else:
           sc = ax.scatter(temp, precip, s= 3, c= 'black', alpha = 0.3 )
    ax.text(-0.1,1.1, label, size = 12,  horizontalalignment='center', 
    verticalalignment='center', transform=ax.transAxes)
    return(fig, sc)

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

cmap = matplotlib.colors.ListedColormap(['#d73027', '#fc8d59', '#fee090', 
                                           '#e0f3f8', '#91bfdb', '#4575b4'])       
img = plt.imshow(np.array([[0,1]]), 
                 cmap = cmap,
                norm = matplotlib.colors.BoundaryNorm([0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0], cmap.N))

plt.clf()
img.set_visible(not img.get_visible())
plt.draw()

#precipitation-temperature plots
fig, ax = plt.subplots(nrows=3, ncols=3, figsize =(10,15))
cbar_ax = fig.add_axes([1.001, 0.69, 0.01, 0.265])
cbar_ax2 = fig.add_axes([1.001, 0.37 , 0.01, 0.265])
cbar_ax3 = fig.add_axes([1.001, 0.05, 0.01, 0.265])


prectemp(df_results_LH.site,
        df_results_LH.meantemp-273,  df_results_LH.meanprec, 
         df_results_LH.lat, df_results_LH.lon,
         df_results_LH.overall, "Qle ratio overall ",  ax[0,0], "(a)")
prectemp(df_results_SH.site, 
        df_results_SH.meantemp-273, df_results_SH.meanprec, 
         df_results_SH.lat, df_results_SH.lon,
         df_results_SH.overall, "Qh ratio overall ",  ax[1,0], "(b) ")
prectemp(df_results_NEE.site, 
        df_results_NEE.meantemp-273, df_results_NEE.meanprec, 
         df_results_NEE.lat, df_results_NEE.lon,
         df_results_NEE.overall,"NEE ratio overall ",  ax[2,0], "(c)")
#above 2 stdev performance LH, SH, NEE
prectemp(df_results_LH.site,
        df_results_LH.meantemp-273, df_results_LH.meanprec, 
         df_results_LH.lat, df_results_LH.lon,
         df_results_LH.largerthan2stdev, "Qle ratio upper extreme", ax[0,2], " ")
prectemp(df_results_SH.site,
        df_results_SH.meantemp-273, df_results_SH.meanprec, 
         df_results_SH.lat, df_results_SH.lon,
         df_results_SH.largerthan2stdev, "Qh ratio upper extreme", ax[1,2], " ")
prectemp(df_results_NEE.site,
        df_results_NEE.meantemp-273, df_results_NEE.meanprec,
         df_results_NEE.lat, df_results_NEE.lon,
         df_results_NEE.largerthan2stdev,"NEE ratio upper extreme", ax[2,2], "")
#below 2 stdev performance LH, SH, NEE
prectemp(df_results_LH.site,
        (df_results_LH.meantemp-273), df_results_LH.meanprec, 
         df_results_LH.lat, df_results_LH.lon,
         df_results_LH.smallerthan2stdev, "Qle ratio lower extreme", ax[0,1], " ")
prectemp(df_results_SH.site,
        df_results_SH.meantemp-273, df_results_SH.meanprec, 
         df_results_SH.lat, df_results_SH.lon,
         df_results_SH.smallerthan2stdev,"Qh ratio lower extreme", ax[1,1], " ")
fig, sc = prectemp(df_results_NEE.site,
        df_results_NEE.meantemp-273, df_results_NEE.meanprec, 
                  df_results_NEE.lat, df_results_NEE.lon,
                  df_results_NEE.smallerthan2stdev, "NEE ratio lower extreme", ax[2,1], " ")

ax[2,0].set_xlabel("Temperature ($^\circ$C)", fontsize = 12)
ax[2,1].set_xlabel("Temperature ($^\circ$C)", fontsize = 12)
ax[2,2].set_xlabel("Temperature ($^\circ$C)", fontsize = 12)
ax[0,0].set_ylabel("Precipitation (mm $yr^{-1}$)", fontsize = 12)
ax[1,0].set_ylabel("Precipitation (mm $yr^{-1}$)", fontsize = 12)
ax[2,0].set_ylabel("Precipitation (mm $yr^{-1}$)", fontsize = 12)

cmap = matplotlib.colors.ListedColormap(['#d73027', '#fc8d59', '#fee090', 
                                            '#e0f3f8', '#91bfdb', '#4575b4'])


                                           
plt.colorbar(img, cax =cbar_ax, orientation = 'vertical',
         boundaries = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0], 
         spacing = 'proportional', 
         ticks = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0])
plt.colorbar(img, cax = cbar_ax2, orientation="vertical", 
         boundaries = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0], 
         spacing = 'proportional', 
         ticks = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0])
plt.colorbar(img, cax = cbar_ax3, orientation="vertical", 
         boundaries = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0], 
         spacing = 'proportional', 
         ticks = [0, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0])


fig.tight_layout()


plot_dir = "../plots"
ofname = "AUS_temp-precip.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)






    
    
    
