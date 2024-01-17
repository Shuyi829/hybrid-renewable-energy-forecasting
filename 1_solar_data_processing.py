from processors import *
from sklearn.preprocessing import RobustScaler, MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the solar data
ncep_files = ["data/ncep_gfs_pes10_20200920_20231027.nc", "data/ncep_gfs_pes10_20231027_20240108.nc"]
dwd_files = ["data/dwd_icon_eu_pes10_20200920_20231027.nc", "data/dwd_icon_eu_pes10_20231027_20240108.nc"]

ncep_df = process_dataset(ncep_files, '_ncep', 'solar')
dwd_df = process_dataset(dwd_files, '_dwd', 'solar')

# Read the pickle file
solar_dwd=pd.read_pickle("data/solar_dwd.pkl")
solar_ncep=pd.read_pickle("data/solar_ncep.pkl")

# Draw the distribution plots
plot_dir = 'data/plots'
os.makedirs(plot_dir, exist_ok=True)
fig, axes = plt.subplots(nrows=1, ncols=solar_dwd.shape[1], figsize=(20, 5))
for ax, column in zip(axes, solar_dwd.columns):
    solar_dwd[column].plot(kind='hist', ax=ax, bins=30, alpha=0.6)
    ax.set_title(column)
plt.tight_layout()
plot_path = os.path.join(plot_dir, 'solar_dwd.png')
fig.savefig(plot_path)

fig, axes = plt.subplots(nrows=1, ncols=solar_ncep.shape[1], figsize=(20, 5))
for ax, column in zip(axes, solar_ncep.columns):
    solar_ncep[column].plot(kind='hist', ax=ax, bins=30, alpha=0.6)
    ax.set_title(column)
plt.tight_layout()
plot_path = os.path.join(plot_dir, 'solar_ncep.png')
fig.savefig(plot_path)


# ncep's solardownwards have a half of zero values so drop it
solar_ncep = solar_ncep.drop(columns=['SolarDownwardRadiation_ncep'])

solar_ncep.to_pickle(f"data/solar_ncep.pkl")
solar_dwd.to_pickle(f"data/solar_dwd.pkl")

# # Define the quantiles
# quantile_range = (0.05, 0.95)
#
# # Initialize RobustScaler and MinMaxScaler
# robust_scaler = RobustScaler(quantile_range=quantile_range)
# minmax_scaler = MinMaxScaler()
#
# # Fit the robust scaler on the data
# data_robust_scaled = robust_scaler.fit_transform(solar_ncep[['SolarDownwardRadiation_ncep']])
#
# # Scale the robust scaled data to [0, 1] range
# data_minmax_scaled = minmax_scaler.fit_transform(data_robust_scaled)
#
# # Transform the scaled data back into a DataFrame
# data_scaled = pd.DataFrame(data_minmax_scaled, columns=['SolarDownwardRadiation_scaled'])
#
# # Add the scaled data back to the original DataFrame
# solar_ncep['SolarDownwardRadiation_scaled'] = data_scaled
#
# robust_scaler = RobustScaler(quantile_range=quantile_range)
# minmax_scaler = MinMaxScaler()
#
# # Fit the robust scaler on the data
# data_robust_scaled = robust_scaler.fit_transform(solar_ncep[['SolarDownwardRadiation']])
#
# # Scale the robust scaled data to [0, 1] range
# data_minmax_scaled = minmax_scaler.fit_transform(data_robust_scaled)
#
# # Transform the scaled data back into a DataFrame
# data_scaled = pd.DataFrame(data_minmax_scaled, columns=['SolarDownwardRadiation_scaled'])
#
# # Add the scaled data back to the original DataFrame
# solar_ncep['SolarDownwardRadiation_scaled'] = data_scaled
# features_to_scale = ['CloudCover_ncep', 'SolarDownwardRadiation_ncep', 'Temperature_ncep']
# data_to_scale = solar_ncep[features_to_scale]
#
# # Fit the robust scaler on the data
# robust_scaled_data = robust_scaler.fit_transform(data_to_scale)
#
# # Scale the robust scaled data to [0, 1] range
# minmax_scaled_data = minmax_scaler.fit_transform(robust_scaled_data)
#
# # Transform the scaled data back into a DataFrame with appropriate column names
# scaled_columns = [f"{col}_scaled" for col in features_to_scale]
# data_scaled = pd.DataFrame(minmax_scaled_data, columns=scaled_columns, index=solar_ncep.index)
#
# # Add the scaled data back to the original DataFrame
# solar_ncep[scaled_columns] = data_scaled
