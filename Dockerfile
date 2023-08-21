FROM python:3.9
# ENV PINECONE_API_KEY=""
# ENV PINECONE_API_ENV=""
ENV HUGGINGFACEHUB_API_TOKEN=""
ENV CHROMA_DB_HOST=localhost
ENV CHROMA_DB_PORT=27017
WORKDIR /src
COPY . /src

EXPOSE 8000

# RUN apk update && \
# apk add --no-cache libvirt build-base gcc rust cargo openssl
#rust cargo openssl openssl-dev git
RUN pip3 install --no-cache-dir -r req.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
# CMD ["sleep", "infinity"]

# Stage 1: Install System Dependencies
# FROM python:3.8 AS system_dependencies
# RUN apt-get update && apt-get install -y \
#     libpoppler-cpp-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Stage 2: Install Python Dependencies
# FROM python:3.8 AS python_dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Final Stage: Create Application Image
# FROM python:3.8
# ENV CHROMA_DB_HOST=localhost
# ENV CHROMA_DB_PORT=27017
# WORKDIR /src
# EXPOSE 8000
# COPY --from=system_dependencies /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
# COPY --from=python_dependencies /usr/local /usr/local
# COPY . /src

# # CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sleep", "infinity"]