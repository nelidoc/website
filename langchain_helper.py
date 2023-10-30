from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import GitHubIssuesLoader, GitLoader

import os
import shutil

import streamlit as st
import streamlit_helper as sh

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from git import Repo, exc

def get_model():
    if not sh.exists(sh.openai_model_key):
        model = ChatOpenAI(temperature=0.7, openai_api_key=sh.get(sh.openai_apikey_key))
        sh.set(sh.openai_model_key, model)
    return sh.get(sh.openai_model_key)



def generate_answer(question: str) -> str:
    chat_model = get_model()
    answer = chat_model.predict(question)
    return answer
    # return "OK"

def get_tuned_model():
    if not sh.exists(sh.openai_model_key):
        model = ChatOpenAI(temperature=0.7, openai_api_key=sh.get(sh.openai_apikey_key))
        chain = load_qa_chain(model, chain_type="stuff")
        sh.set("chain", chain)
    return sh.get("chain")

def generate_tuned_answer(question: str) -> str:
    chat_model = get_tuned_model()

    docs = st.session_state.knowledge_base.similarity_search(question)
    response = chat_model.run(input_documents=docs, question=question)

    return response


def train(): 
    m = "Let me understand this repositories: " + str(sh.get(sh.respository_key))
    message = {"role": "assistant", "content": m}
    st.session_state.messages.append(message)

    st.session_state.finetunedata = []

    for repo_url in sh.get(sh.respository_key):
        output_path = ""
        print("Training repo: " + repo_url)

        if repo_url == "":
            continue

        if str.startswith(repo_url, "https://github.com/"):
            output_path=str.removeprefix(repo_url, "https://github.com/")
        elif str.startswith(repo_url, "github.com/"):
            output_path=str.removeprefix(repo_url, "github.com/")
        else:
            m = "Can not train with repo: " + repo_url
            message = {"role": "assistant", "content": m}
            st.session_state.messages.append(message)
            continue

        output_path =  "./artifacts/" + output_path
        clone_specific_branch(repo_url,output_path)

        loader = GitLoader(repo_path=output_path)
        # loader = GitLoader(repo_path=output_path)

        st.session_state.finetunedata.append(loader.load())



    # split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(str(sh.get("finetunedata")))

    # create embeddings
    embeddings = OpenAIEmbeddings()
    st.session_state.knowledge_base = FAISS.from_texts(texts=chunks, embedding=embeddings)  # Update the parameter names


def clone_specific_branch(repo_url, dest_dir):
    try:
        # Check if the destination directory already exists
        if os.path.exists(dest_dir):
            # If it exists, remove it
            shutil.rmtree(dest_dir)
        # Clone the specified branch
        Repo.clone_from(repo_url, dest_dir)
    except exc.GitCommandError as e:
        print(f'Failed to clone from {repo_url}: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
