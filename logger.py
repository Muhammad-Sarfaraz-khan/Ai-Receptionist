import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name: str) -> logging.Logger:
    """
    Setup a logger with both console and file handlers.
    
    Args:
        name: Logger name (typically the class name)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), '../../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Console handler with UTF-8 encoding for Windows
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # File handler with rotation and UTF-8 encoding
    log_file = os.path.join(log_dir, f'{name}.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'  # Explicit UTF-8 encoding
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger