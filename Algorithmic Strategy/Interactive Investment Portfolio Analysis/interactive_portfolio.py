import pandas as  pd 
import yfinance as yf 
import matplotlib.pyplot as plt 
import numpy as  np 
import streamlit as st 

st.title("Investment Portfolio Analysis - Dashboard") 

assets = st.text_input("Select assets", "AAPL, MSFT, GOOGL, AMD, IBM")

start = st.date_input("Select Start Date", value=pd.to_datetime('2022-01-01')) 

def calc(data):
    ret_df = data.pct_change() 
    cumul_ret = (ret_df+1).cumprod()-1
    pf_cumul_ret = cumul_ret.mean(axis=1) 
    weights = (np.ones(len(ret_df.cov()))/len(ret_df.cov())) 
    pf_std = (weights.dot(ret_df.cov()).dot(weights))**(1/2)
    return ret_df, cumul_ret, pf_cumul_ret, weights, pf_std  

def benchmrk():
    benchmark = yf.download('^GSPC',start=start)['Adj Close']
    bench_ret = benchmark.pct_change()
    bench_dev = (bench_ret+1).cumprod()-1
    return benchmark, bench_ret, bench_dev 

data = yf.download(assets,start=start)['Adj Close'] 

ret_df, cumul_ret, pf_cumul_ret, weights, pf_std = calc(data) 
benchmark, bench_ret, bench_dev = benchmrk() 

st.subheader('Portfolio vs. Index Development')

tog = pd.concat([bench_dev, pf_cumul_ret],axis=1)
tog.columns = ['S&P500 Performance','Portfolio Performance']

st.line_chart(data=tog) 

st.subheader("Portfolio Risk")
pf_std

st.subheader("Benchmark Risk:")
bench_risk = bench_ret.std()
bench_risk 

st.subheader("Portfolio Composition")

fig, ax = plt.subplots(facecolor='#121212')
ax.pie(weights, labels=data.columns, autopct='%1.1f%%', textprops={'color':'white'}) 

st.pyplot(fig) 