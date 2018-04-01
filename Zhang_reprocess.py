#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO

"""
This script was written to generate a plot containing selected genes that are
used as the reference genes in my ICC or RT-qPCR experiments. The source of
the data is Supplementary Table 4 from "Purification and Characterization
of Progenitor and Mature Human Astrocytes Reveals Transcriptional and
Functional Differences with Mouse" by Zhang et al. published in Neuron
2016. DOI: 10.1016/j.neuron.2015.11.013
I do not claim the copyright of the work published as detailed above.
"""

print ("Reading file...")
df = pd.read_excel("Data/TableS4-HumanMouseMasterFPKMList.xlsx", sheet_name=1,
    skiprows=1, index_col=0)
df = df.drop(["Gender"])

goi = ['GFAP', 'VIM', 'NES', 'S100B', 'ALDH1A1', 'NFIA', 'HIF1A', 'CSPG4',
    'TUBB3', 'SOX10', 'SOX9', 'SLC2A1', 'FABP7', 'CD44', 'SOX1']

names = []
for i in range(1, len(df.T)+1):
    if i <= 4:
        names.append('Peri-tumor Astrocytes')
    elif i > 4 and i <= 8:
        names.append('Hippocampi Astrocytes')
    elif i > 8 and i <= 14:
        names.append('Foetal Astrocytes')
    elif i > 14 and i <= 26:
        names.append('Mature Astrocytes')
    elif i == 27:
        names.append('Neurons')
    elif i > 27 and i <= 32:
        names.append('Oligodendrocytes')
    elif i > 32 and i <= 35:
        names.append('Microglia')
    elif i > 35 and i <= 37:
        names.append('Endothelial')
    else:
        names.append('Whole Cortex')

print ("Dropping unwanted cell types...")
df.columns = names
todrop = ['Whole Cortex', 'Peri-tumor Astrocytes', 'Hippocampi Astrocytes',
        'Microglia', 'Endothelial']
df = df.T.drop(todrop).T
dg = df.loc[goi]
dg = dg.astype(np.float64)
dg = dg.sort_index(ascending=False)

print ("Grouping by cell types and calculating the mean and stdev...")
dg = dg.groupby(by=dg.columns, axis=1)
dg_avg = dg.mean()
dg_std = dg.std()

print ("Plotting...")
fig, ax = plt.subplots(figsize=(15/2.54, 18/2.54), tight_layout=True)
plt.xlabel("FPKM")
dg_avg.plot.barh(xerr=dg_std, xlim=0, width=0.9, ax=ax)
# plt.show()

# save figure
# (1) save the image in memory in PNG format
png1 = BytesIO()
fig.savefig(png1, format='png')

# (2) load this image into PIL
png2 = Image.open(png1)

# (3) save as TIFF
print ("Saving plot...")
png2.save('Results/GOI_Zhang.tiff')
png1.close()

print ("DONE!")
