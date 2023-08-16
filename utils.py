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

def validate_envs(envs):
    required_envs = ['INPUT_URL', 'OUTPUT_FILE']
    for env in required_envs:
        if env not in envs:
            raise Exception(f"Environment variable {env} is missing.")