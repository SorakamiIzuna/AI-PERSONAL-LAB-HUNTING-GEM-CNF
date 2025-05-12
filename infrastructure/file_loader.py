import json

def load_grid_from_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["grid"]
