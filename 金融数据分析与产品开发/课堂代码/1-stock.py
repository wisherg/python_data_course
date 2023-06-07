# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 23:08:25 2023

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

def kline_stock(x):
    stock_pinan = ak.stock_zh_a_hist(symbol=x, period="daily", start_date="20170301", end_date='20230207', adjust="")
    stock_pinan.set_index("日期",inplace=True)
    data1=stock_pinan.loc["2020-01-09":"2022-02-07",["开盘","收盘","最高","最低"]]
    y_SMA=talib.SMA(data1["收盘"],10)
    y_SMA20=talib.SMA(data1["收盘"],20)
    
    c1=Line()
    c1.add_xaxis(y_SMA.index.tolist())
    c1.add_yaxis("MA10",y_SMA.values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    
    c3=Line()
    c3.add_xaxis(y_SMA20.index.tolist())
    c3.add_yaxis("MA20",y_SMA20.values.tolist(),
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    
    c=Kline()
    c.add_xaxis(data1.index.tolist())
    c.add_yaxis("kline", data1.values.tolist(),itemstyle_opts=opts.ItemStyleOpts(color="pink", color0="black"),)
    c.set_global_opts(
            yaxis_opts=opts.AxisOpts(is_scale=True,splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(opacity=1)
                )),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="Kline-基本示例"),datazoom_opts=[opts.DataZoomOpts(type_="inside"),opts.DataZoomOpts(type_="slider")]
        )
    
    c2=c.overlap(c1)
    c4=c2.overlap(c3)
    
    return c4

st.text_input("stock_id", key="stock_id")
if st.session_state.stock_id:
    fig0=kline_stock(st.session_state.stock_id)
    st_pyecharts(fig0)