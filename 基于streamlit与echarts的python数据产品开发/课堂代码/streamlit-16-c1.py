# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:20:45 2023

@author: wp
"""

import pandas as pd
import numpy as np
import streamlit as st
from streamlit_echarts import st_echarts


def leida(data):
    
    zuobiao=[]
    for i in data.columns:
        zuobiao.append({"name":i,"max":tz[i].max()+2})
    
    option = {
      "title": {
        "text": 'Basic Radar Chart'
      },
      "legend": {
      },
      "radar": {
        "indicator": zuobiao
      },
      "series": [
        {
          "name": 'Budget vs spending',
          "type": 'radar',
          "data": [
            {
              "value": data.loc["no"].tolist(),
              "name": 'no'
            },
            {
              "value": data.loc["yes"].tolist(),
              "name": 'yes'
            }
          ]
        }
      ]
    };
    
    return option

def pingx(data):
    zuobiao=[]
    for i,j in enumerate(data.columns):
        zuobiao.append({"dim":i,"name":j})

    option = {
      "parallelAxis": zuobiao,
      "series": {
        "type": 'parallel',
        "lineStyle": {
          "width": 4
        },
        "data": [
          data.loc["no"].tolist(),
          data.loc["yes"].tolist(),
        ]
      }
    };
    return option


df=pd.read_csv(r"F:\notebooks1\streamlit\data\old.csv")
tz=df.pivot_table(index="Response")


st.table(tz)
st_echarts(leida(tz))
st_echarts(pingx(tz))