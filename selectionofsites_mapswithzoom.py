#!/usr/bin/env python

"""
This is used to select sites with the highest measurement ratios of Qle, Qh 
and NEE. Sites are selected where all ratios are above 0.9 or 0.8. Also, sites are
selected where Qle and Qh are above 0.8 or 0.9.The maps from this script are 
with zoom. Data generatred by method2.py script.
"""


__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

    # Import packages
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib.patches as mpatches
import os
import matplotlib
from mpl_toolkits.axes_grid.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid.inset_locator import mark_inset


def zoommap(vals, title, label):
    fig =  plt.figure(figsize=(12,8))    
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,
                        wspace=0.15,hspace=0.05)
    ax = plt.subplot(211)
    m = Basemap(projection = 'mill', llcrnrlat = -45, llcrnrlon = -160, 
                urcrnrlat= 82, urcrnrlon = 170, resolution = 'c')

    m.drawcoastlines(linewidth = 0.5)
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,
                        wspace=0.15,hspace=0.05)
    for row in vals:
        x,y = m(vals.lon.values, vals.lat.values)
        m.scatter(x,y, s = 20, color = vals.color.values)
    ax.text(0.03,0.95, label, size = 12,  horizontalalignment='center', 
    verticalalignment='center', transform=ax.transAxes)
    plt.title(title, fontsize = 12)
     
    #Zoom Europe
    axins_1 = zoomed_inset_axes(ax, 2, loc=2, bbox_to_anchor=(0.42, 0.48),
                         bbox_transform=ax.figure.transFigure)
    axins_1.scatter(x, y, s = 20, c = vals.color.values)
    m.drawcoastlines(linewidth = 0.5)
    x2,y2 = m(-12,35) 
    x3,y3 = m(40,65)
    axins_1.set_xlim(x2,x3) 
    axins_1.set_ylim(y2,y3) 
    axes = mark_inset(ax, axins_1, loc1=1, loc2=2, linewidth=1)
    #Zoom Australia
    axins_2 = zoomed_inset_axes(ax, 2.2, loc=3, bbox_to_anchor=(0.61, 0.255),
                         bbox_transform=ax.figure.transFigure)
    axins_2.scatter(x, y, s = 20, c = vals.color.values)
    m.drawcoastlines(linewidth = 0.5)
    x2,y2 = m(110,-43) 
    x3,y3 = m(155,-10)
    axins_2.set_xlim(x2,x3) 
    axins_2.set_ylim(y2,y3) 
    axes = mark_inset(ax, axins_2, loc1=1, loc2=2,linewidth=1)
    #Zoom US
    axins_3 = zoomed_inset_axes(ax, 1.6, loc=3, bbox_to_anchor=(0.21, 0.25),
                         bbox_transform=ax.figure.transFigure)
    axins_3.scatter(x, y, s = 20, c = vals.color.values)
    m.drawcoastlines(linewidth = 0.5)
    x2,y2 = m(-130,22) 
    x3,y3 = m(-60,63)
    axins_3.set_xlim(x2,x3) 
    axins_3.set_ylim(y2,y3) 
    axes = mark_inset(ax, axins_3, loc1=1, loc2=2, linewidth=1)
    return(fig, axes)

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

#Renaming and putting DataFrames together
df_results_LH1 = df_results_LH.rename (columns={'overall': 'overallLH', 
                                 'smallerthan2stdev': 'smallerthan2stdevLH', 
                                 'largerthan2stdev': 'largerthan2stdevLH'})
df_results_SH1 = df_results_SH.rename (columns={'overall': 'overallSH', 
                                 'smallerthan2stdev': 'smallerthan2stdevSH', 
                                 'largerthan2stdev': 'largerthan2stdevSH'})
df_results_NEE1 = df_results_NEE.rename (columns={'overall': 'overallNEE', 
                                 'smallerthan2stdev': 'smallerthan2stdevNEE', 
                                 'largerthan2stdev': 'largerthan2stdevNEE'}) 

  
