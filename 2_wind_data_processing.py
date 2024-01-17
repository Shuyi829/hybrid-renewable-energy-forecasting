from processors import *
import pandas as pd
import numpy as np

# Process the wind data
dwd_wind_files = ["data/dwd_icon_eu_hornsea_1_20200920_20231027.nc", "data/dwd_icon_eu_hornsea_1_20231027_20240108.nc"]
ncep_wind_files = ["data/ncep_gfs_hornsea_1_20200920_20231027.nc", "data/ncep_gfs_hornsea_1_20231027_20240108.nc"]

wind_dwd = process_dataset(dwd_wind_files, '_dwd', 'wind')
wind_ncep = process_dataset(ncep_wind_files, '_ncep', 'wind')

wind_dwd['WindDirection_cos_dwd'] = np.cos(wind_dwd['WindDirection_dwd'] / 180 * np.pi)
wind_ncep['WindDirection_cos_ncep'] = np.cos(wind_ncep['WindDirection_ncep'] / 180 * np.pi)

wind_dwd.interpolate(method='linear', inplace=True)
wind_ncep.interpolate(method='linear', inplace=True)

# wind_dwd_df = fill_with_nearest(wind_dwd_df)
