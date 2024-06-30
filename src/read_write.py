"""
Module for reading and writing data. Works with json and csv files. Also, provides functions for io with reports.
"""
import json
import os
import typing as tp
import logging
import pandas as pd
import csv

def _create_dir(dirname: str) -> None:
    """
    Creates directory.
    :param dirname: path to directory
    """
    if not dirname:
        logging.info(f"Directory name is empty")
        return
    if not os.path.exists(dirname):
        logging.info(f"Creating directory {dirname!r}")
        os.makedirs(dirname, exist_ok=True)

def write_reports(reports: tp.List[tp.Dict[str, tp.Any]], reports_dir: str, ignore_existing_reports: bool = False) -> None:
    """
    Writes reports to reports_dir. Creates directory if it doesn't exist.
    :param reports: list of reports
    :param reports_dir: path to reports
    :param ignore_existing_reports: whether to ignore existing reports. If not, check that for each report to be rewrited exists file with same id.
    """
    _create_dir(reports_dir)
    for report in reports:
        name = f"{report['id']}.json"
        path = os.path.join(reports_dir, name)
        if not ignore_existing_reports:
            if not os.path.exists(path):
                logging.warning(f"There is no report with id {report['id']!r} in {reports_dir!r}")
                raise ValueError(f"Report with id {report['id']!r} didn't exist in {reports_dir!r} before.")
        write_json(report, path, create_dirs=False)

def read_json(path: str) -> tp.Union[tp.Dict, tp.List]:
    """
    Reads json file.
    :param path: path to json file
    :return: json
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(data: tp.Union[tp.Dict, tp.List], path: str, create_dirs: bool = True) -> None:
    """
    Writes json file.
    :param data: data to write
    :param path: path to json file
    :param create_dirs: whether to create directory if it doesn't exist
    """
    if create_dirs:
        _create_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def append_json(path: str, data: tp.List[tp.Dict]) -> None:
    """
    Appends data to json file. If file doesn't exist, creates it.
    :param path: path to json file
    :param data: data to append
    """
    old_data = []
    if os.path.exists(path):
        old_data = read_json(path)
        assert isinstance(old_data, list), f"Expected list, got {type(old_data)} while reading {path!r}"
    
    write_json(old_data + data, path)

def read_csv(path: str) -> pd.DataFrame:
    """
    Reads csv file.
    :param path: path to csv file
    :return: csv
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = pd.read_csv(f)
    return data

def write_csv(data: pd.DataFrame, path: str, create_dirs: bool = True) -> None:
    """
    Writes csv file.
    :param data: data to write
    :param path: path to csv file
    :param create_dirs: whether to create directory if it doesn't exist
    """
    if create_dirs:
        _create_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        data.to_csv(f, index=False)

def append_csv(path: str, data: tp.List[tp.Dict]) -> None:
    """
    Appends data to csv file. If file doesn't exist, creates it and writes column names.
    :param path: path to csv file
    :param data: data to append
    """
    if not data:
        logging.warning(f"Empty data to append to {path!r}")
        return
    
    if not os.path.exists(path):
        _create_dir(os.path.dirname(path))
        with open(path, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()

    with open(path, 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writerows(data)
