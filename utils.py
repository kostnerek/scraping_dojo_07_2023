import json
import os
from consts import REQUIRED_ENVS

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

def validate_envs(envs):
    for env in REQUIRED_ENVS:
        if env not in envs:
            raise Exception(f"Environment variable {env} is missing.")