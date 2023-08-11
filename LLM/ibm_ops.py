"""Perform Various LLM Operations"""
import os
import logging

from dotenv import load_dotenv

# from langchain import PromptTemplate
# from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator #vectorize db index with chromadb
from langchain.embeddings import HuggingFaceEmbeddings #for using HugginFace embedding models
from langchain.text_splitter import CharacterTextSplitter #text splitter
from langchain.chains import RetrievalQA
    

from genai.extensions.langchain import LangChainInterface
from genai.model import Credentials
from genai.schemas import GenerateParams

from common import constants as const


# Create logger
logging.basicConfig(level=logging.INFO,)
logger = logging.getLogger(__name__)

# Load env vars
load_dotenv()

API_KEY = os.getenv("GENAI_KEY", None)
API_URL = os.getenv("GENAI_API", None)
if API_KEY is None or API_URL is None:
    logger.error(const.INVALID_LOGIN)
    # TODO: Should return error message in response?

creds = Credentials(API_KEY, API_URL)

def initialize_model(
        model_name = "google/flan-ul2", # Default model
        decoding="sample",
        max_tokens=300,
        min_tokens=50,
        is_stream=False,
        temp=0.7,
        top_k_val=100,
        top_p_val=1):
    """Initializing watsonx model"""
    params = GenerateParams(
        decoding_method=decoding,
        max_new_tokens=max_tokens,
        min_new_tokens=min_tokens,
        stream=is_stream,
        temperature=temp,
        top_k=top_k_val,
        top_p=top_p_val,
    )

    # Create and return the object having model specific parameters
    model = LangChainInterface(
        model=model_name, 
        credentials=creds, 
        params=params
        )
    logger.info("Model initialized successfully.")
    return model

# pt2 = PromptTemplate(input_variables=["question"],template="Answer the following question: {question}")
def get_answer(
        query = const.DEFAULT_QUES,
        chunk_size=1000, 
        chunk_overlap=100,
        chain_type="stuff"):
    """Get answers based on the document stored."""
    try:
        # pdf="resources/Cloud_Advocate.pdf" # Add any pdf here under resource folder
        pdf = "/Users/prateeksharma/Music/watsonx-challenge/GenAI_Based_Examples/LLMService/resources/Cloud_Advocate.pdf"
        loaders = [PyPDFLoader(pdf)]
        index = VectorstoreIndexCreator(
            embedding=HuggingFaceEmbeddings(),
            text_splitter=CharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
            )
        ).from_loaders(loaders)

        model = initialize_model(model_name="deepset/roberta-base-squad2")

        chain = RetrievalQA.from_chain_type(
            llm=model, 
            chain_type=chain_type, 
            retriever=index.vectorstore.as_retriever(), 
            input_key="question" # TODO: Need to see this, verify if the right prompt template has to be provided here , then consider this input parameter
            )
        # Return answer based on the document
        output = chain.run(query)
        logger.info({"answer" : output})
        return {"answer" : output}
    except Exception as e:
        logger.error(str(e))
        return const.MSG_GENERIC_ERR

get_answer("what all to study for IBM Cloud Advocate Exam?")

# TODO: Extend get_answer() for more than one docs to be considered as input
# TODO: Provide more than one files to loader to set context as more than one.
# TODO: Provide Multishot approach to refine the answer