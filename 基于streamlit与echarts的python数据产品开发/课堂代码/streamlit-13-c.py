# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:47:09 2023

@author: wp
"""

import streamlit as st 
import numpy as np 
import pandas as pd
import pickle

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score,confusion_matrix,f1_score

df=pd.read_csv(r"F:\notebooks1\streamlit\data\old.csv")
st.table(df.head())


df_copy=df.copy()
df_copy.drop(axis=1,columns="Name",inplace=True)
df_copy["Response"]=df_copy["Response"].map({"no":0,"yes":1})
df_copy=pd.get_dummies(df_copy,columns=["Gender","Area","Email","Mobile"])
st.table(df_copy.head())

y=df_copy["Response"].values
x=df_copy.drop(axis=1,columns="Response").values
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

with st.form("参数条件"):
   estimators_val = st.slider("estimators",2,200,10)
   max_depth_val = st.slider("max_depth",1,10,2)
   submitted = st.form_submit_button("Submit")
   
model=RandomForestClassifier(n_estimators=estimators_val,max_depth=max_depth_val, random_state=1234)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
st.table(confusion_matrix(y_test, y_pred))
st.write(f1_score(y_test, y_pred))
