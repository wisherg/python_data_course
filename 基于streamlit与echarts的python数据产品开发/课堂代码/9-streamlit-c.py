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

def paleituo(xse,xse_cum):
    option = {
      "xAxis": {
        "type": 'category',
        "data": [0]+xse.index.tolist()
      },
      "yAxis": [
          {
        "type":'value'
      },          
        {
              "type":'value'
            }
        ],
      "legend":{},
      "series": [
        {
          "data": [0]+xse.tolist(),
          "type": 'bar',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          },
          "name":"xse"
        },
        {
          "data": [0]+xse_cum.tolist(),
          "type": 'line',
          "yAxisIndex": 1,
          "name":"xse_cum"
        }
      ]
    };
    
    return option

def price_sales(d1,d2):
    option = {
      "xAxis": {
          "min":0,
          "max":700
          },
      "yAxis": [{"splitLine":False},{}],
      "legend":{},
      "series": [
        {
          "data": d1,
          "type": 'line',
          "name":"销量",

        },
        {
          "data": d2,
          "type": 'line',
          "yAxisIndex": 1,
          "name":"商品数"
        },
      ]
    };
        
    return option

def tz_pie(data):
    option = {
      "tooltip": {
        "trigger": 'item'
      },
      "legend": {
        "top": '5%',
        "x":"left",
        "orient": 'vertical',
      },
      "series": [
        {
          "name": '类别销量',
          "type": 'pie',
          "radius": ['40%', '70%'],
          "avoidLabelOverlap": False,
          "itemStyle": {
            "borderRadius": 10,
            "borderColor": '#fff',
            "borderWidth": 2
          },
          "label": {
            "show": False,
            "position": 'center'
          },
          "emphasis": {
            "label": {
              "show": True,
              "fontSize": 40,
              "fontWeight": 'bold'
            }
          },
          "labelLine": {
            "show": True
          },
          "data": data
        }
      ]
    };
        
    return option

