from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from regression_lab.analysis import fit_regression, metrics
from regression_lab.config import DATASET_NAME, FORMULA, KAGGLE_DATASET_URL
from regression_lab.data import dataset_summary, load_dataset
from regression_lab.reporting import interpretation
from regression_lab.storage import create_result_package, inspect_result_package

st.set_page_config(
    page_title="IS 665 Assignment 7 - Regression Analysis Lab",
    page_icon="📈",
    layout="wide",
)

st.title("IS 665 Assignment 7 - Regression Analysis Lab")
st.caption(
    "Reproducible multiple linear regression with statistical inference, "
    "diagnostics, and portable result packages."
)

run_tab, results_tab, import_tab, methodology_tab = st.tabs(
    ["Run Analysis", "Results", "Import Result Package", "Methodology"]
)


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    return load_dataset()


def _coefficient_display(coefficients: pd.DataFrame) -> pd.DataFrame:
    """Return the assignment-facing coefficient table in a consistent layout."""
    columns = [
        "term_label",
        "coefficient",
        "p_value",
        "ci_lower",
        "ci_upper",
        "significant_0_05",
    ]
    missing = [column for column in columns if column not in coefficients.columns]
    if missing:
        raise ValueError(f"Coefficient table is missing required columns: {missing}")
    return coefficients[columns].copy()


def _render_coefficient_table(coefficients: pd.DataFrame) -> None:
    display = _coefficient_display(coefficients)
    styled = display.style.format(
        {
            "coefficient": "${:,.2f}",
            "p_value": "{:.4g}",
            "ci_lower": "${:,.2f}",
            "ci_upper": "${:,.2f}",
        }
    )
    st.dataframe(styled, hide_index=True, width="stretch")


def _render_diagnostic_figures(images: dict[str, Any]) -> None:
    """Render live and imported figures with the exact same 2x2 layout."""
    figure_spec = [
        ("actual_vs_fitted.png", "Actual vs. fitted charges"),
        ("residuals_vs_fitted.png", "Residuals vs. fitted values"),
        ("coefficients_ci.png", "Coefficient estimates and 95% confidence intervals"),
        ("charges_by_smoker.png", "Observed charges by smoking status"),
    ]

    st.subheader("Diagnostic Figures")
    first_row = st.columns(2)
    second_row = st.columns(2)
    containers = [first_row[0], first_row[1], second_row[0], second_row[1]]

    for container, (filename, caption) in zip(containers, figure_spec, strict=True):
        image = images.get(filename)
        if image is None:
            container.warning(f"{caption} is not available in this result package.")
            continue
        container.image(image, caption=caption, width="stretch")


def _render_results_view(
    *,
    metric_values: dict[str, float],
    equation: str,
    coefficients: pd.DataFrame,
    interpretation_text: str,
    images: dict[str, Any],
    summary_text: str,
    export_path: str | None = None,
) -> None:
    """Single presentation path for both live and imported regression results."""
    cols = st.columns(4)
    cols[0].metric("R²", f"{metric_values['r_squared']:.3f}")
    cols[1].metric("Adjusted R²", f"{metric_values['adjusted_r_squared']:.3f}")
    cols[2].metric("RMSE", f"${metric_values['rmse']:,.0f}")
    cols[3].metric("Model p-value", f"{metric_values['f_p_value']:.2e}")

    st.subheader("Regression Equation")
    st.code(equation)

    st.subheader("Coefficients and p-values")
    _render_coefficient_table(coefficients)

    st.subheader("Interpretation")
    st.write(interpretation_text)

    _render_diagnostic_figures(images)

    with st.expander("Full statsmodels OLS summary"):
        st.text(summary_text)

    if export_path is not None:
        with open(export_path, "rb") as handle:
            st.download_button(
                "Export Result Package",
                handle.read(),
                file_name=Path(export_path).name,
                mime="application/zip",
                width="stretch",
            )


try:
    df = get_data()
except Exception as exc:
    st.error("The dataset could not be loaded automatically.")
    st.code(str(exc))
    st.info(
        "Check your internet connection and rerun. The application downloads "
        "the public insurance.csv dataset once and caches it under data/insurance.csv."
    )
    st.stop()

