from dashscope import Generation
import dashscope
import streamlit as st
 
dashscope.api_key = ""

st.set_page_config(page_title="通义千问", page_icon="📖")
st.title("📖 通义千问")

if 'history' not in st.session_state:
    st.session_state['history'] = []

def get_response(mess):
    response = Generation.call(
        model='qwen-turbo',
        messages=mess,
        result_format='message', # 将输出设置为message形式
    )
    return response

def prompt_yun(ct):
    st.session_state['history'].append({"role":"user","content":ct})
    return st.session_state['history']

for i in st.session_state['history']:
    st.chat_message(i["role"]).write(i["content"])

if p_y := st.chat_input():
    st.chat_message("user").write(p_y)
    input=prompt_yun(p_y)
    res = get_response(input)
    st.chat_message("assistant").write(res.output.choices[0].message['content'])
    st.session_state['history'].append(dict(res.output.choices[0].message))