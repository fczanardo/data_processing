import logging
from pathlib import Path
from typing import Any

import pandas as pd
from domain.etl import Loader

logger = logging.getLogger(__name__)

OUTPUT_ERROR_DIR = Path("output")


class DataLoader(Loader):
    def load(self, data: Any) -> None:
        df_all, parse_warnings, invalid_values, rejected_rows = data

        OUTPUT_ERROR_DIR.mkdir(exist_ok=True)

        parse_issues = [f"[PARSE WARNING] {w}" for w in parse_warnings]

        invalid_value_issues = []
        if not invalid_values.empty:
            for _, row in invalid_values.iterrows():
                details = " | ".join(f"{col}={row[col]!r}" for col in invalid_values.columns)
                invalid_value_issues.append(f"[INVALID VALUE] {details}")

        filtered_out_issues = []
        if not rejected_rows.empty:
            for _, row in rejected_rows.iterrows():
                details = " | ".join(f"{col}={row[col]!r}" for col in rejected_rows.columns)
                filtered_out_issues.append(f"[FILTERED OUT] {details}")

        if parse_issues:
            for issue in parse_issues:
                (OUTPUT_ERROR_DIR / "INVALID_parse_warnings.txt").write_text("\n".join(parse_issues), encoding="utf-8")

        if invalid_value_issues:
            for issue in invalid_value_issues:
                (OUTPUT_ERROR_DIR / "INVALID_values.txt").write_text("\n".join(invalid_value_issues), encoding="utf-8")

        if filtered_out_issues:
            for issue in filtered_out_issues:
                (OUTPUT_ERROR_DIR / "INVALID_filtered_out.txt").write_text("\n".join(filtered_out_issues), encoding="utf-8")

        total_value = df_all["VALUE"].sum()
        result_message = f"The final sum = {total_value}"
        logger.info(result_message)
        (OUTPUT_ERROR_DIR / "result.txt").write_text(result_message, encoding="utf-8")
