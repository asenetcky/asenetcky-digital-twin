from chromadb.api.types import Document
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader, UnstructuredMarkdownLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_unstructured import UnstructuredLoader

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAG_DOCUMENT_PATH = Path.cwd() / "rag" / "documents/"


def load_documents() -> list[Document]:

    document_paths = [path for path in RAG_DOCUMENT_PATH.rglob("*.*")]
    loader = UnstructuredLoader(document_paths)

    return loader.load()


# def load_pdfs() -> list[Document]:
#     """
#     Load PDFs in specified directory using PyPDFDirectoryLoader

#     Returns:
#     List of Langchain Documents
#     """

#     document_loader = PyPDFDirectoryLoader(RAG_DOCUMENT_PATH, recursive=True)
#     return document_loader.load()


# def load_markdowns() -> list[Document]:
#     """
#     Load markdown documents in specified directory using

#     Returns:
#     List of Langchain Documents
#     """

#     markdowns = [file for file in RAG_DOCUMENT_PATH.rglob(pattern="*.md")]

#     documents = []

#     for markdown in markdowns:
#         document = UnstructuredMarkdownLoader(
#             markdown,
#             mode="elements",
#             strategy="fast",
#         )
#         documents.append(document)

#     loaded_documents = [document.load() for document in documents]

#     return loaded_documents


llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)


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


message = """
        Use the context to answer questions about Alex Senetcky.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

prompt_template = ChatPromptTemplate.from_messages([("human", message)])


rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt_template | llm

response = rag_chain.invoke("What certifications does Alex Senetcky have?")
print(response.content)
