import os
import json

TRAININGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trainings.json')

def load_trainings():
    try:
        with open(TRAININGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_trainings(data):
    with open(TRAININGS_FILE, "w") as f:
        json.dump(data, f, indent=4)
