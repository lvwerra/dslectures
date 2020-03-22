# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_core.ipynb (unless otherwise specified).

__all__ = ['get_dataset', 'rmse', 'convert_strings_to_categories']

# Cell
from nbdev.showdoc import *
import wget
import os
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from pandas.api.types import is_object_dtype, is_numeric_dtype

# Cell
def get_dataset(dataset_name: str):
    """
    Download datasets from Google Drive.
    """

    name_to_id = {
        "word2vec-google-news-300.pkl": "1dRwSXbFTcQbn8c3V24G92wFY4DXZ1SDt",
        "imdb.csv": "1wF0YEmQOwceJz2d6w4CfhBgydU87dPGl",
        "housing.csv": "1d7oOKdDmZFx8wf0c8OfuTW1FpUyJHABh",
        "housing_gmaps_data_raw.csv": "1R1RUHAXxzrIngRJMFwyp4vZRVICd-I6T",
        "housing_addresses.csv": "1mOK0uyRz5Zs-Qo7mVMlxwtb2xn1E6N9Q",
        "housing_merged.csv": "1bdYuBtIPrKiU-ut2MeSSsL47onPtZrRt",
        "housing_processed.csv": "12PxnWhPg_Pj0yx75vD22gwfdkkx80E6_"
    }

    path = '../data/'
    gdrive_path = "https://docs.google.com/uc?export=download&id="
    if dataset_name in name_to_id:
        if os.path.exists(path + dataset_name):
            print(f"Dataset already exists at '{path + dataset_name}' and is not downloaded again.")
            return
        try:
            file_url =  gdrive_path + name_to_id[dataset_name]
            wget.download(file_url, out=path)
        except Exception as e:
            print("Something went wrong during download. Try again.")
            raise e
        print(f"Download of {dataset_name} dataset complete.")
    else:
        raise KeyError("File not on Google Drive.")

# Cell
def rmse(y, yhat):
    """A utility function to calculate the Root Mean Square Error (RMSE).

    Args:
        y (array): Actual values for target.
        yhat (array): Predicted values for target.

    Returns:
        rmse (double): The RMSE.
    """
    return np.sqrt(mean_squared_error(y, yhat))

# Cell
def convert_strings_to_categories(df):
    """A utility function to convert all string columns to Categorical data type."""
    for col in df.columns:
        if is_object_dtype(df[col]):
            df[col] = df[col].astype("category")