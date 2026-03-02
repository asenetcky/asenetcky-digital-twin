import os
import shutil
from pathlib import Path

from chromadb.api.types import Document
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
    chunks = filter_complex_metadata(chunks)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks


# Path to the directory to save Chroma database
CHROMA_PATH = Path.cwd() / "rag" / "vector-store"


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

    embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

    # Create a new Chroma database from the documents using OpenAI embeddings
    Chroma.from_documents(
        collection_name="digital-twin", documents=chunks, embedding=embedding_function, persist_directory=CHROMA_PATH
    )

    # Persist the database to disk
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def generate_data_store():
    """
    Function to generate vector database in chroma from documents.
    """
    documents = load_documents()  # Load documents from a source
    chunks = split_text(documents)  # Split documents into manageable chunks
    save_to_chroma(chunks)  # Save the processed data to a data store


# Generate the data store
generate_data_store()


embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
vector_store = Chroma(
    collection_name="digital-twin", embedding_function=embedding_function, persist_directory=CHROMA_PATH
)


# embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
# vectorstore = Chroma.from_documents(
#     docs, embedding=embedding_function, persist_directory=Path.cwd() / "rag" / "vector-store"
# )

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})


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
