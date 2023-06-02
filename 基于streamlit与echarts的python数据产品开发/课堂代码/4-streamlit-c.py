# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:17:31 2023

@author: wp
"""
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np
from PIL import Image

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

add_selectbox = st.sidebar.selectbox(
    '选择店铺',
    df_te_zheng.index
)

col51, col52, col53, col54,col55 = st.columns(5)

shop_0=df_te_zheng.loc[add_selectbox]

col51.metric(df_te_zheng.columns[0], shop_0.iloc[0], int(df_te_zheng.iloc[:,0].mean()))
col52.metric(df_te_zheng.columns[1], shop_0.iloc[1], int(df_te_zheng.iloc[:,1].mean()))
col53.metric(df_te_zheng.columns[2], shop_0.iloc[2], int(df_te_zheng.iloc[:,2].mean()))
col54.metric(df_te_zheng.columns[3], shop_0.iloc[3], int(df_te_zheng.iloc[:,3].mean()))
col55.metric(df_te_zheng.columns[4], shop_0.iloc[4], int(df_te_zheng.iloc[:,4].mean()))

df_te_zheng

col1, col2 = st.columns(2)

col1.subheader("aaa")
col1.image("http://abs.hznu.edu.cn/upload/resources/image/2022/11/28/7754685_500x500.png",
           caption='Sunrise by the mountains')
col2.subheader("aaa")
col2.image("http://abs.hznu.edu.cn/upload/resources/image/2022/11/28/7754686_500x500.png",
           caption='Sunrise by the mountains')

option4 = st.sidebar.multiselect(
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

option0 = st.sidebar.selectbox(
    '选择鞋面材质',
     a["info.鞋面材质"].unique())
option1 = st.sidebar.slider('price',0.,a.price.max()/4,(100.,300.))
option2 = st.sidebar.slider('sales',0,a.sales.max(),(100,300))

option3 = st.sidebar.multiselect(
    'What are your favorite colors',
    a.columns,
    ['nick','title','price', 'sales'])

a1=a[(a["info.鞋面材质"]==option0)&(a.price>option1[0])&(a.price<option1[1])
     &(a.sales>option2[0])&(a.sales<option2[1])][option3]

a1