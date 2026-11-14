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
import uuid
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


def ensure_latex_preamble_macros(latex: str) -> str:
    """
    Ensure common CV macros are safely defined with \\providecommand if referenced in document.
    Prevents compilation failures on trimmed/tailored snippets missing global macro definitions.
    """
    needed = []
    if "\\resumeItem" in latex and "\\newcommand{\\resumeItem}" not in latex and "\\def\\resumeItem" not in latex:
        needed.append(r"\providecommand{\resumeItem}[1]{\item #1}")
    if "\\resumeItemListStart" in latex and "\\newcommand{\\resumeItemListStart}" not in latex:
        needed.append(r"\providecommand{\resumeItemListStart}{\begin{itemize}}")
    if "\\resumeItemListEnd" in latex and "\\newcommand{\\resumeItemListEnd}" not in latex:
        needed.append(r"\providecommand{\resumeItemListEnd}{\end{itemize}}")
    if "\\resumeHeadingListStart" in latex and "\\newcommand{\\resumeHeadingListStart}" not in latex:
        needed.append(r"\providecommand{\resumeHeadingListStart}{\begin{itemize}}")
    if "\\resumeHeadingListEnd" in latex and "\\newcommand{\\resumeHeadingListEnd}" not in latex:
        needed.append(r"\providecommand{\resumeHeadingListEnd}{\end{itemize}}")
    if "\\uline" in latex and "\\usepackage{ulem}" not in latex and "\\usepackage[normalem]{ulem}" not in latex:
        needed.append(r"\usepackage[normalem]{ulem}")

    if needed and "\\begin{document}" in latex:
        injection = "\n" + "\n".join(needed) + "\n"
        return latex.replace("\\begin{document}", injection + "\\begin{document}", 1)
    return latex


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
    DOCKER_CONTAINERS = [
        "job-agent-saas-worker-1",
        "job-agent-saas-worker",
        "job-agent-saas-backend-1",
        "job-agent-saas-backend",
    ]
    _cached_docker_container: Optional[str] = None
    _last_docker_check: float = 0.0

    @staticmethod
    def find_compiler() -> Optional[str]:
        """Detect available TeX compiler binary on PATH."""
        for cmd in ["pdflatex", "latexmk", "xelatex"]:
            path = shutil.which(cmd)
            if path:
                return cmd
        return None

    @classmethod
    def find_docker_compiler(cls, force_refresh: bool = False) -> Optional[str]:
        """Detect available Docker container with pdflatex."""
        now = time.time()
        if not force_refresh and cls._cached_docker_container and (now - cls._last_docker_check < 60.0):
            return cls._cached_docker_container

        if not shutil.which("docker"):
            cls._cached_docker_container = None
            cls._last_docker_check = now
            return None

        for container in cls.DOCKER_CONTAINERS:
            try:
                res = subprocess.run(
                    ["docker", "exec", container, "which", "pdflatex"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                if res.returncode == 0 and "pdflatex" in res.stdout:
                    cls._cached_docker_container = container
                    cls._last_docker_check = now
                    return container
            except Exception:
                continue

        cls._cached_docker_container = None
        cls._last_docker_check = now
        return None

    @classmethod
    def is_available(cls) -> bool:
        """Return True if a TeX compiler is installed and executable locally or in Docker."""
        if cls.find_compiler() is not None:
            return True
        return cls.find_docker_compiler() is not None

    @classmethod
    def compile_latex_docker(
        cls,
        latex_source: str,
        container: str,
        account_id: str = "anon",
        timeout_seconds: int = 20,
    ) -> Dict[str, Any]:
        """
        Compile LaTeX source into PDF inside a Docker worker container with TeX Live installed.
        """
        start_time = time.time()
        run_id = uuid.uuid4().hex[:8]
        work_dir = f"/tmp/texlive_{account_id}_{run_id}"
        processed_source = ensure_latex_preamble_macros(latex_source)

        try:
            # 1. Create isolated temporary workspace inside container
            subprocess.run(
                ["docker", "exec", container, "mkdir", "-p", work_dir],
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )

            # 2. Pipe source into container document.tex
            subprocess.run(
                ["docker", "exec", "-i", container, "sh", "-c", f"cat > {work_dir}/document.tex"],
                input=processed_source.encode("utf-8"),
                capture_output=True,
                timeout=10,
                check=True,
            )

            # 3. Run pdflatex in nonstopmode with strict container sandboxing flags
            cmd = [
                "docker", "exec",
                "-e", "openin_any=p",
                "-e", "OPENIN_ANY=p",
                "-e", "openout_any=p",
                "-e", "OPENOUT_ANY=p",
                "-e", f"TEXMFOUTPUT={work_dir}",
                "-w", work_dir,
                container,
                "pdflatex",
                "-interaction=nonstopmode",
                "-no-shell-escape",
                f"-output-directory={work_dir}",
                f"{work_dir}/document.tex",
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )

            duration_ms = int((time.time() - start_time) * 1000)

            # 4. Read PDF bytes if generated
            pdf_check = subprocess.run(
                ["docker", "exec", container, "cat", f"{work_dir}/document.pdf"],
                capture_output=True,
                timeout=10,
            )
            pdf_bytes = pdf_check.stdout if (pdf_check.returncode == 0 and len(pdf_check.stdout) > 0) else None

            # 5. Read log file
            log_check = subprocess.run(
                ["docker", "exec", container, "cat", f"{work_dir}/document.log"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            log_content = log_check.stdout if log_check.returncode == 0 else (result.stdout or result.stderr or "")

            success = bool(pdf_bytes and len(pdf_bytes) > 0 and pdf_bytes.startswith(b"%PDF"))

            return {
                "success": success,
                "compiler_available": True,
                "compiler": f"docker:{container}:pdflatex",
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
                "compiler": f"docker:{container}:pdflatex",
                "duration_ms": timeout_seconds * 1000,
                "error": f"Compilation timed out after {timeout_seconds} seconds.",
                "log_output": "Compilation timed out.",
            }
        except Exception as exc:
            return {
                "success": False,
                "compiler_available": True,
                "compiler": f"docker:{container}:pdflatex",
                "duration_ms": int((time.time() - start_time) * 1000),
                "error": str(exc),
                "log_output": str(exc),
            }
        finally:
            try:
                subprocess.run(
                    ["docker", "exec", container, "rm", "-rf", work_dir],
                    capture_output=True,
                    timeout=5,
                )
            except Exception:
                pass

    @classmethod
    def compile_latex(
        cls,
        latex_source: str,
        account_id: str = "anon",
        compiler: Optional[str] = None,
        timeout_seconds: int = 15,
    ) -> Dict[str, Any]:
        """
        Compile LaTeX source into PDF using system TeX Live engine or Docker container with strict sandboxing.
        Returns dict with success flag, log output, duration, and pdf bytes if successful.
        """
        active_compiler = compiler if (compiler and shutil.which(compiler)) else cls.find_compiler()
        if not active_compiler:
            # Fall back to Docker container compiler if available
            docker_container = cls.find_docker_compiler()
            if docker_container:
                return cls.compile_latex_docker(
                    latex_source=latex_source,
                    container=docker_container,
                    account_id=account_id,
                    timeout_seconds=timeout_seconds,
                )
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
            processed_source = ensure_latex_preamble_macros(latex_source)
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(processed_source)

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
