import pytest
from regression_lab.data import dataset_summary, validate_dataset


def test_validate_dataset(sample_df):
    clean = validate_dataset(sample_df)
    assert len(clean) == len(sample_df)
    assert clean["charges"].dtype.kind in "fi"


def test_validate_dataset_missing_column(sample_df):
    with pytest.raises(ValueError):
        validate_dataset(sample_df.drop(columns=["charges"]))


def test_dataset_summary(sample_df):
    summary = dataset_summary(sample_df)
    assert "Continuous numeric" in summary["Value"].astype(str).tolist()
