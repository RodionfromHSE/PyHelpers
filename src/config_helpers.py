"""
Helper functions for reading and printing configs
"""
from omegaconf import OmegaConf
import json
import typing as tp
import os
from hydra import initialize_config_dir, compose
from copy import deepcopy

__ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
__CONFIG_DIR = os.path.join(__ROOT_DIR, "conf")

def read_config(config_dir: str = __CONFIG_DIR, overrides: tp.Optional[tp.List[str]] = None) -> OmegaConf:
    """
    :@param config_dir: path to config directory
    :@param overrides: list of overrides (e.g. ["dataset=model_eval"])
    :@param set_to_none_empty_with_warn: if True, set empty values to None and print warning
    :@return: OmegaConf object
    """
    config_dir = os.path.abspath(config_dir)
    with initialize_config_dir(config_dir=config_dir, version_base=None):
        cfg = compose(config_name="config", overrides=overrides)
        cfg = OmegaConf.create(OmegaConf.to_yaml(cfg, resolve=True))
    return cfg

def _remove_long_fields_recurse(cfg: OmegaConf) -> OmegaConf:
    """Remove long fields from config."""
    for key, value in cfg.items():
        if isinstance(value, str) and len(value) > 150:
            cfg[key] = "..."
        elif hasattr(value, "items"):
            cfg[key] = _remove_long_fields_recurse(value)
        elif isinstance(value, list):
            cfg[key] = [_remove_long_fields_recurse(x) if isinstance(x, dict) else x for x in value]
    return cfg

def _remove_long_fields(cfg: OmegaConf) -> OmegaConf:
    """Remove long fields from config."""
    cfg = deepcopy(cfg)
    return _remove_long_fields_recurse(cfg)


def pprint_config(cfg: OmegaConf, show_long_fields: bool = False) -> None:
    """Pretty print config. By default, it doesn't show long fields (str of length > 100)."""
    if not show_long_fields:
        cfg = _remove_long_fields(cfg)
    print(json.dumps(OmegaConf.to_container(cfg), indent=2, ensure_ascii=False))
