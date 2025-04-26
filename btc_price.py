import yfinance as yf
import pandas as pd

def fetch_btc_data():
    print("Fetching Bitcoin Price...")
    btc = yf.download("BTC-USD", period="max", interval="1h", auto_adjust=True)
    btc.to_csv("data/btc_prices.csv")