# GEN AI service

import uvicorn
from fastapi import FastAPI
from logger import llm_logger
from LLM import hf_ops

app = FastAPI()

@app.get('/health')
def healthcheck():
    """Verify the health of API."""
    llm_logger.info( "\tHealthCheck: Pass")
    return {"health": "ok"}


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


# Test method to verify images to skills
@app.get("/image")
async def get_image(url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fleaders.com%2Farticles%2Fbusiness%2Fibm-history%2F&psig=AOvVaw26M4kCxbNnDz1yXqqYNL87&ust=1691923577142000&source=images&cd=vfe&opi=89978449&ved=0CA4QjRxqFwoTCPiO6dL41oADFQAAAAAdAAAAABAI"):
    import requests
    import base64
    import json
    # URL of the image to download
    image_url = url

    # Download the image
    response = requests.get(image_url)
    image_data = response.content

    # Convert the image data to base64 encoded string
    base64_image = base64.b64encode(image_data).decode("utf-8")

    # Create a dictionary to store the image data
    image_dict = {
        "filename": "image.jpg",
        "base64_encoded_data": base64_image
    }

    # Convert the dictionary to JSON
    json_data = json.dumps(image_dict, indent=4)

    return json_data

if __name__ == "__main__": 
    uvicorn.run(app, host='0.0.0.0', port=8000)
    llm_logger.debug("Server started")