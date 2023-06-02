# -*- coding: utf-8 -*-
"""
Created on Sat May  6 09:05:53 2023

@author: wp
"""

from pyecharts.faker import Faker
import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Line, Pie, Bar
import pandas as pd
import numpy as np

a=pd.read_csv(r"D:\try\shoes.csv")
a.sales=a.sales.str.replace("人付款","").astype(int)
#求出各个商品的销售额并把它并入到原始数据框中去
z1=a.sales*a.price
z1.name="xse"
a=pd.concat([a,z1],axis=1)#给序列命名之后添加入数据框就会直接以序列名作为列标
location=a.location.str.split(" ",expand=True)
a["province"]=location[0]
a["city"]=location[1]


# This will get the value of the slider widget

if 'count' not in st.session_state:
    st.session_state['count'] = 4

container = st.container()

st.write('Count = ', st.session_state['count'])

with container:
    increment = st.button('Increment')
    if increment:
        st.session_state['count'] += 1
    decrement = st.button('Decrement')
    if decrement:
        st.session_state['count'] -= 1

if st.checkbox("show_data"):
    st.table(a[['info.鞋面材质','info.风格',
           'nick', 'price', 'sales','xse', 'province',
           'city']].head(st.session_state['count']))

if 'leibie' not in st.session_state:
    st.session_state['leibie'] = "类别"

column_leibie={"类别":['info.鞋面材质','info.风格','province'],"数值":['price', 'sales','xse']}

st.session_state['leibie'] = st.radio(
    "What\'s your favorite movie genre",
    ("类别","数值"))

option = st.selectbox(
    'How would you like to be contacted?',
    column_leibie[st.session_state['leibie']])





st.write('Count = ', st.session_state['count'])