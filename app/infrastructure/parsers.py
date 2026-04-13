import json
import logging
import warnings
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

STANDARD_COLUMNS = ["SOURCE_FILE","SESSION", "PROCESSOR", "DEPARTMENT", "TIMESTAMP", "REF", "BIN", "VALUE", "CATEGORY"]
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class FileParser(ABC):
    extension: str
    COLUMN_MAP: dict

    def parse(self, file_path: Path) -> tuple[pd.DataFrame, list[str]]:
        parse_warnings: list[str] = []
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                df = self._read(file_path)
            for w in caught:
                parse_warnings.append(f"{file_path.name}: {w.message}")
        except Exception as e:
            parse_warnings.append(f"{file_path.name}: {type(e).__name__}: {e}")
            return pd.DataFrame(columns=STANDARD_COLUMNS), parse_warnings
        df["SOURCE_FILE"] = file_path.name
        df = self._normalize(df)
        return df, parse_warnings

    def _normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns=self.COLUMN_MAP)[STANDARD_COLUMNS]
        parsed = pd.to_datetime(df["TIMESTAMP"], format="mixed", dayfirst=False, errors="coerce")
        invalid_ts = df.loc[parsed.isna() & df["TIMESTAMP"].notna(), "TIMESTAMP"].unique()
        for val in invalid_ts:
            logger.warning("Invalid TIMESTAMP value skipped: %r", val)
        df["TIMESTAMP"] = parsed.dt.strftime(TIMESTAMP_FORMAT)
        return df

    @abstractmethod
    def _read(self, file_path: Path) -> pd.DataFrame:
        ...


class SAParser(FileParser):
    extension = "csv"
    COLUMN_MAP = {
        "session_id": "SESSION",
        "processor": "PROCESSOR",
        "department": "DEPARTMENT",
        "timestamp": "TIMESTAMP",
        "ref": "REF",
        "bin": "BIN",
        "output_metric": "VALUE",
        "classification": "CATEGORY",
    }

    def _read(self, file_path: Path) -> pd.DataFrame:
        return pd.read_csv(file_path, on_bad_lines="warn")


class MDRParser(FileParser):
    extension = "mdr"
    COLUMN_MAP = {
        "session_id": "SESSION",
        "processor": "PROCESSOR",
        "department": "DEPARTMENT",
        "timestamp": "TIMESTAMP",
        "ref": "REF",
        "bin": "BIN",
        "value": "VALUE",
        "category": "CATEGORY",
    }

    def _read(self, file_path: Path) -> pd.DataFrame:
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data["entries"])
        df["session_id"] = data["session_id"]
        df["processor"] = data["processor"]
        df["department"] = data["department"]
        df["timestamp"] = data["timestamp"]
        return df


class WBParser(FileParser):
    extension = "txt"
    COLUMN_MAP = {
        "READING": "VALUE",
        "TYPE": "CATEGORY",
    }

    def _read(self, file_path: Path) -> pd.DataFrame:
        with file_path.open(encoding="utf-8") as f:
            lines = f.readlines()

        metadata = {}
        entries = []
        in_entries = False

        for line in lines:
            line = line.strip()
            if line == "---":
                in_entries = True
                continue
            if not in_entries:
                key, _, value = line.partition(": ")
                metadata[key] = value
            elif line:
                parts = {kv.split(": ")[0].strip(): kv.split(": ")[1].strip()
                         for kv in line.split(" | ")}
                entries.append(parts)

        df = pd.DataFrame(entries)
        df["SESSION"] = metadata.get("SESSION")
        df["PROCESSOR"] = metadata.get("PROCESSOR")
        df["DEPARTMENT"] = metadata.get("DEPARTMENT")
        df["TIMESTAMP"] = metadata.get("TIMESTAMP")
        return df
