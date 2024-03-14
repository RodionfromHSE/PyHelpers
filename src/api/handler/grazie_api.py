import typing as tp
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient, RequestFailedException
from grazie.api.client.llm_parameters import LLMParameters
from grazie.api.client.parameters import Parameters
from grazie.api.client.profiles import Profile

from ..prompter import Prompt
from .error_handlers import SleepErrorHandler

class GrazieApi:
    """Grazie API handler."""
    MODELS_SUPPORTING_SYSTEM = {
        "openai-gpt-4",
        "openai-chat-gpt",
        "openai-chat-gpt-16k",
        "gpt-4-1106-preview",
        "gpt-4-32k-0613"
    }
    def __init__(self, iamtoken: str, model: str) -> None:
        """Initializes the API.
        :@param iamtoken: Grazie API token.
        :@param model: Name of model to use.
        :@param supports_system: Whether the model supports system messages.
        """
        self.client = GrazieApiGatewayClient(
            grazie_agent=GrazieAgent(name="Rodion.Khvorostov", version="dev"),
            url=GrazieApiGatewayUrls.STAGING,
            auth_type=AuthType.USER,
            grazie_jwt_token=iamtoken
        )
        self.model = model
        self.supports_system = model in self.MODELS_SUPPORTING_SYSTEM

    def __call__(self, prompt: Prompt) -> str:
        """Returns generated text."""
        if self.supports_system:
            chat=ChatPrompt().add_system(prompt.system).add_user(prompt.get_prompt())
        else:
            chat=ChatPrompt().add_user(str(prompt))
        
        res = self.client.chat(
            chat=chat,
            profile=Profile.get_by_name(self.model),
            parameters={
                LLMParameters.Temperature: Parameters.FloatValue(0.0)
            }
        )

        return res.content
    
def get_too_many_requests_error_handler(sleep_time: int = 600) -> tp.Callable[[Exception], bool]:
    error_types = [RequestFailedException]
    error_messages_patterns = ["Too many requests"]
    return SleepErrorHandler(sleep_time=sleep_time, error_types=error_types, error_messages_patterns=error_messages_patterns)
