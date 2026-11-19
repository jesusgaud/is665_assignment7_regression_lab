from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper
from regression_lab.config import FORMULA

@dataclass(frozen=True)
class RegressionResult:
    model: RegressionResultsWrapper
    coefficients: pd.DataFrame
    fitted: pd.Series
    residuals: pd.Series
    equation: str
    significant_terms: list[str]


def _human_term(term: str) -> str:
    replacements = {
        "Intercept": "Intercept",
        "C(sex)[T.male]": "Sex: male (vs female)",
        "C(smoker)[T.yes]": "Smoker: yes (vs no)",
        "C(region)[T.northwest]": "Region: northwest (vs northeast)",
        "C(region)[T.southeast]": "Region: southeast (vs northeast)",
        "C(region)[T.southwest]": "Region: southwest (vs northeast)",
        "age": "Age",
        "bmi": "BMI",
        "children": "Children",
    }
    return replacements.get(term, term)


def fit_regression(df: pd.DataFrame) -> RegressionResult:
    model = smf.ols(FORMULA, data=df).fit()
    ci = model.conf_int()
    table = pd.DataFrame({
        "term": model.params.index,
        "coefficient": model.params.values,
        "std_error": model.bse.values,
        "t_stat": model.tvalues.values,
        "p_value": model.pvalues.values,
        "ci_lower": ci[0].values,
        "ci_upper": ci[1].values,
    })
    table.insert(1, "term_label", table["term"].map(_human_term))
    table["significant_0_05"] = table["p_value"] < 0.05
    significant = table.loc[(table["significant_0_05"]) & (table["term"] != "Intercept"), "term_label"].tolist()
    eq_parts = [f"charges = {model.params['Intercept']:.2f}"]
    for term, coef in model.params.items():
        if term == "Intercept":
            continue
        sign = "+" if coef >= 0 else "-"
        eq_parts.append(f" {sign} {abs(coef):.2f}*{_human_term(term)}")
    equation = "".join(eq_parts)
    return RegressionResult(
        model=model,
        coefficients=table,
        fitted=pd.Series(model.fittedvalues, name="fitted"),
        residuals=pd.Series(model.resid, name="residual"),
        equation=equation,
        significant_terms=significant,
    )


def metrics(result: RegressionResult) -> dict[str, float | int]:
    model = result.model
    rmse = float(np.sqrt(np.mean(np.square(result.residuals))))
    mae = float(np.mean(np.abs(result.residuals)))
    return {
        "nobs": int(model.nobs),
        "r_squared": float(model.rsquared),
        "adjusted_r_squared": float(model.rsquared_adj),
        "rmse": rmse,
        "mae": mae,
        "f_statistic": float(model.fvalue),
        "f_p_value": float(model.f_pvalue),
    }
