#!/usr/bin/env python

"""
I use this script to provide the data for figure 1. Thus, showing the global 
distribution of temperature, Qle, Qh and NEE measurements. 
"""

__author__ = "Sophie van der Horst"
__version__ = "1.0 (25.10.2018)"
__email__ = "sophie.vanderhorst@wur.nl"

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
import glob
import xarray as xr
import os
import math



def main(files_met, files_flux, ds_NEE_ITCpz_met, ds_NEE_ITCpz_flux, ofname4, plot_dir):

    # empty lists to add data in for the table/figures
    results_LH = []
    results_SH = []
    results_NEE = []

    # creating dataframes for barplots of global temperature distribution   
    df_temp = pd.DataFrame()
    df_LH = pd.DataFrame()
    df_SH = pd.DataFrame()
    df_NEE = pd.DataFrame()
    
    
    binsize = 1
    nsample = 10

    
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
    
            # creating bins of 1 K and assigning a temperature to a bin.
            minimum_tair = math.floor(min(ds_met.Tair))
            maximum_tair = math.ceil(max(ds_met.Tair))
            bins = np.arange(minimum_tair, maximum_tair + binsize, binsize)
            bin_label = np.arange(minimum_tair,
                                  maximum_tair, binsize)
            data_binned = pd.cut(ds_met.Tair, bins, labels=bin_label)

            #Adding this temperaturebin to the datasets.
            ds_met.loc[:,"tempbin"] = data_binned
            ds_flux.loc[:, "tempbin"] = data_binned

            # For each bin, count the amount of measurements create a
            # pandas Dataframe for temperature
            temp_sorted = ds_met.groupby(['tempbin']).size()
            
            # Create a pandas Dataframe for temperature and add binlabel
            dftemp_sorted = pd.DataFrame(temp_sorted)
            dftemp_sorted.loc[:,"bin_label"] = bin_label

            # LATENT HEAT
            # filtering out only the measured latent heats
            ds_flux_measuredLH = ds_flux[ds_flux.Qle_qc < 1]

            # Ordering the data according to the temperature bin, making a
            # pandaframe and equalizing the index to the index
            #o f the temperature dataframe.
            ds_flux_measuredLH_sorted = ds_flux_measuredLH.groupby(['tempbin']).size()
            df_flux_measuredLH_sorted = pd.DataFrame(ds_flux_measuredLH_sorted)
            dftemp_sorted = dftemp_sorted.set_index(df_flux_measuredLH_sorted.index)
            measuredLH = df_flux_measuredLH_sorted.iloc[:,0]

            # adding the measured LH to temperature pandas dataframe
            dftemp_sorted.loc[:,"measuredLH"]=measuredLH

            # for each temperature bin add: the fraction of LH measurements, the
            # average temperature of the site, stdev
            # of the temperature of the site and the stdev scale.
            dftemp_sorted.loc[:,'ratioLH'] = dftemp_sorted['measuredLH']/\
                                                dftemp_sorted.iloc[:,0]
            dftemp_sorted.loc[:,"averagetemp"] = mean_tair_measured

            #SENSIBLE HEAT
            # filtering out only the measured sensible heats
            ds_flux_measuredSH = ds_flux[ds_flux.Qh_qc<1]

            # Ordering the data according to the temperaturebin, making a
            # pandaframe and equalizing the index to the index of the temperature dataframe.
            ds_flux_measuredSH_sorted = ds_flux_measuredSH.groupby(['tempbin']).size()
            df_flux_measuredSH_sorted = pd.DataFrame(ds_flux_measuredSH_sorted)
            dftemp_sorted = dftemp_sorted.set_index(df_flux_measuredSH_sorted.index)
            measuredSH=df_flux_measuredSH_sorted.iloc[:,0]

            # adding the measured SH to temperature pandas dataframe and the
            # fraction of SH measurements
            dftemp_sorted.loc[:,"measuredSH"]=measuredSH
            dftemp_sorted.loc[:,'ratioSH'] = dftemp_sorted['measuredSH']/\
                                            dftemp_sorted.iloc[:,0]
                                            
            if 'NEE' in ds_flux:                                    
                #NEE
                # filtering out only the measured NEE
               
                ds_flux_measuredNEE = ds_flux[ds_flux.NEE_qc<1]
         
                # Ordering the data according to the temperature bin, making a
                # pandaframe and equalizing the index to the index of the temperature dataframe
                ds_flux_measuredNEE_sorted = ds_flux_measuredNEE.groupby(['tempbin']).size()
                df_flux_measuredNEE_sorted = pd.DataFrame(ds_flux_measuredNEE_sorted)
                dftemp_sorted = dftemp_sorted.set_index(df_flux_measuredNEE_sorted.index)
                measuredNEE = df_flux_measuredNEE_sorted.iloc[:,0]
    
                # adding the measured NEE to temperature pandas dataframe and the
                # fraction of NEE measurements
                dftemp_sorted.loc[:,"measuredNEE"] = measuredNEE
                dftemp_sorted.loc[:,'ratioNEE'] = dftemp_sorted['measuredNEE']/\
                                                    dftemp_sorted.iloc[:,0]
                                                    
            else:
                dftemp_sorted.loc[:,"measuredNEE"] = np.nan
                dftemp_sorted.loc[:,'ratioNEE'] = np.nan
                
                   
        
            # only include temperature bins with >10 temperature measurements
            dftemp_sorted = dftemp_sorted[dftemp_sorted[0] > nsample]
            
            
            # creating data for histogram for global temperature
            df_temp = pd.concat([df_temp, dftemp_sorted.iloc[:,0]], axis=1)
            df_LH = pd.concat([df_LH, dftemp_sorted['measuredLH']], axis=1)
            df_SH = pd.concat([df_SH, dftemp_sorted['measuredSH']], axis=1)
            df_NEE = pd.concat([df_NEE, dftemp_sorted['measuredNEE']], axis=1)
    
            # shorten the filename to first 6 letters, which is the abberviation
            # for the site
            mname = os.path.splitext(os.path.basename(m))[0]
            mname = mname[0:6]           
 
          
    # creating histogram for the global temperature distribution 
    df_temp['Total']= df_temp.iloc[:, :].sum(axis=1)
    df_total = pd.DataFrame(df_temp['Total'])
    df_total ["Qle"] = df_LH.iloc[:, :].sum(axis=1)
    df_total ["Qh"] = df_SH.iloc[:, :].sum(axis=1)
    df_total ["NEE"] = df_NEE.iloc[:, :].sum(axis=1)
    #Normalizing
    df_total ["Temp nor"] = df_total['Total'] / sum(df_total['Total'])
    df_total ["Qle nor"] = df_total['Qle'] / sum(df_total['Total'])
    df_total ["Qh nor"] = df_total['Qh'] / sum(df_total['Total'])
    df_total ["NEE nor"] = df_total['NEE'] / sum(df_total['Total'])
    df_total ["ratio Temp"] = 1
    df_total ["ratio Qle"] = df_total ["Qle"]/ df_total["Total"]
    df_total ["ratio Qh"] = df_total ["Qh"]/ df_total["Total"]
    df_total ["ratio NEE"] = df_total ["NEE"]/ df_total["Total"]
                
    
    df_total.to_csv(ofname4)
        
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

