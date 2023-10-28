import streamlit as st

import langchain_helper as lh
from dotenv import load_dotenv
import time


load_dotenv()

st.set_page_config(page_title="Neli", page_icon="./logo.png")

st.title("Welcome to neli.")

# if lh.apikey_is_empty():
#     input_apikey: str = st.sidebar.text_input("ChatGPT API KEY")
#     if st.sidebar.button("Store api key"):
#         print("Storing apikey" + input_apikey)
#         lh.set_apikey(input_apikey)
#         print(lh.apikey)


#     st.sidebar.divider()

st.sidebar.title("Data sources")
source_list = [st.sidebar.text_input("Repo: 1")]


for value, index in enumerate(source_list):
    if source_list[-1] != "" and len(source_list) <= 2:
        # print(index)
        source_list.append(st.sidebar.text_input("Repo: " + str(value + 2)))


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I am neli, I can help you to interact with git repositories."}]




st.chat_input("Write your message.")
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = lh.generate_answer(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)



if st.sidebar.button("Train"):
    with st.chat_message("assistant"):
        m = "Let me understand this repositories: " + str(source_list)
        st.write(m)
        
        message = {"role": "assistant", "content": m}
        st.session_state.messages.append(message)        
        with st.spinner("Studing hard!"):
            time.sleep(2)
            response = "I am ready to answer your questions!"
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)