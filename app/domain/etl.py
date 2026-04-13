from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Extractor(ABC):
    @abstractmethod
    def extract(self) -> Path:
        """Extract raw data from source. Returns path to extracted files."""


class Transformer(ABC):
    @abstractmethod
    def transform(self, data_path: Path) -> Any:
        """Apply transformations to the extracted data."""


class Loader(ABC):
    @abstractmethod
    def load(self, data: Any) -> None:
        """Persist the transformed data to its destination."""


class ETLPipeline:
    def __init__(self, extractor: Extractor, transformer: Transformer, loader: Loader) -> None:
        self._extractor = extractor
        self._transformer = transformer
        self._loader = loader

    def run(self) -> None:
        data_path = self._extractor.extract()
