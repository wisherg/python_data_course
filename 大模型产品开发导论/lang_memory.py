
import streamlit as st
import os
from langchain_community.llms import Tongyi
#导入模版
from langchain.prompts import PromptTemplate
#输入三个模型各自的key

os.environ["DASHSCOPE_API_KEY"] = ""


from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="📖")
st.title("📖 StreamlitChatMessageHistory")

if 'history' not in st.session_state:
    st.session_state['history'] = ConversationBufferMemory()

model_ty = Tongyi(temperature=0)

conversation = ConversationChain(
    llm=model_ty,  
    memory=st.session_state['history']
)

for i in st.session_state['history'].chat_memory.messages:
    st.chat_message(i.type).write(i.content)

if p_y :=st.chat_input():
    st.chat_message("user").write(p_y)
    res=conversation.invoke(p_y)
    st.chat_message("AI").write(res['response'])
