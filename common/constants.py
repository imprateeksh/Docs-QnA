import random

# LOGGER
LOG_FORMAT="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
LOG_FILE_NAME="llm_svc.log"

# PDF DOC Info
DOC_PATH="resources/catalog.pdf"
MSG_ENV_MISSING = {"Message": "Feel free to add the required API Keys."}
ERR_REF_NOT_FOUND="Reference file/s not found. Please check the file path."

# LLM RELATED INFO
CHAIN_TYPE="stuff"
MODEL_ID="declare-lab/flan-alpaca-large" # "google/flan-t5-xxl"
DEFAULT_TEMPERATURE=0.8
MODEL_LENGTH=512

GENERIC_MSGS = [
    "🚀  Oops! Our spaceship hit a temporal anomaly. Trying to get back to the future.", 
    "🕹️  Oops, it seems our servers are playing hide and seek with your query right now. They'll be back with an answer soon, promise!",
    "🛠️  It seems the gears of innovation got a bit rusty. Our tech ninjas are fixing it.",
    "😅  Don't panic, but a cosmic hiccup disrupted our cosmic code dance. Stay tuned!",
    "🚴‍♀️  Hold tight! Our servers are doing some calisthenics. They'll be back in action soon.",
    "🤖  Uh-oh! It seems we lost a byte along the way. We're retrieving it now."
]
ERR_GENERIC_EXCPN = random.choice(GENERIC_MSGS)

ERR_QBANK_GENERIC= {"Messsage": "Sorry, I couldn't find an answer for this question. Could you please try asking a different question?"}