import os
from unittest.mock import patch, MagicMock
import pytest

from app.services.cv_tailor.texlive_compiler import (
    TeXLiveCompilerService,
    build_sandboxed_tex_env,
    SAFE_ENV_VARS,
)


def test_build_sandboxed_tex_env_strips_secrets_and_sets_paranoid_flags(monkeypatch):
    # Inject sensitive secrets into environment
    monkeypatch.setenv("DATABASE_URL", "postgresql://admin:secretpass@localhost:5432/db")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-proj-supersecret12345")
    monkeypatch.setenv("JWT_SECRET_KEY", "my-jwt-secret-xyz")
    monkeypatch.setenv("OAUTH_ENCRYPTION_KEY", "fernet-key-abcdef")
    monkeypatch.setenv("PATH", "C:\\Windows\\system32;C:\\texlive")

    temp_dir = "/tmp/sandboxed_tex_run"
    clean_env = build_sandboxed_tex_env(temp_dir)

    # 1. Verify secrets are stripped
    assert "DATABASE_URL" not in clean_env
    assert "OPENAI_API_KEY" not in clean_env
    assert "JWT_SECRET_KEY" not in clean_env
    assert "OAUTH_ENCRYPTION_KEY" not in clean_env

    # 2. Verify paranoid file access restriction (G1)
    assert clean_env["openin_any"] == "p"
    assert clean_env["openout_any"] == "p"
    assert clean_env["TEXMFOUTPUT"] == temp_dir

    # 3. Verify safe variables are retained
    assert "PATH" in clean_env


def test_compile_latex_command_includes_no_shell_escape():
    with patch("shutil.which", return_value="C:\\texlive\\bin\\pdflatex.exe"):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Output written on document.pdf (1 page).",
                stderr="",
            )

            # Mock file operations
            with patch("os.path.exists", side_effect=lambda p: True):
                with patch("os.path.getsize", return_value=1024):
                    with patch("builtins.open", MagicMock()):
                        result = TeXLiveCompilerService.compile_latex(
                            latex_source=r"\documentclass{article}\begin{document}Hello\end{document}",
                            account_id="acc_123",
                            compiler="pdflatex",
                        )

            # Verify subprocess call arguments
            assert mock_run.called
            call_args = mock_run.call_args[0][0]
            assert "-no-shell-escape" in call_args
            assert "-halt-on-error" in call_args
            assert "-interaction=batchmode" in call_args

            # Verify sandboxed environment was passed
            call_kwargs = mock_run.call_args[1]
            passed_env = call_kwargs.get("env", {})
            assert passed_env.get("openin_any") == "p"
            assert passed_env.get("openout_any") == "p"


def test_compile_latex_command_latexmk_propagates_no_shell_escape():
    with patch("shutil.which", return_value="C:\\texlive\\bin\\latexmk.exe"):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="Output written on document.pdf (1 page).",
                stderr="",
            )

            with patch("os.path.exists", side_effect=lambda p: True):
                with patch("os.path.getsize", return_value=1024):
                    with patch("builtins.open", MagicMock()):
                        result = TeXLiveCompilerService.compile_latex(
                            latex_source=r"\documentclass{article}\begin{document}Hello\end{document}",
                            account_id="acc_123",
                            compiler="latexmk",
                        )

            assert mock_run.called
            call_args = mock_run.call_args[0][0]
            # latexmk must wrap pdflatex call with -no-shell-escape
            assert any("-no-shell-escape" in arg for arg in call_args)


def test_compile_latex_docker_fallback():
    """When host compiler is missing, compile_latex invokes Docker with -no-shell-escape and nonstopmode."""
    with patch("app.services.cv_tailor.texlive_compiler.TeXLiveCompilerService.find_compiler", return_value=None), \
         patch("app.services.cv_tailor.texlive_compiler.TeXLiveCompilerService.find_docker_compiler", return_value="job-agent-saas-worker-1"), \
         patch("subprocess.run") as mock_run:
        fake_pdf = b"%PDF-1.4 docker generated pdf content"

        def fake_run(cmd, *args, **kwargs):
            m = MagicMock()
            m.returncode = 0
            if "which" in cmd:
                m.stdout = "/usr/bin/pdflatex\n"
            elif "cat" in cmd and "document.pdf" in cmd[-1]:
                m.stdout = fake_pdf
            elif "cat" in cmd and "document.log" in cmd[-1]:
                m.stdout = "Output written on document.pdf (1 page).\n"
            else:
                m.stdout = ""
                m.stderr = ""
            return m

        mock_run.side_effect = fake_run

        res = TeXLiveCompilerService.compile_latex(
            latex_source=r"\documentclass{article}\begin{document}Hello Docker\end{document}",
            account_id="acc_docker",
        )

        assert res["success"] is True
        assert res["compiler_available"] is True
        assert "docker:job-agent-saas-worker-1:pdflatex" in res["compiler"]
        assert res["pdf_bytes"] == fake_pdf


