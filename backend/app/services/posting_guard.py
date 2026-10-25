"""
posting_guard.py — posting integrity gate (ARCHITECTURE.md §4, §8)

Every fetched JobPosting is untrusted input. Before a posting is persisted,
scored, summarized, or used in CV tailoring, run it through this gate.

The gate does two things:
  1. STRIP  — removes hidden/invisible Unicode characters from all text fields.
  2. FLAG   — identifies lines that look like instructions directed at an AI
              agent (prompt-injection attempts). Flagged lines are NOT deleted;
              they remain in the cleaned posting so a human reviewer can see
              exactly what was there. The caller decides how to handle flags
              (log, quarantine, reject) — the gate never silently drops content.

Returns a GateResult(posting, flags). An empty flags list means the posting
passed cleanly. Non-empty flags means the caller should at minimum log the
result and consider human review before the posting reaches an LLM.

Design notes:
  - The gate is a pure function with no I/O — easy to test and composable.
  - It operates on JobPosting DTOs (Pydantic), returns a new JobPosting copy
    with cleaned text fields. The original is not mutated.
  - "Instruction-shaped" detection is intentionally conservative: false
    positives (a line wrongly flagged) are safer than false negatives (a
    real injection slipping through). A flagged posting still gets human
    review; an unflagged injection gets none.
  - Fields checked: description, role, company. salary/location/etc. are
    not LLM inputs and are not inspected here.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from app.models.job import JobPosting


# ---------------------------------------------------------------------------
# Hidden/invisible Unicode character sets
# ---------------------------------------------------------------------------

# Zero-width and formatting characters with no visible glyph that are
# commonly used to hide injected text inside legitimate-looking content.
_INVISIBLE_CATEGORIES = frozenset({
    "Cf",   # Format characters (soft hyphen, zero-width joiner, BOM, etc.)
    "Cs",   # Surrogate characters
    "Co",   # Private use characters
    "Cn",   # Unassigned / not-a-character
})

# Additional individual codepoints worth stripping even if their Unicode
# category is technically "other" or "letter" in some implementations.
_EXTRA_INVISIBLE = frozenset({
    "\u200b",  # ZERO WIDTH SPACE
    "\u200c",  # ZERO WIDTH NON-JOINER
    "\u200d",  # ZERO WIDTH JOINER
    "\u200e",  # LEFT-TO-RIGHT MARK
    "\u200f",  # RIGHT-TO-LEFT MARK
    "\u2028",  # LINE SEPARATOR
    "\u2029",  # PARAGRAPH SEPARATOR
    "\ufeff",  # ZERO WIDTH NO-BREAK SPACE (BOM)
    "\u00ad",  # SOFT HYPHEN
    "\u180e",  # MONGOLIAN VOWEL SEPARATOR
    "\u2060",  # WORD JOINER
    "\u2061",  # FUNCTION APPLICATION
    "\u2062",  # INVISIBLE TIMES
    "\u2063",  # INVISIBLE SEPARATOR
    "\u2064",  # INVISIBLE PLUS
    "\u206a",  # INHIBIT SYMMETRIC SWAPPING
    "\u206b",  # ACTIVATE SYMMETRIC SWAPPING
    "\u206c",  # INHIBIT ARABIC FORM SHAPING
    "\u206d",  # ACTIVATE ARABIC FORM SHAPING
    "\u206e",  # NATIONAL DIGIT SHAPES
    "\u206f",  # NOMINAL DIGIT SHAPES
})


def _is_invisible(char: str) -> bool:
    """Return True if the character should be stripped as invisible/hidden."""
    if char in _EXTRA_INVISIBLE:
        return True
    return unicodedata.category(char) in _INVISIBLE_CATEGORIES


def strip_invisible(text: str) -> str:
    """Remove all hidden/invisible Unicode characters from text."""
    return "".join(ch for ch in text if not _is_invisible(ch))


# ---------------------------------------------------------------------------
# Instruction-detection patterns
# ---------------------------------------------------------------------------
# These patterns look for lines that appear to be giving instructions *to*
# an AI system rather than describing a job. The heuristics are conservative
# by design — better to flag a borderline case than to miss a real injection.

_INSTRUCTION_PATTERNS: List[re.Pattern] = [
    # Explicit system/prompt framing keywords
    re.compile(
        r"\b(system\s*prompt|ignore\s+(previous|prior|above|all)\s+(instructions?|context|text)|"
        r"disregard\s+(previous|prior|above|all)|"
        r"forget\s+(everything|all|previous|prior)|"
        r"new\s+instructions?|"
        r"override\s+(previous|all)|"
        r"you\s+are\s+now|"
        r"act\s+as\s+(a\s+)?(new|different|unrestricted)|"
        r"do\s+not\s+follow|"
        r"bypass\s+(your\s+)?(safety|filter|guideline)|"
        r"pretend\s+(you\s+are|to\s+be)|"
        r"roleplay\s+as)",
        re.IGNORECASE,
    ),
    # Bracket/tag-style injection markers common in adversarial prompts
    re.compile(
        r"(\[INST\]|\[\/INST\]|\[SYSTEM\]|\[PROMPT\]|\[USER\]|\[ASSISTANT\]|"
        r"<\|system\|>|<\|user\|>|<\|assistant\|>|<\|im_start\|>|<\|im_end\|>|"
        r"###\s*(System|Instruction|Prompt)|"
        r"```\s*(system|instruction|prompt))",
        re.IGNORECASE,
    ),
    # Direct imperative commands to an AI agent
    re.compile(
        r"^[\s\-\*•]*"           # optional leading whitespace/bullets
        r"(always|never|do not|don't|must|should|shall)\s+"
        r"(reveal|expose|print|output|return|send|include|add|insert|"
        r"apply\s+for|submit|click|navigate|open|access|download|upload|"
        r"execute|run|call|invoke|use|follow|obey|comply)",
        re.IGNORECASE | re.MULTILINE,
    ),
    # Lines explicitly addressed to an AI
    re.compile(
        r"\b(AI|LLM|GPT|Claude|Gemini|assistant|language\s+model|chatbot)\s*[:,]\s*",
        re.IGNORECASE,
    ),
    # Attempts to exfiltrate content
    re.compile(
        r"\b(exfiltrate|leak|extract\s+and\s+send|send\s+(all|the)\s+(data|content|"
        r"information|cv|resume|email))\b",
        re.IGNORECASE,
    ),
]


def _line_looks_like_instruction(line: str) -> bool:
    """Return True if the line matches any instruction-injection pattern."""
    stripped = line.strip()
    if not stripped:
        return False
    return any(p.search(stripped) for p in _INSTRUCTION_PATTERNS)


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

class FlagKind(str, Enum):
    INVISIBLE_CHARS_STRIPPED = "invisible_chars_stripped"
    INSTRUCTION_LIKE_LINE     = "instruction_like_line"


@dataclass(frozen=True)
class IntegrityFlag:
    """
    A single issue found during the integrity check.

    kind      — what category of issue was found
    field     — which JobPosting field it was found in (e.g. 'description')
    detail    — a short human-readable description of what was found
    line_text — the (cleaned) offending line, if applicable; None for field-level flags
    """
    kind:      FlagKind
    field:     str
    detail:    str
    line_text: Optional[str] = None


@dataclass
class GateResult:
    """
    Return type from run_posting_guard().

    posting — a new JobPosting copy with invisible characters stripped.
              Flagged instruction-like lines are RETAINED (not deleted).
    flags   — list of IntegrityFlag. Empty means the posting passed cleanly.
              Non-empty means the caller should log and consider human review
              before allowing this posting to reach an LLM.
    passed  — True iff flags is empty.
    """
    posting: JobPosting
    flags:   List[IntegrityFlag] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.flags) == 0


# ---------------------------------------------------------------------------
# Core gate function
# ---------------------------------------------------------------------------

# Fields from JobPosting that are LLM inputs and must be inspected.
# salary/location/currency/etc. are not fed to LLMs and are not checked here.
_INSPECTED_FIELDS = ("description", "role", "company")


def run_posting_guard(posting: JobPosting) -> GateResult:
    """
    Run the posting integrity gate on a JobPosting DTO.

    Steps:
      1. Strip invisible/hidden Unicode from all inspected text fields.
         If any characters were removed, raise an INVISIBLE_CHARS_STRIPPED flag.
      2. Scan each line of the cleaned description for instruction-shaped content.
         Each matching line raises a separate INSTRUCTION_LIKE_LINE flag.

    Returns a GateResult with a cleaned copy of the posting and any flags found.
    The original posting object is never mutated.
    Callers must not pass this posting to an LLM if flags are non-empty without
    first performing human review or explicit quarantine handling.
    """
    flags: List[IntegrityFlag] = []
    cleaned_fields: dict = {}

    for fname in _INSPECTED_FIELDS:
        original: str = getattr(posting, fname) or ""
        cleaned: str  = strip_invisible(original)

        if cleaned != original:
            removed_count = len(original) - len(cleaned)
            flags.append(IntegrityFlag(
                kind=FlagKind.INVISIBLE_CHARS_STRIPPED,
                field=fname,
                detail=(
                    f"Stripped {removed_count} invisible/hidden Unicode character(s) "
                    f"from field '{fname}'."
                ),
            ))

        cleaned_fields[fname] = cleaned

    # Scan description line-by-line for instruction-shaped content.
    # We scan the *cleaned* description (invisible chars already removed).
    description_cleaned: str = cleaned_fields.get("description", "")
    for line in description_cleaned.splitlines():
        if _line_looks_like_instruction(line):
            flags.append(IntegrityFlag(
                kind=FlagKind.INSTRUCTION_LIKE_LINE,
                field="description",
                detail=(
                    "Line matches an instruction-injection pattern. "
                    "Review before passing to LLM."
                ),
                line_text=line.strip(),
            ))

    # Build a cleaned copy of the posting.
    # model_copy(update=...) creates a new Pydantic model with updated fields;
    # all other fields are carried over unchanged.
    cleaned_posting = posting.model_copy(update=cleaned_fields)

    return GateResult(posting=cleaned_posting, flags=flags)
