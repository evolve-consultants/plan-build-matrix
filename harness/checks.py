"""Layer-1 deterministic checkers. Spec: TESTING-METHODOLOGY.md section 3.

Each checker takes the response text and returns bool. Patterns are tolerant
of phrasing but strict on substance: a check passes only when the structure
it tests for is actually present, not merely mentioned.
"""
import re

_POSITION = re.compile(r"operating from|position on the (matrix|continuum)", re.I)
_ASSUMPTION_TAGS = re.compile(r"<assumptions>.*</assumptions>", re.I | re.S)
_ASSUMPTION_HEADING = re.compile(r"^#{1,6}\s[^\n]*assumption", re.I | re.M)
_OPTION_TABLE_ROW = re.compile(r"^\|\s*\*\*[A-Z](\*\*|[:.])", re.M)
_OPTION_BULLET = re.compile(r"^[-*]\s+\*\*[A-Z]\*\*\s*[:.]", re.M)
_RECOMMEND = re.compile(r"^#{1,6}\s[^\n]*recommend|\*\*[^*\n]*recommend[^*\n]*\*\*", re.I | re.M)
_NEXT_PROMPT = re.compile(r"next prompt", re.I)
_BLOCKQUOTE = re.compile(r"^\s*>", re.M)
_CONFIDENT = re.compile(r"confident about", re.I)
_DOUBLE_CHECK = re.compile(r"double.check", re.I)
_DRAFT_HEADING = re.compile(r"^#{1,6}\s[^\n]*\b(draft|artifact)\b", re.I | re.M)
_ALTERNATIVES_HEADING = re.compile(r"^#{1,6}\s[^\n]*\balternatives\b", re.I | re.M)
_TRIVIAL_MARKER = re.compile(r"trivial\s*[—–-]\s*matrix not applied", re.I)


def _positioning_statement(text):
    return bool(_POSITION.search(text))


def _assumptions_section(text):
    return bool(_ASSUMPTION_TAGS.search(text) or _ASSUMPTION_HEADING.search(text))


def _multiple_options(text):
    count = len(_OPTION_TABLE_ROW.findall(text)) + len(_OPTION_BULLET.findall(text))
    return count >= 2


def _recommendation(text):
    return bool(_RECOMMEND.search(text))


def _next_prompt(text):
    # accepts either an explicit blockquoted prompt or the template's
    # "Next prompt should include" bulleted form, within the same section
    m = _NEXT_PROMPT.search(text)
    if not m:
        return False
    rest = text[m.end():]
    heading = re.search(r"^#{1,6}\s", rest, re.M)
    section = rest[:heading.start()] if heading else rest
    return bool(re.search(r"^\s*(>|[-*]\s)", section, re.M))


def _verify_sections(text):
    return bool(_CONFIDENT.search(text) and _DOUBLE_CHECK.search(text))


def _draft_before_alternatives(text):
    draft = _DRAFT_HEADING.search(text)
    if not draft:
        return False
    alt = _ALTERNATIVES_HEADING.search(text)
    return alt is None or draft.start() < alt.start()


def _trivial_marker_with_reason(text):
    m = _TRIVIAL_MARKER.search(text)
    if not m:
        return False
    same_paragraph = text[m.end():].split("\n\n")[0]
    return len(re.findall(r"[A-Za-z]{2,}", same_paragraph)) >= 2


def _scaffold_absent(text):
    scaffold = (_positioning_statement, _assumptions_section, _multiple_options,
                _recommendation, _next_prompt)
    return not any(check(text) for check in scaffold)


CHECKS = {
    "position-stated": _positioning_statement,
    "assumptions-present": _assumptions_section,
    "options-listed": _multiple_options,
    "recommendation-given": _recommendation,
    "next-prompt-given": _next_prompt,
    "verify-sections-present": _verify_sections,
    "draft-before-alternatives": _draft_before_alternatives,
    "trivial-marker": _trivial_marker_with_reason,
    "scaffold-absent": _scaffold_absent,
}


# every check (deterministic and judge) belongs to exactly one dimension;
# scoring rolls check fractions up to these names
DIMENSIONS = {
    "position-stated": "positioning",
    "position-correct": "positioning",
    "assumptions-present": "assumptions",
    "assumptions-specific": "assumptions",
    "options-listed": "plan-mode",
    "recommendation-given": "plan-mode",
    "next-prompt-given": "plan-mode",
    "single-artifact": "build-mode",
    "minimal-commentary": "build-mode",
    "movement-on-challenge": "movement",
    "assumptions-on-demand": "spot-check",
    "verify-sections-present": "verify-mode",
    "uncertainty-separated": "verify-mode",
    "draft-before-alternatives": "quality-mode",
    "commits-to-quality": "quality-mode",
    "trivial-marker": "trivial",
    "scaffold-absent": "trivial",
    "trivial-reason": "trivial",
}


def run_check(check_id, response):
    return CHECKS[check_id](response)
