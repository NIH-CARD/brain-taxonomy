#!/usr/bin/env python
# coding: utf-8

### set up markers table for use in cellassign

# reads from @nicks taxonomy table

# In[ ]:
from pathlib import Path
import pandas as pd
import numpy as np

# In[ ]:
## e.g. for xylena data

TAXONOMY_TABLE_v1 = "taxonomy-v1.xlsx"
TAXONOMY_TABLE_v2 = "Taxa Marker (Frontal Cortex) List.xlsx"
CELLASSIGN_MARKERS_TABLE = "cellassign_markers.csv"
CELLASSIGN_SIMPLE_MARKERS_TABLE = "cellassign_simple_markers.csv"
CELLASSIGN_SIMPLE2_MARKERS_TABLE = "cellassign_simple2_markers.csv"
CELLASSIGN_SIMPLE3_MARKERS_TABLE = "cellassign_simple3_markers.csv"

# In[ ]:
root_path = Path.cwd()

# In[ ]:
def get_taxonomy(file_path:Path|None = None, version:str="v2") -> dict[pd.DataFrame]:
    """
    defaults  TAXONOMY_TABLE_v2 but should work for v1 as well
    """
    if file_path is None:
        if version == "v2":
            # DEFAULT: 
            # Taxa Marker (Frontal Cortex) List
            # from google doc:  https://docs.google.com/spreadsheets/d/1G7rsn3PtIzPZIPV-xqIaOgVTBVeBQr3dYDVpWjatKgo/edit?usp=sharing
            GOOGLE_SHEET_ID = "1G7rsn3PtIzPZIPV-xqIaOgVTBVeBQr3dYDVpWjatKgo"
            file_path = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=xlsx"
            try:
                print(f"reading taxonomy file from: google sheet: \"{TAXONOMY_TABLE_v2}\" ")
                sheets_dict = pd.read_excel(file_path, sheet_name=None, header=None)
            except:
                print(f"could not read taxonomy file from google, reading from: \"{TAXONOMY_TABLE_v2}\"")
                file_path = root_path / "taxonomies" / TAXONOMY_TABLE_v2
                sheets_dict = pd.read_excel(file_path, sheet_name=None, header=None)

        elif version == "v1":
                print(f"warning v1 is depricated, reading from: \"{TAXONOMY_TABLE_v1}\"")
                file_path = root_path / "taxonomies" / TAXONOMY_TABLE_v1
                sheets_dict = pd.read_excel(file_path, sheet_name=None, header=None)

        else:
            raise ValueError("version must be 'v1' or 'v2'")

    else:
        print(f"reading from \"{file_path.name}\"")
        sheets_dict = pd.read_excel(file_path, sheet_name=None, header=None)


    taxonomy = {}
    all_genes = []
    # Now you can access each sheet by its name
    for sheet_name, df in sheets_dict.items():
        print(f"Sheet name: {sheet_name}")
        # # convert dataframe into a dictionary
        # df = df.T
        # # Set the first row as the header
        # df.columns = df.iloc[0]
        # df = df.drop(0).reset_index(drop=True)
        cell_types = {}
        for _, row in df.iterrows():
            name = row[0]
            genes = row[1:].dropna().to_list()
            all_genes += genes
            cell_types[name] = genes
            # cell_types[name] = row[1:].dropna().to_list()

        taxonomy[sheet_name] = cell_types

    return taxonomy, all_genes

