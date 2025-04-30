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
    """loops through every *.json folder inside the ./genres_and_tags/sql folder"""
    genres_and_tags_folder = Path("./genres_and_tags")
    genres_and_tags_folder.mkdir(parents=True, exist_ok=True)
    sql_folder = Path(f"{genres_and_tags_folder}/sql")
    sql_folder.mkdir(parents=True, exist_ok=True)
    

    for file in genres_and_tags_folder.glob("*.json"):
        try:
            json_dict = load_json(file)
            file_name = file.name.removesuffix(".json")
            insert = f"""INSERT INTO (NAME, DESCRIPTION) VALUES"""

            for index, element in enumerate(json_dict):
                isLastElement = index == len(json_dict)-1

                insert+= f'("{element["name"].strip()}"'
                if (element["description"] is not None):
                    insert+= f', "{element["description"].strip()}"){'' if isLastElement else ','}'
                else:
                    insert+= f", null){'' if isLastElement else ','}"
                
            with open(f"{sql_folder}/{file_name}{index}.sql", 'w', encoding='utf-8') as sql_file:
                sql_file.write(insert)

        except RuntimeError as e:
            logging.error(f"Failed to process: {e}")


if __name__ == "__main__":
    json_to_sql()