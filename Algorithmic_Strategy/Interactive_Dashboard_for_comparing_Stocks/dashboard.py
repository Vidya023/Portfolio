# streamlit run dashboard.py

import pandas as pd 
import yfinance as yf 
import streamlit as st 

st.title("Stock comparison Dashboard") 

tickers = ('TSLA','AAPL','MSFT','IBM','AMD','GOOGL')

dropdown = st.multiselect('Select assets', tickers) 

start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
end = st.date_input('End',value=pd.to_datetime('today'))

# defining a function to scale values in dataframe relatively
def cumulative_returns(df):
    rel = df.pct_change() 
    cumret = (1+rel).cumprod()-1
    cumret = cumret.fillna(0) 
    return cumret 

if len(dropdown)>0:
    df = cumulative_returns(yf.download(dropdown,start,end)['Adj Close']) 
    st.line_chart(df) 