with st.sidebar:
    st.header("Analysis Contract")
    st.write(f"**Dataset:** {DATASET_NAME}")
    st.write(f"**Observations:** {len(df):,}")
    st.write("**Dependent variable:** charges")
    st.write("**Type:** continuous numeric")
    st.write("**Method:** OLS multiple linear regression")
    st.write("**Significance level:** 0.05")
    st.caption(
        "The regression specification is fixed so the submitted output is reproducible."
    )

with run_tab:
    st.header("Run the Regression")
    st.write(
        "The application models individual medical insurance charges using age, BMI, "
        "number of children, sex, smoking status, and region."
    )
    st.dataframe(dataset_summary(df), hide_index=True, width="stretch")
    with st.expander("Regression specification"):
        st.code(FORMULA)
        st.write(
            "Categorical predictors are dummy-coded automatically. Reference groups "
            "are female, non-smoker, and northeast."
        )
    if st.button("Run Regression Analysis", type="primary", width="stretch"):
        with st.spinner("Fitting OLS regression and creating result artifacts..."):
            result = fit_regression(df)
            run_id = datetime.now(timezone.utc).strftime(
                "assignment7_ols_%Y%m%dT%H%M%SZ"
            )
            run_dir, zip_path = create_result_package(df, result, run_id)
            st.session_state["result"] = result
            st.session_state["run_dir"] = str(run_dir)
            st.session_state["zip_path"] = str(zip_path)
        st.success("Regression completed successfully. Open the Results tab.")

with results_tab:
    result = st.session_state.get("result")
    if result is None:
        st.info("Run the regression from the Run Analysis tab first.")
    else:
        run_dir = Path(st.session_state["run_dir"])
        live_images: dict[str, Any] = {
            "actual_vs_fitted.png": str(run_dir / "actual_vs_fitted.png"),
            "residuals_vs_fitted.png": str(run_dir / "residuals_vs_fitted.png"),
            "coefficients_ci.png": str(run_dir / "coefficients_ci.png"),
            "charges_by_smoker.png": str(run_dir / "charges_by_smoker.png"),
        }
        _render_results_view(
            metric_values=metrics(result),
            equation=result.equation,
            coefficients=result.coefficients,
            interpretation_text=interpretation(result),
            images=live_images,
            summary_text=result.model.summary().as_text(),
            export_path=st.session_state["zip_path"],
        )

with import_tab:
    st.header("Review an Exported Result Package")
    st.write(
        "Upload a result package generated by this application. This lets the "
        "professor or student reopen the exact regression output without rerunning the model."
    )
    uploaded = st.file_uploader("Import result package", type=["zip"])
    if uploaded is not None and st.button("Load Result Package"):
        try:
            payload = inspect_result_package(uploaded.getvalue())
            st.session_state["imported_payload"] = payload
        except Exception as exc:
            st.error(f"Could not import result package: {exc}")

    payload = st.session_state.get("imported_payload")
    if payload:
        _render_results_view(
            metric_values=payload["metrics"],
            equation=payload["equation"],
            coefficients=payload["coefficients"],
            interpretation_text=payload["interpretation"],
            images=payload["images"],
            summary_text=payload["summary"],
        )

with methodology_tab:
    st.header("Methodology & Assignment Mapping")
    st.markdown(
        f"""
**Problem formulation**  
Dependent variable: `charges` (continuous numeric).  
Independent variables: `age`, `bmi`, `children`, `sex`, `smoker`, and `region`.  
Regression type: multiple linear regression estimated by ordinary least squares (OLS).

**Model specification**  
`{FORMULA}`

**Why OLS?**  
The dependent variable is continuous, so linear regression directly estimates how each predictor is associated with expected insurance charges while holding the other predictors constant.

**Required assignment outputs**  
The Results tab provides coefficients, p-values, R², adjusted R², the regression equation, statistical interpretation, and diagnostic charts. The exported ZIP preserves these outputs for the Word submission.

**Dataset**  
Medical Cost Personal / Insurance dataset: {KAGGLE_DATASET_URL}
"""
    )
