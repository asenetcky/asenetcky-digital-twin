import os

from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from asenetcky_digital_twin.prompts.template import fetch_prompt_template
from asenetcky_digital_twin.rag import retrieve_vector_store

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

prompt_template = fetch_prompt_template()

retriever = retrieve_vector_store()

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt_template | llm

response = rag_chain.invoke("What certifications does Alex Senetcky have?")
print(response.content)

response = rag_chain.invoke("What experience does Alex Senetcky have with analytics?")
print(response.content)
