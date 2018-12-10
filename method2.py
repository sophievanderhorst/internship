#!/usr/bin/env python

"""
I use this script to determine the ratio of measurements of fluxes relative to 
the number of temperature measurements for flux tower sites. 

This is done for latent heat (Qle), sensible heat (Qh) and NEE. I focus on 
extreme temperatures (lower and upper 2.2% of the temperatures of each site)
"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

import numpy as np
import pandas as pd
import glob
import xarray as xr
import os

def main(files_met, files_flux, ds_NEE_ITCpz_met, ds_NEE_ITCpz_flux,  ofname1, ofname2, ofname3, ofname4, plot_dir):

    #Empty lists to add data in for the table/figures
    results_LH = []
    results_SH = []
    results_NEE = []
    #These lists can be used to find the really warm sites
    #warm_sites = []
    #warm_sites_length = []
        
    #data for It-Cpz (doesn't have NEE in one of the datasets so for NEE I am using the dataset
    #that contains NEE, before it was merged)
    for ds_NEE_ITCpz_flux, ds_NEE_ITCpz_met in zip(ds_NEE_ITCpz_flux, ds_NEE_ITCpz_met):
        ds_ITCpz_flux = open_file(ds_NEE_ITCpz_flux)
        ds_ITCpz_met = open_file(ds_NEE_ITCpz_met)
    
    for m,f in zip(files_met, files_flux):
        print(m,f)
        
         
        mname = os.path.splitext(os.path.basename(m))[0]
        mname = mname[0:6]
                    
        ds_met = open_file(m)
        ds_flux = open_file(f)
        print(ds_flux.columns)
                
        lat = ds_met['latitude'].mean()
        lon = ds_met['longitude'].mean()
        
        #Distinguishing between half-hourly and hourly datasets
        tdelta = ds_met.index[1] - ds_met.index [0]
        if tdelta.seconds == (30*60):
            time = 48
        else:
            time = 24
        
        length_dataset = round(len(ds_met)/time)
        #Only using datasets where the length is longer than 8 months and 
        #at least 50% of the temperatures are measured
        if len(ds_met) > ((365*time)*(3/4)) and \
        (len(ds_met[ds_met.Tair_qc < 1])/len(ds_met))>0.5:
         
            
            # This part is only used 
            #length_half = int(len(ds_met)/2)
            #ds_met = ds_met[length_half:]
            #ds_flux = ds_flux[length_half:]
                        
            (ds_met, ds_flux,
            Tair_measured, mean_tair_measured, ds_ITCpz_flux, ds_ITCpz_met, ratio_length) = \
             screen_data(ds_met, ds_flux, ds_ITCpz_flux, ds_ITCpz_met) 
    
            ppt_yearly = ((ds_met.Rainf.mean())*time*365)*1000
            
            # Used this part of the code to identify the really warm temperatures
            #(explaining the peak in figure 1)
            #warm_temp = ds_met[ds_met.Tair > 317]
            #if len(warm_temp) > 1:
                #warm_sites.append(mname)
                #warm_sites_length.append(len(warm_temp))
                #print(mname)
                
            # number of measured temperatures
            length = round(len(ds_met))

            #Filtering out only the measured latent heats, sensible heats and NEE. 
            # Not each dataset contains NEE measurements (IT-Cpz merged)
            ds_flux_measuredLH = ds_flux[ds_flux.Qle_qc < 1]
            ds_flux_measuredSH = ds_flux[ds_flux.Qh_qc<1]
            if 'NEE' in ds_flux:
                ds_flux_measuredNEE = ds_flux[ds_flux.NEE_qc<1]
            else:
                ds_flux_measuredNEE = ds_ITCpz_flux[ds_ITCpz_flux.NEE_qc < 1]
                
                              
            #Overall performance
            ratioLH = round((len(ds_flux_measuredLH) / len(ds_met)), 2)
            ratioSH = round((len(ds_flux_measuredSH) / len(ds_met)), 2)
            if 'NEE' in ds_flux:
                ratioNEE = round((len(ds_flux_measuredNEE) / len(ds_met)),2)
            # IT-Cpz again
            else: 
                ratioNEE = round((len(ds_flux_measuredNEE)/ len(ds_ITCpz_met)),2)
                                
            #Lowest 2.3%.  Here I select only the lowest 2.3% (2stdev) of the temperatures. 
            temp_lower = ds_met.Tair.quantile(0.02275)
            ds_met_lower = ds_met[ds_met.Tair < temp_lower]
    
            ds_flux_LH_lower = ds_flux_measuredLH[ds_met.Tair < temp_lower]
            ratioLH_lower = round((len(ds_flux_LH_lower) / len(ds_met_lower)), 2)
    
            ds_flux_SH_lower = ds_flux_measuredSH[ds_met.Tair < temp_lower]
            ratioSH_lower = round((len(ds_flux_SH_lower) / len(ds_met_lower)), 2)
            
            ds_flux_NEE_lower = ds_flux_measuredNEE[ds_met.Tair < temp_lower]
            if 'NEE' in ds_flux:
                ratioNEE_lower = round((len(ds_flux_NEE_lower) / len(ds_met_lower)),2 )
            # IT-Cpz 
            else:
                ds_met_lower = ds_ITCpz_met[ds_ITCpz_met.Tair < temp_lower]
                ratioNEE_lower = round((len(ds_flux_NEE_lower) / len(ds_met_lower)),2 )
                                        
            #Highest 2.3%
            temp_upper = ds_met.Tair.quantile(1 - 0.02275)
            ds_met_upper = ds_met[ds_met.Tair > temp_upper]
            
            ds_flux_LH_upper = ds_flux_measuredLH[ds_met.Tair > temp_upper]
            ratioLH_upper = round((len(ds_flux_LH_upper) / len(ds_met_upper)),2)
            
            ds_flux_SH_upper = ds_flux_measuredSH[ds_met.Tair > temp_upper]
            ratioSH_upper = round((len(ds_flux_SH_upper) / len(ds_met_upper)), 2)
            
            ds_flux_NEE_upper = ds_flux_measuredNEE[ds_met.Tair > temp_upper]
            if 'NEE' in ds_flux:
                ratioNEE_upper = round((len(ds_flux_NEE_upper) / len(ds_met_upper)), 2)
            #IT-Cpz
            else:
                ds_met_upper = ds_ITCpz_met[ds_ITCpz_met.Tair > temp_upper]
                ratioNEE_upper = round((len(ds_flux_NEE_upper) / len(ds_met_upper)),2 )
 
            # Adding the results to the empty lists
            results_LH.append([mname, lat, lon, mean_tair_measured,  ppt_yearly,
                              ratioLH, ratioLH_lower, ratioLH_upper, length, length_dataset, ratio_length])
            results_SH.append([mname, lat, lon, mean_tair_measured,  ppt_yearly,
                              ratioSH, ratioSH_lower, ratioSH_upper, length, length_dataset, ratio_length])
            results_NEE.append([mname, lat, lon, mean_tair_measured,  ppt_yearly,
                               ratioNEE, ratioNEE_lower, ratioNEE_upper, length, length_dataset, ratio_length])
            
            # Making pandas dataframes
            df_results_LH = pd.DataFrame(results_LH)
            df_results_SH = pd.DataFrame(results_SH)
            df_results_NEE = pd.DataFrame(results_NEE)
            
                        
            # adding names to columns of dataframes
            df_results_LH.columns = ['site', 'lat', 'lon',  'meantemp', 'meanprec',  'overall',
                                    'smallerthan2stdev', 'largerthan2stdev', 'length', 'days', 'ratio']
            df_results_SH.columns = ['site', 'lat', 'lon', 'meantemp', 'meanprec', 'overall',
                                    'smallerthan2stdev', 'largerthan2stdev', 'length', 'days', 'ratio']
            df_results_NEE.columns = ['site', 'lat', 'lon', 'meantemp', 'meanprec',  'overall',
                                    'smallerthan2stdev', 'largerthan2stdev','length', 'days', 'ratio']
            
    
    df_results_LH.to_csv(ofname1)
    df_results_SH.to_csv(ofname2)
    df_results_NEE.to_csv(ofname3)
    
      
def open_file(fname):
    ds = xr.open_dataset(fname)
    ds = ds.squeeze(dim=["x","y"], drop=True).to_dataframe()
    ds = ds.reset_index()
    ds = ds.set_index('time')
    return (ds)

def screen_data(ds_met, ds_flux, ds_ITCpz_flux, ds_ITCpz_met):

    #Does the data have enough recorded temperatures? First, selecting
    #only measurements with qc = 0.
    Tair_measured = ds_met[ds_met.Tair_qc < 1]
    mean_tair_measured = np.mean(Tair_measured.Tair)

    # Filter to measured temperature (qc=0) and only shortwave
    #incoming radiation >0 and filtering out data between 11 pm and 6 am.
    #Also, showing the ratio of measured temperature measurements after filtering
    #out the nightimes. 

    ds_ITCpz_flux = ds_ITCpz_flux[ds_ITCpz_met.Tair_qc <1]
    ds_ITCpz_met = ds_ITCpz_met [ds_ITCpz_met.Tair_qc <1]
    ds_flux = ds_flux[ds_met.SWdown > 1]
    ds_met = ds_met[ds_met.SWdown > 1]
    ds_ITCpz_flux = ds_ITCpz_flux [ds_ITCpz_met.SWdown > 1]
    ds_ITCpz_met = ds_ITCpz_met [ds_ITCpz_met.SWdown > 1]
    ds_flux = ds_flux.drop(ds_flux.between_time("23:00", "6:00").index)
    ds_met = ds_met.drop(ds_met.between_time("23:00", "6:00").index)
    before = len(ds_met)
    ds_flux = ds_flux[ds_met.Tair_qc < 1]
    ds_met = ds_met[ds_met.Tair_qc < 1]
    ratio_length =round((len(ds_met)/before), 2)
    ds_ITCpz_flux = ds_ITCpz_flux.drop(ds_ITCpz_flux.between_time("23:00", "6:00").index)
    ds_ITCpz_met = ds_ITCpz_met.drop(ds_ITCpz_met.between_time("23:00", "6:00").index)

    return (ds_met, ds_flux, Tair_measured, mean_tair_measured, ds_ITCpz_flux, ds_ITCpz_met, ratio_length)

if __name__ == "__main__":

    files_met = sorted(glob.glob("../data/Met_merged/*"))
    files_flux = sorted(glob.glob("../data/Flux_merged/*"))
    ds_NEE_ITCpz_met = sorted(glob.glob("../data/Met/IT-Cpz_2000-2009_FLUXNET2015_Met.nc"))
    ds_NEE_ITCpz_flux = sorted(glob.glob("../data/Flux/IT-Cpz_2000-2009_FLUXNET2015_Flux.nc"))
    
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
        