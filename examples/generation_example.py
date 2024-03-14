# SETUP
import os
import sys
import logging
logging.basicConfig(level=logging.WARNING)

root_dir = os.path.abspath(os.path.join(__file__, '../' * 2))
sys.path.append(root_dir)
logging.info(f"Added {root_dir!r} to PYTHONPATH")

# IMPORTS
import typing as tp
import click
from omegaconf import OmegaConf
from tqdm import tqdm
import pandas as pd

from src.config_helpers import read_config, pprint_config
from src.read_write import read_json, write_json, append_json
from src.loggers import get_colorful_logger

from src.api.api import OpenAIApi
from src.api.prompter import TemplatePrompter, Prompter

from src.api.handler.response_processors import CodeBlockExtractorProcessor
from src.api.handler.response_validators import JsonResponseValidator
from src.api.handler.handler import GenerationHandler

logger = get_colorful_logger(__name__, level=logging.INFO)
ReportType = tp.Dict[str, tp.Any]

def form_request(word: tp.Dict, prompter: Prompter, generator_handler: GenerationHandler) -> tp.Optional[str]:
    """
    Forms request to API.
    :param word: word
    :param prompter: Prompter
    :return: request (None if failed)
    """
    prompt = prompter.get_prompt(**word)
    result = generator_handler.generate(prompt)
    return result

def start_generating(dataset_cfg: OmegaConf,
                     generator_handler: GenerationHandler,
                     words: tp.List[tp.Dict],
                     prompter: Prompter) -> tp.Tuple[tp.List, tp.List]:
    """
    Starts generating.
    :param generator_handler: GenerationHandler
    :param words: each word has `word` and `translation` fields
    :param prompter: Prompter
    :return: Generated results and skipped reports ids
    """
    results = []
    keys_to_be_saved = dataset_cfg.keys_to_be_saved
    for word in tqdm(words):
        result = form_request(word, prompter, generator_handler)

        result_dict = {
            **{key: word[key] for key in keys_to_be_saved},
            'result': result
        }
        results.append(result_dict)  

    return results

def save_results(results: tp.List, skipped_reports_ids: tp.List, result_cfg: OmegaConf) -> None:
    """
    Saves results.
    :param results: results
    :param skipped_reports_ids: skipped reports ids
    :param result_cfg: result config
    """
    result_file_raw = result_cfg.result_file_raw

    if skipped_reports_ids:
        skipped_file = result_cfg.skipped_file
        write_json(path=skipped_file, data=skipped_reports_ids)
        logger.warning(f"Skipped reports: {len(skipped_reports_ids)}. Saved to {skipped_file!r}")

    append_json(path=result_file_raw, data=results)
    logger.info(f"Saved results to {result_file_raw}")

def get_generation_handler(cfg: OmegaConf) -> GenerationHandler:
    """
    Returns generation handler.
    :param cfg: configuration
    :return: generation handler
    """
    n_attempts = cfg.generate.n_attempts
    sleep_time = cfg.generate.sleep_time

    api_key = read_json(cfg.secrets)['openai_token']
    model_name = cfg.model.model

    api = OpenAIApi(api_key=api_key, model=model_name)
    error_handlers = []  # get_too_many_requests_error_handler(sleep_time=sleep_time)
    response_processors = [CodeBlockExtractorProcessor()]
    response_validators = [JsonResponseValidator()]
    generation_handler = GenerationHandler(
        generator=api,
        n_attempts=n_attempts,
        error_handlers=error_handlers,
        response_processors=response_processors,
        response_validators=response_validators
    )
    return generation_handler

def get_relevant_words(cfg: OmegaConf) -> tp.List[ReportType]:
    """
    Returns relevant words in convenient format.
    :param cfg: configuration
    :return: relevant reports
    """
    words_df = pd.read_csv(cfg.dataset.words_file)
    return words_df.to_dict(orient='records')

def generate_and_save(cfg: OmegaConf) -> None:
    """
    Generates and saves baseline predictions. Clears results file so that it doesn't contain old results.
    In case of existing skipped reports file, use only reports from it.
    :param cfg: configuration
    """
    words = get_relevant_words(cfg)

    prompter = TemplatePrompter(cfg.prompt.template)
    generator_handler = get_generation_handler(cfg)


    results = start_generating(dataset_cfg=cfg.dataset, generator_handler=generator_handler,
                                words=words, prompter=prompter)
    write_json(data=results, path=cfg.dataset.result_raw)

def set_additional_attributes(cfg: OmegaConf, n_attempts: int, sleep_time: int, n_relaunches: int) -> None:
    """
    Sets additional attributes to config.
    :param cfg: configuration
    :param n_attempts: number of attempts to generate response
    :param sleep_time: time to sleep in seconds
    :param n_relaunches: number of relaunches
    """
    cfg.generate = OmegaConf.create()
    cfg.generate.n_attempts = n_attempts
    cfg.generate.sleep_time = sleep_time
    cfg.generate.n_relaunches = n_relaunches

@click.command()
@click.option("--n_attempts", default=2, help="Number of attempts to generate response (default: 5)")
@click.option("--n_relaunches", default=1, help="Number of relaunches of the whole pipeline (default: 2)")
@click.option("--sleep_time", default=3600 + 100, help="Time to sleep in seconds (default: 600)")
@click.option("--verbose", "-v", is_flag=True, help="Whether to print config")
@click.option("--setup", type=str, help="Name of setup config")
def main(n_attempts: int, n_relaunches: int, sleep_time: int, verbose: bool, setup: str) -> None:
    cfg: OmegaConf = read_config(overrides=[f"setup={setup}"])
    set_additional_attributes(cfg, n_attempts, sleep_time, n_relaunches)
    if verbose:
        pprint_config(cfg)
    generate_and_save(cfg)

if __name__ == "__main__":
    main()
