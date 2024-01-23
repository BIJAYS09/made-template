import pandas as pd
import zipfile
import os
from typing import Callable, Any
import urllib.request
from sqlalchemy import BIGINT, FLOAT, TEXT

def extractFiles(url: str, zipPath, filePath) -> str:
    urllib.request.urlretrieve(url, zipPath)
    with zipfile.ZipFile(zipPath, 'r') as zip_ref:
        zip_ref.extractall(filePath)
    
    return filePath

if __name__ == '__main__':
    zipUrl = 'https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip'
    file = 'data.csv'
    dataPath = extractFiles(zipUrl, zipPath="mowesta-dataset.zip", filePath = "data")
    df = pd.read_csv(os.path.join(dataPath, file),
                     sep=';',
                     index_col=False,
                     usecols=['Geraet', 'Hersteller', 'Model', 'Monat', 'Temperatur in °C (DWD)', 'Batterietemperatur in °C', 'Geraet aktiv'],
                     decimal=',')
    
    df.rename(columns={
        'Temperatur in °C (DWD)': 'Temperatur',
        'Batterietemperatur in °C':'Batterietemperatur'
        }, inplace=True)

    df.dropna(inplace=True)
    df["Temperatur"] = (df["Temperatur"] * 9/5) + 32
    df["Batterietemperatur"] = (df["Batterietemperatur"] * 9/5) + 32
    df = df[df["Geraet"] > 0]
    table = 'temperatures'
    database = 'temperatures.sqlite'
    df.to_sql(table, f'sqlite:///{database}', if_exists='replace', index=False, dtype={
        'Geraet': BIGINT,
        'Hersteller': TEXT,
        'Model': TEXT,
        'Monat': BIGINT,
        'Temperatur': FLOAT,
        'Batterietemperatur': FLOAT,
        'Geraet aktiv': TEXT
    })
    print('Sucessfull')