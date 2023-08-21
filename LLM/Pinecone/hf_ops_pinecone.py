
import os
import pinecone

from pathlib import Path
from common import constants as const
from dotenv import load_dotenv
from common.logger import llm_logger
from common.exceptions import ReferenceNotFound

from langchain.document_loaders import DirectoryLoader
# UnstructuredPDFLoader -> Tried with this, was consuming more time so removed
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain


# Initial ENV VARS LOADING
load_dotenv()

PINECONE_INDEX_NAME = "cloud-docs-help-1" # 768 dimensions considered
PINE_API_KEY = os.getenv("PINECONE_API_KEY", None)
PINE_ENV = os.getenv("PINECONE_API_ENV", None)
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", None)

DIRECTORY_PATH = 'resources'

def load_docs(dir_path): # 2
  loader = DirectoryLoader(dir_path)
  documents = loader.load()
  return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=120): # 3
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

def load_split_docs(): # - 1
  documents = load_docs(DIRECTORY_PATH)
  len(documents)
  docs = split_docs(documents)
  llm_logger.info(f"Length of Document after splitting : {len(docs)}")
  return docs

def get_pinecone_index(): # -4
  pinecone.init(
      api_key = PINE_API_KEY,
      environment = PINE_ENV
  )
  embeddings = HuggingFaceEmbeddings()

  llm_logger.info("Searching using Hugging Face Embeddings")
  
  docs = load_split_docs()
  index = Pinecone.from_documents(
      docs,
      embeddings,
      index_name=PINECONE_INDEX_NAME
  )
  return index

def get_similiar_docs(query,k=2,score=False):
  index = get_pinecone_index()
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

def get_chain_object():
  obj_llm=HuggingFaceHub(
    repo_id="declare-lab/flan-alpaca-large", 
    model_kwargs={
      "temperature":0.7, 
      "max_length": 512
      },
    huggingfacehub_api_token = HF_TOKEN)
  
  return load_qa_chain(obj_llm, chain_type="stuff")

def get_answer(query):
  try:
    # API KEY VALIDATION
    if HF_TOKEN is None or PINE_ENV is None or PINE_API_KEY is None:
        return const.MSG_ENV_MISSING
    
    # FILE PATH VALIDATION
    if not os.path.exists(Path(const.DOC_PATH)):
        llm_logger.error(f"File Path is not correct : {const.DOC_PATH} ")
        raise ReferenceNotFound(const.ERR_REF_NOT_FOUND)
    
    # Get doc loaded/splitted and use vector db
    similar_docs = get_similiar_docs(query)
    llm_logger.info("Scanned the doc, now creating chain to evaluate...")

    chain = get_chain_object()
    answer =  chain.run(input_documents=similar_docs, question=query)

    return  answer
  
  except Exception as e:
    llm_logger.error(f"Unable to process query: {e}")
    return const.ERR_GENERIC_EXCPN

# query = "What is OCP"  
# print(get_answer(query))