def plot_normal_dist(Tair_measured, mean_tair_measured,  ds_met, plot_dir):
    # Create plot normal distribution of the temperature

    width = 9
    height = 6
    fig = plt.figure(figsize=(width, height))
    fig.subplots_adjust(hspace=0.05)
    fig.subplots_adjust(wspace=0.05)
    plt.rcParams['text.usetex'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['font.size'] = 14
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14

    ax = fig.add_subplot(111)

    stdev_tair_measured = np.std(Tair_measured.Tair)
    x = np.linspace(min(ds_met.Tair), max(ds_met.Tair), 1000)
    normal_pdf = norm.pdf(x, mean_tair_measured, stdev_tair_measured)

    ax.plot(x, normal_pdf, "blue", linewidth=2)
    ax.set_title("Temperature distribution")
    ax.set_xlabel("Temperature ($^\circ$C)")
    ax.set_ylabel("Frequency")

    ofname = "normal_distribution.pdf"
    fig.savefig(os.path.join(plot_dir, ofname),
                bbox_inches='tight', pad_inches=0.1)

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
    ofname4 = os.path.join(out_path, "globaltemp.csv")

    main(files_met, files_flux, ds_NEE_ITCpz_met, ds_NEE_ITCpz_flux, ofname4, plot_dir)
        


