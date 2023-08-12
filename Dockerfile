FROM python:3.8-slim

ENV PINECONE_API_KEY=""
ENV PINECONE_API_ENV=""
ENV HUGGINGFACEHUB_API_TOKEN=""

WORKDIR /src
COPY . /src

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* && \ 
    pip3 install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
EXPOSE 8000
# ---
# FROM python:3.8-alpine

# ENV PINECONE_API_KEY=""
# ENV PINECONE_API_ENV=""
# ENV HUGGINGFACEHUB_API_TOKEN=""

# WORKDIR /src
# COPY . /src

# RUN apk update && \
#     apk add --no-cache build-base gcc && \
#     pip3 install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
# EXPOSE 8000