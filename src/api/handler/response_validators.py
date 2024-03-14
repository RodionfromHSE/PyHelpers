
import logging
import typing as tp
import jsonschema
import json
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class BaseResponseValidator(ABC):
    @abstractmethod
    def is_response_valid(self, response: str) -> bool:
        """
        Check if response is valid
        :param response: response to check
        :return: True if response is valid, False otherwise
        """
        pass


class JsonResponseValidator(BaseResponseValidator):
    """
    Check if response is valid json matching the schema
    """
    def __init__(self, schema: tp.Optional[tp.Dict] = None) -> None:
        """
        :param schema: schema to check response against (look in jsonschema documentation for more info)
            - if None, response will be checked for valid json
        """
        self.schema = schema

    def is_response_valid(self, response: str) -> bool:
        """
        Check if response is valid json matching the schema
        """
        try:
            json_response = json.loads(response)
            if self.schema is not None:
                jsonschema.validate(json_response, self.schema)
        except jsonschema.ValidationError as e:
            logger.error(f"Response is not valid json matching the schema: {e}")
            return False
        except json.decoder.JSONDecodeError as e:
            logger.error(f"Response is not valid json: {e}")
            return False
        except Exception as e:
            logger.error(f"Unknown error: {e}")
            return False
        return True
