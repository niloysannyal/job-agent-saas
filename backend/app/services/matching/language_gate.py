import re
from typing import Dict, List, Optional, Set, Tuple


# Common non-English language indicators and their canonical names
KNOWN_LANGUAGES: Dict[str, str] = {
    "german": "German",
    "deutsch": "German",
    "deutschkenntnisse": "German",
    "french": "French",
    "français": "French",
    "francais": "French",
    "spanish": "Spanish",
    "español": "Spanish",
    "espanol": "Spanish",
    "dutch": "Dutch",
    "nederlands": "Dutch",
    "italian": "Italian",
    "italiano": "Italian",
    "polish": "Polish",
    "polski": "Polish",
    "swedish": "Swedish",
    "svenska": "Swedish",
    "danish": "Danish",
    "dansk": "Danish",
    "norwegian": "Norwegian",
    "norsk": "Norwegian",
    "finnish": "Finnish",
    "suomi": "Finnish",
    "japanese": "Japanese",
    "mandarin": "Mandarin",
    "chinese": "Chinese",
}


class LanguageGate:
    """
    Evaluates whether a job description requires a spoken language not declared
    in the user profile (ARCHITECTURE.md §4).

    Rule: If a posting requires a language that the user has not declared at all,
    it is hard-vetoed (vetoed=True, veto_reason set).
    """

    def __init__(self, declared_languages: Optional[List[str]] = None) -> None:
        raw_langs = declared_languages or ["english"]
        self.declared_languages: Set[str] = {
            KNOWN_LANGUAGES.get(l.strip().lower(), l.strip().lower())
            for l in raw_langs
            if l.strip()
        }
        # English is always assumed declared unless explicitly excluded
        self.declared_languages.add("English")

    def _detect_required_languages(self, text: str) -> Set[str]:
        """Detect any language explicitly marked as required or mandatory."""
        if not text:
            return set()

        required_languages: Set[str] = set()
        lower_text = text.lower()

        # 1. Look for phrases: "(fluent/required/native/c1/c2/b2) in <language>"
        req_pattern_1 = re.compile(
            r"\b(?:fluent|fluency\s+in|native|professional\s+proficiency\s+in|"
            r"strong\s+command\s+of|good\s+command\s+of|must\s+speak|speak|"
            r"erforderlich|voraussetzung|verhandlungssicher|flie(?:ß|ss)end|"
            r"courant|exigé|exigee|maîtrise\s+de)\s+(?:in\s+)?([a-zäöüßéèêà]+)\b",
            re.IGNORECASE,
        )
        for match in req_pattern_1.finditer(lower_text):
            word = match.group(1).lower()
            if word in KNOWN_LANGUAGES:
                required_languages.add(KNOWN_LANGUAGES[word])

        # 2. Look for phrases: "<language> (is)? (required|mandatory|essential|a must|erforderlich)"
        req_pattern_2 = re.compile(
            r"\b([a-zäöüßéèêà]+)\s+(?:is\s+)?(?:required|mandatory|essential|"
            r"a\s+must|erforderlich|voraussetzung|indispensable)\b",
            re.IGNORECASE,
        )
        for match in req_pattern_2.finditer(lower_text):
            word = match.group(1).lower()
            if word in KNOWN_LANGUAGES:
                required_languages.add(KNOWN_LANGUAGES[word])

        # 3. Look for CEFR level markers: "German (C1)", "C1 German", "B2 French"
        cefr_pattern = re.compile(
            r"\b(?:(?:c1|c2|b2)\s+([a-zäöüßéèêà]+)|([a-zäöüßéèêà]+)\s*\((?:c1|c2|b2)\))\b",
            re.IGNORECASE,
        )
        for match in cefr_pattern.finditer(lower_text):
            word = (match.group(1) or match.group(2) or "").lower()
            if word in KNOWN_LANGUAGES:
                required_languages.add(KNOWN_LANGUAGES[word])

        # 4. Native text heuristics: if standard German/French job intro markers appear
        german_markers = ["wir suchen", "ihre aufgaben", "dein profil", "das bringst du mit", "wir bieten"]
        if any(marker in lower_text for marker in german_markers):
            required_languages.add("German")

        french_markers = ["nous recherchons", "vos missions", "votre profil", "ce que nous offrons"]
        if any(marker in lower_text for marker in french_markers):
            required_languages.add("French")

        dutch_markers = ["wij zoeken", "jouw taken", "jouw profiel", "wat wij bieden"]
        if any(marker in lower_text for marker in dutch_markers):
            required_languages.add("Dutch")

        return required_languages

    def check(self, description: str) -> Tuple[bool, Optional[str]]:
        """
        Evaluate description against declared languages.

        Returns:
            (is_vetoed, veto_reason)
        """
        required = self._detect_required_languages(description)

        undeclared = [lang for lang in required if lang not in self.declared_languages]
        if undeclared:
            undeclared_str = ", ".join(sorted(undeclared))
            return True, f"Requires undeclared language(s): {undeclared_str}"

        return False, None
