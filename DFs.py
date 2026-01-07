# File to test out some data frames with yfinance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


rets = yf.download(["SPYI", "VYM"], interval='1d')["Close"]

print(type(rets))
print(rets.head())

data = yf.Tickers("SPYI VYM SDY VXUS JEPI")
divs = {"SPYI" : data.tickers['SPYI'].dividends, 
        "VYM" : data.tickers['VYM'].dividends,
        "SDY" : data.tickers['SDY'].dividends,
        "VXUS" : data.tickers['VXUS'].dividends,
        "JEPI" : data.tickers['JEPI'].dividends}  

df = pd.DataFrame(divs).fillna(0).sort_index(ascending=False)
df_monthly = df.resample('M').sum().sort_index(ascending=False)
df_monthly.index = df_monthly.index.to_period("M")

print(df_monthly.head())

