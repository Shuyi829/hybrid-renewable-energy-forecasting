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

# Load the energy data as y variable
energy_data = pd.read_csv("data/Energy_Data_20200920_20231027.csv")
energy_data["datetime"] = pd.to_datetime(energy_data["dtm"])
energy_data["Wind_MWh_credit"] = 0.5*energy_data["Wind_MW"] - energy_data["boa_MWh"]
energy_data["Solar_MWh_credit"] = 0.5*energy_data["Solar_MW"]
energy_data_solar = energy_data[['datetime','Solar_MWh_credit']]
energy_data_wind = energy_data[['datetime','Wind_MWh_credit']]

# Create a boolean mask for rows where the time is exactly on the hour
on_the_hour_mask = energy_data_solar['datetime'].dt.minute == 0
# Create a DataFrame for the on-the-hour times
df_on_the_hour = energy_data_solar[on_the_hour_mask].copy()

# Create a DataFrame for the half-hour marks and adjust the 'datetime' to match on-the-hour times
df_half_hour = energy_data_solar[~on_the_hour_mask].copy()
df_half_hour.loc[:, 'datetime'] = df_half_hour['datetime'] - pd.Timedelta(minutes=30)

# This will add the half-hour values as a new column in the on-the-hour DataFrame
result_df = pd.merge(df_on_the_hour, df_half_hour, on='datetime', how='left', suffixes=('_on_hour', '_half_hour'))



energy_data_solar.to_pickle("data/y_solar.pkl")
energy_data_wind.to_pickle("data/y_wind.pkl")



ncep_demand_his = xr.open_dataset('data/ncep_gfs_demand_20200920_20231027.nc')
ncep_demand_now = xr.open_dataset('data/ncep_gfs_demand_20231027_20240108.nc')

ncep_demand_his_df = ncep_demand_his.to_dataframe()
ncep_demand_now_df = ncep_demand_now.to_dataframe()

ncep_demand_now_df.index.rename(['ref_datetime','valid_datetime','point'],inplace=True)

combined_ncep_df =pd.concat([ncep_demand_his_df,ncep_demand_now_df])

combined_ncep_df.to_pickle('data/combined_ncep_demand_dataframe.pkl')

dwd_demand_his = xr.open_dataset('data/dwd_icon_eu_demand_20200920_20231027.nc')
dwd_demand_now = xr.open_dataset('data/dwd_icon_eu_demand_20231027_20240108.nc')

dwd_demand_his_df = dwd_demand_his.to_dataframe()
dwd_demand_now_df = dwd_demand_now.to_dataframe()

dwd_demand_now_df.index.rename(['valid_datetime','ref_datetime','point'],inplace=True)

combined_dwd_df =pd.concat([dwd_demand_his_df,dwd_demand_now_df])

combined_dwd_df.to_pickle('data/combined_dwd_demand_dataframe.pkl')
