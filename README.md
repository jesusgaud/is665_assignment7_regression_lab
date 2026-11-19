# IS 665 Assignment 7 - Regression Analysis Lab

A reproducible Windows-friendly Streamlit application for **Assignment 7: Regression Analysis**.

## Dataset selected

**Medical Cost Personal / Insurance**. The dependent variable is `charges` (continuous). Predictors are `age`, `bmi`, `children`, `sex`, `smoker`, and `region`.

Dataset page: https://www.kaggle.com/datasets/mirichoi0218/insurance

The application downloads the public CSV mirror on first run and caches it under `data/insurance.csv`.

## Why this dataset

- 1,338 observations and only six predictors.
- Continuous dependent variable fits the linear-regression assignment directly.
- Mixed numeric/categorical predictors produce an interpretable multiple-regression model.
- Coefficients, p-values, R-squared, confidence intervals, and practical significance are easy to explain.

## One-click Windows run

1. Install Python 3.11-3.15. Python 3.15 is recommended.
2. Clone or download this repository.
3. Double-click `START_ASSIGNMENT.bat`.
4. The launcher creates `.venv`, installs dependencies, and starts Streamlit.
5. Open the Local URL (normally http://localhost:8501).
6. Click **Run Regression Analysis**.
7. Review the **Results** tab and click **Export Result Package**.
8. The exported ZIP can be re-opened under **Import Result Package**.

## Manual VS Code run

```powershell
cd C:\python_code\is665_assignment7_regression_lab
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
streamlit run app.py
```

## Quality checks

```powershell
ruff check .
mypy src
pytest --cov=regression_lab --cov-report=term-missing --cov-fail-under=80
```

## Assignment mapping

The application produces:

- problem formulation and variable definitions;
- OLS multiple-linear-regression specification;
- coefficients and p-values;
- R-squared and adjusted R-squared;
- regression equation;
- significant-factor interpretation;
- actual-vs-fitted plot;
- residual plot;
- coefficient confidence-interval plot;
- smoking-status charge comparison;
- portable result ZIP for use in the final Word report.

## Important interpretation note

This is an observational public dataset. Regression coefficients are interpreted as statistical associations, not causal effects.
