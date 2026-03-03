import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from asenetcky_digital_twin.rag import retrieve_vector_store

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAG_DOCUMENT_PATH = Path.cwd() / "rag" / "documents/"
CHROMA_PATH = Path.cwd() / "rag" / "vector-store"

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

message = """
        Use the context to answer questions about Alex Senetcky.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

prompt_template = ChatPromptTemplate.from_messages([("human", message)])

retriever = retrieve_vector_store()

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt_template | llm

response = rag_chain.invoke("What certifications does Alex Senetcky have?")
print(response.content)

response = rag_chain.invoke("What experience does Alex Senetcky have with analytics?")
print(response.content)
