import json
from termcolor import colored


def read_json(filename: str) -> dict:
    filepath = f"json/{filename}"
    with open(filepath, "r", encoding="utf8") as infile:
        return json.load(infile)


def write_json(filename: str, data: dict):
    filepath = f"json/{filename}"
    with open(filepath, "w", encoding="utf8") as outfile:
        json.dump(data, outfile)
        print(colored(f"Saved {filepath}.", "green"))
