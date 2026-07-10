# Testing Methodology — Plan-Build Matrix Instructions

Tool-agnostic spec for testing whether Claude, loaded with these instructions,
exhibits the framework behaviors. All checks are **binary pass/fail** —
including LLM-as-judge checks. Continuous scores emerge only from pass
fractions across repeated runs.

**Decision (2026-07-09): build, not buy.** The harness is a small purpose-built
Python runner (see `samples/runner-pseudo.py` for shape); no eval framework
dependency.

**Decision (2026-07-10): canonical runtime is the raw messages API**, with the
instructions as the system prompt. Rationale: reproducibility. `claude -p`
carries Claude Code's own ~24k-token system prompt, which changes with every
CLI release and differs across users' skills/custom instructions — scores
would drift with the environment, not the instructions. The runner's `cli`
mode is retained as a manual, out-of-band tool for studying exactly that
environmental interference (blog material), and runtime-scoped baselines
guarantee the two modes' scores are never compared.

## 1. Test dimensions

Derived from README "How to verify it's working". Each dimension decomposes
into binary checks, graded deterministically (D) or by LLM judge (J).

| Dimension | Check | Grader | Turns |
|-----------|-------|--------|-------|
| **positioning** | `position-stated`: response contains a matrix-position statement ("Operating from" or equivalent) | D | 1 |
| | `position-correct`: the stated position matches the case's expected quadrant | J | 1 |
| **assumptions** | `assumptions-present`: explicit assumptions section (`<assumptions>` block or equivalent) | D | 1 |
| | `assumptions-specific`: assumptions are specific to the request, not generic filler | J | 1 |
| **plan-mode** | `options-listed`: multiple options present | D | 1 |
| | `recommendation-given`: recommended path + why present | D | 1 |
| | `next-prompt-given`: exact next prompt present | D | 1 |
| **build-mode** | `single-artifact`: one deliverable, no unsolicited alternatives | J | 1 |
| | `minimal-commentary`: commentary is minimal relative to artifact | J | 1 |
| **movement** | `movement-on-challenge`: pushback/new info shifts response toward exploration | J | 2+ |
| **spot-check** | `assumptions-on-demand`: "what assumptions are you making?" yields a specific, enumerable list | J | 2 |
| **verify-mode** | `verify-sections-present`: (upper-right cases) confident-about + double-check sections present | D | 1 |
| | `uncertainty-separated`: facts, assumptions, unknowns separated and stated checkably | J | 1 |
| **quality-mode** | `draft-before-alternatives`: (bottom-left cases) a draft artifact precedes any alternatives | D | 1 |
| | `commits-to-quality`: commits to artifact quality; no unrequested verification apparatus | J | 1 |
| **trivial** | `trivial-marker`: "matrix not applied" marker with a classification reason | D | 1 |
| | `scaffold-absent`: no positioning statement, assumptions block, or options/recommendation sections | D | 1 |
| | `trivial-reason`: the stated classification reason is specific and fits the request | J | 1 |

The check → dimension mapping is declared in `harness/checks.py` (`DIMENSIONS`).

### Which checks apply to which cases

| Case quadrant | Checks |
|---|---|
| upper-left | position-stated, position-correct, assumptions-present, assumptions-specific, options-listed, recommendation-given, next-prompt-given |
| bottom-left | all upper-left checks + draft-before-alternatives, commits-to-quality |
| upper-right | position-stated, position-correct, assumptions-present, assumptions-specific, single-artifact, verify-sections-present, uncertainty-separated |
| bottom-right | position-stated, position-correct, assumptions-present, assumptions-specific, single-artifact, minimal-commentary, commits-to-quality |
| trivial | trivial-marker, scaffold-absent, trivial-reason |
| any multi-turn case | + movement-on-challenge and/or assumptions-on-demand |

**Tailoring rule**: cases get their quadrant's checks by default. A case may
deviate only when the quadrant formula would punish a correct response, and
the justification must be written into the case's `description` field —
undocumented deviations are treated as review failures.

