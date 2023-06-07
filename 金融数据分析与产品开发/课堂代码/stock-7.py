# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:15:34 2023

@author: wp
"""
import sqlite3
import pandas as pd  
import talib
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt
import akshare as ak
import numpy as np 
import streamlit as st
from streamlit_echarts import st_echarts
from pylab import mpl

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

@st.cache_data
def read_hq():
    stock_daily=pd.read_sql("select * from stock_daily where 股票代码>'003000.SZ'",con=conn)
    stock_daily.columns=['index', 'date', '股票代码', '股票简称', 'open', 'high', 'low', 'close', 'volume',
           '成交额(千元)', '换手率(%)', '量比', '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率',
           '市销率', '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)', '总股本(万股)', '流通股本(万股)',
           '总市值(万元)', '流通市值(万元)']
    stock_daily["date"]=stock_daily["date"].astype("str").astype("datetime64")
    stock_daily.set_index("date",inplace=True,drop=False)
    stock_daily["openinterest"]=0
    return stock_daily

def get_data_1(syboml):
    stock=stock_daily[stock_daily["股票代码"]==syboml][["open","high","low","close","volume","openinterest"]]
    stock=pd.concat([stock,z1],axis=1).fillna(method="bfill").fillna(method="ffill")
#    stock=pd.concat([get_data_0("003002.SZ"),z1],axis=1).fillna(method="bfill").fillna(method="ffill")
    return stock[["open","high","low","close","volume","openinterest"]]

class my_strategy_date_2(bt.Strategy):
    #全局设定交易策略的参数

    def __init__(self):
        # 初始化交易指令、买卖价格和手续费
        self.order = None

    def next(self):
        # 检查是否持仓 
        #print(str(self.datetime.date(0)))
        cash_value.update({str(self.datetime.date(0)):self.broker.getvalue()})
        if str(self.datetime.date(0)) in sell_date.keys(): # 没有持仓
            s_list=sell_date[str(self.datetime.date(0))]
            for i in s_list:
                self.order_target_percent(target=0,data=i)
        if str(self.datetime.date(0)) in buy_date.keys(): # 没有持仓
            s_list=buy_date[str(self.datetime.date(0))]
            for i in s_list:
                self.order_target_percent(target=0.9/len(s_list),data=i)
                

            
    def log(self, txt, dt=None):
        ''' 输出日志'''
        dt = dt or self.datas[0].datetime.date(0) # 拿现在的日期
        #st.write('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(f"""买入{order.data._name}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
            elif order.issell():
                self.log(f"""卖出{order.data._name}, 成交量{order.executed.size}，成交价{order.executed.price:.2f}""")
            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None

def huice_run_num(start,end,stock_list,strategy):

    cerebro = bt.Cerebro()
    for i in stock_list:
        stock=get_data_1(i)
        data = bt.feeds.PandasData(dataname=stock,fromdate=start,todate=end)           
        cerebro.adddata(data,name=i) 
        
    cerebro.addstrategy(strategy) 
    cerebro.broker.setcash(100000) 
    cerebro.broker.setcommission(commission=0.002) 


    st.write(start.date(),end.date())
    st.write('初始资金: %.2f' % cerebro.broker.getvalue())
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    results = cerebro.run()
    strat = results[0]
    st.write('最终资金: %.2f' % cerebro.broker.getvalue())
    st.write('夏普比率:', strat.analyzers.SharpeRatio.get_analysis())
    st.write('回撤指标:', strat.analyzers.DW.get_analysis())
    
    return cerebro

def line_cash(x):
    option = {
      "xAxis": {
        "type": 'category',
        "data": list(x.keys())
      },
      "yAxis": {
        "type": 'value'
      },
      "series": [
        {
          "data": list(x.values()),
          "type": 'line'
        }
      ]
    };
    return option

conn=sqlite3.connect(r'F:\量化金融\stock_2018.db')
stock_daily=read_hq()
n1=len(stock_daily.date.unique())
z1=pd.Series(range(0,n1),index=stock_daily.date.unique()).sort_index()

cash_value={}
start=datetime(2018,2,22)
end=datetime(2023,2,10)

# stock_list=["003002.SZ","003003.SZ","300001.SZ"]
# buy_date={"2020-09-22":["003002.SZ","003003.SZ"]}
# sell_date={"2023-02-02":["003002.SZ","003003.SZ"]}

st.markdown("## 单因子策略")

with st.form("my_form"):
   time_id_val = st.slider("单因子周期",4,100,30)
   columns_val=st.selectbox("选择因子",['volume','成交额(千元)', '换手率(%)', '量比', '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率',
          '市销率', '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)', '总股本(万股)', '流通股本(万股)',
          '总市值(万元)', '流通市值(万元)'],index=4)
   sort0=st.selectbox("选择排序方式",[False,True])
   first_num=st.slider("排名前几",2,100,5)
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        time_id=pd.Series(stock_daily.date.unique()).sort_values().tolist()[::time_id_val]
        buy_date={}
        sell_date={}
        postion=set([])
        stock_list=set([])
        for i in time_id:
            buy_list=stock_daily[stock_daily["date"]==i].sort_values(by=columns_val,ascending=sort0).head(first_num)["股票代码"].tolist()
            buy_date.update({str(i.date()):buy_list})
            sell_date.update({str(i.date()):list(postion-set(buy_list))})
            postion=set(buy_list)
            stock_list=stock_list|postion
        
        result=huice_run_num(start,end,stock_list,my_strategy_date_2)
        st_echarts(line_cash(cash_value))


st.markdown("## 多因子策略")

with st.form("my_form_muti"):
   time_id_muti_val = st.slider("多因子周期",4,100,30)
   columns_muti_val=st.multiselect("选择因子_muti",['volume','成交额(千元)', '换手率(%)', '量比', '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率',
          '市销率', '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)', '总股本(万股)', '流通股本(万股)',
          '总市值(万元)', '流通市值(万元)'],default=['总市值(万元)','市盈率(静态)'],max_selections=2)
   
   sort0_muti=st.selectbox("因子1排序方式",[False,True])
   sort1_muti=st.selectbox("因子2排序方式",[False,True])
   first_muti_num=st.slider("排名前几_muti",2,100,5)
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit_muti")
   if submitted:
        time_id=pd.Series(stock_daily.date.unique()).sort_values().tolist()[::time_id_muti_val]
        buy_date={}
        sell_date={}
        postion=set([])
        stock_list=set([])
        for i in time_id:
            
            factor1_stock=stock_daily[stock_daily["date"]==i].sort_values(by=columns_muti_val[0],ascending=sort0_muti)["股票代码"].tolist()
            factor2_stock=stock_daily[stock_daily["date"]==i].sort_values(by=columns_muti_val[1],ascending=sort1_muti)["股票代码"].tolist()
            f_1_df=pd.Series(range(1,len(factor1_stock)+1),index=factor1_stock)
            f_2_df=pd.Series(range(1,len(factor2_stock)+1),index=factor2_stock)
            f_1_2=pd.concat([f_1_df,f_2_df],axis=1)
            f_1_2[2]=f_1_2[0]+f_1_2[1]
            
            buy_list=f_1_2.sort_values(by=2).head(first_muti_num).index.tolist()
            buy_date.update({str(i.date()):buy_list})
            sell_date.update({str(i.date()):list(postion-set(buy_list))})
            postion=set(buy_list)
            stock_list=stock_list|postion
        
        result=huice_run_num(start,end,stock_list,my_strategy_date_2)
        st_echarts(line_cash(cash_value))