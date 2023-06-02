# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:30:34 2023

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

def map_province(data0):
    with open(r"F:\notebooks1\streamlit\echarts-map-master\echarts-4.2.1-rc1-map\json\china.json", "r",encoding="utf-8") as f:
        map = Map(
            "china",
            json.loads(f.read())
        )
    
    options = {
        "tooltip": {
              "trigger": 'item',
              "showDelay": 0,
              "transitionDuration": 0.2,
            },
        "visualMap": {
            "show": False,
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
                "name": "商品数量地域分布",
                "type": "map",
                "roam": True,
                "map": "china",
                "emphasis": {"label": {"show": True}},
                "data": data0,
            }
        ],
    }
    
    events = {
    "click": "function(params) {return params.name }",
}
    
    return options,map,events


def map_city(province):
    
    data_city=[]
    for i in a[a["province"]==province].groupby("city").size().items():
        data_city.append({"name":i[0]+"市","value":i[1]})
        
    
    dir0="F:\\notebooks1\\streamlit\\echarts-map-master\\echarts-4.2.1-rc1-map\\json\\province\\"
    dir1=dir0+province_pinyin[province]+".json"
    with open(dir1, "r",encoding="utf-8") as f:
        map = Map(
            "zhejiang",
            json.loads(f.read())
        )
    
    options = {
        "tooltip": {
              "trigger": 'item',
              "showDelay": 0,
              "transitionDuration": 0.2,
            },
        "visualMap": {
            "show": False,
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
                "name": "商品数量地域分布",
                "type": "map",
                "roam": True,
                "map": "zhejiang",
                "emphasis": {"label": {"show": True}},
                "data": data_city,
            }
        ],
    }
    
    return options,map


a=pd.read_csv(r"D:\try\shoes.csv")
a.sales=a.sales.str.replace("人付款","").astype(int)
#求出各个商品的销售额并把它并入到原始数据框中去
z1=a.sales*a.price
z1.name="xse"
a=pd.concat([a,z1],axis=1)#给序列命名之后添加入数据框就会直接以序列名作为列标
location=a.location.str.split(" ",expand=True)
a["province"]=location[0]
a["city"]=location[1]


data_province=[]
for i in a.groupby("province").size().items():
    data_province.append({"name":i[0],"value":i[1]})

province_pinyin={"浙江":"zhejiang","福建":"fujian","安徽":"anhui"}

option_province, map_province,events_province=map_province(data_province)

province=st_echarts(option_province,map=map_province,events=events_province)

if province:
    pro=province
else:
    pro="浙江"

option_city, map_city=map_city(pro)

st_echarts(option_city,map=map_city)


