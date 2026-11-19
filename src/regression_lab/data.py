from __future__ import annotations
import io
import urllib.request
from pathlib import Path
import pandas as pd
from regression_lab.config import DATA_FILE, DATA_URL, REQUIRED_COLUMNS


def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    clean = df[list(sorted(REQUIRED_COLUMNS))].copy()
    for col in ["age", "bmi", "children", "charges"]:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")
    for col in ["sex", "smoker", "region"]:
        clean[col] = clean[col].astype("string").str.strip().str.lower()
    clean = clean.dropna().drop_duplicates().reset_index(drop=True)
    if clean.empty:
        raise ValueError("Dataset contains no usable rows after validation.")
    return clean


def download_dataset(url: str = DATA_URL, destination: Path = DATA_FILE, timeout: int = 30) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        payload = response.read()
    df = pd.read_csv(io.BytesIO(payload))
    clean = validate_dataset(df)
    clean.to_csv(destination, index=False)
    return destination


def load_dataset(path: Path = DATA_FILE, allow_download: bool = True) -> pd.DataFrame:
    if not path.exists():
        if not allow_download:
            raise FileNotFoundError(f"Dataset not found: {path}")
        download_dataset(destination=path)
    return validate_dataset(pd.read_csv(path))


def dataset_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Observations", len(df)),
        ("Predictors", 6),
        ("Dependent variable", "charges"),
        ("Dependent variable type", "Continuous numeric"),
        ("Regression type", "Multiple linear regression (OLS)"),
        ("Missing values", int(df.isna().sum().sum())),
    ]
    return pd.DataFrame(rows, columns=["Item", "Value"])
