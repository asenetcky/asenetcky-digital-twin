from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from pathlib import Path

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

rag_document_path = Path.cwd() / "rag" / "documents/"


pdfs = [file for file in rag_document_path.rglob(pattern="*.pdf")]
markdowns = [file for file in rag_document_path.rglob(pattern="*.md")]

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)


from langchain_community.document_loaders import PyPDFLoader

docs = [PyPDFLoader(pdf).load()[0] for pdf in pdfs]

# chunk_size = 500
# chunk_overlap = 100

# rc_splitter = RecursiveCharacterTextSplitter(
#     separators=["\n\n", "\n", " ", ""],
#     chunk_size=chunk_size,
#     chunk_overlap=chunk_overlap
#     )

# docs = rc_splitter.split_text(quote)
# print(docs)


embedding_function = OpenAIEmbeddings(api_key=openai_api_key, model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    docs, embedding=embedding_function, persist_directory=Path.cwd() / "rag" / "vector-store"
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

from langchain_core.prompts import ChatPromptTemplate

message = """
        Use the context to answer questions about Alex Senetcky.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

prompt_template = ChatPromptTemplate.from_messages([("human", message)])


from langchain_core.runnables import RunnablePassthrough

rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt_template | llm)

response = rag_chain.invoke("What certifications does Alex Senetcky have?")
print(response.content)
