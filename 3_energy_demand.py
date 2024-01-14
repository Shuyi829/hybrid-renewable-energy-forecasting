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
energy_data_subset = energy_data[['datetime','Wind_MWh_credit', 'Solar_MWh_credit']]
energy_data_subset.to_pickle("data/y_energy.pkl")


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
