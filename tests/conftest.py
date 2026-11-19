import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Return deterministic, non-collinear insurance-like regression test data."""
    rng = np.random.default_rng(665)
    n_rows = 120

    age = rng.integers(18, 65, size=n_rows)
    bmi = np.clip(rng.normal(loc=30.5, scale=5.8, size=n_rows), 17.0, 46.0)
    children = rng.integers(0, 5, size=n_rows)
    sex = rng.choice(["female", "male"], size=n_rows)
    smoker = rng.choice(["no", "yes"], size=n_rows, p=[0.78, 0.22])
    region = rng.choice(
        ["northeast", "northwest", "southeast", "southwest"],
        size=n_rows,
    )

    noise = rng.normal(loc=0.0, scale=1200.0, size=n_rows)
    charges = (
        750
        + age * 235
        + bmi * 155
        + children * 425
        + np.where(smoker == "yes", 21_500, 0)
        + np.where(sex == "male", 350, 0)
        + noise
    )

    return pd.DataFrame(
        {
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region,
            "charges": charges,
        }
    )
