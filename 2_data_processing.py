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

# to dataframe
dwd_hornsea1_df = dwd_Hornsea1.to_dataframe()
dwd_hornsea2_df = dwd_Hornsea2.to_dataframe()
ncep_hornsea1_df = ncep_Hornsea1.to_dataframe()
ncep_hornsea2_df = ncep_Hornsea2.to_dataframe()

dwd_hornsea2_df.index.rename(['ref_datetime','valid_datetime','latitude','longitude'], inplace=True)
ncep_hornsea2_df.index.rename(['ref_datetime','valid_datetime','latitude','longitude'], inplace=True)

dwd_hornsea2_df = dwd_hornsea2_df.reorder_levels(['ref_datetime', 'valid_datetime', 'latitude', 'longitude'])
ncep_hornsea2_df = ncep_hornsea2_df.reorder_levels(['ref_datetime', 'valid_datetime', 'latitude', 'longitude'])


# merge dataFrames
dwd_hornsea_df = pd.concat([dwd_hornsea1_df, dwd_hornsea2_df])
ncep_hornsea_df = pd.concat([ncep_hornsea1_df, ncep_hornsea2_df])


# Reset index and keep the 6am ref time
dwd_hornsea_df = dwd_hornsea_df.reset_index()
dwd_hornsea_df["ref_datetime"] = pd.to_datetime(dwd_hornsea_df["ref_datetime"]).dt.tz_localize("UTC")
dwd_hornsea_df = dwd_hornsea_df[dwd_hornsea_df['ref_datetime'].dt.hour == 6]

ncep_hornsea_df = ncep_hornsea_df.reset_index()
ncep_hornsea_df["ref_datetime"] = pd.to_datetime(ncep_hornsea_df["ref_datetime"]).dt.tz_localize("UTC")
ncep_hornsea_df = ncep_hornsea_df[ncep_hornsea_df['ref_datetime'].dt.hour == 6]



# # Filter the 'valid_datetime'
filtered_dwd_hornsea_df = dwd_hornsea_df[(dwd_hornsea_df['valid_datetime'] >= 18) & (dwd_hornsea_df['valid_datetime'] <= 41)]
filtered_ncep_hornsea_df = ncep_hornsea_df[(ncep_hornsea_df['valid_datetime'] >= 18) & (ncep_hornsea_df['valid_datetime'] <= 41)]


# filtered_ncep_df = filtered_ncep_df.copy()
filtered_dwd_hornsea_df['valid_datetime'] = filtered_dwd_hornsea_df['valid_datetime'].astype(int)
filtered_ncep_hornsea_df['valid_datetime'] = filtered_ncep_hornsea_df['valid_datetime'].astype(int)

# # Add the 'valid_datetime' as hours to 'ref_datetime' to get the datetime
filtered_dwd_hornsea_df['datetime'] = filtered_dwd_hornsea_df['ref_datetime'] + pd.to_timedelta(filtered_dwd_hornsea_df['valid_datetime'], unit='H')
filtered_ncep_hornsea_df['datetime'] = filtered_ncep_hornsea_df['ref_datetime'] + pd.to_timedelta(filtered_ncep_hornsea_df['valid_datetime'], unit='H')

# # Set datetime as the index
filtered_dwd_hornsea_df.set_index(['datetime', 'latitude', 'longitude'], inplace=True)
filtered_ncep_hornsea_df.set_index(['datetime', 'latitude', 'longitude'], inplace=True)

# # Drop the 'valid_datetime' column from the DataFrame
filtered_dwd_hornsea_df = filtered_dwd_hornsea_df.drop(columns=['ref_datetime','valid_datetime'])
filtered_dwd_hornsea_df = filtered_dwd_hornsea_df.add_suffix('_dwd')

filtered_ncep_hornsea_df = filtered_ncep_hornsea_df.drop(columns=['ref_datetime','valid_datetime'])
filtered_ncep_hornsea_df = filtered_ncep_hornsea_df.add_suffix('_ncep')


# Save the final DataFrame as a pickle file
filtered_dwd_hornsea_df.to_pickle("data/combined_dwd_hornsea_dataframe.pkl")
filtered_ncep_hornsea_df.to_pickle("data/combined_ncep_hornsea_dataframe.pkl")

