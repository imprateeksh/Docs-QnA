import os
from pathlib import Path
from dotenv import load_dotenv
from common import constants as const
from common.logger import llm_logger
from common.exceptions import ReferenceNotFound

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain

load_dotenv()

CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST")
CHROMA_DB_PORT = os.getenv("CHROMA_DB_PORT")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

DIRECTORY_PATH = 'resources'

def load_docs(dir_path):
    loader = DirectoryLoader(dir_path)
    documents = loader.load()
    return documents

def split_docs(documents, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs

def load_split_docs():
    documents = load_docs(DIRECTORY_PATH)
    docs = split_docs(documents, chunk_size=1000, chunk_overlap=120)
    llm_logger.info(f"Length of Document after splitting: {len(docs)}")
    return docs

def create_or_load_chromadb_index():
    index_directory = "./chroma_db"
    if os.path.exists(index_directory):
        return Chroma.load(index_directory)
    else:
        embeddings = HuggingFaceEmbeddings()
        llm_logger.info("Searching using Hugging Face Embeddings")
        docs = load_split_docs()
        index = Chroma.from_documents(docs, embeddings, persist_directory=index_directory)
        index.persist()
        return index

def get_similar_docs(query, k=2, score=False):
    try:
        index = create_or_load_chromadb_index()
        if score:
            similar_docs = index.similarity_search_with_score(query, k=k)
        else:
            similar_docs = index.similarity_search(query, k=k)
        return similar_docs
    except Exception as e:
        llm_logger.error(f"Unable to process query: {e}")
        return const.ERR_GENERIC_EXCPN

def get_chain_object():
    obj_llm = HuggingFaceHub(
        repo_id="declare-lab/flan-alpaca-large",
        model_kwargs={"temperature": 0.7, "max_length": 512},
        huggingfacehub_api_token=HF_TOKEN
    )
    return load_qa_chain(obj_llm, chain_type="stuff")

def get_answer(query):
    try:
        if HF_TOKEN is None or CHROMA_DB_HOST is None or CHROMA_DB_PORT is None:
            return const.MSG_ENV_MISSING

        if not os.path.exists(Path(const.DOC_PATH)):
            llm_logger.error(f"File Path is not correct: {const.DOC_PATH}")
            raise ReferenceNotFound(const.ERR_REF_NOT_FOUND)

        similar_docs = get_similar_docs(query)
        llm_logger.info("Scanned the doc, now creating chain to evaluate...")
        chain = get_chain_object()
        answer = chain.run(input_documents=similar_docs, question=query)
        return answer
    except Exception as e:
        llm_logger.error(f"Unable to process query: {e}")
        return const.ERR_GENERIC_EXCPN

# query = "What is OCP"
# print(get_answer(query))