df_results = result = pd.concat([df_results_LH1.site, df_results_LH1.length, df_results_LH1.overallLH, df_results_LH1.smallerthan2stdevLH,
                                 df_results_LH1.largerthan2stdevLH,df_results_SH1.overallSH, 
                                 df_results_SH1.smallerthan2stdevSH,df_results_SH1.largerthan2stdevSH,
                                 df_results_NEE1.overallNEE, df_results_NEE1.smallerthan2stdevNEE,
                                 df_results_NEE1.largerthan2stdevNEE, df_results_LH1.lon, 
                                 df_results_LH1.lat], axis = 1)

#Overall measurement ratios for all above 0.9, all above 0.8, SH and LH above 0.9 and SH and LH above 0.8
overallbestsitesall = df_results[(df_results['overallLH'] >= 0.9) & 
                                 (df_results['overallSH'] >= 0.9) &
                                 (df_results['overallNEE'] >= 0.9)]
overall2ndbestsitesall = df_results [(df_results['overallLH'] >= 0.8)& 
                                     (df_results['overallSH'] >= 0.8) &
                                     (df_results['overallNEE'] >= 0.8)] 
overallbestsitesSHLH = df_results [(df_results['overallLH'] >= 0.9) & 
                                   (df_results['overallSH'] >= 0.9) ]                                   
overall2ndbestsitesSHLH = df_results [(df_results['overallLH'] >= 0.8) &
                                      (df_results['overallSH'] >= 0.8) ] 
                                     
# all above 90%
overallbestsitesall = pd.concat([overallbestsitesall.site, overallbestsitesall.length, overallbestsitesall.overallLH, 
                      overallbestsitesall.overallSH, overallbestsitesall.overallNEE, 
                      overallbestsitesall.lon, overallbestsitesall.lat], axis =1)
overallbestsitesall['color'] = '#4575b4'
# all above 80%
overall2ndbestsitesall = pd.concat([overall2ndbestsitesall.site, overall2ndbestsitesall.length, overall2ndbestsitesall.overallLH, 
                      overall2ndbestsitesall.overallSH, overall2ndbestsitesall.overallNEE,
                      overall2ndbestsitesall.lon, overall2ndbestsitesall.lat], axis =1)
overall2ndbestsitesall['color'] = 'red'
#SH and LH above 90%
overallbestsitesSHLH = pd.concat([overallbestsitesSHLH.site, overallbestsitesSHLH.length,  overallbestsitesSHLH.overallLH, 
                      overallbestsitesSHLH.overallSH, overallbestsitesSHLH.overallNEE,
                      overallbestsitesSHLH.lon, overallbestsitesSHLH.lat], axis =1)
overallbestsitesSHLH['color'] = 'orange'
#SH and LH above 80%
overall2ndbestsitesSHLH = pd.concat([overall2ndbestsitesSHLH.site, overall2ndbestsitesSHLH.length, overall2ndbestsitesSHLH.overallLH, 
                      overall2ndbestsitesSHLH.overallSH, overall2ndbestsitesSHLH.overallNEE,
                      overall2ndbestsitesSHLH.lon, overall2ndbestsitesSHLH.lat], axis =1)
overall2ndbestsitesSHLH['color'] = 'purple'

#putting results together and tropping duplicates
table_overall = overallbestsitesall.append([overall2ndbestsitesall, 
                                            overallbestsitesSHLH, overall2ndbestsitesSHLH ])
table_overall = table_overall.drop_duplicates(subset=['site', 'length', 'overallLH', 'overallSH', 'overallNEE'],
                                              keep='first', inplace=False)


#Lower extreme measurement ratios for all above 0.9, all above 0.8, SH and LH above 0.9 and SH and LH above 0.8
lowerbestsitesall = df_results[(df_results['smallerthan2stdevLH'] >= 0.9) & 
                                 (df_results['smallerthan2stdevSH'] >= 0.9) &
                                 (df_results['smallerthan2stdevNEE'] >= 0.9)]
