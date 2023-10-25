
def run_btc_analysis(analysis,x,y,from_date,to_date):
    import json
    import pandas as pd
    import json
    import numpy as np
    from dateutil import parser
    import datetime
    import numpy as np
    import matplotlib.pyplot as plt
    from pandas.plotting import scatter_matrix
    import plotly.express as px
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

    df = eda_df.copy()
    df.time = pd.to_datetime(df.date, format="%Y-%m-%d %H:%M:%S")
    df = df.set_index("date")
    t = df.groupby(pd.Grouper(freq='15Min')).agg({"open": "first", 
                                                "close": "last", 
                                                "low": "min", 
                                                "high": "max"})
    t.columns = ["open", "close", "low", "high"]
    print(t.shape)
    t['S/F'] = ''
    t['date2']=''
    t = t.reset_index()
    t = t.dropna(axis=0, subset=['close'])

    df = t[(t['date'] > from_date) & (t['date']<to_date)]
    print(df.shape)
    df = df.reset_index(drop=True)
    graph1 = df.copy()
    graph1.index = graph1['date']
    graph1['close'].plot(label = 'BTC/USDT', figsize = (23,10))
    plt.title('BTC Price Action')
    # #Input in Percentage
    if analysis == 'LONG':
        for i,r in df.iterrows():
            x1 = r['close']
            t2 = df[i:]
            for index,row in t2.iterrows():
                x2 = row['close']
                d2=row['date']
                percentage = ((x2-x1)/x1)*100
                if  percentage > x:
                    df['S/F'][i]='Success'
                    df['date2'][i]=d2
                    break
                elif percentage < -y:
                    df['S/F'][i]='Failure'
                    df['date2'][i]=d2
                    break
        df['date2'] = pd.to_datetime(df['date2'], format='%Y-%m-%d %H:%M:%S')
        df['time_taken']= ((df['date2']-df['date'])/np.timedelta64(1, 'm')).astype('float')
        print(df['S/F'].value_counts())
        graph = pd.DataFrame({'S/F': ['Success', 'Failure'],
                                'Count': [df[df['S/F']=='Success'].shape[0],df[df['S/F']=='Failure'].shape[0]]})
        graph.index = graph['S/F']
        fig_pie = px.pie(graph,values = 'Count',names = 'S/F',color='S/F',color_discrete_map={'Success':'palegreen',
                                        'Failure':'salmon',},
                                        title = 'LONG ANALYSIS: UP '+str(x)+'% (SUCCESS) DOWN '+str(y)+'% (FAILURE) for '+str(from_date)[0:10]+' to '+str(to_date)[0:10]
                                )
        fig_pie.show()
        graph_bar = pd.DataFrame({'S/F': ['Success', 'Failure'],
                                'Minutes': [df[df['S/F']=='Success']['time_taken'].describe()[5],df[df['S/F']=='Failure']['time_taken'].describe()[5]]})
        fig = px.bar(graph_bar, x="S/F", y="Minutes", color="S/F", title="Average Time taken for Success or Failure (minutes)",width=500,text='Minutes')
        fig.show()
    elif analysis == 'SHORT':
        for i,r in df.iterrows():
            x1 = r['close']
            t2 = df[i:]
            for index,row in t2.iterrows():
                x2 = row['close']
                d2=row['date']
                percentage = ((x2-x1)/x1)*100
                if  percentage > y:
                    df['S/F'][i]='Failure'
                    df['date2'][i]=d2
                    break
                elif percentage < -x:
                    df['S/F'][i]='Success'
                    df['date2'][i]=d2
                    break
        df['date2'] = pd.to_datetime(df['date2'], format='%Y-%m-%d %H:%M:%S')
        df['time_taken']= ((df['date2']-df['date'])/np.timedelta64(1, 'm')).astype('float')
        print(df['S/F'].value_counts())
        graph = pd.DataFrame({'S/F': ['Success', 'Failure'],
                                'Count': [df[df['S/F']=='Success'].shape[0],df[df['S/F']=='Failure'].shape[0]]})
        graph.index = graph['S/F']
        fig_pie = px.pie(graph,values = 'Count',names = 'S/F',color='S/F',color_discrete_map={'Success':'palegreen',
                                        'Failure':'salmon',
                                        'No Result':'lightskyblue',},
                                        title = 'SHORT ANALYSIS: DOWN '+str(x)+'% (SUCCESS) UP '+str(y)+'% (FAILURE) for '+str(from_date)[0:10]+' to '+str(to_date)[0:10]
                                )
        fig_pie.show()
        graph_bar = pd.DataFrame({'S/F': ['Success', 'Failure'],
                                'Minutes': [df[df['S/F']=='Success']['time_taken'].describe()[5],df[df['S/F']=='Failure']['time_taken'].describe()[5]]})
        fig = px.bar(graph_bar, x="S/F", y="Minutes", color="S/F", title="Average Time taken for Success or Failure (minutes)",width=500,text='Minutes')
        fig.show()

