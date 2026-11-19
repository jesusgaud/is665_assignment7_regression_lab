from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from regression_lab.analysis import RegressionResult


def _save(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def actual_vs_fitted(df: pd.DataFrame, result: RegressionResult, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.scatter(result.fitted, df["charges"], alpha=0.55, s=28)
    lo = min(float(result.fitted.min()), float(df["charges"].min()))
    hi = max(float(result.fitted.max()), float(df["charges"].max()))
    ax.plot([lo, hi], [lo, hi], linestyle="--", linewidth=1.5)
    ax.set_title("Actual vs. Fitted Insurance Charges")
    ax.set_xlabel("Fitted charges ($)")
    ax.set_ylabel("Actual charges ($)")
    ax.grid(alpha=0.2)
    return _save(fig, path)


def residuals_vs_fitted(result: RegressionResult, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.scatter(result.fitted, result.residuals, alpha=0.55, s=28)
    ax.axhline(0, linestyle="--", linewidth=1.5)
    ax.set_title("Residuals vs. Fitted Values")
    ax.set_xlabel("Fitted charges ($)")
    ax.set_ylabel("Residual ($)")
    ax.grid(alpha=0.2)
    return _save(fig, path)


def coefficient_plot(result: RegressionResult, path: Path) -> Path:
    frame = result.coefficients[result.coefficients["term"] != "Intercept"].copy()
    frame = frame.sort_values("coefficient")
    fig, ax = plt.subplots(figsize=(9.0, 5.8))
    y = np.arange(len(frame))
    coef = frame["coefficient"].to_numpy()
    xerr = np.vstack([coef - frame["ci_lower"].to_numpy(), frame["ci_upper"].to_numpy() - coef])
    ax.errorbar(coef, y, xerr=xerr, fmt="o", capsize=4)
    ax.axvline(0, linestyle="--", linewidth=1.2)
    ax.set_yticks(y, frame["term_label"].tolist())
    ax.set_title("OLS Coefficients with 95% Confidence Intervals")
    ax.set_xlabel("Estimated change in charges ($), holding other variables constant")
    ax.grid(axis="x", alpha=0.2)
    return _save(fig, path)


def smoker_distribution(df: pd.DataFrame, path: Path) -> Path:
    groups = [df.loc[df["smoker"] == value, "charges"] for value in ["no", "yes"]]
    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    ax.boxplot(groups, tick_labels=["Non-smoker", "Smoker"], showfliers=False)
    ax.set_title("Insurance Charges by Smoking Status")
    ax.set_ylabel("Charges ($)")
    ax.grid(axis="y", alpha=0.2)
    return _save(fig, path)
