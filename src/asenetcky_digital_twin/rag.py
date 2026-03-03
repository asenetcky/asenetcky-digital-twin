import os
import shutil
from pathlib import Path

from chromadb.api.types import Document
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAG_DOCUMENT_PATH = Path.cwd() / "rag" / "documents/"
CHROMA_PATH = Path.cwd() / "rag" / "vector-store"


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

    chunk_size = 500
    chunk_overlap = 100

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    chunks = filter_complex_metadata(chunks)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks


def embedding_function():
    return OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")


def save_to_chroma(chunks: list[Document]):
    """
    Save the given list of Document objects to a Chroma database.
    Args:
    chunks (list[Document]): List of Document objects representing text chunks to save.
    Returns:
    None
    """

    # Clear out the existing database directory if it exists
    if CHROMA_PATH.exists():
        shutil.rmtree(CHROMA_PATH)

    # Create a new Chroma database from the documents using OpenAI embeddings
    Chroma.from_documents(
        collection_name="digital-twin", documents=chunks, embedding=embedding_function(), persist_directory=CHROMA_PATH
    )

    print(f"[INFO]: Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def generate_vector_store():
    """
    Function to generate vector database in chroma from documents.
    """
    documents = load_documents()  # Load documents from a source
    chunks = split_text(documents)  # Split documents into manageable chunks
    save_to_chroma(chunks)  # Save the processed data to a data store


def retrieve_vector_store(
    search_type: str = "similarity",
    n_docs: int = 4,
):

    vector_store = Chroma(
        collection_name="digital-twin", embedding_function=embedding_function(), persist_directory=CHROMA_PATH
    )

    retriever = vector_store.as_retriever(search_type=search_type, search_kwargs={"k": n_docs})
    return retriever
