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

# Standardize column names in hornsea2_df to match hornsea1_df
ncep_pes2_df.index.rename(['ref_datetime','valid_datetime','point'], inplace=True)

# Concatenate the DataFrames
combined_necp_df = pd.concat([ncep_pes1_df,ncep_pes2_df])

# Group by 'ref_datetime' and 'valid_datetime' and calculate the mean
combined_necp_features = combined_necp_df.groupby(['ref_datetime', 'valid_datetime']).mean()

# Reset index and then localize 'ref_datetime' to UTC and adjust 'valid_datetime'
combined_necp_features.reset_index(inplace=True)
combined_necp_features["ref_datetime"] = combined_necp_features["ref_datetime"].dt.tz_localize("UTC")
combined_necp_features["valid_datetime"] = combined_necp_features["ref_datetime"] + pd.TimedeltaIndex(combined_necp_features["valid_datetime"], unit="hours")

# Remove duplicates and keep the last occurrence
unique_necp_features = combined_necp_features.groupby('valid_datetime').last().reset_index()

# Set 'valid_datetime' as the index
unique_necp_features.set_index('valid_datetime', inplace=True)

# Save the final DataFrame as a pickle file
unique_necp_features.to_pickle("data/combined_ncep_pes_dataframe.pkl")


# Merge the dwd pes files
dwd_pes1 = xr.open_dataset("data/dwd_icon_eu_pes10_20200920_20231027.nc")
dwd_pes2 = xr.open_dataset("data/dwd_icon_eu_pes10_20231027_20240108.nc")

dwd_pes1_df = dwd_pes1.to_dataframe()
dwd_pes2_df = dwd_pes2.to_dataframe()

# Standardize column names in hornsea2_df to match hornsea1_df
dwd_pes2_df.index.rename(['valid_datetime','ref_datetime','point'], inplace=True)

# Concatenate the DataFrames
combined_dwd_df = pd.concat([dwd_pes1_df,dwd_pes2_df])

# Save the combined DataFrame as a pickle file
combined_dwd_df.to_pickle("data/combined_dwd_pes_dataframe.pkl")





# dwd_Hornsea1 = xr.open_dataset("data/dwd_icon_eu_hornsea_1_20200920_20231027.nc")
# dwd_Hornsea1_features = dwd_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
# dwd_Hornsea1_features["ref_datetime"] = dwd_Hornsea1_features["ref_datetime"].dt.tz_localize("UTC")
# dwd_Hornsea1_features["valid_datetime"] = dwd_Hornsea1_features["ref_datetime"] + pd.TimedeltaIndex(dwd_Hornsea1_features["valid_datetime"],unit="hours")
#
# dwd_solar = xr.open_dataset("data/dwd_icon_eu_pes10_20200920_20231027.nc")
# dwd_solar_features = dwd_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
# dwd_solar_features["ref_datetime"] = dwd_solar_features["ref_datetime"].dt.tz_localize("UTC")
# dwd_solar_features["valid_datetime"] = dwd_solar_features["ref_datetime"] + pd.TimedeltaIndex(dwd_solar_features["valid_datetime"],unit="hours")
#
# energy_data = pd.read_csv("data/Energy_Data_20200920_20231027.csv")
# energy_data["dtm"] = pd.to_datetime(energy_data["dtm"])
# energy_data["Wind_MWh_credit"] = 0.5*energy_data["Wind_MW"] - energy_data["boa_MWh"]
# energy_data["Solar_MWh_credit"] = 0.5*energy_data["Solar_MW"]
#
#
#
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




