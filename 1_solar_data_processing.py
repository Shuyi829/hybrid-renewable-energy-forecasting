import os
import datetime
import numpy as np
import pandas as pd
from processors import *
import matplotlib.pyplot as plt

# Load the solar data
x_train = xr.open_dataset("data/dwd_icon_eu_pes10_20200920_20231027.nc").to_dataframe()
x_valid = xr.open_dataset("data/dwd_icon_eu_pes10_20231027_20240108.nc").to_dataframe()

# Standardize column names and reorder levels
x_valid.index.rename(['valid_datetime', 'ref_datetime', 'point'], inplace=True)

# Process the valid datetime
x_train = x_train.reset_index()
x_train["ref_datetime"] = pd.to_datetime(x_train["ref_datetime"]).dt.tz_localize("UTC")
x_train['valid_datetime'] = x_train['ref_datetime'] + pd.to_timedelta(x_train['valid_datetime'], unit='H')

x_valid = x_valid.reset_index()
x_valid["ref_datetime"] = pd.to_datetime(x_valid["ref_datetime"]).dt.tz_localize("UTC")
x_valid['valid_datetime'] = x_valid['ref_datetime'] + pd.to_timedelta(x_valid['valid_datetime'], unit='H')


# Reduce weather forecasts' redundancy.
duplicate_label = x_train.duplicated(subset=['valid_datetime', 'point'], keep='last')
x_train = x_train.loc[~duplicate_label, :].copy()
x_train.drop(columns=['ref_datetime'], inplace=True)
x_train.rename(columns={"valid_datetime": "datetime"}, inplace=True)
x_train.set_index('datetime', inplace=True)


duplicate_label = x_valid.duplicated(subset=['valid_datetime', 'point'], keep='last')
x_valid = x_valid.loc[~duplicate_label, :].copy()
x_valid.drop(columns=['ref_datetime'], inplace=True)
x_valid.rename(columns={"valid_datetime": "datetime"}, inplace=True)
x_valid.set_index('datetime', inplace=True)


# Split the x into 20 subsets by points
solar_dir = 'data/raw'
os.makedirs(solar_dir, exist_ok=True)

def pivot_wider(df):
    # Pivot the DataFrame to have 'point' as part of the columns MultiIndex
    new_df = df.pivot(columns='point', values=[c for c in df.columns if c != 'point'])
    # Flatten the MultiIndex in columns by joining the level values with an underscore
    new_df.columns = ['_'.join(str(level) for level in col) for col in new_df.columns]
    return new_df

# Apply pivot_wider to your dataframes
x_train_wide = pivot_wider(x_train)
x_valid_wide = pivot_wider(x_valid)

# Get the unique points
points = x_train['point'].unique()

# Dictionary to store each point DataFrame
dfs_train = {}

# Loop through each point and create a separate DataFrame for train dataset
for point in points:
    # Select columns for the current point
    cols = [col for col in x_train_wide.columns if col.endswith(f'_{point}')]
    # Create a DataFrame for the current point and add it to the dictionary
    dfs_train[f'solar_{point}'] = x_train_wide[cols]
    # Optionally, rename columns to remove the point suffix if desired
    dfs_train[f'solar_{point}'].columns = [col.split('_')[0] for col in cols]
    # Save the DataFrame
    dfs_train[f'solar_{point}'].to_pickle(f"{solar_dir}/x_{point}_train.pkl")

# Repeat the same for the validation dataset
dfs_valid = {}
for point in points:
    cols = [col for col in x_valid_wide.columns if col.endswith(f'_{point}')]
    dfs_valid[f'solar_{point}'] = x_valid_wide[cols]
    dfs_valid[f'solar_{point}'].columns = [col.split('_')[0] for col in cols]
    dfs_valid[f'solar_{point}'].to_pickle(f"{solar_dir}/x_{point}_valid.pkl")



