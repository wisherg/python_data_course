import requests
import streamlit as st
import base64

API_KEY = ""
SECRET_KEY = ""

def main():

    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        # To read image file buffer as bytes:
        st.image(img_file_buffer)
        bytes_data = img_file_buffer.getvalue()
        img = base64.b64encode(bytes_data)
        
        url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime?access_token=" + get_access_token()
        
        payload={"image":img}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        st.image(base64.b64decode(response.json()["image"]))
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
