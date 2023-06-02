# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:26:26 2023

@author: wp
"""
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np

st.write('Hello,World!')

"fjdklafjdkls"

a=88

a

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)
st.table(dataframe)

a=pd.read_csv(r"D:\try\shoes.csv")

a.iloc[0:3]
st.write(a.iloc[0:3])
st.dataframe(a.loc[0:10,["price","itemid"]].style.highlight_max(axis=0))
st.table(a.iloc[0:10])