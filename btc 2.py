import json
import pandas as pd
from pathlib import Path
from azure.storage.blob import BlockBlobService
from io import StringIO
import json
import numpy as np
from azure.cosmosdb.table.tableservice import TableService
from pathlib import Path
# from azure.storage.blob import BlockBlobService
from io import StringIO
from datetime import datetime
from dateutil import parser

# df = pd.read_csv("Binance_BTCUSDT_1h.csv")
def read_clean_data():
    df = pd.read_csv("Binance_BTCUSDT_minute.csv")
    df1= df.reset_index()
    df2 = df1.rename(columns = {'level_0': 'unix', 
                            'level_1': 'date',
                            'level_2':'symbol',
                            'level_3':'open',
                            'level_4':'high',
                            'level_5':'low',
                            'level_6':'close',
                            'level_7':'Volume_BTC',
                            'level_8':'Volume_USDT',
                            }, inplace = False)
    df2 = df2.drop(columns = ['https://www.CryptoDataDownload.com'])
    df3 = df2.drop([0])
    df3['date'] = pd.to_datetime(df3['date'], format='%Y-%m-%d %H:%M:%S')
    df3['open'] = df3['open'].astype(float)
    df3['high'] = df3['high'].astype(float)
    df3['low'] = df3['low'].astype(float)
    df3['close'] = df3['close'].astype(float)
    df3['Volume_BTC'] = df3['Volume_BTC'].astype(float)
    df3['Volume_USDT'] = df3['Volume_USDT'].astype(float)
    df3['open'] = df3['open'].round()
    df3['high'] = df3['high'].round()
    df3['low'] = df3['low'].round()
    df3['close'] = df3['close'].round()
    df3['Volume_BTC'] = df3['Volume_BTC'].round()
    df3['Volume_USDT'] = df3['Volume_USDT'].round()
    df3['open'] = df3['open'].astype(int)
    df3['high'] = df3['high'].astype(int)
    df3['low'] = df3['low'].astype(int)
    df3['close'] = df3['close'].astype(int)
    df3['Volume_BTC'] = df3['Volume_BTC'].astype(int)
    df3['Volume_USDT'] = df3['Volume_USDT'].astype(int)
    df3 = df3.drop(columns = ['unix'])
    rev = df3.iloc[::-1]
    rev['Perc_Change'] = rev['close'].pct_change()*100
    eda_df = rev.iloc[74: , :]
    eda_df = eda_df.reset_index(drop=True)
    return eda_df

def anal(eda_df):
    read_clean_data()
    df = eda_df[(eda_df['date'] > '2019-12-20 19:13:00') & (eda_df['date']<'2020-01-08 19:16:00')]
    df.time = pd.to_datetime(df.date, format="%Y-%m-%d %H:%M:%S")
    df = df.set_index("date")
    t = df.groupby(pd.Grouper(freq='15Min')).agg({"open": "first", 
                                            "close": "last", 
                                            "low": "min", 
                                            "high": "max"})
    t.columns = ["open", "close", "low", "high"]
    t['S/F'] = ''
    #Input in Percentage
    x = 5
    y = 3 
    for i,r in t.iterrows():
        x1 = r['close']
        t2 = t[i:]
        for index,row in t2.iterrows():
            x2 = row['close']
            if ((x2-x1)/x1)*100 > x:
                t['S/F'][i]='Success'
            elif ((x2-x1)/x1)*100 < -y:
                t['S/F'][i]='Failure'
    return t
