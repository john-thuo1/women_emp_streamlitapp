import json
import logging
import os

def setup_logger(logger_file: str, log_dir: str = 'Logs', level=logging.INFO, 
                 format='%(asctime)s - %(levelname)s - %(message)s') -> logging.Logger:
    """
    Set up a logger for logging messages to a file.

    Args:
        logger_file (str): The name of the log file to store the log messages.
        log_dir (str, optional): The directory where the log file will be saved. Default is 'Logs'.
        level (int, optional): The logging level (e.g., logging.INFO, logging.DEBUG). Default is logging.INFO.
        format (str, optional): The format in which log messages will be recorded. Default is '%(asctime)s - %(levelname)s - %(message)s'.

    Returns:
        logging.Logger: The configured logger object.
    
    Raises:
        FileNotFoundError: If the log file or directory cannot be accessed or created.
    """
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(logger_file)
    
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(os.path.join(log_dir, f"{logger_file}.log"))
        file_handler.setLevel(level)

        formatter = logging.Formatter(format)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.setLevel(level)

    return logger

def load_categories(file_path: str) -> dict:
    """
    Load the categories from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing categories.

    Returns:
        dict: The categories data parsed from the JSON file.

    Raises:
        FileNotFoundError: If the JSON file is not found at the specified path.
        ValueError: If the JSON file is not formatted correctly.
    """
    try:
        with open(file_path, "r") as file:
            file_content = file.read()  
            categories = json.loads(file_content) 
        return categories
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file '{file_path}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"JSON file '{file_path}' is not formatted correctly.")
