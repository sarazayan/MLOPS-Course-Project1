from src.logger import get_logger
from src.customer_exception import CustomException
import sys  # to show error message

logger = get_logger(__name__)

def divide_number(a, b):
    try:
        result = a/b
        logger.info("dividing two numbers")
        return result
    except Exception as e:
        logger.error("ouchhh error")
        raise CustomException("custom error zero", sys)  # Fixed: added sys parameter

if __name__ == "__main__":
    try:
        logger.info("starting program")
        divide_number(10, 0)
    except CustomException as ce:
        logger.error(str(ce))  # store explanation of error in terminal and store it as file