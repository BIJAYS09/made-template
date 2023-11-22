import pandas as pd
import os
from io import BytesIO
from zipfile import ZipFile
import requests
from kaggle.api.kaggle_api_extended import KaggleApi


def download_csv(save_path):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files("gautamchettiar/bitcoin-sentiment-analysis-twitter-data", 
                                      path=save_path, unzip=True)
    files = os.listdir(save_path)
    csv_file = [file for file in files if file.endswith('.csv')][0]
    df = pd.read_csv(os.path.join(save_path, csv_file),encoding='latin1')
    print(df.head())


    api.dataset_download_files("arslanr369/bitcoin-price-2014-2023", 
                                      path=save_path, unzip=True)
    files = os.listdir(save_path)
    csv_file = [file for file in files if file.endswith('.csv')][1]
    df = pd.read_csv(os.path.join(save_path, csv_file),encoding='latin1')
    print(df.head())

    

if __name__ == "__main__":
    
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    save_path = os.path.join(parent_dir,"data")

    download_csv(save_path)
