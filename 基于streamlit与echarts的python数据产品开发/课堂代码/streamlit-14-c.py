# -*- coding: utf-8 -*-
"""
Created on Wed May 31 09:36:13 2023

@author: wp
"""

import requests
import base64
import streamlit as st

API_KEY = ""
SECRET_KEY = ""

def main():
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.image(bytes_data)
        
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
        
        img = base64.b64encode(bytes_data)
        
        payload={"image":img}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        for i in response.json()["words_result"]:
            st.write(i["words"])
    

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
