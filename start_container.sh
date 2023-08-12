#!/bin/bash

nerdctl build --platform linux/amd64  -t doc-reader-skill .
# nerdctl build -t doc-reader-skill .

nerdctl run -d --platform linux/amd64 -p 8000:8000 \
-e PINECONE_API_KEY=$PINECONE_API_KEY \
-e PINECONE_API_ENV=$PINECONE_API_ENV \
-e HUGGINGFACEHUB_API_TOKEN=$HUGGINGFACEHUB_API_TOKEN \
doc-reader-skill
