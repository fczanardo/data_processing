import logging
import tarfile
from pathlib import Path

import config
from domain.etl import Extractor
from exceptions import ArchiveNotFoundError, ExtractionError

logger = logging.getLogger(__name__)


class TarGzExtractor(Extractor):
    def __init__(self, archive: Path = config.ARCHIVE_PATH, destination: Path = config.EXTRACTION_DESTINATION) -> None:
        self._archive = archive
        self._destination = destination

    def extract(self) -> Path:
        if not self._archive.exists():
            raise ArchiveNotFoundError(f"Archive not found: {self._archive}")

        self._destination.mkdir(parents=True, exist_ok=True)

        try:
            with tarfile.open(self._archive, "r:gz") as tar:
                tar.extractall(path=self._destination)
        except tarfile.TarError as e:
            raise ExtractionError(f"Failed to extract archive: {e}") from e

        logger.info("Extraction completed successfully: %s → %s", self._archive, self._destination)
        return self._destination
