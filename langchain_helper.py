from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

import os

# llm = OpenAI(temperature=0.7, openai_api_key=os.environ["OPENAI_API_KEY"])

# def generate_answer(question: str) -> str:
#     anwser = llm(question)
#     return anwser
import streamlit as st


def generate_answer(question: str) -> str:
    chat_model = ChatOpenAI(temperature=0.7, openai_api_key=st.secrets["OPENAI_API_KEY"])
    answer = chat_model.predict(question)
    return answer