import regression_lab.storage as storage
from regression_lab.analysis import fit_regression


def test_package_roundtrip(sample_df, tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "RESULTS_DIR", tmp_path)
    result = fit_regression(sample_df)
    run_dir, zip_path = storage.create_result_package(sample_df, result, "test_run")
    assert (run_dir / "coefficients.csv").exists()
    assert zip_path.exists()
    payload = storage.inspect_result_package(zip_path.read_bytes())
    assert "r_squared" in payload["metrics"]
    assert not payload["coefficients"].empty
    assert "Actual vs" not in payload["interpretation"] or isinstance(payload["interpretation"], str)
