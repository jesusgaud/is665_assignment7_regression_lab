from __future__ import annotations
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"
DATA_FILE = DATA_DIR / "insurance.csv"
DATA_URL = "https://raw.githubusercontent.com/MainakRepositor/Datasets/master/insurance.csv"
DATASET_NAME = "Medical Cost Personal / Insurance"
DATASET_SOURCE = "Kaggle Medical Cost Personal Datasets (public mirror cached from GitHub)"
KAGGLE_DATASET_URL = "https://www.kaggle.com/datasets/mirichoi0218/insurance"
TARGET = "charges"
NUMERIC_FEATURES = ["age", "bmi", "children"]
CATEGORICAL_FEATURES = ["sex", "smoker", "region"]
FORMULA = "charges ~ age + bmi + children + C(sex) + C(smoker) + C(region)"
REQUIRED_COLUMNS = {TARGET, *NUMERIC_FEATURES, *CATEGORICAL_FEATURES}
