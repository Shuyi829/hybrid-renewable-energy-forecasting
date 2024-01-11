import pandas as pd
import xarray as xr
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.iolib.smpickle import load_pickle

import comp_utils

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pickle as pkl

# open nc file
dwd_Hornsea1 = xr.open_dataset("data/dwd_icon_eu_hornsea_1_20200920_20231027.nc")
dwd_Hornsea2 = xr.open_dataset("data/dwd_icon_eu_hornsea_1_20231027_20240108.nc")

ncep_Hornsea1 = xr.open_dataset("data/ncep_gfs_hornsea_1_20200920_20231027.nc")
ncep_Hornsea2 = xr.open_dataset("data/ncep_gfs_hornsea_1_20231027_20240108.nc")

# rename cols
dwd_Hornsea2 = dwd_Hornsea2.rename({'reference_time': 'ref_datetime', 'valid_time': 'valid_datetime'})
ncep_Hornsea2 = ncep_Hornsea2.rename({'reference_time': 'ref_datetime', 'valid_time': 'valid_datetime'})

# to dataframe
dwd_hornsea1_df = dwd_Hornsea1.to_dataframe()
dwd_hornsea2_df = dwd_Hornsea2.to_dataframe()
ncep_hornsea1_df = ncep_Hornsea1.to_dataframe()
ncep_hornsea2_df = ncep_Hornsea2.to_dataframe()

# merge dataFrames
dwd_hornsea_df = pd.concat([dwd_hornsea1_df, dwd_hornsea2_df])
ncep_hornsea_df = pd.concat([ncep_hornsea1_df, ncep_hornsea2_df])

# to pkl
combined_hornsea_df.to_pickle("data/combined_dwd_hornsea_dataframe.pkl")
combined_ncep_df.to_pickle("data/combined_ncep_hornsea_dataframe.pkl")


# merge dataFrames
combined_hornsea_df = pd.concat([hornsea1_df, hornsea2_df])


# 保存合并后的DataFrame为pickle文件
combined_hornsea_df.to_pickle("data/combined_dwd_hornsea_dataframe.pkl")
