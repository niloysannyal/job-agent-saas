"""
Tests for TeX Live compilation service and /compile-texlive endpoint.
"""
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_compile_texlive_endpoint_when_compiler_unavailable():
    """When TeX Live is not on PATH, the endpoint gracefully returns compiler_available=False."""
    with patch("app.services.cv_tailor.texlive_compiler.TeXLiveCompilerService.find_compiler", return_value=None):
        resp = client.post(
            "/api/v1/profile/compile-texlive",
            json={
                "latex_source": "\\documentclass{article}\\begin{document}Hello\\end{document}",
                "account_id": "test-account-123",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is False
        assert data["compiler_available"] is False
        assert "No TeX Live compiler" in data["error"]


def test_compile_texlive_endpoint_mock_success():
    """When TeX Live compiles successfully, returns PDF base64 and logs."""
    fake_pdf = b"%PDF-1.4 fake pdf content"
    with patch("app.services.cv_tailor.texlive_compiler.TeXLiveCompilerService.find_compiler", return_value="pdflatex"), \
         patch("app.services.cv_tailor.texlive_compiler.subprocess.run") as mock_run, \
         patch("os.path.exists", return_value=True), \
         patch("os.path.getsize", return_value=len(fake_pdf)), \
         patch("builtins.open", create=True) as mock_open:
        mock_run.return_value.stdout = "This is pdfTeX"
        mock_run.return_value.stderr = ""
        mock_open.return_value.__enter__.return_value.read.return_value = fake_pdf

        resp = client.post(
            "/api/v1/profile/compile-texlive",
            json={
                "latex_source": "\\documentclass{article}\\begin{document}Hello\\end{document}",
                "account_id": "test-account-123",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["compiler_available"] is True
        assert data["compiler"] == "pdflatex"
        assert "pdf_base64" in data

