#!/bin/bash

# what am i doing!

rm ../data/Met_merged/*

files="BE-Bra IL-Yat IT-Cpz IT-Non IT-Ro2 SD-Dem SE-Fla UK-Gri US-Cop US-Los US-Syv US-WCr ZM-Mon"

for i in $files;
do

  echo "$i"

  site_files=$(ls -l "../data/Met/$i"* | gawk '{print $9}')

  count=1

  for j in $site_files;
  do

    if [ $i == "IT-Cpz" ];
    then
      cdo select,name=Tair,Tair_qc,longitude,latitude,Rainf,SWdown $j tmp_$count.nc
    else
      cdo select,name=Tair,Tair_qc,longitude,latitude,Rainf,SWdown $j tmp_$count.nc

    fi
    #cdo select,name=Qle,Qle_qc,Qh,Qh_qc,NEE,NEE_qc $j tmp_$count.nc

    let count=count+1

  done


  fbname=$(basename "$j")

  cdo mergetime *.nc merged.nc
  mv merged.nc "../data/Met_merged/$fbname"

  rm tmp_*.nc

done
