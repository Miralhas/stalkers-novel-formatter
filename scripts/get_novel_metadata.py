import argparse
from pathlib import Path

from metadata.sources import NovelUpdatesSource, WebnovelDotComSource

if __name__ == "__main__":

    root = Path("C:/Users/bob/Desktop/NovelOutput/AcademysSilverGatekeeper")
    source = NovelUpdatesSource(root, "academys-silver-gatekeeper/")
    source.execute()