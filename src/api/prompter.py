import typing as tp
from abc import ABC, abstractmethod

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

    def _smart_format(self, **kwargs: tp.Any) -> str:
        """Smart format. If there is a redundant key among the arguments, it will be ignored"""
        actual_keys = [key for key in kwargs if "{" + key + "}" in self.template]
        return self.template.format(**{key: kwargs[key] for key in actual_keys})

    def get_prompt(self, **kwargs: tp.Any) -> str:
        return self._smart_format(**kwargs)
