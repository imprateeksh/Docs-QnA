# Base image - Python (Alpine)
FROM python:3.11-alpine3.18
# Setting up the required env vars
ENV PINECONE_API_KEY=""
ENV PINECONE_API_ENV=""
ENV HUGGINGFACEHUB_API_TOKEN=""
# Creating Work directory to be used and copying the contents
WORKDIR /src
COPY . /src
# Running important commands in the container
RUN apk add --no-cache gcc vim curl && \
pip install -r requirements.txt --no-cache-dir
# Port 8000 is chosen because of uvicorn
EXPOSE 8000
# Actual command to be executed
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]