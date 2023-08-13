
import os
import pinecone

from pathlib import Path
from common import constants as const
from dotenv import load_dotenv
from common.logger import llm_logger
from common.exceptions import ReferenceNotFound

from langchain.document_loaders import UnstructuredPDFLoader, DirectoryLoader
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

directory = 'resources'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)
len(documents)

def split_docs(documents,chunk_size=1000,chunk_overlap=120):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
llm_logger.info(f"Length of Document after splitting : {len(docs)}")

embeddings = HuggingFaceEmbeddings()
pinecone.init(
    api_key = PINE_API_KEY,
    environment = PINE_ENV
)

# index = pinecone.Index(PINECONE_INDEX_NAME) # this is not used, but given as it is in doc
llm_logger.info("Searching using Hugging Face Embeddings")
index = Pinecone.from_documents(
    docs,
    embeddings,
    index_name=PINECONE_INDEX_NAME
)

def get_similiar_docs(query,k=2,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

# query = "How is india's economy"
# similar_docs = get_similiar_docs(query)

llm=HuggingFaceHub(
    repo_id="declare-lab/flan-alpaca-large", 
    model_kwargs={
        "temperature":0.7, 
        "max_length": 512
        },
    huggingfacehub_api_token = HF_TOKEN
    )


chain = load_qa_chain(llm, chain_type="stuff")

def get_answer(query):
  try:
    # API KEY VALIDATION
    if HF_TOKEN is None or PINE_ENV is None or PINE_API_KEY is None:
        return const.MSG_ENV_MISSING
    
    # FILE PATH VALIDATION
    if not os.path.exists(Path(const.DOC_PATH)):
        llm_logger.error(f"File Path is not correct : {const.DOC_PATH} ")
        raise ReferenceNotFound(const.ERR_REF_NOT_FOUND)
    
    similar_docs = get_similiar_docs(query)
    llm_logger.info("Scanned the doc, now creating chain to evaluate...")
    answer =  chain.run(input_documents=similar_docs, question=query)
    return  answer
  except Exception as e:
    llm_logger.error(f"Unable to process query: {e}")
    return const.ERR_GENERIC_EXCPN

# query = "What is OCP"  
# print(get_answer(query))

#########
# def load_pdf(doc_path=const.DOC_PATH):
#     """Load the PDF document(s)"""
#     # Check for valid file here first
#     # if os.path.exists(doc_path):
#     #     llm_logger.error(f"File Path is not correct : {doc_path} ")
#     #     return None
#     llm_logger.info("Loading file...")
#     loader = UnstructuredPDFLoader(doc_path)
#     return loader.load()

# def text_split(chunk_size=1000,chunk_overlap=0):
#     """Split the text in chunks from the loaded document."""
#     data = load_pdf()

#     if not data:
#         return None
    
#     llm_logger.debug(f"Total {len(data)} documents to be searched for the queries.")
#     llm_logger.debug(f"Total {len(data[0].page_content)} characters in PDF")

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size = chunk_size,
#         chunk_overlap=chunk_overlap
#     )
#     texts = text_splitter.split_documents(data)
#     llm_logger.debug(f"After splitting: Total {len(texts)} documents to be searched.")
#     return texts

# def vector_search():
#     """Search the vector database."""
#     texts = text_split()
#     if not texts:
#         return None
    
#     embeddings = HuggingFaceEmbeddings()

#     llm_logger.info(f"Initialize pinecone vector DB...\n Index name: {PINECONE_INDEX_NAME}")
#     pinecone.init(
#         api_key = PINE_API_KEY,
#         environment = PINE_ENV
#     )

#     # index = pinecone.Index(PINECONE_INDEX_NAME) # this is not used, but given as it is in doc
#     llm_logger.info("Searching using Hugging Face Embeddings")
#     docsearch = Pinecone.from_texts(
#         [t.page_content for t in texts],
#         embeddings,
#         index_name=PINECONE_INDEX_NAME
#     )
#     return docsearch

# def get_answer(
#         query,
#         chain=const.CHAIN_TYPE,
#         model=const.MODEL_ID,
#         temp=const.DEFAULT_TEMPERATURE, 
#         model_max_length=const.MODEL_LENGTH
#         ):
#     """Process the query asked and return the answer."""
#     try:
#         # API KEY VALIDATION
#         if HF_TOKEN is None or PINE_ENV is None or PINE_API_KEY is None:
#             return const.MSG_ENV_MISSING
        
#         # FILE PATH VALIDATION
#         if not os.path.exists(Path(const.DOC_PATH)):
#             llm_logger.error(f"File Path is not correct : {const.DOC_PATH} ")
#             raise ReferenceNotFound(const.ERR_REF_NOT_FOUND)

#         obj_llm=HuggingFaceHub(
#             repo_id=model, 
#             model_kwargs={
#                 "temperature":temp, 
#                 # "max_length":model_max_length
#                 },
#             huggingfacehub_api_token = HF_TOKEN
#             )
        
#         llm_logger.info(f"{'#'*50}LLM object Initialized: HF{'#'*50}")
#         chain = load_qa_chain(obj_llm, chain_type=chain)
#         llm_logger.debug(f"Starting Vector search for the query: {query}")
#         search = vector_search()

#         if not search:
#             raise ReferenceNotFound(const.ERR_REF_NOT_FOUND)

#         docs = search.similarity_search(query)   # query = "What is Egress?"
#         output = chain.run(input_documents=docs, question=query)
#         llm_logger.info(f"{'=>'*20}Returning Output... ")
#         return output
    
#     except Exception as e:
#         llm_logger.error(f"Unable to process query: {e}")
#         return const.ERR_GENERIC_EXCPN


#TODO: Instead of multiple returns, raise exception once file not found