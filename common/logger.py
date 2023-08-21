import logging
import logging.handlers
from common import constants as const

logging.basicConfig(
    level=logging.DEBUG,
    format=const.LOG_FORMAT,
    filename=const.LOG_FILE_NAME,
    filemode="a" 
)


# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO) 

# Add a rotating log handler as the log file size was drastically increasing (When using PineCone)
log_handler = logging.handlers.RotatingFileHandler(
    const.LOG_FILE_NAME,
    maxBytes=500 * 1024 * 1024,  # 500 MB
    backupCount=3  # Number of backup log files
)
log_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s - %(filename)s:%(lineno)d - %(message)s")
log_handler.setFormatter(formatter)

# Creating logger instance
llm_logger = logging.getLogger(__name__)
llm_logger.addHandler(log_handler)  
