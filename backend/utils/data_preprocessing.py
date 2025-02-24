import os
import pandas as pd

def save_dataset_csv(df: pd.DataFrame, csv_path: str):
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        existing_df = pd.read_csv(csv_path)
        combined_df = pd.concat([existing_df, df])
        combined_df = combined_df.drop_duplicates(subset=["date", "stock_symbol"]).reset_index(drop=True)
        combined_df.to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, index=False)

def save_raw_data(df: pd.DataFrame, folder: str, filename: str):
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, filename)
    df.to_csv(path, index=False)
