import typing as tp
from abc import ABC, abstractmethod
import openai

class LLMBaseApi(ABC):
    """Base class for LLM API."""
    def __init__(self, *args: tp.Any, **kwargs: tp.Any) -> None:
        pass

    @abstractmethod
    def __call__(self, request: str) -> str:
        """Returns generated text."""
        pass

class OpenAIApi(LLMBaseApi):
    """OpenAI API handler."""
    DEFAULT_PARAMS = {
        "temperature": 0.6
    }
    def __init__(self, api_key: str, model: str, params: tp.Dict[str, tp.Any] | None = None) -> None:
        """Initializes the API.
        :@param api_key: OpenAI API key.
        :@param model: Name of model to use. (e.g. "text-davinci-003")
        :@param params: Additional parameters for the API.
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.params = params or self.DEFAULT_PARAMS

    def __call__(self, prompt: str) -> str:
        """Returns generated text."""
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            **self.params
        )
        return response.choices[0].message.content