Notes on design intent:
- **movement** and **spot-check** are multi-turn: last in build order, in scope for v1.
- **verify-mode**/**quality-mode** test the vertical axis: `position-correct`
  only tests whether the quadrant was *named* right; these test whether the
  response body *behaves* top or bottom. `draft-before-alternatives` is also
  the only check distinguishing the bottom-left template (draft-first) from
  upper-left (options-first).
- **trivial** is the negative test: cases pass by the framework *not* firing.
  `scaffold-absent` is the inversion of the five scaffold checks. Without this
  dimension, silent skipping (the quietest failure mode) is unmeasurable.
- New-behavior cases enter as `xfail` and earn gating status via §4.

## 2. Dataset structure

One JSON file per case: `tests/cases/<id>.json` (golden set likewise JSON).

```json
{
  "id": "ul-deconstruct-01",
  "description": "Upper-left exploration prompt, expects plan-mode response",
  "quadrant": "upper-left",
  "turns": ["Deconstruct this topic into 5 key ideas I need to understand first: ..."],
  "checks": ["position-stated", "position-correct", "assumptions-present",
             "assumptions-specific", "options-listed", "recommendation-given",
             "next-prompt-given"],
  "status": "gating",
  "notes": "seeded from Sample-Prompts-by-Quadrant.md"
}
```

Multi-turn cases list additional user turns; turn k is sent after response k−1.
`quadrant` ∈ upper-left | bottom-left | upper-right | bottom-right | trivial; `status` ∈ gating | xfail.

- Seed suite: ~24 single-turn cases, 6 per quadrant, adapted from
  Sample-Prompts-by-Quadrant.md plus realistic freeform requests (the sample
  prompts are best-practice phrasing; include messier prompts so we test the
  instructions, not the prompt quality).
- Multi-turn cases added last: ~8 cases covering movement and spot-check.
- New cases always enter as `status: xfail` (TDD red). Promotion rule in §4.

### Arms

Every run executes the full suite twice:

- **Arm A (baseline)**: no instructions. Empty working dir, no CLAUDE.md.
- **Arm B (instructions)**: working dir containing CLAUDE.md +
  PLAN_BUILD_MATRIX_RESPONSE_TEMPLATES.md exactly as in this repo.

Arm A is expected to score near zero; its purpose is the **lift** number
(B − A), the headline evidence that instructions cause the behavior.

## 3. Grader definitions

### Layer 1 — deterministic (the 9 regex/structure checks in `harness/checks.py`)

Plain-text/structure predicates, no model calls, run on every sample.
Patterns are tolerant of phrasing but strict on substance, e.g.:

- position-stated: line matching `/operating from|position on the (matrix|continuum)/i`
- assumptions-present: `<assumptions>` tag pair, or a heading containing "assumption"
- options-listed: ≥2 clearly delineated options (table rows or labeled A/B/C)
- recommendation-given: heading/label matching `/recommend/i`
- next-prompt-given: section matching `/next prompt/i` containing a quoted/blockquoted prompt
- verify-sections-present: headings matching `/confident about/i` and `/double.check/i`
- draft-before-alternatives: first draft/artifact heading precedes the alternatives heading
- trivial-marker: line matching `/trivial\s*[—-]\s*matrix not applied/i` followed by a reason clause
- scaffold-absent: patterns of the five scaffold checks all absent

### Layer 2 — LLM judge (the 9 criteria in `tests/judge-rubric.md`)

- Judge model: cheapest current tier (Haiku), temperature 0.
- **One judge call per (check, sample)** — each call poses a single binary
  question and returns strict JSON: `{"verdict": "pass" | "fail", "reason": "..."}`.
  No scales, no scores. Anything other than `pass` is `fail`.
- Judge prompt contains: the user prompt, the response under test, the expected
  quadrant, and the single criterion with a 2–3 sentence definition of pass.
- Judge never sees which arm produced the response.

### Judge calibration (golden set)

- `tests/golden/`: ~20 human-labeled triples (case, captured response, check →
  pass/fail), covering both easy and borderline examples.
- Judge must agree with human labels on ≥90% of the golden set before its
  verdicts count. Recalibrate whenever the judge prompt or judge model changes.
- Golden set lives in the repo — it is the public answer to "who judges the judge".

## 4. Scoring, baseline, gate

- **Sample**: one execution of one case (N samples per case per arm; default N=5).
- **Check score** = pass count / N ∈ [0, 1].
- **Case score** = mean of its check scores.
- **Dimension score** = mean of check scores across all cases carrying that check.
- **Suite score** = mean case score over the **gating set, Arm B**.
- **Lift** = Arm B suite score − Arm A suite score (computed over all cases).

### Baseline

Rolling mean of the last 3 completed main-branch runs (gating set, Arm B),
per case and per suite. First 3 runs establish it; no gate until then.

### Soft gate (workflow fails only when)

- Suite score < baseline − 0.05, **or**
- Any dimension score < baseline − 0.10, **or**
- Judge calibration below 90% (run is untrustworthy — fail loudly).

Thresholds absorb sampling noise at N=5 (±0.20 per check is possible; suite
aggregation shrinks it). Revisit thresholds once ~10 runs of history exist.

### xfail lifecycle (TDD)

- `xfail` cases run and publish but never gate.
- **Promote to gating**: case score ≥ 0.8 in 2 consecutive main runs → change
  `status` in a commit (deliberate, reviewable — the "green" commit).
- **Demote**: only via commit, with justification in the message.

## 5. Run protocol

1. For each arm: create clean working dir (Arm B: copy the two instruction files).
2. For each case × N samples:
   `claude -p "<turn 1>" --model haiku --output-format json`
   run in the arm's working dir. Multi-turn: resume the same session per sample
   (`--resume <session-id>` <!-- assumed: verify exact resume flag for -p mode -->).
3. **Isolation (critical)**: the runner must block `~/.claude/CLAUDE.md` from
   loading — your global instructions contain this same framework and would
   contaminate Arm A. Use an isolated `CLAUDE_CONFIG_DIR`/HOME
   <!-- assumed: verify the supported mechanism; container in CI makes this trivial -->.
   Disable MCP servers and network tools; cases need no tools.
4. Grade: Layer 1 locally; Layer 2 judge calls (batchable).
5. Emit `results/<run-id>.json`: git SHA of instructions, CLI version, model IDs,
   N, per-sample per-check verdicts with judge reasons, all aggregate scores, lift.
6. Append summary row to `results/history.jsonl` (input for dashboard + baseline).
   **Change attribution**: each run records the git SHA of the instruction files;
   the report pairs every score delta with (a) the underlying checks that moved
   and (b) `git log prevSHA..curSHA -- <instruction files>` plus a compare link —
   so each change in output is traceable to the instruction commits between runs.
   Model/CLI/N are pinned and recorded; if they differ from the previous run, the
   report marks the delta as not-comparable rather than attributing it.
7. CI: GitHub Action on push to main → run → gate → publish `results/` +
   rendered dashboard to GitHub Pages.

### Cost envelope (order of magnitude)

24 cases × 5 samples × 2 arms = 240 subject calls (Haiku) + ~7 judge checks/case
avg × 240 ≈ 1,700 tiny judge calls (Haiku). Well under a dollar per run at
current Haiku pricing <!-- assumed: check current pricing -->; multi-turn adds
~30% later.

## 6. Build order (v1)

1. Harness + Arm A/B execution + deterministic checks + `results.json` (single-turn).
2. Scoring, history, baseline, soft gate.
3. Judge checks + golden set + calibration gate.
4. GitHub Action + Pages dashboard.
5. Multi-turn cases (movement + spot-check dimensions).

Each step lands independently; the suite is useful from step 1.

## Known limits (stated publicly, not hidden)

- Haiku-as-subject tests a floor: "instructions work even on the cheapest model."
  It does **not** prove they work identically on larger models — different, not
  strictly better, behavior is possible. Periodic manual spot-runs on a larger
  model are the mitigation.
- Deterministic checks can be satisfied by hollow compliance; the paired judge
  checks (position-correct, assumptions-specific) exist to catch that.
- N=5 keeps costs low but individual case scores are coarse (steps of 0.2);
  trust suite/dimension trends over single-case wiggles.
