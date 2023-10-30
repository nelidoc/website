import streamlit as st

import langchain_helper as lh
import streamlit_helper as sh
# from dotenv import load_dotenv
import time
from git import Repo


# load_dotenv()

st.set_page_config(
    page_title="Neli",
    page_icon="./imgs/logo.png",
    layout='wide'
)

st.title("Welcome to neli.")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)


# Check if 'openai_apikey' is in session state and if it's empty

max_repo_number = 3


if not sh.exists(sh.openai_apikey_key):
    # Display the text box for the API key
    api_key = st.text_input("Enter OpenAI API Key:")

    # If the text box has a value (i.e., user has entered the API key)
    if st.button("Add ApiKey") or api_key:
        if st.secrets["AUTO_KEY"] == api_key:
            sh.set(sh.openai_apikey_key, st.secrets["OPENAI_API_KEY_CUSTOM"])
        else:
            sh.set(sh.openai_apikey_key, api_key)
        st.write("API Key stored successfully!")
        time.sleep(1)
        st.rerun()
else:

    # Data sources
    st.sidebar.title("Data sources")

    # If repos does not exists
    if not sh.exists(sh.respository_key):
        sh.set(sh.respository_key, [""])

    # Display chat messages
    for i, repo in enumerate(sh.get(sh.respository_key)):
        st.session_state[sh.respository_key][i]=st.sidebar.text_input("Repo " + str(i+1))

    # for value, index in enumerate(source_list):
    #     if source_list[-1] != "" and len(source_list) <= 2:
    #         # print(index)
    #         source_list.append(st.sidebar.text_input("Repo: " + str(value + 2)))

    col1, col2 = st.sidebar.columns(2)
    with col1:
        disabled = False
        if len(sh.get(sh.respository_key)) == max_repo_number:
            disabled = True
        if st.button('New repo', disabled=disabled):
            if sh.get(sh.respository_key)[-1] != "" and len(sh.get(sh.respository_key)) <= max_repo_number - 1:
                st.session_state[sh.respository_key].append("")
                st.rerun()
            # Handle button 1 click

    with col2:
        if st.button('Train'):
            lh.train()



    print("Repositories: " + str(sh.get(sh.respository_key)))

    # Chat definition

    # Store LLM generated responses
    if not sh.exists(sh.messages_key):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I am Neli, I can help you to interact with git repositories."}]

    st.chat_input("Write your message.")
    # Display chat messages
    for message in sh.get(sh.messages_key):
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
                response = lh.generate_tuned_answer(prompt)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

    # if st.sidebar.button("Train"):
    #     m = "Let me understand this repositories: " + str(source_list)
    #     with st.chat_message("assistant"):
    #         st.write(m)
    #     message = {"role": "assistant", "content": m}
    #     st.session_state.messages.append(message)

    st.sidebar.divider()

    if st.sidebar.button("Clean chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi, I am neli, I can help you to interact with git repositories."}]
