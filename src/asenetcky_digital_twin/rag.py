from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from pathlib import Path

rag_document_path = Path.cwd() / "rag_documents/"


pdfs=[file for file in rag_document_path.rglob(pattern='*.pdf')]
markdowns=[file for file in rag_document_path.rglob(pattern='*.md')]

chunk_size = 500
chunk_overlap = 100


rc_splitter = RecursiveCharacterTextSplitter(
separators=["\n\n", "\n", " ", ""],
chunk_size=chunk_size,
chunk_overlap=chunk_overlap)
docs = rc_splitter.split_text(quote)
print(docs)



embedding_function = OpenAIEmbeddings(api_key=openai_api_key, model='text-embedding-3-small')
vectorstore = Chroma.from_documents(
    # docs,
    embedding=embedding_function,
    persist_directory="path/to/directory"
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)