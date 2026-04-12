import os
from pathlib import Path

_archive_path = os.environ.get("QUARTERLY_ARCHIVE_PATH")
if not _archive_path:
    raise EnvironmentError(
        "Environment variable 'QUARTERLY_ARCHIVE_PATH' is required but was not set."
    )
ARCHIVE_PATH = Path(_archive_path)

EXTRACTION_DESTINATION = Path(
    os.environ.get("EXTRACTION_DESTINATION", "./file")
)
