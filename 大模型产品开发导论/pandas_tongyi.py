from dashscope import Generation
import dashscope
import streamlit as st
import pandas as pd
import io
from langchain_core.tools import tool
from langchain.utilities import PythonREPL
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain_core.output_parsers import JsonOutputParser
 
dashscope.api_key = ""
st.title("📖 通义千问")

if uploaded_file := st.file_uploader("Upload an data"):
    df = pd.read_csv(uploaded_file,names=["user_id","brand_id","behavior_type","date"],sep="\t")
    st.write(df.head())
    buf = io.StringIO()
    df.info(buf=buf)
    df_info = buf.getvalue()
else:
    st.stop()

#st.write(df_info)

system_prompt_t=f"""已知代码中数据信息如下：
{df_info}
此数据已经赋值给全局变量df，在已知df的基础上基于pandas编写代码然后调用工具coderunner完成任务,注意统计结果的变量名必须是result_data
"""

@tool
def coderunner(code: str) -> dict:
    """python代码执行器"""
    run_code=PythonREPL(_globals={"df":df})
    res=run_code.run(code)
    if res=='':
        return run_code
    else:
        return res

if 'history' not in st.session_state:
    st.session_state['history'] = []

parser = JsonOutputParser()

def get_response_t(messages):
    response = Generation.call(
        model='qwen-max',
        messages=messages,
        tools=[convert_to_openai_tool(coderunner)],
        result_format='message', # 将输出设置为message形式
    )
    return response

def prompt_data(content):

    prompt=[{"role":"system","content":system_prompt_t},\
            {"role":"user","content":"总共有多少行记录"},\
            {'role': 'assistant', 'content': '', 'tool_calls': [{'function': {'name': 'coderunner', 'arguments': '{"code": "import pandas as pd\nresult_data=len(df)"}'}}]}]
    prompt.append({"role":"user","content":content})
    st.session_state['history'].append({"role":"user","content":content})
    return prompt

for i in st.session_state['history']:
    st.chat_message(i["role"]).write(i["content"])


if p_y := st.chat_input():
    st.chat_message("user").write(p_y)
    input=prompt_data(p_y)
    res = get_response_t(input)
    code=parser.parse(res.output.choices[0].message['tool_calls'][0]['function']['arguments'])["code"]
    st.write(code)
    run_res=coderunner.invoke(code)
    out_put=run_res.dict()["locals"]["result_data"]
    st.chat_message("assistant").write(out_put)
    st.session_state['history'].append({'role': 'assistant', 'content': out_put})