lower2ndbestsitesall = df_results [(df_results['smallerthan2stdevLH'] >= 0.8)& 
                                     (df_results['smallerthan2stdevSH'] >= 0.8) &
                                     (df_results['smallerthan2stdevNEE'] >= 0.8)] 
lowerbestsitesSHLH = df_results [(df_results['smallerthan2stdevLH'] >= 0.9) & 
                                   (df_results['smallerthan2stdevSH'] >= 0.9)]
lower2ndbestsitesSHLH = df_results [(df_results['smallerthan2stdevLH'] >= 0.8) &
                                      (df_results['smallerthan2stdevSH'] >= 0.8) ]

# all above 90%
lowerbestsitesall = pd.concat([lowerbestsitesall.site, lowerbestsitesall.length, lowerbestsitesall.smallerthan2stdevLH, 
                      lowerbestsitesall.smallerthan2stdevSH, lowerbestsitesall.smallerthan2stdevNEE, 
                      lowerbestsitesall.lon, lowerbestsitesall.lat], axis =1)
lowerbestsitesall['color'] = '#4575b4'
# all above 80%
lower2ndbestsitesall = pd.concat([lower2ndbestsitesall.site, lower2ndbestsitesall.length,lower2ndbestsitesall.smallerthan2stdevLH, 
                      lower2ndbestsitesall.smallerthan2stdevSH, lower2ndbestsitesall.smallerthan2stdevNEE,
                      lower2ndbestsitesall.lon, lower2ndbestsitesall.lat], axis =1)
lower2ndbestsitesall['color'] = 'red'
#SH and LH above 90%
lowerbestsitesSHLH = pd.concat([lowerbestsitesSHLH.site, lowerbestsitesSHLH.length, lowerbestsitesSHLH.smallerthan2stdevLH, 
                      lowerbestsitesSHLH.smallerthan2stdevSH, lowerbestsitesSHLH.smallerthan2stdevNEE,
                      lowerbestsitesSHLH.lon, lowerbestsitesSHLH.lat], axis =1)
lowerbestsitesSHLH['color'] = 'orange'
#SH and LH above 80%
lower2ndbestsitesSHLH = pd.concat([lower2ndbestsitesSHLH.site, lower2ndbestsitesSHLH.length,  lower2ndbestsitesSHLH.smallerthan2stdevLH, 
                      lower2ndbestsitesSHLH.smallerthan2stdevSH, lower2ndbestsitesSHLH.smallerthan2stdevNEE,
                      lower2ndbestsitesSHLH.lon, lower2ndbestsitesSHLH.lat], axis =1)
lower2ndbestsitesSHLH['color'] = 'purple'
#putting results together and tropping duplicates
table_lower= lowerbestsitesall.append([lower2ndbestsitesall, lowerbestsitesSHLH, 
                                       lower2ndbestsitesSHLH ])
table_lower = table_lower.drop_duplicates(subset=['site', 'length', 'smallerthan2stdevLH',
                                                  'smallerthan2stdevSH', 'smallerthan2stdevNEE'],
                                          keep='first', inplace=False)


#Upper extreme measurement ratios for all above 0.9, all above 0.8, SH and LH above 0.9 and SH and LH above 0.8
upperbestsitesall = df_results[(df_results['largerthan2stdevLH'] >= 0.9) & 
                                 (df_results['largerthan2stdevSH'] >= 0.9) &
                                 (df_results['largerthan2stdevNEE'] >= 0.9)]
upper2ndbestsitesall = df_results [(df_results['largerthan2stdevLH'] >= 0.8)& 
                                     (df_results['largerthan2stdevSH'] >= 0.8) &
                                     (df_results['largerthan2stdevNEE'] >= 0.8)] 
upperbestsitesSHLH = df_results [(df_results['largerthan2stdevLH'] >= 0.9) & 
                                   (df_results['largerthan2stdevSH'] >= 0.9)]
