import logging
from pathlib import Path
from typing import Any

import pandas as pd
from domain.etl import Transformer
from infrastructure.parsers import MDRParser, SAParser, WBParser
from infrastructure.validators import apply_filters, validate_value_column

logger = logging.getLogger(__name__)

_DEFAULT_PARSERS = [SAParser(), MDRParser(), WBParser()]


def _consolidate(dir_path: Path, parsers=_DEFAULT_PARSERS) -> tuple[pd.DataFrame, list[str]]:
    frames = []
    all_parse_warnings: list[str] = []
    for parser in parsers:
        for file_path in sorted(dir_path.rglob(f"*.{parser.extension}")):
            df, parse_warnings = parser.parse(file_path)
            frames.append(df)
            all_parse_warnings.extend(parse_warnings)

    if not frames:
        raise ValueError(f"No matching files found in: {dir_path}")

    return pd.concat(frames, ignore_index=True), all_parse_warnings


class QuarterlyDataTransformer(Transformer):
    def __init__(self, parsers=None) -> None:
        self._parsers = parsers or _DEFAULT_PARSERS

    def transform(self, data_path: Path) -> Any:
        df, parse_warnings = _consolidate(data_path, self._parsers)
        df, invalid_values = validate_value_column(df)
        df, rejected_rows = apply_filters(df)
        return df, parse_warnings, invalid_values, rejected_rows

