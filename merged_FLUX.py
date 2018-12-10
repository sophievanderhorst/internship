#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 09:07:43 2018

@author: z5228341
"""
from nco import Nco
import pandas as pd
import xarray as xr
import glob


def open_file(fname):
    ds = xr.open_dataset(fname)
    ds = ds.squeeze(dim=["x","y"], drop=True).to_dataframe()
    ds = ds.reset_index()
    ds = ds.set_index('time') 
    return (ds)
    
Be_Bra1 = glob.glob("/home/z5228341/FLUX_measurements/sophie(1)/sophie/data/Flux_merged/BE-Bra_1996-2002_FLUXNET2015_Flux.nc")
Be_Bra2 = glob.glob("/home/z5228341/FLUX_measurements/sophie(1)/sophie/data/Flux_merged/BE-Bra_2004-2014_FLUXNET2015_Flux.nc")
Be_Bra1 = open_file(Be_Bra1[0])
Be_Bra2 = open_file(Be_Bra2[0])
Be_Bra2 = Be_Bra2.drop(['SWup'], axis =1)

Be_Bra = pd.concat([Be_Bra1, Be_Bra2])

