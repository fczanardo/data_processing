import pandas as pd

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


def validate_value_column(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    numeric = pd.to_numeric(df["VALUE"], errors="coerce")
    invalid = df[numeric.isna() & df["VALUE"].notna()].copy()
    df = df.copy()
    df["VALUE"] = numeric
    return df, invalid


def apply_filters(
    df: pd.DataFrame,
    filters: dict[str, set | None] = COLUMN_FILTERS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask = pd.Series(True, index=df.index)

    for col, allowed in filters.items():
        if allowed is not None and col in df.columns:
            mask &= df[col].isin(allowed)

    if "VALUE" in df.columns:
        mask &= df["VALUE"].notna() & (df["VALUE"] > 0)

    if "TIMESTAMP" in df.columns:
        ts = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
        mask &= ts.notna() & ts.between(TIMESTAMP_MIN, TIMESTAMP_MAX)

    return df[mask].copy(), df[~mask].copy()
