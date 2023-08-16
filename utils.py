import json
import os


def save_to_json(data_list, filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

        existing_data.extend(data_list)

        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        with open(filename, 'w') as file:
            json.dump(data_list, file, indent=4)