# In[ ]:
def make_markers_table_v2(dfs:dict, cell_types:list, all_genes:list) -> pd.DataFrame:
    """
    to make a markers table from the taxonomy table
    we need to know how the taxonomy tables are named...  this "function" is a bit 
    of a hack to get the cell types from the TAXONOMY_TABLE_v2 ONLY
    """
    ### pack the Frontal Coretex defined taxa into a cell_assign table

    # define top level types.
    NEURON = dfs["ROOT_LEVEL"]["NEURON"]
    ASTROCYTE = dfs["ROOT_LEVEL"]["ASTROCYTE"]
    OLIGO = dfs["ROOT_LEVEL"]["OLIGO"]
    OPC = dfs["ROOT_LEVEL"]["OPC"]
    IMMUNE = dfs["ROOT_LEVEL"]["IMMUNE"]
    BLOOD_VESSEL = dfs["ROOT_LEVEL"]["BLOOD_VESSEL"]

    # define subtypes
    neuron_subs = dfs['neuron']
    astro_sub = dfs['astrocyte']
    immune_sub = dfs['immune']
    blood_sub = dfs['blood_vessel'] 

    # define all cell types
    neuron_other = NEURON
    glutamatergic = NEURON + neuron_subs["glutamatergic"]
    gabergic = NEURON + neuron_subs["gabaergic"]

    astrocyte = ASTROCYTE
    protoplasmic_astrocyte = ASTROCYTE + astro_sub["protoplasmic"]
    fibrous_astrocyte = ASTROCYTE + astro_sub["fibrous"]

    immune = IMMUNE
    microglia = IMMUNE + immune_sub["microglia"]
    t_cell = IMMUNE + immune_sub["t_cell"]
    b_cell = IMMUNE + immune_sub["b_cell"]

    blood = BLOOD_VESSEL
    pericyte = BLOOD_VESSEL + blood_sub["pericytes"]
    endothelial = BLOOD_VESSEL + blood_sub["endothelial"]

    oligo = OLIGO
    opc = OPC
    unknown = []
    ###

    df = pd.DataFrame(index=all_genes)

    for t in cell_types:
        tt = eval(t)
        df[t] = df.index.isin(tt)

    df = df.astype(int)
    return df


# %%
taxonomy_file = root_path / "taxonomies" / TAXONOMY_TABLE_v2
# %%
# tests
# dfs = get_taxonomy(version="v1")
# dfs = get_taxonomy(version="v2")
# dfs = get_taxonomy(file_path=taxonomy_file)



# %%
cell_types = [
    "oligo",
    "opc",
    "glutamatergic",
    "gabergic",
    "astrocyte",
    "immune",
    "blood",
    "unknown",
]

df = make_markers_table_v2(dfs, cell_types, all_genes)

# In[ ]:
# export to csv
cellassign_file = root_path / "markers" / CELLASSIGN_SIMPLE_MARKERS_TABLE
df.to_csv(cellassign_file)

# In[ ]:
# test
markers_new = pd.read_csv(cellassign_file, index_col=0)
print(markers_new)

# %%

# %%
cell_types = [
    "oligo",
    "opc",
    "glutamatergic",
    "gabergic",
    "astrocyte",
    "immune",
    "blood",
]

df = make_markers_table_v2(dfs, cell_types, all_genes)

# In[ ]:
# export to csv
cellassign_file = root_path / "markers" / CELLASSIGN_SIMPLE2_MARKERS_TABLE
df.to_csv(cellassign_file)

# In[ ]:
# test
markers_new = pd.read_csv(cellassign_file, index_col=0)
print(markers_new)

# %%
dfs, all_genes = get_taxonomy(version="v2")

# Oligo   <- OLIGO: CLDN11	CNP	PLP1	ST18	MBP	MOG	MAG
# ExN     <- NEURON+glutamatergic:GRIN2A	RBFOX3  SLC17A6	NEUROD6	SATB2
# InN     <- NEURON+gabaergic:GRIN2A	RBFOX3 SLC32A1	GAD2	LHX6
# Astro  <- ASTROCYTE: AQP4	RFX4
# MG     <- IMMUNE (t and b cells are implicitly ignored or called microglia): PTPRC
# OPC    <- OPC: LHFPL3	MEGF11	PCDH15	PDGFRA
# VC       <- BLOOD_VESSEL: CD34

# %%


df = make_markers_table_v2(dfs, cell_types, all_genes)

# In[ ]:
# remap columns as above
mapping = {"oligo": "Oligo",
           "opc": "OPC",
           "glutamatergic": "ExN",
           "gabergic": "InN",
           "astrocyte": "Astro",
           "immune": "MG",
           "blood": "VC"}


df.rename(columns=mapping, inplace=True)

# In[ ]:
# export to csv
cellassign_file = root_path / "markers" / CELLASSIGN_SIMPLE3_MARKERS_TABLE
df.to_csv(cellassign_file)

# In[ ]:
# test
markers_new = pd.read_csv(cellassign_file, index_col=0)
print(markers_new)

# %%
