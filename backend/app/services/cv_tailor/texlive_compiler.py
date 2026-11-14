"""
TeX Live backend compiler service.
Adapted from Overleaf CLSI (Common LaTeX Service Interface) execution patterns.

Executes sandboxed batchmode compilation using system pdflatex/latexmk or Docker
with timeout protection, stdout/stderr capture, and full log parsing support.
"""

import os
import shutil
import subprocess
import tempfile
import time
from typing import Any, Dict, Optional, Set

# Safe environment variables allowed in child TeX compiler process (G1 Sandbox)
SAFE_ENV_VARS: Set[str] = {
    "PATH",
    "SYSTEMROOT",
    "WINDIR",
    "TEMP",
    "TMP",
    "TEXMFCNF",
    "TEXMFHOME",
    "TEXMFDIST",
    "TEXMFLOCAL",
    "TEXMFVAR",
    "TEXMFCONFIG",
    "USERPROFILE",
    "HOME",
    "LANG",
    "LC_ALL",
}


def build_sandboxed_tex_env(temp_dir: str) -> Dict[str, str]:
    """
    Construct scrubbed environment for TeX compilation child processes.
    - Strips all secrets, database credentials, API keys, and JWT tokens.
    - Enforces openin_any=p (paranoid) and openout_any=p to block reading/writing outside cwd.
    - Sets TEXMFOUTPUT to isolated temporary directory.
    """
    clean_env: Dict[str, str] = {
        k: v for k, v in os.environ.items() if k.upper() in SAFE_ENV_VARS
    }
    # Enforce paranoid file access restriction (blocks /etc/passwd, .env, parent directory traversal)
    clean_env["openin_any"] = "p"
    clean_env["OPENIN_ANY"] = "p"
    clean_env["openout_any"] = "p"
    clean_env["OPENOUT_ANY"] = "p"
    clean_env["TEXMFOUTPUT"] = temp_dir
    return clean_env


class TeXLiveCompilerService:
    @staticmethod
    def find_compiler() -> Optional[str]:
        """Detect available TeX compiler binary on PATH."""
        for cmd in ["pdflatex", "latexmk", "xelatex"]:
            path = shutil.which(cmd)
            if path:
                return cmd
        return None

    @classmethod
    def is_available(cls) -> bool:
        """Return True if a TeX compiler is installed and executable."""
        return cls.find_compiler() is not None

    @classmethod
    def compile_latex(
        cls,
        latex_source: str,
        account_id: str = "anon",
        compiler: Optional[str] = None,
        timeout_seconds: int = 15,
    ) -> Dict[str, Any]:
        """
        Compile LaTeX source into PDF using system TeX Live engine with strict sandboxing.
        Returns dict with success flag, log output, duration, and pdf bytes if successful.
        """
        active_compiler = compiler if (compiler and shutil.which(compiler)) else cls.find_compiler()
        if not active_compiler:
            return {
                "success": False,
                "compiler_available": False,
                "error": "No TeX Live compiler (pdflatex/latexmk) detected on system PATH.",
                "log_output": "",
                "duration_ms": 0,
            }

        start_time = time.time()
        temp_dir = tempfile.mkdtemp(prefix=f"texlive_{account_id}_")
        tex_path = os.path.join(temp_dir, "document.tex")
        pdf_path = os.path.join(temp_dir, "document.pdf")
        log_path = os.path.join(temp_dir, "document.log")

        try:
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(latex_source)

            # Build command args with strict sandboxing flags (-no-shell-escape)
            if active_compiler == "latexmk":
                cmd = [
                    "latexmk",
                    "-pdf",
                    "-cd",
                    "-interaction=batchmode",
                    "-halt-on-error",
                    '-pdflatex=pdflatex -interaction=batchmode -no-shell-escape -halt-on-error',
                    f"-outdir={temp_dir}",
                    tex_path,
                ]
            else:
                cmd = [
                    active_compiler,
                    "-interaction=batchmode",
                    "-no-shell-escape",
                    "-halt-on-error",
                    f"-output-directory={temp_dir}",
                    tex_path,
                ]

            sandboxed_env = build_sandboxed_tex_env(temp_dir)

            result = subprocess.run(
                cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=sandboxed_env,
            )

            duration_ms = int((time.time() - start_time) * 1000)

            # Read log output if generated
            log_content = ""
            if os.path.exists(log_path):
                try:
                    with open(log_path, "r", encoding="utf-8", errors="replace") as lf:
                        log_content = lf.read()
                except Exception:
                    pass

            if not log_content:
                log_content = result.stdout or result.stderr or ""

            success = os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0

            pdf_bytes = None
            if success:
                with open(pdf_path, "rb") as pf:
                    pdf_bytes = pf.read()

            return {
                "success": success,
                "compiler_available": True,
                "compiler": active_compiler,
                "duration_ms": duration_ms,
                "log_output": log_content,
                "pdf_bytes": pdf_bytes,
                "pdf_size": len(pdf_bytes) if pdf_bytes else 0,
                "error": None if success else (result.stderr or "Compilation halted with errors."),
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "compiler_available": True,
                "compiler": active_compiler,
                "duration_ms": timeout_seconds * 1000,
                "error": f"Compilation timed out after {timeout_seconds} seconds.",
                "log_output": "Compilation timed out.",
            }
        except Exception as exc:
            return {
                "success": False,
                "compiler_available": True,
                "compiler": active_compiler,
                "duration_ms": int((time.time() - start_time) * 1000),
                "error": str(exc),
                "log_output": str(exc),
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
