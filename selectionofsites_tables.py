#!/usr/bin/env python

"""
This is used to select sites with the highest measurement ratios of Qle, Qh 
and NEE. Sites are selected where all ratios are above 0.9 or 0.8. Also, sites are
selected where Qle and Qh are above 0.8 or 0.9. The maps from this script are 
without zoom. Also, the results are shown in tables. In the end, I exported the results
to word and excel because table editing in python was difficult.  Data generatred by method2.py script.
"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

    # Import packages
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
import os


__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

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

  
df_results = result = pd.concat([df_results_LH1.site, df_results_LH1.length, df_results_LH1.days, df_results_LH1.ratio, df_results_LH1.overallLH, df_results_LH1.smallerthan2stdevLH,
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
overallbestsitesall = pd.concat([overallbestsitesall.site, round(overallbestsitesall.length), round(overallbestsitesall.days),
                    overallbestsitesall.overallLH, overallbestsitesall.ratio,
                      overallbestsitesall.overallSH, overallbestsitesall.overallNEE, 
                      overallbestsitesall.lon, overallbestsitesall.lat], axis =1)
overallbestsitesall['color'] = '#4575b4'
# all above 80%
overall2ndbestsitesall = pd.concat([overall2ndbestsitesall.site, round(overall2ndbestsitesall.length),
                                    overall2ndbestsitesall.overallLH, round(overall2ndbestsitesall.days),
                                    overall2ndbestsitesall.ratio, overall2ndbestsitesall.overallSH, 
                                    overall2ndbestsitesall.overallNEE, overall2ndbestsitesall.lon, 
                                    overall2ndbestsitesall.lat], axis =1)
overall2ndbestsitesall['color'] = 'red'
#SH and LH above 90%
overallbestsitesSHLH = pd.concat([overallbestsitesSHLH.site, round(overallbestsitesSHLH.length),  
                                  round(overallbestsitesSHLH.days), overallbestsitesSHLH.ratio, 
                                  overallbestsitesSHLH.overallLH, overallbestsitesSHLH.overallSH,
                                  overallbestsitesSHLH.overallNEE,
                                  overallbestsitesSHLH.lon, overallbestsitesSHLH.lat], axis =1)
overallbestsitesSHLH['color'] = 'orange'
#SH and LH above 80%
overall2ndbestsitesSHLH = pd.concat([overall2ndbestsitesSHLH.site, round(overall2ndbestsitesSHLH.length), 
                                     round(overall2ndbestsitesSHLH.days), overall2ndbestsitesSHLH.ratio,
                                     overall2ndbestsitesSHLH.overallLH, 
                      overall2ndbestsitesSHLH.overallSH, overall2ndbestsitesSHLH.overallNEE,
                      overall2ndbestsitesSHLH.lon, overall2ndbestsitesSHLH.lat], axis =1)
overall2ndbestsitesSHLH['color'] = 'purple'

#putting results together and tropping duplicates
table_overall = overallbestsitesall.append([overall2ndbestsitesall, 
                                            overallbestsitesSHLH, overall2ndbestsitesSHLH ])
table_overall = table_overall.drop_duplicates(subset=['site', 'length', 'overallLH', 'overallSH', 'overallNEE'],
                                              keep='first', inplace=False)

#Table creating for overall measurement ratio
fig, ax = plt.subplots()
plt.title("All temperatures", y = 2.3)
ax.axis('off')
colours = table_overall.color.values
table_overall_stripped = table_overall[['site', 'overallLH', 'overallSH', 'overallNEE', 'length', 'days', 'ratio']]
table_overall_stripped = table_overall_stripped.set_index('site')
out_path = "../data/processed"
table_overall_stripped.to_csv('overall.csv')

table = ax.table(cellText = (table_overall_stripped[0:62].values),
         rowColours = colours[0:62],
         colLabels= ["Qle", "Qh", "NEE", "# Temp measurements", 'Length', 'Ratio measured T'],
         rowLabels = table_overall_stripped.index[0:62].values,
         colWidths = [0.15, 0.15, 0.15, 0.35, 0.2, 0.35],
         loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
blue_patch = mpatches.Patch(color='#4575b4', label='Qle, Qh and NEE above 0.9')
red_patch = mpatches.Patch(color='red', label='Qle, Qh  and NEE above 0.8')
orange_patch = mpatches.Patch(color='orange', label='Qle, Qh  above 0.9')
purple_patch = mpatches.Patch(color='purple', label='Qle, Qh  above 0.8')
ax.legend(handles=[blue_patch, red_patch, orange_patch, purple_patch], bbox_to_anchor = (1.5, 1.9, 0.3, 0.3))

plot_dir = "../plots"
ofname = "table_suitable_overall1.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)

fig, ax = plt.subplots()
ax.axis('off')
table = ax.table(cellText = table_overall_stripped[62:].values, 
         rowColours = colours[62:],
         colLabels= ["Qle", "Qh", "NEE", "# Temp measurements", 'Length', 'Ratio measured T'], 
         rowLabels = table_overall_stripped.index[62:].values,
         colWidths = [0.15, 0.15, 0.15, 0.35, 0.2, 0.35],
         loc='center')

table.auto_set_font_size(False)
table.set_fontsize(9)
blue_patch = mpatches.Patch(color='white')
red_patch = mpatches.Patch(color='white')
orange_patch = mpatches.Patch(color='white')
purple_patch = mpatches.Patch(color='white')
ax.legend(handles=[blue_patch, red_patch, orange_patch, purple_patch], bbox_to_anchor = (1.25, 0.75, 0.3, 0.3), frameon = False)

plot_dir = "../plots"
ofname = "table_suitable_overall2.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)


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
lowerbestsitesall = pd.concat([lowerbestsitesall.site, lowerbestsitesall.length,
                               lowerbestsitesall.days, lowerbestsitesall.ratio,
                               lowerbestsitesall.smallerthan2stdevLH, 
                      lowerbestsitesall.smallerthan2stdevSH, lowerbestsitesall.smallerthan2stdevNEE, 
                      lowerbestsitesall.lon, lowerbestsitesall.lat], axis =1)
lowerbestsitesall['color'] = '#4575b4'
# all above 80%
lower2ndbestsitesall = pd.concat([lower2ndbestsitesall.site, lower2ndbestsitesall.length,
                                  lower2ndbestsitesall.days, lower2ndbestsitesall.ratio,
                                  lower2ndbestsitesall.smallerthan2stdevLH, 
                      lower2ndbestsitesall.smallerthan2stdevSH, lower2ndbestsitesall.smallerthan2stdevNEE,
                      lower2ndbestsitesall.lon, lower2ndbestsitesall.lat], axis =1)
lower2ndbestsitesall['color'] = 'red'
#SH and LH above 90%
lowerbestsitesSHLH = pd.concat([lowerbestsitesSHLH.site, lowerbestsitesSHLH.length, 
                                lowerbestsitesSHLH.days, lowerbestsitesSHLH.ratio,
                                lowerbestsitesSHLH.smallerthan2stdevLH, 
                      lowerbestsitesSHLH.smallerthan2stdevSH, lowerbestsitesSHLH.smallerthan2stdevNEE,
                      lowerbestsitesSHLH.lon, lowerbestsitesSHLH.lat], axis =1)
lowerbestsitesSHLH['color'] = 'orange'
#SH and LH above 80%
lower2ndbestsitesSHLH = pd.concat([lower2ndbestsitesSHLH.site, lower2ndbestsitesSHLH.length,  
                                   lower2ndbestsitesSHLH.days, lower2ndbestsitesSHLH.ratio,
                                   lower2ndbestsitesSHLH.smallerthan2stdevLH, 
                      lower2ndbestsitesSHLH.smallerthan2stdevSH, lower2ndbestsitesSHLH.smallerthan2stdevNEE,
                      lower2ndbestsitesSHLH.lon, lower2ndbestsitesSHLH.lat], axis =1)
lower2ndbestsitesSHLH['color'] = 'purple'
#putting results together and tropping duplicates
table_lower= lowerbestsitesall.append([lower2ndbestsitesall, lowerbestsitesSHLH, 
                                       lower2ndbestsitesSHLH ])
table_lower = table_lower.drop_duplicates(subset=['site', 'length', 'smallerthan2stdevLH',
                                                  'smallerthan2stdevSH', 'smallerthan2stdevNEE'],
                                          keep='first', inplace=False)


#Table creation for Lower extreme
fig, ax = plt.subplots()
plt.title("Lower extreme", y = 1.7)
ax.axis('off')
colours = table_lower.color.values
table_lower_stripped = table_lower[['site', 'smallerthan2stdevLH',
                                    'smallerthan2stdevSH', 'smallerthan2stdevNEE', 'length', 'days', 'ratio']]

table_lower_stripped = table_lower_stripped.set_index('site')
table_lower_stripped.to_csv('lower.csv')

table = ax.table(cellText=table_lower_stripped.values,
         rowColours = colours, 
         colLabels=("Qle", "Qh", "NEE", "# Temp measurements", 'length', 'ratio measured T'), 
         rowLabels = table_lower_stripped.index.values,
         colWidths = [0.15, 0.15, 0.15, 0.35, 0.2, 0.35],
         loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
blue_patch = mpatches.Patch(color='#4575b4', label='Qle, Qh and NEE above 0.9')
red_patch = mpatches.Patch(color='red', label='Qle, Qh  and NEE above 0.8')
orange_patch = mpatches.Patch(color='orange', label='Qle, Qh  above 0.9')
purple_patch = mpatches.Patch(color='purple', label='Qle, Qh  above 0.8')
ax.legend(handles=[blue_patch, red_patch, orange_patch, purple_patch], bbox_to_anchor = (1.5, 1.3, 0.3, 0.3))

ofname = "table_suitable_lowerextreme.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)

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
upperbestsitesall = pd.concat([upperbestsitesall.site, upperbestsitesall.length,
                               upperbestsitesall.days, upperbestsitesall.ratio,
                               upperbestsitesall.largerthan2stdevLH, 
                      upperbestsitesall.largerthan2stdevSH, upperbestsitesall.largerthan2stdevNEE,
                      upperbestsitesall.lon, upperbestsitesall.lat], axis =1)
upperbestsitesall['color'] = '#4575b4'
# all above 80%
upper2ndbestsitesall = pd.concat([upper2ndbestsitesall.site, upper2ndbestsitesall.length, 
                                  upper2ndbestsitesall.days, upper2ndbestsitesall.ratio, 
                                  upper2ndbestsitesall.largerthan2stdevLH, 
                      upper2ndbestsitesall.largerthan2stdevSH, upper2ndbestsitesall.largerthan2stdevNEE,
                      upper2ndbestsitesall.lon, upper2ndbestsitesall.lat], axis =1)
upper2ndbestsitesall['color'] = 'red'
#SH and LH above 90%
upperbestsitesSHLH = pd.concat([upperbestsitesSHLH.site, upperbestsitesSHLH.length,
                                upperbestsitesSHLH.days, upperbestsitesSHLH.ratio,
                                upperbestsitesSHLH.largerthan2stdevLH, 
                      upperbestsitesSHLH.largerthan2stdevSH, upperbestsitesSHLH.largerthan2stdevNEE,
                      upperbestsitesSHLH.lon, upperbestsitesSHLH.lat], axis =1)
upperbestsitesSHLH['color'] = 'orange'
#SH and LH above 80%
upper2ndbestsitesSHLH = pd.concat([upper2ndbestsitesSHLH.site, upper2ndbestsitesSHLH.length, 
                                   upper2ndbestsitesSHLH.days, upper2ndbestsitesSHLH.ratio,
                                   upper2ndbestsitesSHLH.largerthan2stdevLH, 
                      upper2ndbestsitesSHLH.largerthan2stdevSH, upper2ndbestsitesSHLH.largerthan2stdevNEE,
                      upper2ndbestsitesSHLH.lon, upper2ndbestsitesSHLH.lat], axis =1)
upper2ndbestsitesSHLH['color'] = 'purple'
#putting results together and dropping duplicates
table_upper= upperbestsitesall.append([upper2ndbestsitesall, upperbestsitesSHLH, 
                                       upper2ndbestsitesSHLH ])
table_upper = table_upper.drop_duplicates(subset=['site', 'length', 'largerthan2stdevLH',
                                                 'largerthan2stdevSH', 'largerthan2stdevNEE'], 
                                          keep='first', inplace=False)



table_overall_Aus = table_overall[(table_overall.lat < -10) & (table_overall.lat > -40 )
                               & (table_overall.lon > 110)  & (table_overall.lon < 155)]
table_overall_Euro = table_overall[(table_overall.lat < 70) & (table_overall.lat > 35 )
                               & (table_overall.lon > -10)  & (table_overall.lon < 40)]
table_overall_NA = table_overall[(table_overall.lat < 80) & (table_overall.lat > 25 )
                               & (table_overall.lon > -165)  & (table_overall.lon < -50)]
table_overall_geo = pd.concat ([table_overall_Aus, table_overall_Euro, table_overall_NA] )


table_lower_Aus = table_lower[(table_lower.lat < -10) & (table_lower.lat > -40 )
                               & (table_lower.lon > 110)  & (table_lower.lon < 155)]
table_lower_Euro = table_lower[(table_lower.lat < 70) & (table_lower.lat > 35 )
                               & (table_lower.lon > -10)  & (table_lower.lon < 40)]
table_lower_NA = table_lower[(table_lower.lat < 80) & (table_lower.lat > 25 )
                               & (table_lower.lon > -165)  & (table_lower.lon < -50)]
table_lower_geo = pd.concat ([table_lower_Aus, table_lower_Euro, table_lower_NA ])
 
table_upper_Aus = table_upper[(table_upper.lat < -10) & (table_upper.lat > -40 )
                               & (table_upper.lon > 110)  & (table_upper.lon < 155)]
table_upper_Euro = table_upper[(table_upper.lat < 70) & (table_upper.lat > 35 )
                               & (table_upper.lon > -10)  & (table_upper.lon < 40)]
table_upper_NA = table_upper[(table_upper.lat < 80) & (table_upper.lat > 25 )
                               & (table_upper.lon > -165)  & (table_upper.lon < -50)]
table_upper_geo = pd.concat ([table_upper_Aus, table_upper_Euro, table_upper_NA])


percentage_geo_overall = len(table_overall_geo)/len(table_overall)
percentage_geo_lower = len(table_lower_geo)/len(table_lower)
percentage_geo_upper = len(table_upper_geo)/len(table_upper)

print(percentage_geo_overall)
print(percentage_geo_lower)
print(percentage_geo_upper)

#Table creation for upper extreme
fig, ax = plt.subplots()
plt.title ("Upper extreme", y = 2.3)
ax.axis('off')
colours = table_upper.color.values
table_upper_stripped = table_upper[['site', 'largerthan2stdevLH',
                                    'largerthan2stdevSH', 'largerthan2stdevNEE', 'length', 'days', 'ratio']]
table_upper_stripped = table_upper_stripped.set_index('site')
table_upper_stripped.to_csv('upper.csv')
table = ax.table(cellText=table_upper_stripped[0:62].values,
         rowColours = colours[0:62], 
         colLabels=("Qle", "Qh", "NEE", "# temp measurements", 'length', 'ratio measured T'), 
         rowLabels = table_upper_stripped.index[0:62].values, 
         colWidths = [0.15, 0.15, 0.15, 0.35, 0.2, 0.35],
         loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
ax.legend(handles=[blue_patch, red_patch, orange_patch, purple_patch], 
          bbox_to_anchor = (1.5, 1.9, 0.3, 0.3))


ofname = "table_suitable_upperextreme1.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)

#Table creation for upper extreme
fig, ax = plt.subplots()
ax.axis('off')
table = ax.table(cellText=table_upper_stripped.values[62:],
         rowColours = colours[62:], 
         colLabels=("Qle", "Qh", "NEE", "# temp measurements", 'length', 'ratio measured T'), 
         rowLabels = table_upper_stripped.index[62:].values, 
         colWidths = [0.15, 0.15, 0.15, 0.35, 0.2, 0.35],
         loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
blue_patch = mpatches.Patch(color='white')
red_patch = mpatches.Patch(color='white')
orange_patch = mpatches.Patch(color='white')
purple_patch = mpatches.Patch(color='white')
ax.legend(handles=[blue_patch, red_patch, orange_patch, purple_patch], bbox_to_anchor = (1.25, 0.75, 0.3, 0.3), frameon = False)


ofname = "table_suitable_upperextreme2.pdf"
fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)
