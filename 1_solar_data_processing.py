import os
import datetime
import numpy as np
import pandas as pd
from processors import *
import matplotlib.pyplot as plt


# Load the solar data
ncep_files = ["data/ncep_gfs_pes10_20200920_20231027.nc", "data/ncep_gfs_pes10_20231027_20240108.nc"]
dwd_files = ["data/dwd_icon_eu_pes10_20200920_20231027.nc", "data/dwd_icon_eu_pes10_20231027_20240108.nc"]

solar_ncep = process_dataset(ncep_files, '_ncep', 'solar')
solar_dwd = process_dataset(dwd_files, '_dwd', 'solar')

# Split the x into different subsets by points
solar_dir = 'data/solar'
os.makedirs(solar_dir, exist_ok=True)

x = pivot_wider(solar_dwd)

# Get the unique points from the second level of the MultiIndex
points = x.columns.get_level_values(1).unique()

# Dictionary to store each point DataFrame
dfs = {}

# Loop through each point and create a separate DataFrame
for point in points:
    # Select columns for the current point
    cols = [col for col in x.columns if col[1] == point]
    # Create a DataFrame for the current point and add it to the dictionary
    dfs[f'solar_{point}'] = x[cols]
    dfs[f'solar_{point}'].to_pickle(f"{solar_dir}/solar_{point}.pkl")





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



