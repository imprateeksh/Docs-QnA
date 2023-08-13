"""
For new hires: 
 - How to access resources
 - Raise Access
 - Common Errors Resolution
"""
from common.errors import COMMON_ERRORS
from common.logger import llm_logger
import common.constants as const

def has_common_word_character(question:str):
    """Check if any word in the question is part of a common dictionary key"""
    words = question.split(' ')
    common_words = ["i", "me", "myself", "get", "provide","please", "am"]  # List of words to be excluded
    filtered_words = [w for w in words if w.lower() not in common_words]

    for key in COMMON_ERRORS.keys():
        for w in filtered_words:
            if w.lower() in key.lower():
                return COMMON_ERRORS[key]
    llm_logger.info("🗄️ Question not found in question bank.")
    return False


def common_errors_resolution(question):
    """Provide basic error resolution."""
    try:
        result = has_common_word_character(question)
        if not result:
            llm_logger.info("No character of the question is part of a common dictionary key.")
            return const.ERR_QBANK_GENERIC

        llm_logger.info("Able to match the question asked with questions in questionaire repo.")
        return {
            "description": result["Description"], 
            "solution": result["Solution"]
            }
    except Exception as e:
        llm_logger.error(f"Error seens as: {e}")
        return const.ERR_QBANK_GENERIC
