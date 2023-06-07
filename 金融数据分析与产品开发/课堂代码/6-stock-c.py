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
    cwzbsj.set_index("报告期",inplace=True,drop=False)
    return cwzbsj

@st.cache_data
def read_price():
    stock_daily=pd.read_sql("select * from stock_daily where 股票代码<'003000.SZ'",con=conn)
    stock_daily["交易日期"]=stock_daily["交易日期"].astype("str").astype("datetime64")
    stock_daily.set_index("交易日期",inplace=True)
    return stock_daily

@st.cache_data
def read_xx():
    stock_hy=pd.read_excel(r'G:\BaiduNetdiskDownload\上市公司基本信息列表\上市公司基本信息列表-20230217.xlsx')
    return stock_hy[["股票代码","二级行业"]]

cwzbsj=read_cw()
stock_daily=read_price()
stock_xx=read_xx()
cw_xx=pd.merge(cwzbsj,stock_xx,on="股票代码")

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

def line_hq_cw(index_id):
    
    data_cw1=cw_price[index_id[0]]
    data_cw2=cw_price[index_id[1]]

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data_cw1.index.tolist()]
      },
      "yAxis": [{
        "type": 'value'
      },{
        "type": 'value'
      },],
      "tooltip": {},
      "series": [
        {
          "data": data_cw1.tolist(),
          "type": 'line',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          }
        },
        {
          "data": data_cw2.tolist(),
          "type": 'line',
          "yAxisIndex":1
        }
      ]
    };
    
    return option

def line_muti(data):

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "legend":{},
      "tooltip": {},
      "series": [
      ]
    }
    for i in data.columns:
        option["series"].append({"data":data[i].tolist(),"type":"line","name":i})
          
        # {
        #   "data": data_cw1.tolist(),
        #   "type": 'line',
        #   "showBackground": True,
        #   "backgroundStyle": {
        #     "color": 'rgba(180, 180, 180, 0.2)'
        #   }
        # },
        # {
        #   "data": data_cw2.tolist(),
        #   "type": 'line',
        #   "yAxisIndex":1
        # }
    
    return option


def cw_muti_index(cw_index):
    st.title(cw_index)
    cw_xx_hy_pivot=cw_xx_hy.pivot(index="报告期",values=cw_index, columns='股票代码').fillna(-1)
    st_echarts(line_muti(cw_xx_hy_pivot))
    cw_xx_hy_pivot


choice2 = st.sidebar.selectbox('选择一个股票ID', ["000651.SZ","002594.SZ","000777.SZ","000800.SZ","000333.SZ","000338.SZ","000547.SZ","002595.SZ"])
st.title(choice2)
stock_cw=cwzbsj[cwzbsj["股票代码"]==choice2][['扣除非经常性损益后的净利润(扣非净利润)','净资产收益率(扣除非经常损益)','销售毛利率','销售净利率', '企业自由现金流量', '非经常性损益','净债务','每股净资产','每股营业总收入']]
stock_price_gl=stock_daily[stock_daily["股票代码"]==choice2][['收盘价', '成交量(手)','量比', '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率','市销率', '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)','总市值(万元)', '流通市值(万元)']]
stock_cw1=stock_cw.resample("d").bfill()
cw_price=pd.concat([stock_price_gl,stock_cw1],axis=1).dropna()
hy=stock_xx[stock_xx["股票代码"]==choice2].values[0,1]
cw_xx_hy=cw_xx[cw_xx["二级行业"]==hy]

st.sidebar.title("安全性指标")

agree0 = st.sidebar.checkbox('流动比率')

if agree0:
    cw_muti_index("流动比率")

agree1 = st.sidebar.checkbox('速动比率')

if agree1:
    cw_muti_index("速动比率")

agree0 = st.sidebar.checkbox('资产负债率')

if agree0:
    cw_muti_index("资产负债率")
    
agree0 = st.sidebar.checkbox('已获利息倍数(EBIT/利息费用)')

if agree0:
    cw_muti_index("已获利息倍数(EBIT/利息费用)")


choice1 = st.sidebar.selectbox('选择一个财务指标', stock_cw.columns)
choice3 = st.sidebar.selectbox('选择一个行情指标', stock_price_gl.columns)

choice4 = st.sidebar.multiselect(
    '选择两个指标',
    cw_price.columns,
    ['收盘价','销售毛利率'], max_selections=2)

st_echarts(bar_cw(choice1))
st_echarts(line_hq(choice3))
if len(choice4)==2:
    st_echarts(line_hq_cw(choice4))
st.table(stock_cw)