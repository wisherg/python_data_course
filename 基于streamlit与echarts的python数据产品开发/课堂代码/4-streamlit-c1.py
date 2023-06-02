# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:17:07 2023

@author: wp
"""
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np

#下面这行程序必须写入
st.markdown(" <style>iframe{ height: 300px !important } ", unsafe_allow_html=True)

a=pd.read_csv(r"D:\try\shoes.csv")
a.sales=a.sales.str.replace("人付款","").astype(int)
#求出各个商品的销售额并把它并入到原始数据框中去
z1=a.sales*a.price
z1.name="xse"
a1=pd.concat([a,z1],axis=1)#给序列命名之后添加入数据框就会直接以序列名作为列标

#先做成字典，把各个特征放入字典中
te_zheng={"nick":[],"z_xse":[],"z_num":[],"p_sales":[],"p_bdj":[],"p_price":[]}
for i in a1.groupby("nick"):
    te_zheng["nick"].append(i[0])
    te_zheng["z_xse"].append(i[1].xse.sum())
    te_zheng["z_num"].append(len(i[1]))
    te_zheng["p_sales"].append(round(i[1].sales.mean(),1))
    if i[1].sales.sum()==0:#存在除零的情况，所以做判断
        te_zheng["p_bdj"].append(0)
    else:
        te_zheng["p_bdj"].append(round(i[1].xse.sum()/i[1].sales.sum(),1))
    te_zheng["p_price"].append(round(i[1].price.mean(),1))

df_te_zheng=pd.DataFrame(te_zheng)
df_te_zheng.sort_values(by="z_xse",ascending=False,inplace=True)
df_te_zheng.set_index("nick",inplace=True)

df_te_zheng

option4 = st.sidebar.multiselect(
    'What are your favorite shopes',
    df_te_zheng.index,
    ['意尔康男鞋旗舰店'])



option = {
  "legend": {
    "data": option4
  },
  "radar": {
    "indicator": [
      { "name": 'z_xse', "max": df_te_zheng.loc[option4].z_xse.max() },
      { "name": 'z_num', "max": df_te_zheng.loc[option4].z_num.max() },
      { "name": 'p_sales', "max": df_te_zheng.loc[option4].p_sales.max() },
      { "name": 'p_bdj', "max": df_te_zheng.loc[option4].p_bdj.max() },
      { "name": 'p_price', "max": df_te_zheng.loc[option4].p_price.max() },
    ]
  },
  "series": [
    {
      "name": 'Budget vs spending',
      "type": 'radar',
      "data": [
      ]
    }
  ]
};

for i in option4:
    option["series"][0]["data"].append({
      "value": df_te_zheng.loc[i].tolist(),
      "name": i
    })
        

left_column, right_column = st.columns(2)

with left_column:
    st_echarts(option)
    
right_column.dataframe(df_te_zheng.loc[option4])

a_xm=a.groupby("info.鞋面材质").size()

def echart_shoes():
    return {
        "color":"red",
        "tooltip": {
          "trigger": 'axis',
          "axisPointer": {
            "type": 'shadow'
          }
        },
        "xAxis": {
            "type": "category",
            "data": a_xm.index.tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": a_xm.values.tolist(), "type": "line"}
        ],
    }

def echarts_random_options():
    return {
        "xAxis": {"type": "category", "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
        "yAxis": {"type": "value"},
        "series": [
            {"data": list(np.random.random(size=7) * 800),
             "type": "line"}
        ],
    }

option = {
  "xAxis": {
    "type": 'category',
    "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "data": [150, 230, 224, 218, 135, 147, 260],
      "type": 'line'
    }
  ]
};



with left_column:
    st_echarts(option)

with left_column:
    st_echarts(options=echart_shoes())


with right_column:
    st_echarts(options=echarts_random_options())