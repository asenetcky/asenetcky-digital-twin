from langchain_text_splitters import RecursiveCharacterTextSplitter
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

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)


def load_documents() -> list[Document]:
    """
    Load documents from RAG_DOCUMENT_PATH using unstructured[local].

    Returns:
        List of Langchain Document objects.
    """

    document_paths = [path for path in RAG_DOCUMENT_PATH.rglob("*.*")]
    loader = UnstructuredLoader(document_paths)

    return loader.load()


def split_text(documents: list[Document]):
    """ """

    chunk_size = 300
    chunk_overlap = 100

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks


docs = load_documents()
chunks = split_text(docs)

# embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
# vectorstore = Chroma.from_documents(
#     docs, embedding=embedding_function, persist_directory=Path.cwd() / "rag" / "vector-store"
# )

# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})


# message = """
#         Use the context to answer questions about Alex Senetcky.

#         Context:
#         {context}

#         Question:
#         {question}

#         Answer:
#         """

# prompt_template = ChatPromptTemplate.from_messages([("human", message)])


# rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt_template | llm

# response = rag_chain.invoke("What certifications does Alex Senetcky have?")
# print(response.content)
