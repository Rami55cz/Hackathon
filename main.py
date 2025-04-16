import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY") 

st.set_page_config(page_title="Tax Chatbot", layout="centered")
st.markdown(
    """
    <style>
    body {background-color: #fff;}
    .stButton > button {background-color: green; color: white; border: 1px solid black;}
    .stTextInput > div > input {background-color: white; color: black; border: 1px solid black;}
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_tax_response(query):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "deepseek-chat", 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant specializing in taxes."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No specific answer found.")
    else:
        return f"API Error: {response.status_code} - {response.text}"

st.title("💬 Tax Chatbot")
st.markdown("I’m here to help with your tax-related questions. Feel free to ask!")

user_query = st.text_input("Your tax question:", "")

if st.button("Submit"):
    if user_query.strip():
        with st.spinner("Fetching response..."):
            answer = fetch_tax_response(user_query)
            st.markdown(f"**Chatbot:** {answer}")
    else:
        st.warning("Please enter a valid question!")

st.markdown(
    """
    <hr style='border: 1px solid black;'>
    <div style="text-align: center; color: green; font-weight: bold;">
        Powered by Deepseek API
    </div>
    """,
    unsafe_allow_html=True
)
