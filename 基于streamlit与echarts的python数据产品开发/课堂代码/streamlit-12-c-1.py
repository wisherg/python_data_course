# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:14:13 2023

@author: wp
"""

import streamlit as st 
import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

choice = st.sidebar.selectbox('选择一个数据', ["iris","wine","breast_cancer"])

if choice == "iris":
    data = datasets.load_iris()
elif choice == 'wine':
    data = datasets.load_wine()
elif choice == 'breast_cancer':
    data = datasets.load_breast_cancer()

#data = datasets.load_wine()
#data = datasets.load_breast_cancer()

x = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1234)


choice0 = st.sidebar.selectbox('选择一个模型', ["RandomForest","SVC","KNeighborsClassifier"])

if choice0 == "RandomForest":
    model=RandomForestClassifier(n_estimators=50,max_depth=3, random_state=1234)
elif choice0 == 'SVC':
    model=SVC(C=2)
elif choice0 == 'KNeighborsClassifier':
    model = KNeighborsClassifier(n_neighbors=4)

#model=SVC(C=2)
#model = KNeighborsClassifier(n_neighbors=4)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

acc

