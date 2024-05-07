
import streamlit as st
import os
from langchain_community.llms import Tongyi

os.environ["DASHSCOPE_API_KEY"] = ""

st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="📖")
st.title("📖 StreamlitChatMessageHistory")

model_ty = Tongyi(temperature=0)

if p_y :=st.chat_input():
    st.chat_message("user").write(p_y)
    res=model_ty(p_y)
    st.chat_message("AI").write(res)
