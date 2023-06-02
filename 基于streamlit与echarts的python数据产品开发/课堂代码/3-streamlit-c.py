# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:02:27 2023

@author: wp
"""

import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np

a=pd.read_csv(r"D:\try\shoes.csv")
a.sales=a.sales.str.replace("人付款","").astype(int)


option4 = st.multiselect(
    'What are your favorite shopes',
    a.groupby("nick").size().sort_values(ascending=False).index,
    ['意尔康男鞋旗舰店'])

p1=a.groupby('info.鞋面材质').size().sort_values()
p1.name="all"

chart0 = {
  "yAxis": {
    "type": 'category',
    "data": p1.index.tolist()
  },
  "xAxis": {
    "type": 'value'
  },
  "legend": {},
  "series": [
      {
        "data": p1.values.tolist(),
        "type": 'bar',
        "name":"all"
      },
  ]
}

for i in option4:
    p2=a[a["nick"]==i].groupby('info.鞋面材质').size()
    p2.name=i
    p1=pd.concat([p1,p2],axis=1).fillna(0)
    chart0["series"].append({
      "data": p1[i].values.tolist(),
      "type": 'bar',
      "name": i
    })

st_echarts(chart0)

p1



option0 = st.selectbox(
    '选择鞋面材质',
     a["info.鞋面材质"].unique())
option1 = st.slider('price',0.,a.price.max()/4,(100.,300.))
option2 = st.slider('sales',0,a.sales.max(),(100,300))

option3 = st.multiselect(
    'What are your favorite colors',
    a.columns,
    ['nick','title','price', 'sales'])

a1=a[(a["info.鞋面材质"]==option0)&(a.price>option1[0])&(a.price<option1[1])
     &(a.sales>option2[0])&(a.sales<option2[1])][option3]

a1