upper2ndbestsitesSHLH = df_results [(df_results['largerthan2stdevLH'] >= 0.8) &
                                      (df_results['largerthan2stdevSH'] >= 0.8)]

# all above 90%
upperbestsitesall = pd.concat([upperbestsitesall.site, upperbestsitesall.length, upperbestsitesall.largerthan2stdevLH, 
                      upperbestsitesall.largerthan2stdevSH, upperbestsitesall.largerthan2stdevNEE,
                      upperbestsitesall.lon, upperbestsitesall.lat], axis =1)
upperbestsitesall['color'] = '#4575b4'
# all above 80%
upper2ndbestsitesall = pd.concat([upper2ndbestsitesall.site, upper2ndbestsitesall.length, upper2ndbestsitesall.largerthan2stdevLH, 
                      upper2ndbestsitesall.largerthan2stdevSH, upper2ndbestsitesall.largerthan2stdevNEE,
                      upper2ndbestsitesall.lon, upper2ndbestsitesall.lat], axis =1)
upper2ndbestsitesall['color'] = 'red'
#SH and LH above 90%
upperbestsitesSHLH = pd.concat([upperbestsitesSHLH.site, upperbestsitesSHLH.length, upperbestsitesSHLH.largerthan2stdevLH, 
                      upperbestsitesSHLH.largerthan2stdevSH, upperbestsitesSHLH.largerthan2stdevNEE,
                      upperbestsitesSHLH.lon, upperbestsitesSHLH.lat], axis =1)
upperbestsitesSHLH['color'] = 'orange'
#SH and LH above 80%
upper2ndbestsitesSHLH = pd.concat([upper2ndbestsitesSHLH.site, upper2ndbestsitesSHLH.length, upper2ndbestsitesSHLH.largerthan2stdevLH, 
                      upper2ndbestsitesSHLH.largerthan2stdevSH, upper2ndbestsitesSHLH.largerthan2stdevNEE,
                      upper2ndbestsitesSHLH.lon, upper2ndbestsitesSHLH.lat], axis =1)
upper2ndbestsitesSHLH['color'] = 'purple'
#putting results together and tropping duplicates
table_upper= upperbestsitesall.append([upper2ndbestsitesall, upperbestsitesSHLH, 
                                       upper2ndbestsitesSHLH ])
table_upper = table_upper.drop_duplicates(subset=['site', 'length', 'largerthan2stdevLH',
                                                 'largerthan2stdevSH', 'largerthan2stdevNEE'], 
                                          keep='first', inplace=False)

p1 = zoommap(table_overall, 
             "Suitable sites all temperatuers", "(a)")
blue_patch = mpatches.Patch(color='#4575b4', label='Qle, Qh and NEE above 0.9')
red_patch = mpatches.Patch(color='red', label='Qle, Qh  and NEE above 0.8')
orange_patch = mpatches.Patch(color='orange', label='Qle, Qh  above 0.9')
purple_patch = mpatches.Patch(color='purple', label='Qle, Qh  above 0.8')
plt.legend(handles=[blue_patch, red_patch, orange_patch, purple_patch], bbox_to_anchor=(0.3, 1, 0.5, 0.5), prop={'size': 7.5})
p2 = zoommap(table_lower, 
             "Suitable sites lower extreme", "(b)")
p3 = zoommap(table_upper, 
             "Suitable sites upper extreme", "(c)")

plot_dir = "../plots/"
p1[0].savefig(os.path.join(plot_dir, "zoommap_suitable_overall.png"), dpi = 600,
            bbox_inches='tight', pad_inches=0.1)
p2[0].savefig(os.path.join(plot_dir, "zoommap_suitable_lower.png"), dpi = 600,
            bbox_inches='tight', pad_inches=0.1)
p3[0].savefig(os.path.join(plot_dir, "zoommap_suitable_upper.png"), dpi = 600,
            bbox_inches='tight', pad_inches=0.1)






