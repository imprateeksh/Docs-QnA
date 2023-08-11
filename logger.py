import logging
from common import constants as const

logging.basicConfig(
    level=logging.DEBUG,
    format=const.LOG_FORMAT,
    filename=const.LOG_FILE_NAME,
    filemode="a" 
)


handler = logging.StreamHandler()
handler.setLevel(logging.INFO) 

formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Creating logger instance
llm_logger = logging.getLogger(__name__)
llm_logger.addHandler(handler)  
