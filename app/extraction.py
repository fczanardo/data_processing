import tarfile
from pathlib import Path

print("Extraction module imported successfully.")

def extract_quarterly_output(destination: str | Path = "./file") -> Path:
    archive = Path(__file__).parent.parent.parent / "file" / "quarterly_output.tar.gz"

    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(path=destination)

    return destination

def extract_data():
    print("Extracting data...")
    extract_quarterly_output()
