import pandas as pd
import xarray as xr

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

    # Save the final DataFrame
    combined_df.to_pickle(f"data/{dataset_type}{suffix}.pkl")

    return combined_df