st.set_page_config(page_title="男鞋", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>意尔康男鞋数据分析</h1>", unsafe_allow_html=True)

bg_img="""
<style>
[data-testid="stAppViewContainer"]{ 
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url("data:image/svg+xml;utf8,%3Csvg viewBox=%220 0 2000 1000%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cmask id=%22b%22 x=%220%22 y=%220%22 width=%222000%22 height=%221000%22%3E%3Cpath fill=%22url(%23a)%22 d=%22M0 0h2000v1000H0z%22%2F%3E%3C%2Fmask%3E%3Cpath fill=%22%23000336%22 d=%22M0 0h2000v1000H0z%22%2F%3E%3Cg style=%22transform-origin:center center%22 stroke=%22%234c4e72%22 stroke-width=%222%22 mask=%22url(%23b)%22%3E%3Cpath fill=%22%234c4e7236%22 d=%22M0 0h100v100H0z%22%2F%3E%3Cpath fill=%22none%22 d=%22M100 0h100v100H100zM200 0h100v100H200zM300 0h100v100H300zM400 0h100v100H400z%22%2F%3E%3Cpath fill=%22%234c4e72db%22 d=%22M500 0h100v100H500z%22%2F%3E%3Cpath fill=%22none%22 d=%22M600 0h100v100H600zM700 0h100v100H700zM800 0h100v100H800zM900 0h100v100H900zM1000 0h100v100h-100zM1100 0h100v100h-100zM1200 0h100v100h-100zM1300 0h100v100h-100zM1400 0h100v100h-100zM1500 0h100v100h-100zM1600 0h100v100h-100zM1700 0h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72a3%22 d=%22M1800 0h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1900 0h100v100h-100zM0 100h100v100H0z%22%2F%3E%3Cpath fill=%22%234c4e72e8%22 d=%22M100 100h100v100H100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M200 100h100v100H200zM300 100h100v100H300zM400 100h100v100H400z%22%2F%3E%3Cpath fill=%22%234c4e7216%22 d=%22M500 100h100v100H500z%22%2F%3E%3Cpath fill=%22none%22 d=%22M600 100h100v100H600z%22%2F%3E%3Cpath fill=%22%234c4e72be%22 d=%22M700 100h100v100H700z%22%2F%3E%3Cpath fill=%22none%22 d=%22M800 100h100v100H800zM900 100h100v100H900zM1000 100h100v100h-100zM1100 100h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72f8%22 d=%22M1200 100h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1300 100h100v100h-100zM1400 100h100v100h-100zM1500 100h100v100h-100zM1600 100h100v100h-100zM1700 100h100v100h-100zM1800 100h100v100h-100zM1900 100h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72f3%22 d=%22M0 200h100v100H0z%22%2F%3E%3Cpath fill=%22none%22 d=%22M100 200h100v100H100zM200 200h100v100H200z%22%2F%3E%3Cpath fill=%22%234c4e726d%22 d=%22M300 200h100v100H300z%22%2F%3E%3Cpath fill=%22%234c4e7275%22 d=%22M400 200h100v100H400z%22%2F%3E%3Cpath fill=%22none%22 d=%22M500 200h100v100H500zM600 200h100v100H600z%22%2F%3E%3Cpath fill=%22%234c4e72ab%22 d=%22M700 200h100v100H700z%22%2F%3E%3Cpath fill=%22none%22 d=%22M800 200h100v100H800zM900 200h100v100H900zM1000 200h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72a7%22 d=%22M1100 200h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1200 200h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72df%22 d=%22M1300 200h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1400 200h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7299%22 d=%22M1500 200h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72c5%22 d=%22M1600 200h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7248%22 d=%22M1700 200h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1800 200h100v100h-100zM1900 200h100v100h-100zM0 300h100v100H0z%22%2F%3E%3Cpath fill=%22%234c4e724c%22 d=%22M100 300h100v100H100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M200 300h100v100H200zM300 300h100v100H300z%22%2F%3E%3Cpath fill=%22%234c4e72a7%22 d=%22M400 300h100v100H400z%22%2F%3E%3Cpath fill=%22%234c4e722c%22 d=%22M500 300h100v100H500z%22%2F%3E%3Cpath fill=%22none%22 d=%22M600 300h100v100H600zM700 300h100v100H700zM800 300h100v100H800zM900 300h100v100H900z%22%2F%3E%3Cpath fill=%22%234c4e722d%22 d=%22M1000 300h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1100 300h100v100h-100zM1200 300h100v100h-100zM1300 300h100v100h-100zM1400 300h100v100h-100zM1500 300h100v100h-100zM1600 300h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72ce%22 d=%22M1700 300h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1800 300h100v100h-100zM1900 300h100v100h-100zM0 400h100v100H0zM100 400h100v100H100zM200 400h100v100H200zM300 400h100v100H300zM400 400h100v100H400zM500 400h100v100H500zM600 400h100v100H600z%22%2F%3E%3Cpath fill=%22%234c4e7211%22 d=%22M700 400h100v100H700z%22%2F%3E%3Cpath fill=%22none%22 d=%22M800 400h100v100H800zM900 400h100v100H900zM1000 400h100v100h-100zM1100 400h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7286%22 d=%22M1200 400h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1300 400h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e721d%22 d=%22M1400 400h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7246%22 d=%22M1500 400h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72ce%22 d=%22M1600 400h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1700 400h100v100h-100zM1800 400h100v100h-100zM1900 400h100v100h-100zM0 500h100v100H0zM100 500h100v100H100zM200 500h100v100H200zM300 500h100v100H300zM400 500h100v100H400z%22%2F%3E%3Cpath fill=%22%234c4e727b%22 d=%22M500 500h100v100H500z%22%2F%3E%3Cpath fill=%22none%22 d=%22M600 500h100v100H600z%22%2F%3E%3Cpath fill=%22%234c4e721e%22 d=%22M700 500h100v100H700z%22%2F%3E%3Cpath fill=%22none%22 d=%22M800 500h100v100H800zM900 500h100v100H900zM1000 500h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e725d%22 d=%22M1100 500h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1200 500h100v100h-100zM1300 500h100v100h-100zM1400 500h100v100h-100zM1500 500h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72da%22 d=%22M1600 500h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1700 500h100v100h-100zM1800 500h100v100h-100zM1900 500h100v100h-100zM0 600h100v100H0zM100 600h100v100H100zM200 600h100v100H200z%22%2F%3E%3Cpath fill=%22%234c4e7264%22 d=%22M300 600h100v100H300z%22%2F%3E%3Cpath fill=%22none%22 d=%22M400 600h100v100H400zM500 600h100v100H500zM600 600h100v100H600zM700 600h100v100H700zM800 600h100v100H800z%22%2F%3E%3Cpath fill=%22%234c4e72fe%22 d=%22M900 600h100v100H900z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1000 600h100v100h-100zM1100 600h100v100h-100zM1200 600h100v100h-100zM1300 600h100v100h-100zM1400 600h100v100h-100zM1500 600h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72c4%22 d=%22M1600 600h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7212%22 d=%22M1700 600h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1800 600h100v100h-100zM1900 600h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7286%22 d=%22M0 700h100v100H0z%22%2F%3E%3Cpath fill=%22none%22 d=%22M100 700h100v100H100zM200 700h100v100H200z%22%2F%3E%3Cpath fill=%22%234c4e723c%22 d=%22M300 700h100v100H300z%22%2F%3E%3Cpath fill=%22%234c4e726e%22 d=%22M400 700h100v100H400z%22%2F%3E%3Cpath fill=%22none%22 d=%22M500 700h100v100H500z%22%2F%3E%3Cpath fill=%22%234c4e7283%22 d=%22M600 700h100v100H600z%22%2F%3E%3Cpath fill=%22none%22 d=%22M700 700h100v100H700zM800 700h100v100H800z%22%2F%3E%3Cpath fill=%22%234c4e722b%22 d=%22M900 700h100v100H900z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1000 700h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e720b%22 d=%22M1100 700h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1200 700h100v100h-100zM1300 700h100v100h-100zM1400 700h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7209%22 d=%22M1500 700h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72dd%22 d=%22M1600 700h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1700 700h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e720c%22 d=%22M1800 700h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1900 700h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7226%22 d=%22M0 800h100v100H0z%22%2F%3E%3Cpath fill=%22none%22 d=%22M100 800h100v100H100zM200 800h100v100H200zM300 800h100v100H300zM400 800h100v100H400zM500 800h100v100H500zM600 800h100v100H600zM700 800h100v100H700zM800 800h100v100H800zM900 800h100v100H900zM1000 800h100v100h-100zM1100 800h100v100h-100zM1200 800h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72c7%22 d=%22M1300 800h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72bf%22 d=%22M1400 800h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1500 800h100v100h-100zM1600 800h100v100h-100zM1700 800h100v100h-100zM1800 800h100v100h-100zM1900 800h100v100h-100zM0 900h100v100H0zM100 900h100v100H100z%22%2F%3E%3Cpath fill=%22%234c4e7203%22 d=%22M200 900h100v100H200z%22%2F%3E%3Cpath fill=%22none%22 d=%22M300 900h100v100H300z%22%2F%3E%3Cpath fill=%22%234c4e7217%22 d=%22M400 900h100v100H400z%22%2F%3E%3Cpath fill=%22%234c4e720f%22 d=%22M500 900h100v100H500z%22%2F%3E%3Cpath fill=%22none%22 d=%22M600 900h100v100H600zM700 900h100v100H700zM800 900h100v100H800z%22%2F%3E%3Cpath fill=%22%234c4e727a%22 d=%22M900 900h100v100H900z%22%2F%3E%3Cpath fill=%22%234c4e72c9%22 d=%22M1000 900h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7262%22 d=%22M1100 900h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e7215%22 d=%22M1200 900h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e720c%22 d=%22M1300 900h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e729e%22 d=%22M1400 900h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1500 900h100v100h-100zM1600 900h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e721f%22 d=%22M1700 900h100v100h-100z%22%2F%3E%3Cpath fill=%22none%22 d=%22M1800 900h100v100h-100z%22%2F%3E%3Cpath fill=%22%234c4e72ad%22 d=%22M1900 900h100v100h-100z%22%2F%3E%3C%2Fg%3E%3Cdefs%3E%3CradialGradient id=%22a%22%3E%3Cstop offset=%220%22 stop-color=%22%23fff%22%2F%3E%3Cstop offset=%221%22 stop-color=%22%23fff%22 stop-opacity=%220%22%2F%3E%3C%2FradialGradient%3E%3C%2Fdefs%3E%3C%2Fsvg%3E");
}
[data-testid="stHeader"]{
    background-color:rgba(0, 0, 0, 0)
    }
[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: white;
}
[data-testid="stMarkdownContainer"]{
    color: white;
    }
</style>
 """
#background-image: url(./背景2.png)
st.markdown(bg_img, unsafe_allow_html=True)

a=pd.read_csv(r"D:\try\shoes.csv")
a.sales=a.sales.str.replace("人付款","").astype(int)
#求出各个商品的销售额并把它并入到原始数据框中去
z1=a.sales*a.price
z1.name="xse"
a=pd.concat([a,z1],axis=1)#给序列命名之后添加入数据框就会直接以序列名作为列标
location=a.location.str.split(" ",expand=True)
a["province"]=location[0]
a["city"]=location[1]

nick_xse=a.groupby("nick").xse.sum().sort_values(ascending=False)
nick_xse=nick_xse[nick_xse>10000]
nick_xse_cum=nick_xse.cumsum()/nick_xse.sum()

y1,x1=np.histogram(a.price.values,np.linspace(a.price.min(),a.price.max(),500),weights=a.sales.values)#商品销量
y2,x2=np.histogram(a.price.values,np.linspace(a.price.min(),a.price.max(),500))#商品数量
data1=[]
for i in range(0,len(y1)):
    data1.append([x1[i],int(y1[i])])
data2=[]
for i in range(0,len(y2)):
    data2.append([x2[i],int(y2[i])])


shoe_xm=a.groupby('info.鞋面材质').xse.sum().sort_values(ascending=False)[0:6]
shoe_fg=a.groupby('info.风格').xse.sum().sort_values(ascending=False)[0:6]
shoe_lx=a.groupby('info.流行元素').xse.sum().sort_values(ascending=False)[0:6]

data_xm=[]
for i in shoe_xm.items():
    data_xm.append({"value":i[1],"name":i[0]})
data_fg=[]
for i in shoe_fg.items():
    data_fg.append({"value":i[1],"name":i[0]})
data_lx=[]
for i in shoe_lx.items():
    data_lx.append({"value":i[1],"name":i[0]})

data_province=[]
for i in a.groupby("province").size().items():
    data_province.append({"name":i[0],"value":i[1]})

province_pinyin={"浙江":"zhejiang","福建":"fujian","安徽":"anhui"}

c41,c42,c43,c44=st.columns(4)
c31,c32,c33=st.columns([1,2,1])
c21,c22=st.columns(2)

c41.metric("商品数",len(a))
c42.metric("店铺数",len(a.nick.unique()))
c43.metric("销售额",round(a.xse.sum()))
c44.metric("笔单价",round(a.xse.sum()/a.sales.sum()))

with c31:
    st_echarts(tz_pie(data_lx),theme='dark')
    st_echarts(tz_pie(data_fg),theme='dark')

with c32:
    option_province, map_province0,events_province=map_province(data_province)
    province=st_echarts(option_province,map=map_province0,events=events_province, height=620, width=600,theme='dark')

with c33:
    if province:
        pro=province
    else:
        pro="浙江"
    option_city, map_city0=map_city(pro)
    st_echarts(option_city,map=map_city0,theme='dark')
    st_echarts(tz_pie(data_xm),theme='dark')

with c21:
    st_echarts(paleituo(nick_xse,nick_xse_cum),theme='dark')
with c22:
    st_echarts(price_sales(data1,data2),theme='dark')

