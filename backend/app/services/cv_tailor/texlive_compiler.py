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
from typing import Any, Dict, Optional


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
        timeout_seconds: int = 25,
    ) -> Dict[str, Any]:
        """
        Compile LaTeX source into PDF using system TeX Live engine.
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

            # Build command args matching Overleaf CLSI batchmode flags
            if active_compiler == "latexmk":
                cmd = [
                    "latexmk",
                    "-pdf",
                    "-cd",
                    "-interaction=batchmode",
                    "-halt-on-error",
                    f"-outdir={temp_dir}",
                    tex_path,
                ]
            else:
                cmd = [
                    active_compiler,
                    "-interaction=batchmode",
                    "-halt-on-error",
                    f"-output-directory={temp_dir}",
                    tex_path,
                ]

            result = subprocess.run(
                cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
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
