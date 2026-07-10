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

| # | Dimension | Checks | Grader | Turns |
|---|-----------|--------|--------|-------|
| 1 | Positioning statement | 1a: response contains a matrix-position statement ("Operating from" or equivalent) | D | 1 |
| | | 1b: the stated position matches the case's expected quadrant | J | 1 |
| 2 | Assumption surfacing | 2a: response contains an explicit assumptions section (`<assumptions>` block or equivalent) | D | 1 |
| | | 2b: stated assumptions are specific to the request, not generic filler | J | 1 |
| 3 | Mode matching (left) | 3a: multiple options present | D | 1 |
| | | 3b: Recommended path + why present | D | 1 |
| | | 3c: exact next prompt present | D | 1 |
| 4 | Mode matching (right) | 4a: single artifact, no unsolicited alternatives | J | 1 |
| | | 4b: commentary is minimal relative to artifact | J | 1 |
| 5 | Movement on challenge | 5a: after pushback/new info, response shifts toward exploration (options/assumptions reopen) | J | 2+ |
| 6 | Spot check | 6a: "what assumptions are you making?" yields a specific, enumerable list | J | 2 |
| 7 | Verify-mode (top) | 7a: (upper-right cases) "what I'm confident about" + "what I'd double-check" sections present, or equivalents | D | 1 |
| | | 7b: facts, assumptions, and unknowns are separated and stated checkably, not blended into hedged prose | J | 1 |
| 8 | Quality-mode (bottom) | 8a: (bottom-left cases) a draft artifact appears before any alternatives | D | 1 |
| | | 8b: commits to artifact quality; no unrequested verification apparatus | J | 1 |
| 9 | Trivial handling (not triggered) | 9a: trivial marker present ("matrix not applied" + a classification reason) | D | 1 |
| | | 9b: scaffold absent — no positioning statement, no assumptions block, no options/recommendation sections | D | 1 |
| | | 9c: the stated classification reason is specific and fits the request | J | 1 |

Dimensions 5–6 are multi-turn: **last in build order, in scope for v1**.
Dimensions 7–8 test the vertical (verify/quality) axis; check 1b tests only
whether the quadrant was *named* correctly — 7–8 test whether the response
body *behaves* top or bottom. Their cases enter as `xfail` (unproven
behaviors) and earn gating status via the promotion rule in §4. Note 8a is
also the only check that distinguishes the bottom-left template (draft-first)
from upper-left (options-first); without it a bottom-left case could score
perfectly on 3a–3c with a pure upper-left response.
Dimension 9 is the negative test: its cases are labeled `quadrant: trivial`
and pass by the framework *not* firing — marker present, scaffold absent.
9b reuses the patterns of 1a/2a/3a–3c inverted (all must be absent). Without
this dimension, silent skipping (the framework's quietest failure mode) is
unmeasurable. Dimension 9 cases also enter as `xfail`.

## 2. Dataset structure

One JSON file per case: `tests/cases/<id>.json` (golden set likewise JSON).

```json
{
  "id": "ul-deconstruct-01",
  "description": "Upper-left exploration prompt, expects plan-mode response",
  "quadrant": "upper-left",
  "turns": ["Deconstruct this topic into 5 key ideas I need to understand first: ..."],
  "checks": ["1a", "1b", "2a", "2b", "3a", "3b", "3c"],
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
- Multi-turn cases added last: ~8 cases covering dimensions 5–6.
- New cases always enter as `status: xfail` (TDD red). Promotion rule in §4.

### Arms

Every run executes the full suite twice:

- **Arm A (baseline)**: no instructions. Empty working dir, no CLAUDE.md.
- **Arm B (instructions)**: working dir containing CLAUDE.md +
  PLAN_BUILD_MATRIX_RESPONSE_TEMPLATES.md exactly as in this repo.

Arm A is expected to score near zero; its purpose is the **lift** number
(B − A), the headline evidence that instructions cause the behavior.

## 3. Grader definitions

### Layer 1 — deterministic (checks 1a, 2a, 3a–3c, 7a, 8a, 9a, 9b)

Plain-text/structure predicates, no model calls, run on every sample.
Patterns are tolerant of phrasing but strict on substance, e.g.:

- 1a: line matching `/operating from|position on the (matrix|continuum)/i`
- 2a: `<assumptions>` tag pair, or a heading containing "assumption"
- 3a: ≥2 clearly delineated options (table rows or labeled A/B/C)
- 3b: heading/label matching `/recommend/i`
- 3c: section matching `/next prompt/i` containing a quoted/blockquoted prompt
- 7a: headings matching `/confident about/i` and `/double.check/i`
- 8a: position of first draft/artifact heading < position of alternatives heading
- 9a: line matching `/trivial\s*[—-]\s*matrix not applied/i` followed by a reason clause
- 9b: patterns of 1a, 2a, 3a–3c all absent

### Layer 2 — LLM judge (checks 1b, 2b, 4a, 4b, 5a, 6a, 7b, 8b, 9c)

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
5. Multi-turn cases (dimensions 5–6).

Each step lands independently; the suite is useful from step 1.

## Known limits (stated publicly, not hidden)

- Haiku-as-subject tests a floor: "instructions work even on the cheapest model."
  It does **not** prove they work identically on larger models — different, not
  strictly better, behavior is possible. Periodic manual spot-runs on a larger
  model are the mitigation.
- Deterministic checks can be satisfied by hollow compliance; the paired judge
  checks (1b, 2b) exist to catch that.
- N=5 keeps costs low but individual case scores are coarse (steps of 0.2);
  trust suite/dimension trends over single-case wiggles.
