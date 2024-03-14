import logging
import os

DEFAULT_FORMAT = "%(levelname)s from %(name)s (%(filename)s:%(lineno)d):\n%(message)s "
DEFAULT_PATH_TO_FILE = os.path.join(os.path.dirname(__file__), '..', 'log.log')

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = DEFAULT_FORMAT

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def _clear_logger(logger: logging.Logger) -> None:
    """Clear logger, i.e. remove all handlers from it and set propagate to False."""
    logger.propagate = False
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

def get_file_logger(name: str, level: int = logging.DEBUG, file_path: str = DEFAULT_PATH_TO_FILE) -> logging.Logger:
    """Return file logger.
    
    :@param name: logger name
    :@param level: logger level
    :@param file_path: path to file to save logs (default: "log.txt")
        The file will be cleared at the beginning of the program
    :@return: logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler(file_path, encoding='utf-8')
    open(file_path, 'w').close()
    handler.setLevel(level)

    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler.setFormatter(formatter)

    _clear_logger(logger)
    logger.addHandler(handler)
    
    return logger
    

    
def get_colorful_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Return colorful logger.
    
    :@param name: logger name
    :@param level: logger level
    :@return: logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler() 
    handler.setLevel(level)

    formatter = CustomFormatter()
    handler.setFormatter(formatter)

    _clear_logger(logger)
    logger.addHandler(handler)
    
    return logger
