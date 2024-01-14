from processors import *

# Process the wind data
dwd_wind_files = ["data/dwd_icon_eu_hornsea_1_20200920_20231027.nc", "data/dwd_icon_eu_hornsea_1_20231027_20240108.nc"]
ncep_wind_files = ["data/ncep_gfs_hornsea_1_20200920_20231027.nc", "data/ncep_gfs_hornsea_1_20231027_20240108.nc"]

dwd_wind_df = process_dataset(dwd_wind_files, '_dwd', 'wind')
ncep_wind_df = process_dataset(ncep_wind_files, '_ncencep', 'wind')


