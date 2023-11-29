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
    parts = value.split(":")
    if len(parts) < 3:
        return False
    if len(parts) >= 3 :
        first_part = parts[0]
        if len(first_part) !=2:
            return False
        for part in parts[1:]:
            if not part.isdigit():
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


