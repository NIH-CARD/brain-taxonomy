#!/usr/bin/env python
# coding: utf-8

### set up markers table for use in cellassign

# hand coded tables from @nicks taxonomy table

# In[ ]:
from pathlib import Path
import pandas as pd
import numpy as np

# In[ ]:
## e.g. for xylena data
CELLASSIGN_MARKERS_TABLE = "cellassign_markers.csv"

## load raw data.

# In[ ]:
root_path = Path.cwd()

# In[ ]:
# taxonomy from @nick

NEURON = ["GRIN2A", "RBFOX3"]
ASTROCYTE = ["AQP4", "RFX4"]
OLIGO = ["CLDN11", "CNP", "PLP1", "ST18", "MBP", "MOG", "MAG"]
OPC = ["LHFPL3", "MEGF11", "PCDH15", "PDGFRA"]
IMMUNE = ["PTPRC"]
BLOOD_VESSEL = ["CD34"]


neuron_subs = dict(
    glutamatergic=["SLC17A6", "NEUROD6", "SATB2"],
    gabaergic=["SLC32A1", "GAD2", "LHX6"],
    # dopaminergic=["SLC6A3", "SLC18A2"],
)

astro_sub = dict(protoplasmic=["GJA1"], fibrous=["GFAP", "CD44"])

immune_sub = dict(
    microglia=["P2RY12"], t_cell=["CD8B", "CD8A", "CD3E"], b_cell=["IGHG1"]
)


blood_sub = dict(
    pericytes=["HIGD1B", "ABCC9", "NDUFA4L2", "NOTCH3", "RGS5"],
    endothelial=["PECAM1", "FLT1", "KDR", "SLC2A1", "VWF", "CLDN5", "TIE1"],
)


neuron_other = NEURON
glutamatergic = NEURON + neuron_subs["glutamatergic"]
gabaergic = NEURON + neuron_subs["gabaergic"]

astrocyte_other = ASTROCYTE
protoplasmic_astrocyte = ASTROCYTE + astro_sub["protoplasmic"]
fibrous_astrocyte = ASTROCYTE + astro_sub["fibrous"]

immune_other = IMMUNE
microglia = IMMUNE + immune_sub["microglia"]
t_cell = IMMUNE + immune_sub["t_cell"]
b_cell = IMMUNE + immune_sub["b_cell"]

blood_other = BLOOD_VESSEL
pericyte = BLOOD_VESSEL + blood_sub["pericytes"]
endothelial = BLOOD_VESSEL + blood_sub["endothelial"]

oligo = OLIGO
opc = OPC
unknown = []

cell_types = [
    "oligo",
    "opc",
    "glutamatergic",
    "gabaergic",
    "protoplasmic_astrocyte",
    "fibrous_astrocyte",
    "microglia",
    "t_cell",
    "b_cell",
    "pericyte",
    "endothelial",
    "unknown",
]

# "loose" taxonomy includes a non-subtype for our top-level cell types
# "neuron_other",
# "astrocyte_other",
# "immune_other",
# "blood_other",


# ]


# In[ ]:

colnms = []
colnms = [eval(ct) for ct in cell_types]
col = []
for e in colnms:
    col += e


# In[ ]:
marker = np.unique(col)

# In[ ]:
df = pd.DataFrame(index=marker)

for t in cell_types:
    tt = eval(t)
    df[t] = df.index.isin(tt)

# In[ ]:
df = df.astype(int)

# In[ ]:
cellassign_file = root_path / "markers" / CELLASSIGN_MARKERS_TABLE

df.to_csv(cellassign_file)

# In[ ]:
# test
markers_new = pd.read_csv(cellassign_file, index_col=0)
print(markers_new)

