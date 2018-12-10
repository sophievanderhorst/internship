#!/usr/bin/env python

"""
I use this script to make plots that show the measurement ratios of Qle, Qh and 
NEE varying with time of day.These are used for Supplementary figure 2. 

"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import xarray as xr
import os
from matplotlib.dates import DateFormatter

def timeofday(LH, SH, NEE, ax, name):  
        LH.index = pd.to_datetime(LH.index)
        SH.index = pd.to_datetime(SH.index)
        NEE.index = pd.to_datetime(NEE.index)
        ax.xaxis_date()
        formatter = DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(LH)
        ax.plot(SH)
        ax.plot(NEE)
        
        ax.set_title(name, fontsize = 14)
        ax.set_xlim(pd.Timestamp('6:00'), pd.Timestamp('23:00'))
        
        n = 2
        [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 1]
        return (ax)
        


def main(files_met, files_flux, ds_NEE_ITCpz_met, ds_NEE_ITCpz_flux,  ofname1, ofname2, ofname3, ofname4, plot_dir):
    nsample = 10
    
    
    selection = []
    name = []
    LH = []
    SH = []
    NEE = []
    
    for m,f in zip(files_met, files_flux):
        print(m,f)
 
        mname = os.path.splitext(os.path.basename(m))[0]
        mname = mname[0:6]                    
        ds_met = open_file(m)
        ds_flux = open_file(f)

        #distinguishing between half-hourly and hourly datasets
        tdelta = ds_met.index[1] - ds_met.index [0]
        if tdelta.seconds == (30*60):
            time = 48
        else:
            time = 24
            
        
        if len(ds_met) > ((365*time)*(3/4)) and (len(ds_met[ds_met.Tair_qc < 1])/len(ds_met))>0.5:
                  
            (ds_met, ds_flux,
            Tair_measured, mean_tair_measured) = screen_data(ds_met, ds_flux)
            ds_met.index = ds_met.index.time
            time_sorted = ds_met.groupby(ds_met.index).size()
            dftime_sorted = pd.DataFrame(time_sorted, columns = ['temp'])
            
            # LATENT HEAT
            # filtering out only the measured latent heats
            ds_flux_measuredLH = ds_flux[ds_flux.Qle_qc < 1]
            ds_flux_measuredLH.index = ds_flux_measuredLH.index.time
            ds_flux_measuredLH_time = ds_flux_measuredLH.groupby(ds_flux_measuredLH.index).size()
            df_flux_measuredLH_time = pd.DataFrame(ds_flux_measuredLH_time, columns = ['LH'])
            dftime_sorted = pd.concat([dftime_sorted, df_flux_measuredLH_time], axis=1, sort=False)
                        
            #SENSIBLE HEAT
            # filtering out only the measured sensible heats
            ds_flux_measuredSH = ds_flux[ds_flux.Qh_qc < 1]
            ds_flux_measuredSH.index = ds_flux_measuredSH.index.time
            ds_flux_measuredSH_time = ds_flux_measuredSH.groupby(ds_flux_measuredSH.index).size()
            df_flux_measuredSH_time = pd.DataFrame(ds_flux_measuredSH_time, columns = ['SH'])
            dftime_sorted = pd.concat([dftime_sorted, df_flux_measuredSH_time], axis=1, sort=False)
                       
            #NEE
            # filtering out only the measured NEE
            if 'NEE' in ds_flux: 
                ds_flux_measuredNEE = ds_flux[ds_flux.NEE_qc < 1]
                ds_flux_measuredNEE.index = ds_flux_measuredNEE.index.time
                ds_flux_measuredNEE_time = ds_flux_measuredNEE.groupby(ds_flux_measuredNEE.index).size()
                df_flux_measuredNEE_time = pd.DataFrame(ds_flux_measuredNEE_time, columns = ['NEE'])
                dftime_sorted = pd.concat([dftime_sorted, df_flux_measuredNEE_time], axis=1, sort=False)
            dftime_sorted = dftime_sorted.fillna(0)
            dftime_sorted = dftime_sorted[dftime_sorted['temp'] > nsample]
           
            dftime_sorted["ratioLH"] = dftime_sorted["LH"]/dftime_sorted["temp"]
            dftime_sorted["ratioSH"] = dftime_sorted["SH"]/dftime_sorted["temp"]
            if 'NEE' in ds_flux: 
                dftime_sorted["ratioNEE"] = dftime_sorted["NEE"]/dftime_sorted["temp"]
            #else:
                #dftime_sorted["ratioNEE"] = np.nan
            dftime_sorted.index =dftime_sorted.index.map(lambda t: t.strftime('%H:%M'))
            
            if mname == 'US-Whs' or mname == 'AU-ASM' or mname == 'AU-Tum' or \
            mname == 'CA-NS4' or mname == 'DE-Hai' or mname == 'DE-Meh' or \
            mname == 'DK-NuF' or mname == 'IT-Tor':   
                selection.append(dftime_sorted)
                name.append(mname)
                LH.append(dftime_sorted.ratioLH)
                SH.append(dftime_sorted.ratioSH)
                NEE.append(dftime_sorted.ratioNEE)
            dftime_sorted.index = pd.to_datetime(dftime_sorted.index)
    

           
    fig, ax = plt.subplots(nrows=4, ncols=2, figsize =(10,15), sharex = True, sharey =True)
      
    timeofday(LH[0], SH[0], NEE[0], ax[0,0], name[0])
    timeofday(LH[1], SH[1], NEE[1], ax[0,1], name[1])
    timeofday(LH[2], SH[2], NEE[2], ax[1,0], name[2])
    timeofday(LH[3], SH[3], NEE[3], ax[1,1], name[3])
    timeofday(LH[4], SH[4], NEE[4], ax[2,0], name[4])
    timeofday(LH[5], SH[5], NEE[5], ax[2,1], name[5])
    timeofday(LH[6], SH[6], NEE[6], ax[3,0], name[6])
    timeofday(LH[7], SH[7], NEE[7], ax[3,1], name[7])
    ax[0,0].legend(['Qle', 'Qh', 'NEE'])
    fig.tight_layout()
    
    plot_dir = "../plots"
    ofname = "timeofday.pdf"
    fig.savefig(os.path.join(plot_dir, ofname),
            bbox_inches='tight', pad_inches=0.1)

    

            
def open_file(fname):
    ds = xr.open_dataset(fname)
    ds = ds.squeeze(dim=["x","y"], drop=True).to_dataframe()
    ds = ds.reset_index()
    ds = ds.set_index('time')
    return (ds)

def screen_data(ds_met, ds_flux):

    #Does the data have enough recorded temperatures? First, selecting
    #only measurements with qc = 0.
    Tair_measured = ds_met[ds_met.Tair_qc < 1]
    mean_tair_measured = np.mean(Tair_measured.Tair)

    # Filter to measured temperature (qc=0) and only shortwave
    #incoming radiation >0 and filtering out data between 11 pm and 6 am
    ds_flux = ds_flux[ds_met.Tair_qc < 1]
    ds_met = ds_met[ds_met.Tair_qc < 1]
    ds_flux = ds_flux[ds_met.SWdown > 1]
    ds_met = ds_met[ds_met.SWdown > 1]
    ds_flux = ds_flux.drop(ds_flux.between_time("23:00", "6:00").index)
    ds_met = ds_met.drop(ds_met.between_time("23:00", "6:00").index)

    return (ds_met, ds_flux, Tair_measured, mean_tair_measured)

if __name__ == "__main__":

    files_met = sorted(glob.glob("../data/Met_merged/*"))
    files_flux = sorted(glob.glob("../data/Flux_merged/*"))
    ds_NEE_ITCpz_met = (glob.glob("../data/Met/IT-Cpz_2000-2009_FLUXNET2015_Met.nc"))
    ds_NEE_ITCpz_flux = (glob.glob("../data/Flux/IT-Cpz_2000-2009_FLUXNET2015_Flux.nc"))
    
    out_path = "../data/processed"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    plot_dir = "../plots"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    ofname1 = os.path.join(out_path, "results_LH.csv")
    ofname2 = os.path.join(out_path, "results_SH.csv")
    ofname3 = os.path.join(out_path, "results_NEE.csv")
    ofname4 = os.path.join(out_path, "globaltemp.csv")

    main(files_met, files_flux, ds_NEE_ITCpz_met, ds_NEE_ITCpz_flux, ofname1, ofname2, ofname3, ofname4, plot_dir)


