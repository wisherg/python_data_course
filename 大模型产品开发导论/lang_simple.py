
import streamlit as st
import numpy as np

import os
from langchain_community.llms import Tongyi
from langchain_community.llms import SparkLLM
from langchain_community.llms import QianfanLLMEndpoint

import pandas as pd
#导入模版
from langchain.prompts import PromptTemplate

#导入聊天模型
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain_community.chat_models import ChatSparkLLM
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.chat_models import QianfanChatEndpoint

#输入三个模型各自的key

os.environ["DASHSCOPE_API_KEY"] = "sk-39a2d85e79a5493a8859b60b725e5e55"

os.environ["IFLYTEK_SPARK_APP_ID"] = "8a0a858a"
os.environ["IFLYTEK_SPARK_API_KEY"] = "074dfcac2a41dae77ae98d8400dcca85"
os.environ["IFLYTEK_SPARK_API_SECRET"] = "YTk0M2Q1YzNmMTNjY2JkNGI1MWY5MDg2"

os.environ["QIANFAN_AK"] = "og6mWrRcqJqb1a8aiDl81tyC"
os.environ["QIANFAN_SK"] = "QV7NVmwMlXwoA67TOWu3lqP9gCujj0mk"

from operator import itemgetter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser



st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="📖")
st.title("📖 StreamlitChatMessageHistory")

model_ty = Tongyi(temperature=0)

if p_y :=st.chat_input():
    st.chat_message("user").write(p_y)
    res=model_ty(p_y)
    st.chat_message("AI").write(res)
