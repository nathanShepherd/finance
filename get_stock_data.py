import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import yfinance as yf

plt.style.use('ggplot') 

def get_year_stock(ticker='TSLA'):

    # Specify date range
    start = dt.datetime(2020, 1, 1)
    end = dt.datetime.now()

    # Get Stock Data in date range
    tickerData = yf.Ticker(ticker)
    df = tickerData.history(period='1d', start=start, end=end)

    # Select columns from raw data
    columns = ['Open', 'Close']# 'Volume', 'High', 'Low', 
    df = df[columns] 
    df = df.interpolate()
    #print(df.tail())
    return df

def volatility(df):
    # Compute coef of variance to determine volatility
    coef_var = df.std() / df.mean()
    return coef_var

def recent_concavity(df):
    # Returns if price trend is up or down
    degree = 2
    num_days_past = 5
    x = np.arange(0, num_days_past)
    price = df.iloc[-num_days_past:]
    coef_fit = np.polyfit(x, price, degree)

    # If regressor for x^2 is positive
    # price change has upward concavity
    return coef_fit[0]
    

investments = ['DAR', 'SNAP', 'VOO', 'TSLA', 'VTWO',
               'WPX', 'DE', 'GOOG', 'GPRO', 'TGNA',
               'PYPL', 'DRI', 'IDXX', 'GS', 'CAT',
               'FB', 'BAC', 'PEP', 'PSEC', 'PAYX',]
risk_df = pd.DataFrame(columns=['tick', 'coef_var', 'concave'])

for i, tick in enumerate(investments):
    historical_data = get_year_stock(tick).mean(axis=1)

    vola = volatility(historical_data)
    conc = recent_concavity(historical_data)
    risk_df.loc[i] = [tick, vola, conc]
    
risk_df.dropna(inplace=True)

print(risk_df.sort_values('coef_var'))

risk_df[['tick', 'coef_var']].plot.hist()







