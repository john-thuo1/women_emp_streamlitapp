import logging
import os

def setup_logger(logger_file: str, log_dir: str = 'Logs', level=logging.INFO, 
                 format='%(asctime)s - %(levelname)s - %(message)s') -> logging.Logger:
    """
    Set up a logger to log messages to a file in the specified directory.

    Args:
        logger_file (str): The base name of the log file.
        log_dir (str): The directory to store log files (default: 'Logs').
        level (int): The logging level (default: logging.INFO).
        format (str): The log message format (default: standard format).

    Returns:
        logging.Logger: Configured logger instance.
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
