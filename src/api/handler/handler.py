# SETUP
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)

root_dir = os.path.abspath(os.path.join(__file__, '../../../..'))
sys.path.append(root_dir)
logging.info(f"Added {root_dir!r} to PYTHONPATH")

# IMPORTS
import typing as tp
import logging

from src.loggers import get_colorful_logger, get_file_logger

from .error_handlers import BaseErrorHandler
from .response_processors import BaseResponseProcessor
from .response_validators import BaseResponseValidator

logger = get_colorful_logger(__name__, level=logging.INFO)
file_logger = get_file_logger('invalid_responses', level=logging.DEBUG)


class GenerationHandler:
    """
    Class is designed to generate response and handle errors and validate responses
    """
    def __init__(self,
                 generator: tp.Callable[..., str],
                 n_attempts: int = 1,
                 error_handlers: tp.Optional[tp.List[BaseErrorHandler]] = None,
                 response_processors: tp.Optional[tp.List[BaseResponseProcessor]] = None,
                 response_validators: tp.Optional[tp.List[BaseResponseValidator]] = None) -> None:
        """
        :param generator: function to generate response
        :param n_attempts: number of attempts to generate response
        :param error_handlers: list of error handlers
        :param response_processors: list of response processors
        :param response_validators: list of response validators
        """
        self.generator = generator
        self.n_attempts = n_attempts
        self.error_handlers = error_handlers or []
        self.response_processors = response_processors or []
        self.response_validators = response_validators or []

    def _report_gen_error(self, response: str | None, description: str) -> None:
        """
        Report error during generation
        :param response: response
        :param description: description of error
        """
        logger.error(description)
        file_logger.error(description)
        
        if response is not None:
            sep = "\n" + "-" * 20 + "\n"
            file_logger.info(f"Response:\n\n{response}{sep}")

    def is_response_valid(self, response: str) -> bool:
        """
        Check if response is valid
        :param response: response to check
        :return: True if response is valid, False otherwise
        """
        for response_validator in self.response_validators:
            if not response_validator.is_response_valid(response):
                self._report_gen_error(response, f"Validator {response_validator.__class__.__name__} failed")
                return False
        return True
    
    def process_response(self, response: str) -> str:
        """
        Process response
        :param response: response to process
        :return: processed response
        """
        for response_processor in self.response_processors:
            response = response_processor.process(response)
        return response
    
    def handle_error(self, exception: Exception) -> bool:
        """
        Handle error
        :param exception: exception to handle
        :return: True if error was handled, False otherwise
        """
        for error_handler in self.error_handlers:
            if error_handler.is_error_to_be_handled(exception):
                logger.info(f"Error handler {error_handler.__class__.__name__} is handling error of type {type(exception).__name__}")
                return error_handler.handle(exception)
        return False

    def generate(self, *args, **kwargs) -> tp.Optional[str]:
        """
        Generate response
        :return: response or None if could not generate response
        """
        for attempt_id in range(self.n_attempts):
            try:
                response = self.generator(*args, **kwargs)
            except Exception as e:
                if not self.handle_error(e):
                    msg = f"Unhandled error occurred during attempt {attempt_id}: {e}"
                    self._report_gen_error(response=None, description=msg)
                continue
            
            response = self.process_response(response)
            if self.is_response_valid(response):
                return response
        
        logger.error(f"Could not generate response after {self.n_attempts} attempts")
        
        return None
