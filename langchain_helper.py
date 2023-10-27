from langchain.llms import OpenAI


llm = OpenAI(temperature=0)

def generate_answer(question: str) -> str:
    anwser = llm(question)
    return anwser
