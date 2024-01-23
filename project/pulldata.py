import pandas as pd
import os
from io import BytesIO
from zipfile import ZipFile
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer



sid = SentimentIntensityAnalyzer()
def download_csv(save_path):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files("gautamchettiar/bitcoin-sentiment-analysis-twitter-data", 
                                      path=save_path, unzip=True)
    files = os.listdir(save_path)
    csv_file = [file for file in files if file.endswith('.csv')][0]
    df = pd.read_csv(os.path.join(save_path, csv_file),encoding='latin1')
    
    selected_columns = ['user_name', 'user_created', 'user_followers', 'user_friends', 'user_favourites', 
                        'date', 'text', 'is_retweet', 'cleanText', 'Polarity Score', 'sentiment']
    df = df[selected_columns]

    df['user_created'] = pd.to_datetime(df['user_created'], errors='coerce').dt.date
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df = df.dropna()

    nltk.download('vader_lexicon')
    scores = df['cleanText'].apply(get_sentiment_scores)
    print(scores.head().all)

    # api.dataset_download_files("arslanr369/bitcoin-price-2014-2023", 
    #                                   path=save_path, unzip=True)
    # files = os.listdir(save_path)
    # csv_file = [file for file in files if file.endswith('.csv')][1]
    # btc_data = pd.read_csv(os.path.join(save_path, csv_file),encoding='latin1')
    # print(btc_data.head())


    # #plot btc price vs closing
    # btc_data['Date'] = pd.to_datetime(btc_data['Date'])
    # btc_data.set_index('Date', inplace=True)
    # btc_data['Close'].plot(figsize=(10,5))
    # plt.title('BTC closingg price over time')
    # plt.xlabel('Date')
    # plt.ylabel('BTC price(USD)')
    # plt.show()



def get_sentiment_scores(text):
    scores = sid.polarity_scores(text)
    return scores

if __name__ == "__main__":
    
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    save_path = os.path.join(parent_dir,"data")

    download_csv(save_path)
