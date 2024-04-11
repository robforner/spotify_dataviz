import os
import json

selections_file = 'selections.json'
otherfile = 'otherfile.json'

# Function to load selections from a file
def load_selections(file):
    if os.path.exists(file):
        with open(file, 'r') as file:
            selections = json.load(file)
        return selections

# Function to save selections to a file
def save_selections(savefile, selections):
    with open(savefile, 'w') as file:
        json.dump(selections, file)

def clear_selections(file):
    with open(file, 'w') as file:
        json.dump([], file)  # Overwrite with an empty list

def make_file(filepath):
    with open(filepath, 'w') as file:
        json.dump([], file)