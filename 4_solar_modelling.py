import os
import datetime

# import IPython
# import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
# import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


solar_ncep = pd.read_pickle("data/solar_ncep.pkl")
x = pd.read_pickle("data/solar_dwd.pkl")
y = pd.read_pickle("data/y_solar.pkl")
y = y.iloc[:, 1]
# df = pd.merge(solar_dwd, solar_ncep, left_index=True, right_index=True, how='outer')

# Split the data
column_indices = {name: i for i, name in enumerate(x.columns)}
n = len(x)
num_features = x.shape[1]

def pivot_wider(df):
    df['point1'] = np.array([r[1] for r in df.index])
    new_df = pd.pivot_table(df, index='datetime', columns='point1', values=df.columns)
    return new_df

x = pivot_wider(x)

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
    dfs[f'solar_{point}'].to_pickle(f"data/solar/solar_{point}.pkl")




# x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, shuffle=False)
#
#
# # Standardization.
# x_scaler = StandardScaler()
# x_train_std = x_scaler.fit_transform(x_train)
# x_train_std = pd.DataFrame(x_train_std, columns=x_train.columns, index=x_train.index)
# x_test_std = x_scaler.transform(x_test)
# x_test_std = pd.DataFrame(x_test_std, columns=x_test.columns, index=x_test.index)
#
# y_scaler = StandardScaler()
# y_train_std = y_scaler.fit_transform(y_train)
# y_train_std = pd.DataFrame(y_train_std, columns=y_train.columns, index=y_train.index)
# y_test_std = y_scaler.transform(y_test)
# y_test_std = pd.DataFrame(y_test_std, columns=y_test.columns, index=y_test.index)
#
# pd.to_pickle([x_train_std, y_train_std, x_test_std, y_test_std],
#              "raw/4_data_std.pkl")
# pd.to_pickle([x_scaler, y_scaler], 'raw/4_scaler.pkl')

