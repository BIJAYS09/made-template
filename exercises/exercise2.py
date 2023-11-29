import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, BIGINT, TEXT, FLOAT, INTEGER

df = pd.read_csv("https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV",
                 sep=";", decimal=",")
df = df.drop(columns="Status")
df = df.drop(df[(df.Verkehr != "FV") & (df.Verkehr != "RV") & (df.Verkehr != "nur DPN")].index)
df = df.drop(df[(df.Laenge < -90) & (df.Laenge > 90)].index)
df = df.drop(df[(df.Breite < -90) & (df.Breite > 90)].index)

def isValid_IFOPT(value):
    if pd.isnull(value):
        return False
    data = value.split(":")
    if len(data) < 3:
        return False
    else:
        col1 = data[0]
        if len(col1) !=2:
            return False
        for reaminig_data in data[1:]:
            if not reaminig_data.isdigit():
                return False
    return True

df = df[df["IFOPT"].apply(isValid_IFOPT)]        
df = df.dropna()

sqlite_engine = create_engine("sqlite:///trainstops.sqlite")
data_types = {
    "EVA_NR": BIGINT, 
    "DS100": TEXT,   
    "IFOPT": TEXT,   
    "NAME": TEXT,   
    "Verkehr": TEXT,   
    "Laenge": FLOAT,  
    "Breite": FLOAT,  
    "Betreiber_Name": TEXT,  
    "Betreiber_Nr": INTEGER 
}

df.to_sql("trainstops", sqlite_engine, if_exists="replace", index=False, dtype=data_types)


