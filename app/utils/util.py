import json
import os


def read_data():
    basedir = os.path.abspath(os.path.dirname(__file__))

    with open('{}/imdb_sample_data.json'.format(basedir)) as file:
        data = json.load(file)
    return data
