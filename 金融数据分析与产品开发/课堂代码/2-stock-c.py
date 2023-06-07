# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:30:39 2023

@author: wp
"""
import akshare as ak
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Kline
from pyecharts.charts import Line
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np
import talib


st.text_input("Your stockID", key="stockID")

# You can access the value at any point with:
if st.session_state.stockID:
    stock_liant = ak.stock_zh_a_hist(symbol=st.session_state.stockID, period="daily", start_date="20200301", end_date='20230207', adjust="")
    stock_liant.set_index("日期",inplace=True)
    y_SMA=talib.SMA(stock_liant["收盘"],10).fillna(0)
    y_SMA20=talib.SMA(stock_liant["收盘"],20).fillna(0)
    
    option1 = {
  "xAxis": {
    "data": stock_liant.index.tolist()
  },
  "yAxis": {},
  "dataZoom": [
    {
      "type": 'inside',
    },
    {
      "show": True,
      "type": 'slider',
    }
  ],
  "series": [
    {
      "type": 'candlestick',
      "data": stock_liant[["开盘","收盘","最高","最低"]].values.tolist()
    },
    {
      "type": 'line',
      "data": y_SMA.values.tolist()
    },
    {
      "type": 'line',
      "data": y_SMA20.values.tolist()
    },
  ]
}
    st_echarts(option1)
    
    c=Kline()
    c.add_xaxis(stock_liant.index.tolist())
    c.add_yaxis("kline", stock_liant[["开盘","收盘","最高","最低"]].values.tolist(),itemstyle_opts=opts.ItemStyleOpts(color="pink", color0="black"),)
    c.set_global_opts(
        yaxis_opts=opts.AxisOpts(is_scale=True,splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(opacity=1)
            )),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        title_opts=opts.TitleOpts(title="Kline-基本示例"),datazoom_opts=[opts.DataZoomOpts(type_="inside"),opts.DataZoomOpts(type_="slider")]
    )
    c.render_notebook()
    
    c3=Line()
    c3.add_xaxis(y_SMA20.index.tolist())
    c3.add_yaxis("MA20",y_SMA20.values.tolist(),
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    c3.render_notebook()
    
    c1=Line()
    c1.add_xaxis(y_SMA.index.tolist())
    c1.add_yaxis("MA10",y_SMA.values.tolist(),
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    c1.render_notebook()
    
    c2=c.overlap(c1)
    c4=c2.overlap(c3)
    
    st_pyecharts(c4)

    
    
