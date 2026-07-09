"""Layer-1 deterministic checker tests. Spec: TESTING-METHODOLOGY.md section 3.

Each checker takes a response string, returns bool. Fixtures mirror the
response templates in PLAN_BUILD_MATRIX_RESPONSE_TEMPLATES.md plus
plain/adversarial negatives.
"""
import pytest
from checks import run_check

UPPER_LEFT = """\
**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You want caching but don't know where the slowness is.

<assumptions>
  <project>Web app, no profiling done yet.</project>
  <task>Reduce perceived latency.</task>
  <operator>You can run a profiler if told how.</operator>
</assumptions>

### Options
| | Upside | Downside | Best when |
|---|---|---|---|
| **A** | fast | shallow | slowness is DB reads |
| **B** | thorough | slow | cause unknown |

### Recommendation
Option B because the cause is unknown.

### Next prompt should include
- Which option you prefer

**Exact next prompt to use:**
> Option B confirmed. Profile the app and report the top 3 hotspots.
"""

BOTTOM_LEFT = """\
**Operating from: Bottom-Left (Plan + Quality)**

<assumptions>
  <task>You want a launch email draft.</task>
</assumptions>

### Here's a rough draft (Option A)
Subject: We're live — here's what's new
Body: ...

### Alternatives I considered
- **B**: shorter, link-first version
- **C**: plain-text personal note
"""

UPPER_RIGHT = """\
**Operating from: Upper-Right (Build + Verify)**

<assumptions>
  <project>Config lives in config.yaml.</project>
</assumptions>

### The artifact
max_connections: 128  <!-- assumed: check actual limit -->

### What I'm confident about
- The YAML structure matches your schema

### What I'd double-check
- The 128 limit; wrong value causes connection refusals
"""

BOTTOM_RIGHT = """\
**Operating from: Bottom-Right (Build + Quality)**

<assumptions>
  <task>Conventional Commits, type refactor, no body.</task>
</assumptions>

### The artifact
refactor: rename getUser to fetchUser
"""

TRIVIAL = """\
**Trivial — matrix not applied.** Single-fact lookup; the answer doesn't \
depend on any assumption about your project.

PostgreSQL's default port is 5432.

*(Misread? Say so and I'll re-enter the matrix.)*
"""

PLAIN = """\
Caching could help. You might try Redis in front of your database, or add
an HTTP cache. It depends on where the slowness comes from, so maybe start
by profiling.
"""


# --- 1a: positioning statement present -----------------------------------

def test_1a_passes_on_operating_from():
    assert run_check("1a", UPPER_LEFT) is True

def test_1a_passes_on_position_wording():
    text = "My position on the matrix is bottom-right, so here's the artifact."
    assert run_check("1a", text) is True

def test_1a_fails_on_plain_prose():
    assert run_check("1a", PLAIN) is False


# --- 2a: assumptions section present --------------------------------------

def test_2a_passes_on_assumptions_tags():
    assert run_check("2a", UPPER_LEFT) is True

def test_2a_passes_on_assumptions_heading():
    text = "## Assumptions I'm making\n- You deploy on Linux\n"
    assert run_check("2a", text) is True

def test_2a_fails_on_plain_prose():
    assert run_check("2a", PLAIN) is False

def test_2a_fails_on_mere_mention():
    # the word "assume" in prose is not a section
    assert run_check("2a", "I assume you want Redis, so here it is.") is False


# --- 3a: >=2 delineated options -------------------------------------------

def test_3a_passes_on_options_table():
    assert run_check("3a", UPPER_LEFT) is True

def test_3a_passes_on_labeled_bullets():
    assert run_check("3a", BOTTOM_LEFT) is True  # **B**: / **C**: alternatives

def test_3a_fails_on_single_artifact():
    assert run_check("3a", BOTTOM_RIGHT) is False

def test_3a_fails_on_plain_prose():
    # "Redis ... or an HTTP cache" is prose, not delineated options
    assert run_check("3a", PLAIN) is False


# --- 3b: recommendation present --------------------------------------------

def test_3b_passes_on_recommendation_heading():
    assert run_check("3b", UPPER_LEFT) is True

def test_3b_passes_on_recommended_path_label():
    text = "**Recommended path:** option B, because the cause is unknown."
    assert run_check("3b", text) is True

def test_3b_fails_when_absent():
    assert run_check("3b", PLAIN) is False


# --- 3c: exact next prompt present -----------------------------------------

def test_3c_passes_on_next_prompt_with_blockquote():
    assert run_check("3c", UPPER_LEFT) is True

def test_3c_fails_on_next_prompt_heading_without_prompt():
    text = "### Next prompt should include\n- Which option you prefer\n"
    # section exists but contains no quoted/blockquoted prompt text
    assert run_check("3c", text) is False

def test_3c_fails_when_absent():
    assert run_check("3c", PLAIN) is False


# --- 7a: verify-mode sections present (upper-right cases) -------------------

def test_7a_passes_on_upper_right_template():
    assert run_check("7a", UPPER_RIGHT) is True

def test_7a_fails_when_only_one_section_present():
    text = "### What I'm confident about\n- Everything\n"
    assert run_check("7a", text) is False

def test_7a_fails_on_upper_left_template():
    assert run_check("7a", UPPER_LEFT) is False


# --- 8a: draft precedes alternatives (bottom-left cases) --------------------

def test_8a_passes_on_draft_first():
    assert run_check("8a", BOTTOM_LEFT) is True

def test_8a_fails_when_alternatives_come_first():
    text = """\
### Alternatives I considered
- **B**: shorter version
- **C**: personal note

### Here's a rough draft (Option A)
Subject: We're live
"""
    assert run_check("8a", text) is False

def test_8a_fails_when_no_draft_section():
    assert run_check("8a", UPPER_LEFT) is False


# --- 9a: trivial marker with reason -----------------------------------------

def test_9a_passes_on_marker_with_reason():
    assert run_check("9a", TRIVIAL) is True

def test_9a_passes_on_hyphen_variant():
    text = "**Trivial - matrix not applied.** Acknowledgment only. You're set."
    assert run_check("9a", text) is True

def test_9a_fails_on_marker_without_reason():
    assert run_check("9a", "**Trivial — matrix not applied.**") is False

def test_9a_fails_when_absent():
    assert run_check("9a", "Port 5432.") is False


# --- 9b: scaffold absent -----------------------------------------------------

def test_9b_passes_on_trivial_response():
    assert run_check("9b", TRIVIAL) is True

def test_9b_passes_on_bare_answer():
    assert run_check("9b", "Port 5432.") is True

@pytest.mark.parametrize("scaffolded", [UPPER_LEFT, BOTTOM_LEFT, UPPER_RIGHT, BOTTOM_RIGHT])
def test_9b_fails_on_any_scaffolded_template(scaffolded):
    assert run_check("9b", scaffolded) is False


# --- registry ---------------------------------------------------------------

def test_unknown_check_id_raises():
    with pytest.raises(KeyError):
        run_check("zz", "anything")
