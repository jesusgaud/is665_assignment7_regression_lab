from __future__ import annotations
from regression_lab.analysis import RegressionResult, metrics


def interpretation(result: RegressionResult) -> str:
    m = metrics(result)
    coef = result.coefficients.set_index("term")
    smoker = coef.loc["C(smoker)[T.yes]"]
    age = coef.loc["age"]
    bmi = coef.loc["bmi"]
    sig = ", ".join(result.significant_terms) if result.significant_terms else "None"
    return (
        f"The OLS model explains {m['r_squared']:.1%} of the observed variation in insurance charges "
        f"(adjusted R-squared {m['adjusted_r_squared']:.3f}). Holding the other predictors constant, "
        f"smoking is associated with an estimated ${smoker['coefficient']:,.0f} change in charges "
        f"(p={smoker['p_value']:.3g}); each additional year of age is associated with about "
        f"${age['coefficient']:,.0f}; and each one-unit increase in BMI is associated with about "
        f"${bmi['coefficient']:,.0f}. Terms significant at alpha=0.05: {sig}. "
        "These coefficients describe statistical associations in this observational dataset and should not be interpreted as causal effects."
    )
