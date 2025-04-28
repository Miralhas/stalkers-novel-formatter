import json
import logging
from pathlib import Path
from typing import Dict
from rich import print

logging.basicConfig(level=logging.INFO)

def load_json(file_path: Path) -> Dict:
    """Load JSON data from a file."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load JSON from {file_path}: {e}") from e

def json_to_sql():
    """loops through every *.json folder inside the ./genres_and_tags folder"""
    genres_and_tags_folder = Path("./genres_and_tags")
    
    for index, file in enumerate(genres_and_tags_folder.glob("*.json")):
        try:
            json_dict = load_json(file)
            file_name = file.name.removesuffix(".json").split("_")[1]
            insert = f"""INSERT INTO {file_name} VALUES"""
            for element in json_dict:
                insert+= f"({element["name"]}, {element["description"]}),"
            insert.removesuffix(",")
            with open(f"{genres_and_tags_folder}/{file_name}.sql", 'w', encoding='utf-8') as sql_file:
                file.write_text(insert)

        except RuntimeError as e:
            logging.error(f"Failed to process: {e}")


if __name__ == "__main__":
    json_to_sql()