# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:12:09 2023

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


option = st.selectbox(
    'Which number do you like best?',
     a.columns.tolist())

r1=a.groupby(option).size()

options1 = {
    "color":'#ff4060',
    "tooltip": {
  "trigger": 'axis',
  "axisPointer": {
    "type": 'shadow'
  }
},
    "xAxis": {
        "type": "category",
        "data": r1.index.tolist(),
        "axisTick": {"alignWithLabel": True},
    },
    "yAxis": {"type": "value"},
    "series": [
        {"data": r1.values.tolist(), "type": "bar"}
    ],
}
st_echarts(options=options1)


st.text_input("Your columns", key="columns")

# You can access the value at any point with:

if st.session_state.columns:
    r1=a.groupby(st.session_state.columns).size()
    
    options1 = {
        "color":'#ff4060',
        "tooltip": {
      "trigger": 'axis',
      "axisPointer": {
        "type": 'shadow'
      }
    },
        "xAxis": {
            "type": "category",
            "data": r1.index.tolist(),
            "axisTick": {"alignWithLabel": True},
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": r1.values.tolist(), "type": "bar"}
        ],
    }
    st_echarts(options=options1)



df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })


x = st.slider('x')#本质上实现了数据的传入
st.write(x, 'squared is', x * x)




if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data




a.iloc[0:3]
st.write(a.iloc[0:3])
#st.dataframe(a.loc[0:10,["price","itemid"]].style.highlight_max(axis=0))
#st.table(a.iloc[0:10])

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

b = (
    Bar()
    .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
    .add_yaxis(
        "2017-2018 Revenue in (billion $)", [21.2, 20.4, 10.3, 6.08, 4, 2.2]
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
        ),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
st_pyecharts(b)

options = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
    ],
}
st_echarts(options=options)

op1={
  "xAxis": {
    "type": 'category',
    "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "data": [820, 932, 901, 934, 1290, 1330, 1320],
      "type": 'bar',
      "smooth": True
    }
  ]
}
st_echarts(options=op1)