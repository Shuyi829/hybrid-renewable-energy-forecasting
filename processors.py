import pandas as pd
import xarray as xr
import numpy as np
from scipy.spatial.distance import cdist

def process_dataset(file_paths, suffix, dataset_type):
    # Load and concatenate datasets
    datasets = [xr.open_dataset(path).to_dataframe() for path in file_paths]
    combined_df = pd.concat(datasets)

    # Standardize column names and reorder levels based on dataset type
    if dataset_type == 'solar':
        combined_df.index.rename(['ref_datetime', 'valid_datetime', 'point'], inplace=True)
        combined_df = combined_df.reorder_levels(['ref_datetime', 'valid_datetime', 'point'])
    elif dataset_type == 'wind':
        combined_df.index.rename(['ref_datetime', 'valid_datetime', 'latitude', 'longitude'], inplace=True)
        combined_df = combined_df.reorder_levels(['ref_datetime', 'valid_datetime', 'latitude', 'longitude'])

    # Common processing steps
    combined_df = combined_df.reset_index()
    combined_df["ref_datetime"] = pd.to_datetime(combined_df["ref_datetime"]).dt.tz_localize("UTC")
    combined_df = combined_df[combined_df['ref_datetime'].dt.hour == 6]
    combined_df = combined_df[(combined_df['valid_datetime'] >= 18) & (combined_df['valid_datetime'] <= 41)]
    combined_df['valid_datetime'] = combined_df['valid_datetime'].astype(int)
    combined_df['datetime'] = combined_df['ref_datetime'] + pd.to_timedelta(combined_df['valid_datetime'], unit='H')

    # Set index and drop columns based on dataset type
    if dataset_type == 'solar':
        combined_df.set_index(['datetime', 'point', 'latitude', 'longitude'], inplace=True)
    elif dataset_type == 'wind':
        combined_df.set_index(['datetime', 'latitude', 'longitude'], inplace=True)

    combined_df = combined_df.drop(columns=['ref_datetime', 'valid_datetime']).add_suffix(suffix)

    # # Save the final DataFrame
    # combined_df.to_pickle(f"data/{dataset_type}{suffix}.pkl")

    return combined_df


def pivot_wider(df):
    df['point1'] = np.array([r[1] for r in df.index])
    new_df = pd.pivot_table(df, index='datetime', columns='point1', values=df.columns)
    return new_df


# def find_nearest(group, missing_coords, all_coords):
#     """
#     在同一时间戳下，找到离缺失数据最近的非空数据点。
#     group: 当前时间戳下的数据分组
#     missing_coords: 缺失数据点的经纬度
#     all_coords: 当前分组中所有数据点的经纬度
#     """
#     # 计算距离并找到最近的非空数据点
#     distances = cdist([missing_coords], all_coords)
#     nearest_idx = distances.argmin()

#     return group.iloc[nearest_idx]

# def fill_with_nearest(df):
#     # 对DataFrame按照时间戳分组
#     grouped = df.groupby(level=0)

#     # 初始化一个空的DataFrame用于保存结果
#     filled_df = pd.DataFrame()

#     # 遍历每个时间戳分组
#     for name, group in grouped:
#         # 获取该组内所有的经纬度
#         coords = group.index.get_level_values(1, 2).values  # 获取 latitude 和 longitude

#         # 找出缺失值的索引
#         missing_indices = group[group.isnull().any(axis=1)].index

#         # 对每个缺失值应用查找最近邻居并填充的逻辑
#         for idx in missing_indices:
#             nearest_row = find_nearest(group, coords[idx], coords)
#             df.loc[idx] = nearest_row

#         # 将填充后的数据追加到结果DataFrame
#         filled_df = filled_df.append(group)

#     return filled_df
# # 应用函数
# filled_df = fill_with_nearest(wind_dwd_df)
