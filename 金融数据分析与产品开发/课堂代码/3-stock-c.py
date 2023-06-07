# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:27:33 2023

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

if st.session_state.stockID:
    stock_pinan = ak.stock_zh_a_hist(symbol=st.session_state.stockID, period="daily", start_date="20200301", end_date='20230207', adjust="")["收盘"]
    
    r_pinan=stock_pinan/stock_pinan.shift(1)-1
    r_pinan=r_pinan.dropna()
    
    st.line_chart(r_pinan)
    
    feng_xian=((r_pinan-r_pinan.mean())**2).mean()**0.5
    feng_xian
    
    xia_feng_xian=(((r_pinan[r_pinan<r_pinan.mean()]-r_pinan.mean())**2).sum()/len(r_pinan))**0.5
    xia_feng_xian
    
    hui_ce=stock_pinan.max()-stock_pinan.iloc[-1]
    hui_ce
    
    hui_ce_lv=(stock_pinan.max()-stock_pinan.iloc[-1])/stock_pinan.max()
    hui_ce_lv
