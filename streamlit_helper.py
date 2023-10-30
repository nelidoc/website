import streamlit as st

openai_apikey_key = "openai_apikey"
openai_model_key = "openai_model"
messages_key = "messages"
respository_key = "repositories"




def exists(key: str) -> bool:
    return key in st.session_state

def get(key: str) -> any:
    return st.session_state[key]

def set(key: str, value: any) -> None:
    st.session_state[key] = value