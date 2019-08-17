import os
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__.split("/")[-1])


def _cache_file(experiment, year):
    """
    Return the full path of a cache file for the given experiment and year.
    """
    root_path = os.path.dirname(os.path.realpath(__file__))
    file_name = f"comp_{experiment['dataset']}_{experiment['id']}_{year}.p"
    return f"{root_path}/cache/{file_name}"


def load_components(experiment, year):
    """
    Load a list of components from an experiment at a given year, along with
    productions from that year and their respective teams.
    """
    code = f"{experiment['dataset']}, {experiment['id']}, {year}"
    logger.info(f"Fetching components cache ({code}).")
    f = _cache_file(experiment, year)
    return pickle.load(open(f, 'rb')) if os.path.isfile(f) else None


def save_components(experiment, year, components, works_from_year):
    """
    Saves a list of components from an experiment at a given year, along with
    productions from that year and their respective teams.
    """
    code = f"{experiment['dataset']}, {experiment['id']}, {year}"
    logger.info(f"Saving components cache ({code}).")
    f = _cache_file(experiment, year)
    pickle.dump((components, works_from_year), open(f, 'wb'))
