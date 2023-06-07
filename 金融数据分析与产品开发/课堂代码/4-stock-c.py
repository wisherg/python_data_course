# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 11:00:42 2023

@author: wp
"""

import matplotlib.pyplot as plt  
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
import scipy.optimize as sco

title = st.text_input('Movie title', '000413,000063,002007,000001,000002')
st.write('The current movie title is', title)

stock_set =title.split(",")

p0=ak.stock_zh_a_hist(symbol=stock_set[0], period="daily", start_date="20210201", end_date='20230201', 
                     adjust="hfq")[["日期","收盘"]]
p0.set_index("日期",inplace=True)

for i in stock_set[1:]:
    p1=ak.stock_zh_a_hist(symbol=i, period="daily", start_date="20210201", end_date='20230201', 
                     adjust="hfq")[["日期","收盘"]]
    p1.set_index("日期",inplace=True)
    p0=pd.concat([p0,p1],axis=1)

p0.columns=stock_set
p0=p0.fillna(method="ffill")

p0

r=(p0/p0.shift(1)-1).dropna()
r_log=np.log(p0/p0.shift(1)).dropna()

data=[]
for i in range(1000):
    w0=np.random.random(len(stock_set))
    w0=w0/np.sum(w0)
    r_n_0=np.dot(r_log,w0)
    data.append([r_n_0.std(),r_n_0.sum()])
    
def xiapu(w0):
    w0=w0/np.sum(w0)
    r_n_0=np.dot(r_log,w0)
    return r_n_0.std()/r_n_0.sum()

noa=len(stock_set)
#约束是所有参数(权重)的总和为1。这可以用minimize函数的约定表达如下
cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1})

#我们还将参数值(权重)限制在0和1之间。这些值以多个元组组成的一个元组形式提供给最小化函数
bnds = tuple((0,1) for x in range(noa))

#优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。我们简单的使用平均分布。
opts = sco.minimize(xiapu, noa*[1./noa,], method = 'SLSQP', bounds = bnds, constraints = cons)

r_n_0=np.dot(r_log,opts.x)

option = {
  "xAxis": {},
  "yAxis": {},
  "series": [
    {
      "symbolSize": 5,
      "data": data,
      "type": 'scatter'
    },
    {
      "symbolSize": 20,
      "data": [[r_n_0.std(),r_n_0.sum()]],
      "type": 'scatter'
    }
  ]
};

st_echarts(option)