"""Module containing helper functions to conveniently load the blue ark data into dictionaries of pandas data frames."""

import os

import pandas as pd


def get_all_file_paths(dir_path):
    """Creates dictionary holding file name keys and absolute path values for all files in a dir.

    Arguments
    ---------
    dir_path: absolute dir path holding the blue ark excel data files
    """
    return {file_name: os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)}


def load_data_files(file_name_dict):
    """Creates a dict holding file name keys and pandas data frames as values.

    Arguments
    ---------
    file_name_dict: dictionary with file_name, file_path key value pairs returned by get_all_file_paths

    Returns
    -------
    all_data: dict organized in file_names and every file name has a dict with sheet name, pandas df key value pair
    """

    all_data = {}

    for file_name, file_path in file_name_dict.items():
        all_data[file_name] = {}
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names

        for sheet in sheet_names:
            all_data[file_name][sheet] = pd.read_excel(xls, sheet)

    return all_data
