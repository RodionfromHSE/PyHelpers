import typing as tp
from abc import ABC, abstractmethod

from ..helpers import smart_format

class Prompter(ABC):
    """Prompter interface."""
    @abstractmethod
    def get_prompt(self, *args: tp.Any, **kwargs: tp.Any) -> str:
        """Prompt user for input."""
        pass


class TemplatePrompter:
    """Prompter using a template for the prompt message."""
    def __init__(self, template: str):
        self.template = template

    def get_prompt(self, **kwargs: tp.Any) -> str:
        return smart_format(self.template, **kwargs)
