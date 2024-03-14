import logging
import typing as tp
import time

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class BaseErrorHandler(ABC):
    @abstractmethod
    def is_error_to_be_handled(self, exception: Exception) -> bool:
        """
        Check if exception should be handled
        :param exception: exception to check
        :return: True if exception should be handled, False otherwise
        """
        pass

    @abstractmethod
    def handle(self, exception: Exception) -> bool:
        """
        Handle exception. If exception should not be handled, do nothing and return False
        :param exception: exception to handle
        :return: True if exception was handled, False otherwise
        """
        pass

class SleepErrorHandler(BaseErrorHandler):
    def __init__(self, sleep_time: int = 5,
                 error_types: tp.List[tp.Type[Exception]] = [Exception],
                 error_messages_patterns: tp.Optional[tp.List[tp.Optional[str]]] = None) -> None:
        """
        :param sleep_time: time to sleep in seconds
        :param error_types: list of error types to handle
        :param error_messages_patterns: list of error messages patterns to handle
          - if None, all errors of type error_types will be handled
          - if not None, must be of the same length as error_types
          - if message pattern is None, all errors of type error_types[i] will be handled
          - if message pattern is not None, will correspond to error_types[i] **ignoring the case of the message**
        """
        self.sleep_time = sleep_time
        self.error_types = error_types
        self.error_messages_patterns = error_messages_patterns or [None] * len(error_types)

    def is_error_to_be_handled(self, exception: Exception) -> bool:
        """
        Check if exception should be handled
        """
        for error_type, error_message_pattern in zip(self.error_types, self.error_messages_patterns):
            if isinstance(exception, error_type):
                if error_message_pattern is None:
                    return True
                is_error_message_pattern_found = error_message_pattern.lower() in str(exception).lower()
                if is_error_message_pattern_found:
                    return True
                
        return False
    
    def handle(self, exception: Exception) -> bool:
        if self.is_error_to_be_handled(exception):
            logger.error(f"Error {exception} occured. Sleeping for {self.sleep_time} seconds.")
            time.sleep(self.sleep_time)
            return True
        return False

