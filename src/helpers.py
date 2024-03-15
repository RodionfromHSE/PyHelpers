"""
Set of helper functions
"""
import typing as tp

def smart_format(template, **kwargs: tp.Any) -> str:
    """Smart format. If there is a redundant key among the arguments, it will be ignored"""
    actual_keys = [key for key in kwargs if "{" + key + "}" in template]
    return template.format(**{key: kwargs[key] for key in actual_keys})