import os

import pandas as pd
import yfinance as yf


# write a function to check if the pickle file exists
# if it does, load the data from the pickle file
# if it doesn't, download the data from yfinance
# and save the data to a pickle file
# return the data
def get_stocks(start_date, end_date, output_dir):
    try:
        pkl_filepath = os.path.join(output_dir, "data.pkl")
        if not os.path.exists(pkl_filepath):
            df = download_stock_data(start_date, end_date)
            df.to_pickle(pkl_filepath)
        else:
            df = pd.read_pickle(pkl_filepath)
        return df
    except  Exception as ex:
        raise ValueError(f"error in getting stocks..{ex}")


def download_stock_data(start_date, end_date):
    # tickers = ["HDFCBANK.NS", "RELIANCE.NS", "CIPLA.NS", "DIVISLAB.NS", "HDFCLIFE.NS",
    #            "BHARTIARTL.NS", "ASIANPAINT.NS", "INFY.NS", "TITAN.NS", "HCLTECH.NS",
    #            "TATASTEEL.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "GRASIM.NS", "BPCL.NS",
    #            "BAJFINANCE.NS", "JSWSTEEL.NS", "ONGC.NS", "BAJAJFINSV.NS", "NTPC.NS"]
    # #  # # # Example list of Nifty 50 stock tickers
    tickers = ["HDFCBANK.NS", "RELIANCE.NS", "CIPLA.NS", "DIVISLAB.NS", "HDFCLIFE.NS",
               "BHARTIARTL.NS", "ASIANPAINT.NS", "INFY.NS", "TITAN.NS", "HCLTECH.NS",
               "TATASTEEL.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "GRASIM.NS", "BPCL.NS",
               "BAJFINANCE.NS", "JSWSTEEL.NS", "ONGC.NS", "BAJAJFINSV.NS", "NTPC.NS",
               "LT.NS", "HINDUNILVR.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "TATACONSUM.NS",
               "M&M.NS", "ULTRACEMCO.NS", "WIPRO.NS", "NESTLEIND.NS", "INDUSINDBK.NS",
               "EICHERMOT.NS", "SBILIFE.NS", "BRITANNIA.NS", "UPL.NS", "AXISBANK.NS",
               "APOLLOHOSP.NS", "ADANIPORTS.NS", "DRREDDY.NS", "SUNPHARMA.NS", "SBIN.NS",
               "MARUTI.NS", "POWERGRID.NS", "HINDALCO.NS", "TCS.NS", "HEROMOTOCO.NS",
               "COALINDIA.NS", "ITC.NS", "TECHM.NS", "SHREECEM.NS"]

    tickers.sort()
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
    return data
