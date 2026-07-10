"""Render results.json + history into a self-contained static HTML report.

No backend: everything is computed here at generation time and served as
bytes. Language rules (operator-approved via samples/report.html): no trial
jargon — "with/without instructions", not arms; "in development", not xfail.
"""
import html as html_mod

STYLE = """
  body { font: 15px/1.5 system-ui, sans-serif; max-width: 780px; margin: 2rem auto; padding: 0 1rem; color: #222; }
  h1 { font-size: 1.3rem; } h2 { font-size: 1.05rem; margin-top: 2rem; }
  .meta { color: #666; font-size: .85rem; }
  .gate { padding: .6rem 1rem; border-radius: 6px; font-weight: 600; margin: 1rem 0; }
  .pass { background: #e6f4ea; color: #137333; }
  .fail { background: #fce8e6; color: #c5221f; }
  .headline { display: flex; gap: 2rem; margin: 1.5rem 0; }
  .headline div { text-align: center; }
  .headline .num { font-size: 1.8rem; font-weight: 700; }
  table { border-collapse: collapse; width: 100%; font-size: .9rem; }
  th, td { text-align: left; padding: .35rem .6rem; border-bottom: 1px solid #eee; vertical-align: top; }
  th { color: #666; font-weight: 600; }
  .up { color: #137333; } .down { color: #c5221f; } .flat { color: #999; }
  .tag { font-size: .75rem; padding: .05rem .4rem; border-radius: 4px; background: #fef7e0; color: #b06000; white-space: nowrap; }
  details { display: inline; } details summary { cursor: pointer; text-decoration: underline dotted; }
  details div { margin-top: .4rem; padding: .5rem .7rem; background: #f6f8fa; border-radius: 6px; font-size: .82rem; color: #444; }
"""


def _fmt(x):
    return "—" if x is None else f"{x:.2f}"


def _delta(cur, prev):
    if prev is None:
        return '<span class="flat">first run</span>'
    d = cur - prev
    cls = "up" if d > 0.005 else ("down" if d < -0.005 else "flat")
    return f'<span class="{cls}">{d:+.2f}</span>'


def _moved_checks(case_id, cur_case, prev_results):
    if not prev_results:
        return []
    prev_case = prev_results.get("arms", {}).get("B", {}).get(case_id)
    if not prev_case:
        return []
    moves = []
    for check, frac in cur_case["checks"].items():
        old = prev_case["checks"].get(check)
        if old is not None and abs(old - frac) > 0.005:
            moves.append(f"{check} {old:.2f} → {frac:.2f}")
    return moves


def render_report(results, history, prev_results=None, compare_url=None):
    e = html_mod.escape
    summary = results["summary"]
    gate = results["gate"]
    base = gate.get("baseline")
    arm_a, arm_b = results["arms"].get("A", {}), results["arms"]["B"]

    def mean_all(cases):
        scores = [c["score"] for c in cases.values() if c["score"] is not None]
        return sum(scores) / len(scores) if scores else None

    out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
           f"<title>Instruction test results · {e(results.get('timestamp', ''))}</title>"
           f"<style>{STYLE}</style></head><body>"]
    out.append("<h1>Plan-Build Matrix — do the instructions work?</h1>")
    calibration = results.get("judge_calibration")
    out.append(
        f"<p class='meta'>run {e(results.get('timestamp', '?'))} · instructions version "
        f"<code>{e(results.get('instructions_sha', '?'))}</code> · model {e(results.get('model', '?'))} "
        f"· runtime {e(results.get('runtime', '?'))} · each test repeated {results.get('n', '?')}x"
        + (f" · judge agreement with human labels: {calibration:.0%}" if calibration else "")
        + " · scores are the share of repetitions that behaved correctly (1.00 = always)</p>")

    if gate["ok"]:
        vs = f" — overall {_fmt(summary['suite'])}" + (
            f", previous average {_fmt(base['suite'])}" if base else " (first run, no baseline yet)")
        out.append(f"<div class='gate pass'>✔ No regressions{vs}</div>")
    else:
        reasons = "; ".join(e(r) for r in gate["reasons"])
        out.append(f"<div class='gate fail'>✗ Regression detected — {reasons}</div>")

    out.append("<div class='headline'>"
               f"<div><div class='num'>{_fmt(mean_all(arm_a))}</div>Without instructions</div>"
               f"<div><div class='num'>{_fmt(mean_all(arm_b))}</div>With instructions</div>"
               f"<div><div class='num up'>{summary['lift']:+.2f}</div>Improvement<br>"
               f"<span class='meta'>caused by the instructions</span></div></div>")

    out.append("<h2>Scores by behavior <span class='meta'>(with instructions, "
               "including tests in development)</span></h2>")
    out.append("<table><tr><th>Behavior</th><th>Score</th><th>Previous baseline</th><th>Change</th></tr>")
    for dim, score in sorted(summary.get("dimensions_all", {}).items()):
        prev = (base or {}).get("dimensions", {}).get(dim)
        out.append(f"<tr><td>{e(dim)}</td><td>{_fmt(score)}</td><td>{_fmt(prev)}</td>"
                   f"<td>{_delta(score, prev)}</td></tr>")
    out.append("</table>")

    out.append("<h2>Individual tests <span class='meta'>(with instructions)</span></h2>")
    out.append("<table><tr><th>Test</th><th>Score</th><th>Change</th></tr>")
    for cid, c in sorted(arm_b.items(), key=lambda kv: kv[1]["score"] or 0):
        tag = " <span class='tag'>in development</span>" if c.get("status") == "xfail" else ""
        prev_case = (prev_results or {}).get("arms", {}).get("B", {}).get(cid, {})
        moves = _moved_checks(cid, c, prev_results)
        delta = _delta(c["score"], prev_case.get("score"))
        if moves:
            detail = "<br>".join(e(m) for m in moves)
            link = (f"<br><a href='{e(compare_url)}'>view instruction changes since previous run</a>"
                    if compare_url else "")
            delta = (f"<details><summary>{delta}</summary><div>{detail}{link}"
                     f"<br><em>small moves can be repetition-to-repetition randomness</em></div></details>")
        out.append(f"<tr><td>{e(cid)}{tag}</td><td>{_fmt(c['score'])}</td><td>{delta}</td></tr>")
    out.append("</table>")
    out.append("<p class='meta'>“In development” tests are behaviors we're still "
               "writing instructions for (test-first). They're reported but cannot fail the run; "
               "a test graduates once it scores ≥ 0.8 in 2 consecutive runs.</p>")

    out.append("<h2>History</h2>")
    out.append("<table><tr><th>Run</th><th>Instructions version</th><th>Overall</th>"
               "<th>Improvement</th><th>Result</th></tr>")
    for h in reversed(history):
        cls = "up" if h.get("gate") else "down"
        word = "pass" if h.get("gate") else "regression"
        out.append(f"<tr><td>{e(str(h.get('timestamp', '?'))[:10])}</td>"
                   f"<td><code>{e(h.get('sha', '?'))}</code></td><td>{_fmt(h.get('suite'))}</td>"
                   f"<td>{h.get('lift', 0):+.2f}</td><td class='{cls}'>{word}</td></tr>")
    out.append("</table></body></html>")
    return "\n".join(out)
