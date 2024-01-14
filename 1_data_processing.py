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


# Merge the ncep pes files
ncep_pes1 = xr.open_dataset("data/ncep_gfs_pes10_20200920_20231027.nc")
ncep_pes2 = xr.open_dataset("data/ncep_gfs_pes10_20231027_20240108.nc")

ncep_pes1_df = ncep_pes1.to_dataframe()
ncep_pes2_df = ncep_pes2.to_dataframe()

# Standardize column names
ncep_pes2_df.index.rename(['ref_datetime','valid_datetime','point'], inplace=True)
ncep_pes2_df = ncep_pes2_df.reorder_levels(['ref_datetime', 'valid_datetime', 'point'])

# Concatenate the DataFrames
combined_ncep_df = pd.concat([ncep_pes1_df,ncep_pes2_df])

# Reset index and keep the 6am ref time
combined_ncep_df = combined_ncep_df.reset_index()
combined_ncep_df["ref_datetime"] = pd.to_datetime(combined_ncep_df["ref_datetime"]).dt.tz_localize("UTC")
combined_ncep_df = combined_ncep_df[combined_ncep_df['ref_datetime'].dt.hour == 6]

# Filter the 'valid_datetime'
filtered_ncep_df = combined_ncep_df[(combined_ncep_df['valid_datetime'] >= 18) & (combined_ncep_df['valid_datetime'] <= 41)]

filtered_ncep_df = filtered_ncep_df.copy()
filtered_ncep_df['valid_datetime'] = filtered_ncep_df['valid_datetime'].astype(int)

# Add the 'valid_datetime' as hours to 'ref_datetime' to get the datetime
filtered_ncep_df['datetime'] = filtered_ncep_df['ref_datetime'] + pd.to_timedelta(filtered_ncep_df['valid_datetime'], unit='H')

# Set datetime as the index
filtered_ncep_df.set_index(['datetime','point', 'latitude', 'longitude'], inplace=True)

# Drop the 'valid_datetime' column from the DataFrame
filtered_ncep_df = filtered_ncep_df.drop(columns=['ref_datetime','valid_datetime'])
filtered_ncep_df = filtered_ncep_df.add_suffix('_ncep')

# Save the final DataFrame as a pickle file
filtered_ncep_df.to_pickle("data/combined_ncep_pes_dataframe.pkl")



# Merge the dwd pes files
dwd_pes1 = xr.open_dataset("data/dwd_icon_eu_pes10_20200920_20231027.nc")
dwd_pes2 = xr.open_dataset("data/dwd_icon_eu_pes10_20231027_20240108.nc")

dwd_pes1_df = dwd_pes1.to_dataframe()
dwd_pes2_df = dwd_pes2.to_dataframe()

# Standardize column names
dwd_pes2_df.index.rename(['ref_datetime','valid_datetime','point'], inplace=True)
dwd_pes2_df = dwd_pes2_df.reorder_levels(['ref_datetime', 'valid_datetime', 'point'])

# Concatenate the DataFrames
combined_dwd_df = pd.concat([dwd_pes1_df,dwd_pes2_df])

# Reset index and keep the 6am ref time
combined_dwd_df = combined_dwd_df.reset_index()
combined_dwd_df["ref_datetime"] = pd.to_datetime(combined_dwd_df["ref_datetime"]).dt.tz_localize("UTC")
combined_dwd_df = combined_dwd_df[combined_dwd_df['ref_datetime'].dt.hour == 6]

# Filter the 'valid_datetime'
filtered_dwd_df = combined_dwd_df[(combined_dwd_df['valid_datetime'] >= 18) & (combined_dwd_df['valid_datetime'] <= 41)]

filtered_dwd_df = filtered_dwd_df.copy()
filtered_dwd_df['valid_datetime'] = filtered_dwd_df['valid_datetime'].astype(int)

# Add the 'valid_datetime' as hours to 'ref_datetime' to get the datetime
filtered_dwd_df['datetime'] = filtered_dwd_df['ref_datetime'] + pd.to_timedelta(filtered_dwd_df['valid_datetime'], unit='H')

# Set datetime as the index
filtered_dwd_df.set_index(['datetime','point', 'latitude', 'longitude'], inplace=True)

# Drop the 'valid_datetime' column from the DataFrame
filtered_dwd_df = filtered_dwd_df.drop(columns=['ref_datetime','valid_datetime'])
filtered_dwd_df = filtered_dwd_df.add_suffix('_dwd')

# Save the combined DataFrame as a pickle file
filtered_dwd_df.to_pickle("data/combined_dwd_pes_dataframe.pkl")






# # Test API
# rebase_api_client = comp_utils.RebaseAPI(api_key = open("team_key.txt").read())
#
# test_date = "2020-05-05"
#
# latest_dwd_Hornsea1 = comp_utils.weather_df_to_xr(rebase_api_client.get_hornsea_dwd())
# latest_dwd_solar = comp_utils.weather_df_to_xr(rebase_api_client.get_pes10_nwp("DWD_ICON-EU"))
#
# latest_dwd_Hornsea1_features = latest_dwd_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
# latest_dwd_solar_features = latest_dwd_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
#
# latest_forecast_table = latest_dwd_Hornsea1_features.merge(latest_dwd_solar_features,how="outer",on=["ref_datetime","valid_datetime"])
# latest_forecast_table = latest_forecast_table.set_index("valid_datetime").resample("30T").interpolate("linear",limit=5).reset_index()
#
# latest_forecast_table.rename(columns={"WindSpeed:100":"WindSpeed"},inplace=True)
#
# print(latest_forecast_table)



# # Get day ahead price
# day_ahead_price_df = rebase_api_client.get_variable(day=test_date, variable="solar_and_wind_forecast")
# print(day_ahead_price_df.columns)

# # Get imbalance price
# imbalance_price_df = rebase_api_client.get_variable(day=test_date, variable="imbalance_price")
# print(imbalance_price_df.head())
#
# # get wind and solar production data
# wind_prod_df = rebase_api_client.get_variable(day=test_date, variable="wind_total_production")
# solar_prod_df = rebase_api_client.get_variable(day=test_date, variable="solar_total_production")
#
# energy_data_filtered = energy_data.loc[
#     (energy_data["dtm"] >= pd.to_datetime(test_date).tz_localize("Europe/Paris")) &
#     (energy_data["dtm"] < pd.to_datetime(test_date).tz_localize("Europe/Paris") + pd.Timedelta(1, unit="day"))
# ]
# print(energy_data_filtered)




