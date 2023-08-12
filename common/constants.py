# LOGGER
LOG_FORMAT="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
LOG_FILE_NAME="llm_svc.log"

# PDF DOC Info
DOC_PATH="../resources/icr-docs.pdf"
MSG_ENV_MISSING = {"Message": "Feel free to add the required API Keys."}

# LLM RELATED INFO
CHAIN_TYPE="stuff"
MODEL_ID="declare-lab/flan-alpaca-large" # "google/flan-t5-xxl"
DEFAULT_TEMPERATURE=0.8
MODEL_LENGTH=512

ERR_GENERIC_EXCPN="Oops, it seems our servers are playing hide and seek with your query right now. They'll be back with an answer soon, promise!"