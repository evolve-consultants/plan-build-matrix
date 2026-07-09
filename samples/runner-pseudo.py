# SAMPLE — runner pseudo-code (sense-check only, not runnable)

N = 5
DETERMINISTIC = {"1a", "2a", "3a", "3b", "3c", "7a", "8a", "9a", "9b"}   # regex/structure checks
GATING_EPS_SUITE, GATING_EPS_DIM = 0.05, 0.10

def run_subject(case, arm):
    workdir = fresh_tmp_dir()
    if arm == "B":
        copy(["CLAUDE.md", "PLAN_BUILD_MATRIX_RESPONSE_TEMPLATES.md"], workdir)
    env = isolated_env()   # blocks ~/.claude/* so globals can't contaminate Arm A
    session = None
    for turn in case.turns:                      # multi-turn: resume same session
        out = sh(f'claude -p "{turn}" --model haiku --output-format json',
                 cwd=workdir, env=env, resume=session)
        session = out.session_id
    return out.result

def judge(check, case, response):
    # one Haiku call, one binary question, strict JSON {"verdict","reason"}
    v = llm(JUDGE_PROMPTS[check].format(prompt=case.turns, response=response,
                                        quadrant=case.quadrant), temp=0)
    return v.verdict == "pass"

def grade(case, response):
    return {c: (regex_check(c, response) if c in DETERMINISTIC
                else judge(c, case, response))
            for c in case.checks}

def calibrate_judge(golden):
    agree = mean(judge(g.check, g.case, g.response) == g.label for g in golden)
    if agree < 0.90:
        die("judge below calibration threshold — run untrustworthy")

def instruction_changes(prev_run, cur_sha):
    # THE ATTRIBUTION MECHANISM: every run records the git SHA of the
    # instruction files it tested. The commits between the previous run's SHA
    # and this run's SHA are, by construction, the only instruction changes
    # that can explain a score delta (everything else — model, CLI, N — is
    # pinned and recorded; if those changed, the report flags the run as
    # not-comparable instead).
    commits = sh(f"git log --oneline {prev_run.sha}..{cur_sha} "
                 f"-- CLAUDE.md PLAN_BUILD_MATRIX_RESPONSE_TEMPLATES.md")
    return commits, github_compare_url(prev_run.sha, cur_sha)

def explain_deltas(scores, prev):
    # per-behavior and per-case: which underlying checks moved, by how much
    # (e.g. "2b fell 5/5 -> 3/5 on ul-deconstruct-02"), paired with the
    # instruction commits above. Rendered as the click-to-expand in the report.
    # Deltas within noise range get a "may be randomness" caveat.
    return {key: moved_checks(scores[key], prev[key]) for key in scores}

def main():
    cases = load_json("tests/cases/")
    calibrate_judge(load_json("tests/golden/"))

    verdicts = {}                                # (arm, case, check) -> pass fraction
    for arm in ["A", "B"]:
        for case in cases:
            samples = [grade(case, run_subject(case, arm)) for _ in range(N)]
            verdicts[arm, case.id] = pass_fractions(samples)

    scores = aggregate(verdicts)                 # case -> dimension -> suite; lift = B - A
    baseline = rolling_mean(load("results/history.jsonl"), last=3)  # gating set only

    gate_ok = (scores.suite >= baseline.suite - GATING_EPS_SUITE and
               all(scores.dim[d] >= baseline.dim[d] - GATING_EPS_DIM
                   for d in scores.dim))

    prev = last_run("results/history.jsonl")
    changes = instruction_changes(prev, current_sha())
    write_json(f"results/{run_id()}.json", verdicts, scores, changes, metadata())
    append_jsonl("results/history.jsonl", summary(scores, gate_ok, changes))
    render_html("results/report.html", scores, baseline, gate_ok,
                explain_deltas(scores, prev), changes)
    exit(0 if gate_ok else 1)                    # soft gate: CI reads exit code
