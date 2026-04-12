from pathlib import Path
from typing import Any

from domain.etl import Transformer


class QuarterlyDataTransformer(Transformer):
    def transform(self, data_path: Path) -> Any:
        pass
