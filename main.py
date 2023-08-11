# GEN AI service

import uvicorn
from fastapi import FastAPI
from logger import llm_logger
from LLM import hf_ops

app = FastAPI()

@app.get('/healthcheck')
def index():
    """Verify the health of API."""
    llm_logger.info( "\tHealthCheck: Pass")
    return {"ping": "pong"}


@app.get('/answer')
def conversation(query:str):
    """Get answers based on the document stored."""
    llm_logger.info(f"Getting answers for: {query}")
    ans = hf_ops.get_answer(query)
    return ans

# @app.get('/tune')
# def model_tune(model_name:str, **kwargs):
#     """Fine tune the models."""
#     pass

if __name__ == "__main__": 
    uvicorn.run(app, host='0.0.0.0', port=8000)
    llm_logger.debug("Server started")