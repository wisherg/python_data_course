# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:21:17 2023

@author: wp
"""

import pandas as pd
import numpy as np
import streamlit as st
from streamlit_echarts import st_echarts


def leida():
    option = {
      "title": {
        "text": 'Basic Radar Chart'
      },
      "legend": {
      },
      "radar": {
        "indicator": [
          { "name": 'Age', "max": 100 },
          { "name": 'Logins 4 weeks', "max": 5 },
          { "name": 'Logins 6 months', "max": 7 },
          { "name": 'Sales 4 weeks', "max": 10 },
          { "name": 'Sales 6 months', "max": 30 },
          { "name": 'Sales total', "max": 50 }
        ]
      },
      "series": [
        {
          "name": 'Budget vs spending',
          "type": 'radar',
          "data": [
            {
              "value": tz.loc["no"].values.tolist(),
              "name": 'Allocated Budget'
            },
            {
              "value": tz.loc["yes"].values.tolist(),
              "name": 'Actual Spending'
            }
          ]
        }
      ]
    };
    
    return option

def pingxing():
    option = {
      "parallelAxis": [{'dim': 0, 'name': 'Age'},
 {'dim': 1, 'name': 'Logins 4 weeks'},
 {'dim': 2, 'name': 'Logins 6 months'},
 {'dim': 3, 'name': 'Sales 4 weeks'},
 {'dim': 4, 'name': 'Sales 6 months'},
 {'dim': 5, 'name': 'Sales total'}],
      "series": {
        "type": 'parallel',
        "lineStyle": {
          "width": 4
        },
        "data": [
          tz.loc["no"].values.tolist(),
          tz.loc["yes"].values.tolist(),
        ]
      }
    };
    return option


df=pd.read_csv(r"F:\notebooks1\streamlit\data\old.csv")

tz=df.pivot_table(index="Response")

st_echarts(leida())
st_echarts(pingxing())
