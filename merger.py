#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 17:25:53 2018

@author: z5228341
"""

from PyPDF2 import PdfFileMerger
import os

path = "../plots/"




pdf_files = ['global_temp.pdf', 
             'Zoommaps/Qle overall.pdf', 'Zoommaps/Qle lower.pdf', 'Zoommaps/Qle upper.pdf',
             'Zoommaps/Qh overall.pdf', 'Zoommaps/Qh lower.pdf', 'Zoommaps/Qh upper.pdf',
             'Zoommaps/NEE overall.pdf', 'Zoommaps/NEE lower.pdf', 'Zoommaps/NEE upper.pdf',
             'temp-precip.pdf', 'scatterplots.pdf', 'heatmap_LH.pdf', 'heatmap_SH.pdf',
             'heatmap_NEE.pdf', 'map_suitable_overall.pdf', 'map_suitable_lowerextreme.pdf',
             'map_suitable_upperextreme.pdf', 'table_suitable_overall.pdf', 
             'table_suitable_lowerextreme.pdf','table_suitable_upperextreme.pdf']
             
merger = PdfFileMerger()
for files in pdf_files:
    merger.append(path+files)

merger.write(path + 'merged.pdf')
merger.close()
    




