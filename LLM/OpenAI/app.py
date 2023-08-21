# Example demonstrating usage of OpenAI and Faiss to query a Pdf

import os
from PyPDF2 import PdfReader

from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
raw_text = ''

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
pdfreader = PdfReader("resources/catalog.pdf")

for _, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

# Split the text
text_splitter = CharacterTextSplitter(
    separator= "\n", 
    chunk_size=CHUNK_SIZE, 
    chunk_overlap = CHUNK_OVERLAP, 
    length_function = len,
    )

texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()
document_search = FAISS.from_texts(texts, embeddings)

# Create Chain

chain = load_qa_chain(OpenAI(), chain_type="stuff")

# ask question based on the pdf
query = "what is virtualization"

docs = document_search.similarity_search(query)
output = chain.run(input_documents=docs, question=query)
print(output)
