# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:58:34 2023

@author: wp
"""
import json
from streamlit_echarts import JsCode
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import numpy as np
from PIL import Image
import sqlite3
import talib
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt
import akshare as ak

conn=sqlite3.connect(r'F:\量化金融\stock_2018.db')

@st.cache_data
def read_cw():
    cwzbsj=pd.read_sql("select * from cwzbsj",con=conn)
    cwzbsj["报告期"]=cwzbsj["报告期"].astype("str").astype("datetime64")
    cwzbsj.set_index("报告期",inplace=True)
    return cwzbsj

@st.cache_data
def read_price():
    stock_daily=pd.read_sql("select * from stock_daily where 股票代码<'003000.SZ'",con=conn)
    stock_daily["交易日期"]=stock_daily["交易日期"].astype("str").astype("datetime64")
    stock_daily.set_index("交易日期",inplace=True)
    return stock_daily

cwzbsj=read_cw()
stock_daily=read_price()

def bar_cw(index_id):
    
    data_cw=stock_cw[index_id]

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data_cw.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "tooltip": {},
      "series": [
        {
          "data": data_cw.tolist(),
          "type": 'bar',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          }
        }
      ]
    };
    
    return option

def line_hq(index_id):
    
    data_cw=stock_price_gl[index_id]

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data_cw.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "tooltip": {},
      "series": [
        {
          "data": data_cw.tolist(),
          "type": 'line',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          }
        }
      ]
    };
    
    return option


choice2 = st.sidebar.selectbox('选择一个股票ID', ["000651.SZ","002594.SZ","000777.SZ","000800.SZ","000333.SZ","000338.SZ","000547.SZ","002595.SZ"])
st.title(choice2)
stock_cw=cwzbsj[cwzbsj["股票代码"]==choice2][['扣除非经常性损益后的净利润(扣非净利润)','净资产收益率(扣除非经常损益)','销售毛利率','销售净利率', '企业自由现金流量', '非经常性损益','净债务','每股净资产']]
stock_price_gl=stock_daily[stock_daily["股票代码"]==choice2][['收盘价', '成交量(手)','量比', '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率','市销率', '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)','总市值(万元)', '流通市值(万元)']]

choice1 = st.sidebar.selectbox('选择一个财务指标', stock_cw.columns)
choice3 = st.sidebar.selectbox('选择一个行情指标', stock_price_gl.columns)



st_echarts(bar_cw(choice1))
st_echarts(line_hq(choice3))

st.table(stock_cw)