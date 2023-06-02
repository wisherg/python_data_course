# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 09:06:29 2023

@author: wp
"""
import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode
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

location=a1.location.str.split(" ",expand=True)
a1["province"]=location[0]
a1["city"]=location[1]
data0=[]
for i in a1.groupby("province").size().items():
    data0.append({"name":i[0],"value":i[1]})

def render_usa():

    with open(r"F:\notebooks1\streamlit\echarts-map-master\echarts-4.2.1-rc1-map\json\china.json", "r",encoding="utf-8") as f:
        map = Map(
            "USA",
            json.loads(f.read())
        )
    options = {
        "visualMap": {
            "left": "right",
            "min": 0,
            "max": 2500,
            "inRange": {
                "color": [
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "series": [
            {
                "name": "USA PopEstimates",
                "type": "map",
                "roam": True,
                "map": "USA",
                "emphasis": {"label": {"show": True}},
                "data": data0,
            }
        ],
    }
    st_echarts(options, map=map)


render_usa()