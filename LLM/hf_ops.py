
import os
import pinecone

from common import constants as const
from dotenv import load_dotenv
from logger import llm_logger

from langchain.document_loaders import UnstructuredPDFLoader
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


def load_doc(doc_path='resources/icr-docs.pdf'):
    """Load the PDF document(s)"""
    llm_logger.info("Loading file")
    loader = UnstructuredPDFLoader(doc_path)
    return loader.load()

def text_split(chunk_size=1000,chunk_overlap=100):
    """Split the text in chunks from the loaded document."""
    data = load_doc()
    llm_logger.debug(f"Total {len(data)} documents to be searched for the queries.")
    llm_logger.debug(f"Total {len(data[0].page_content)} characters in PDF")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap=chunk_overlap
    )
    texts = text_splitter.split_documents(data)
    llm_logger.debug(f"After splitting: Total {len(texts)} documents to be searched.")
    return texts

def vector_search():
    """Search the vector database."""
    embeddings = HuggingFaceEmbeddings()
    texts = text_split()

    llm_logger.info(f"Initialize pinecone vector DB...\n Index name: {PINECONE_INDEX_NAME}")
    pinecone.init(
        api_key = PINE_API_KEY,
        environment = PINE_ENV
    )

    index = pinecone.Index(PINECONE_INDEX_NAME) # this is not used, but given as it is in doc
    llm_logger.info("Searching using Hugging Face Embeddings")
    docsearch = Pinecone.from_texts(
        [t.page_content for t in texts],
        embeddings,
        index_name=PINECONE_INDEX_NAME
    )
    return docsearch

def get_answer(
        query,
        chain=const.CHAIN_TYPE,
        model=const.MODEL_ID,
        temp=const.DEFAULT_TEMPERATURE, 
        model_max_length=const.MODEL_LENGTH
        ):
    """Process the query asked and return the answer."""
    try:
        obj_llm=HuggingFaceHub(
            repo_id=model, 
            model_kwargs={
                "temperature":temp, 
                "max_length":model_max_length
                },
            huggingfacehub_api_token = HF_TOKEN
            )
        llm_logger.info("LLM object Initialized: HF")
        chain = load_qa_chain(obj_llm, chain_type=chain)
        llm_logger.debug(f"Performing Vector search for the query: {query}")
        docs = vector_search().similarity_search(query)   # query = "What is Egress?"
        output = chain.run(input_documents=docs, question=query)
        return output
    except Exception as e:
        llm_logger.error(f"Unable to process query: {e}")
        return const.ERR_GENERIC_EXCPN


get_answer("What is Cloud Advocate?")