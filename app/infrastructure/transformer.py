import logging
import os
from pathlib import Path
from typing import Any
import pandas as pd
from domain.etl import Transformer
from infrastructure.parsers import MDRParser, SAParser, WBParser

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

_extraction_destination = os.environ.get("EXTRACTION_DESTINATION")
if not _extraction_destination:
    raise EnvironmentError("Environment variable 'EXTRACTION_DESTINATION' is required but was not set.")

DEFAULT_DIR = Path(_extraction_destination)
DEFAULT_OUTPUT = Path(__file__).parent.parent.parent / "output.csv"
PARSERS = [SAParser(), MDRParser(), WBParser()]

# Allowed values per column (set). None means no filter.
COLUMN_FILTERS: dict[str, set | None] = {
    "SESSION":    None,
    "PROCESSOR":  {"James.L", "Nora.K", "Arthur.B", "Lena.P", "Felix.G", "Dr.Voss", "Clara.M"},
    "DEPARTMENT": {"MDR", "SA", "WB"},
    "TIMESTAMP":  None,
    "REF":        None,
    "BIN":        {"GR", "BL", "AX", "SP"},
    "VALUE":      None,
    "CATEGORY":   {"alpha", "beta", "gamma", "delta"},
}

TIMESTAMP_MIN = pd.Timestamp("2025-10-01")
TIMESTAMP_MAX = pd.Timestamp("2025-12-31 23:59:59")


def consolidate_all(
    dir_path: Path = DEFAULT_DIR,
    parsers=PARSERS,
) -> tuple[pd.DataFrame, list[str]]:
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

def preview_by_type(
    dir_path: Path = DEFAULT_DIR,
    parsers=PARSERS,
    n: int = 5,
) -> None:
    for parser in parsers:
        files = sorted(dir_path.rglob(f"*.{parser.extension}"))
        if not files:
            print(f"\n[{parser.extension.upper()}] No files found.\n")
            continue

        frames = [parser.parse(f)[0] for f in files]
        df = pd.concat(frames, ignore_index=True)


def apply_filters(
    df: pd.DataFrame,
    filters: dict[str, set | None] = COLUMN_FILTERS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask = pd.Series(True, index=df.index)

    # Set-based filters
    for col, allowed in filters.items():
        if allowed is not None and col in df.columns:
            mask &= df[col].isin(allowed)

    # VALUE: must be positive
    if "VALUE" in df.columns:
        mask &= df["VALUE"].notna() & (df["VALUE"] > 0)

    # TIMESTAMP: must be within Q4 2025
    if "TIMESTAMP" in df.columns:
        ts = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
        mask &= ts.notna() & ts.between(TIMESTAMP_MIN, TIMESTAMP_MAX)

    rejected = df[~mask].copy()
    accepted = df[mask].copy()
    return accepted, rejected


def validate_value_column(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    numeric = pd.to_numeric(df["VALUE"], errors="coerce")
    invalid = df[numeric.isna() & df["VALUE"].notna()].copy()
    df["VALUE"] = numeric
    return df, invalid


def transform_call() -> tuple[pd.DataFrame, list[str], pd.DataFrame, pd.DataFrame]:
    preview_by_type()
    df_all, parse_warnings = consolidate_all()
    df_all, invalid_values = validate_value_column(df_all)
    df_all, rejected_rows = apply_filters(df_all)

    return df_all, parse_warnings, invalid_values, rejected_rows


class QuarterlyDataTransformer(Transformer):
    def transform(self, data_path: Path) -> Any:
        return transform_call()
