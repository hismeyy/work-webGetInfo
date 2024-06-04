import json
import os


def json_write_to_file(json_data, filename):
    filepath = os.path.join(filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


def parse_file_to_map(filename):
    filepath = os.path.join(filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        map_data = json.load(file)
    return map_data
