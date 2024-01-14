from processors import *

# Load the energy data as y variable
energy_data = pd.read_csv("data/Energy_Data_20200920_20231027.csv")
energy_data["datetime"] = pd.to_datetime(energy_data["dtm"])
energy_data["Wind_MWh_credit"] = 0.5*energy_data["Wind_MW"] - energy_data["boa_MWh"]
energy_data["Solar_MWh_credit"] = 0.5*energy_data["Solar_MW"]
energy_data_subset = energy_data[['datetime','Wind_MWh_credit', 'Solar_MWh_credit']]
energy_data_subset.to_pickle("data/y_energy.pkl")

# Load the solar data
ncep_files = ["data/ncep_gfs_pes10_20200920_20231027.nc", "data/ncep_gfs_pes10_20231027_20240108.nc"]
dwd_files = ["data/dwd_icon_eu_pes10_20200920_20231027.nc", "data/dwd_icon_eu_pes10_20231027_20240108.nc"]

ncep_df = process_dataset(ncep_files, '_ncep', 'solar')
dwd_df = process_dataset(dwd_files, '_dwd', 'solar')


# from sklearn.preprocessing import RobustScaler, MinMaxScaler
# import numpy as np
# import pandas as pd
#
# # Example DataFrame
# data = pd.DataFrame({
#     'SolarDownwardRadiation': np.random.rand(100) * 100
# })
#
# # Define the quantiles
# quantile_range = (0.05, 0.95)
#
# # Initialize RobustScaler and MinMaxScaler
#
# robust_scaler = RobustScaler(quantile_range=quantile_range)
# minmax_scaler = MinMaxScaler()
#
# # Fit the robust scaler on the data
# data_robust_scaled = robust_scaler.fit_transform(data[['SolarDownwardRadiation']])
#
# # Scale the robust scaled data to [0, 1] range
# data_minmax_scaled = minmax_scaler.fit_transform(data_robust_scaled)
#
# # Transform the scaled data back into a DataFrame
# data_scaled = pd.DataFrame(data_minmax_scaled, columns=['SolarDownwardRadiation_scaled'])
#
# # Add the scaled data back to the original DataFrame
# data['SolarDownwardRadiation_scaled'] = data_scaled
#
# robust_scaler = RobustScaler(quantile_range=quantile_range)
# minmax_scaler = MinMaxScaler()
#
# # Fit the robust scaler on the data
# data_robust_scaled = robust_scaler.fit_transform(data[['SolarDownwardRadiation']])
#
# # Scale the robust scaled data to [0, 1] range
# data_minmax_scaled = minmax_scaler.fit_transform(data_robust_scaled)
#
# # Transform the scaled data back into a DataFrame
# data_scaled = pd.DataFrame(data_minmax_scaled, columns=['SolarDownwardRadiation_scaled'])
#
# # Add the scaled data back to the original DataFrame
# data['SolarDownwardRadiation_scaled'] = data_scaled
#
# # Assuming 'data' is your DataFrame and 'features_to_scale' is a list of columns you want to scale
# features_to_scale = ['CloudCover_ncep', 'SolarDownwardRadiation_ncep', 'Temperature_ncep']  # example feature columns
# data_to_scale = data[features_to_scale]
#
# # Fit the robust scaler on the data
# robust_scaled_data = robust_scaler.fit_transform(data_to_scale)
#
# # Scale the robust scaled data to [0, 1] range
# minmax_scaled_data = minmax_scaler.fit_transform(robust_scaled_data)
#
# # Transform the scaled data back into a DataFrame with appropriate column names
# scaled_columns = [f"{col}_scaled" for col in features_to_scale]
# data_scaled = pd.DataFrame(minmax_scaled_data, columns=scaled_columns, index=data.index)
#
# # Add the scaled data back to the original DataFrame
# data[scaled_columns] = data_scaled
