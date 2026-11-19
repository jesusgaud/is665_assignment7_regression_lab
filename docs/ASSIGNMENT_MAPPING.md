# Assignment 7 Mapping

## 1. Problem formulation

**Question:** Which demographic and lifestyle factors are associated with individual medical insurance charges?

- Dependent variable: `charges`
- Data type: continuous numeric
- Independent variables: `age`, `bmi`, `children`, `sex`, `smoker`, `region`
- Regression: multiple linear regression (OLS)

## 2. Python code

The full Python implementation is in `src/regression_lab/` and `app.py`.

## 3. Results

The exported result package contains `coefficients.csv`, `metrics.json`, and `model_summary.txt`, plus PNG figures.

## 4. Interpretation

The application identifies terms significant at alpha=0.05 and creates a report-ready narrative. Interpret coefficients as associations, not causation.
