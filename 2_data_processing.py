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

# Merge the dwd hornsea nc files
dwd_Hornsea1 = xr.open_dataset("data/dwd_icon_eu_hornsea_1_20200920_20231027.nc")
dwd_Hornsea2 = xr.open_dataset("data/dwd_icon_eu_hornsea_1_20231027_20240108.nc")
dwd_Hornsea2 = dwd_Hornsea2.rename({'reference_time': 'ref_datetime', 'valid_time': 'valid_datetime'})

hornsea1_df = dwd_Hornsea1.to_dataframe()
hornsea2_df = dwd_Hornsea2.to_dataframe()

dwd_Hornsea1_features = dwd_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
dwd_Hornsea1_features["ref_datetime"] = dwd_Hornsea1_features["ref_datetime"].dt.tz_localize("UTC")
dwd_Hornsea1_features["valid_datetime"] = dwd_Hornsea1_features["ref_datetime"] + pd.TimedeltaIndex(dwd_Hornsea1_features["valid_datetime"],unit="hours")

dwd_Hornsea2_features = dwd_Hornsea2["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
dwd_Hornsea2_features["ref_datetime"] = dwd_Hornsea2_features["ref_datetime"].dt.tz_localize("UTC")
dwd_Hornsea2_features["valid_datetime"] = dwd_Hornsea2_features["ref_datetime"] + pd.to_timedelta(dwd_Hornsea2_features["valid_datetime"], unit='h')

dwd_Hornsea1_features = dwd_Hornsea1_features.drop_duplicates(subset='valid_datetime', keep='first')
