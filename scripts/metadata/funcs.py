import json
import logging
from pathlib import Path
from typing import Dict

logging.basicConfig(level=logging.INFO)

def load_json(file_path: Path) -> Dict:
    """Load JSON data from a file."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load JSON from {file_path}: {e}") from e


def dump_json(output_path: Path, data: Dict) -> None:
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
