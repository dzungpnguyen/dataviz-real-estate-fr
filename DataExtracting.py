import pandas as pd

def read_data(filename):
  return pd.read_csv(filename)

def extract_sample(df, fraction):
  return df.sample(frac=fraction)

def extract_columns(df, list_cols):
  return df[list_cols]

def save_data(df, filename):
  new_df = df.copy()
  new_df.to_csv(filename)