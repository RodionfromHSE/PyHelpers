import logging
import typing as tp
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class BaseResponseProcessor(ABC):
    @abstractmethod
    def process(self, response: str) -> str:
        """
        Process response
        :param response: response to process
        :return: processed response
        """
        pass


class CodeBlockExtractorProcessor(BaseResponseProcessor):
    """
    Extract the content of a code blocks from response
    """
    def __init__(self, lang: str = 'json') -> None:
        super().__init__()
        self.lang = lang

    def process(self, response: str) -> str:
        """
        Strip code blocks from response
        """
        block_open, block_close = f"```{self.lang}", "```"
        try:
            block_open_index_start = response.index(block_open)
            block_open_index_end = block_open_index_start + len(block_open)
            block_close_index_start = response.index(block_close, block_open_index_end)
        except ValueError:
            logger.debug(f"Code block not found in response: {response[:30]}")
            return response
        response_extracted = response[block_open_index_end:block_close_index_start]
        return response_extracted

class CodeBlockStripperProcessor(BaseResponseProcessor):
    """
    Strip code blocks from response
    """
    def process(self, response: str) -> str:
        """
        Strip code blocks from response
        """
        response_stripped = response.lstrip("```json").lstrip("```").rstrip("```")
        return response_stripped
