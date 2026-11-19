from __future__ import annotations
import io
import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any
import pandas as pd
from regression_lab.analysis import RegressionResult, metrics
from regression_lab.config import RESULTS_DIR
from regression_lab.plots import actual_vs_fitted, coefficient_plot, residuals_vs_fitted, smoker_distribution
from regression_lab.reporting import interpretation


def _safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.infolist():
        target = (destination / member.filename).resolve()
        if root not in target.parents and target != root:
            raise ValueError("Unsafe result package path detected.")
    archive.extractall(destination)


def create_result_package(df: pd.DataFrame, result: RegressionResult, run_id: str) -> tuple[Path, Path]:
    run_dir = RESULTS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    m = metrics(result)
    (run_dir / "metrics.json").write_text(json.dumps(m, indent=2), encoding="utf-8")
    result.coefficients.to_csv(run_dir / "coefficients.csv", index=False)
    pd.DataFrame({"actual": df["charges"], "fitted": result.fitted, "residual": result.residuals}).to_csv(
        run_dir / "fitted_and_residuals.csv", index=False
    )
    (run_dir / "regression_equation.txt").write_text(result.equation, encoding="utf-8")
    (run_dir / "interpretation.txt").write_text(interpretation(result), encoding="utf-8")
    (run_dir / "model_summary.txt").write_text(result.model.summary().as_text(), encoding="utf-8")
    actual_vs_fitted(df, result, run_dir / "actual_vs_fitted.png")
    residuals_vs_fitted(result, run_dir / "residuals_vs_fitted.png")
    coefficient_plot(result, run_dir / "coefficients_ci.png")
    smoker_distribution(df, run_dir / "charges_by_smoker.png")
    manifest = {
        "package_type": "IS665 Assignment 7 Regression Result",
        "run_id": run_id,
        "files": sorted(p.name for p in run_dir.iterdir() if p.is_file()),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    zip_path = RESULTS_DIR / f"{run_id}_result_package.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in run_dir.iterdir():
            if file.is_file():
                archive.write(file, arcname=file.name)
    return run_dir, zip_path


def inspect_result_package(package_bytes: bytes) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        with zipfile.ZipFile(io.BytesIO(package_bytes), "r") as archive:
            _safe_extract(archive, root)
        required = ["metrics.json", "coefficients.csv", "model_summary.txt", "interpretation.txt", "manifest.json"]
        missing = [name for name in required if not (root / name).exists()]
        if missing:
            raise ValueError(f"Invalid result package; missing: {missing}")
        metrics_payload = json.loads((root / "metrics.json").read_text(encoding="utf-8"))
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        coeff = pd.read_csv(root / "coefficients.csv")
        return {
            "metrics": metrics_payload,
            "manifest": manifest,
            "coefficients": coeff,
            "summary": (root / "model_summary.txt").read_text(encoding="utf-8"),
            "interpretation": (root / "interpretation.txt").read_text(encoding="utf-8"),
            "equation": (root / "regression_equation.txt").read_text(encoding="utf-8") if (root / "regression_equation.txt").exists() else "",
            "images": {name: (root / name).read_bytes() for name in ["actual_vs_fitted.png", "residuals_vs_fitted.png", "coefficients_ci.png", "charges_by_smoker.png"] if (root / name).exists()},
        }
