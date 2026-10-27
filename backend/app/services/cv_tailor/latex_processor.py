import re
from typing import Tuple


def extract_preamble_and_body(latex_source: str) -> Tuple[str, str]:
    """
    Splits a LaTeX document into preamble (from \\documentclass to \\begin{document})
    and body (from \\begin{document} to \\end{document}).
    Strips any control comments preceding \\documentclass.
    """
    begin_doc = "\\begin{document}"
    if begin_doc not in latex_source:
        raise ValueError("Invalid LaTeX document: missing \\begin{document}")

    # Find the first un-commented \documentclass line
    docclass_start = None
    for line_match in re.finditer(r"(?m)^[ \t]*\\documentclass", latex_source):
        docclass_start = line_match.start()
        break

    if docclass_start is not None:
        trimmed_source = latex_source[docclass_start:]
    else:
        trimmed_source = latex_source

    parts = trimmed_source.split(begin_doc, 1)
    preamble = parts[0].strip() + "\n" + begin_doc
    body = parts[1]

    return preamble, body


def strip_control_comments(text: str) -> str:
    """
    Strips lines starting with %% (agent control notes) while preserving
    actual LaTeX escaped percentage signs (\\%).
    """
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("%%"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def escape_latex_special_chars(text: str) -> str:
    """
    Escapes LaTeX special characters (% & $ # _) if they are not already escaped.
    Does not touch LaTeX commands like \\textbf or \\section.
    """
    # Replace & not preceded by backslash
    text = re.sub(r"(?<!\\)&", r"\&", text)
    # Replace $ not preceded by backslash
    text = re.sub(r"(?<!\\)\$", r"\$", text)
    # Replace # not preceded by backslash
    text = re.sub(r"(?<!\\)#", r"\#", text)
    # Replace _ not preceded by backslash
    text = re.sub(r"(?<!\\)_", r"\_", text)
    # Replace % not preceded by backslash
    text = re.sub(r"(?<!\\)%", r"\%", text)
    return text


def check_brace_balance(text: str) -> bool:
    """Checks whether curly braces { } are balanced in the LaTeX body."""
    count = 0
    escaped = False
    for char in text:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
            if count < 0:
                return False
    return count == 0
