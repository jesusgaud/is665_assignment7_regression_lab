from regression_lab.analysis import fit_regression, metrics
from regression_lab.reporting import interpretation


def test_fit_regression(sample_df):
    result = fit_regression(sample_df)
    m = metrics(result)
    assert 0 <= m["r_squared"] <= 1
    assert "C(smoker)[T.yes]" in result.coefficients["term"].tolist()
    assert "charges =" in result.equation


def test_interpretation(sample_df):
    result = fit_regression(sample_df)
    text = interpretation(result)
    assert "OLS model explains" in text
    assert "observational" in text
