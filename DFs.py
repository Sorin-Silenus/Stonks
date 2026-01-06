import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

rets = yf.download(tickers=["SPYI", "VYM"], interval='1d')["Close"]

type(rets)
print(rets.head())