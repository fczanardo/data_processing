import tarfile
from pathlib import Path

import config


def extract_quarterly_output(
    archive: Path = config.ARCHIVE_PATH,
    destination: str | Path = config.EXTRACTION_DESTINATION,
) -> Path:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(path=destination)

    return destination


def extract_data():
    print("Extracting data...")
    extract_quarterly_output()
