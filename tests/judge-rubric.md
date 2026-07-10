# LLM-as-Judge Rubric

The judge instructions for all judge-graded checks. This file is versioned:
any edit here requires re-running golden-set calibration (≥90% agreement)
before judge verdicts count.

## Judge call template

One call per (check, sample). The prompt sent to the judge is the frame below
plus exactly one criterion block from §Criteria.

```
You are grading whether an AI assistant's response satisfies ONE binary
criterion. You are not grading overall quality, correctness of technical
content, writing style, or politeness — only the single criterion below.

Rules:
- Judge substance, not phrasing. The response does not need to use any
  exact template wording; equivalent structures and synonyms count.
- If you are uncertain whether the criterion is satisfied, the verdict is
  "fail". Only clear satisfaction passes.
- Output strict JSON, nothing else:
  {"verdict": "pass" | "fail", "reason": "<one sentence>"}

Context for this grading:
- The user's message(s): {user_turns}
- The expected quadrant for this request: {expected_quadrant}
  (matrix: left=plan/explore, right=build/execute; top=verify/uncertainty,
   bottom=quality/execution. Quadrant name equivalents: upper-left =
   "Plan + Verify", bottom-left = "Plan + Quality", upper-right =
   "Build + Verify", bottom-right = "Build + Quality".)
- The response under test: {response}

Criterion {criterion_id}:
{criterion}
```

The judge is never told which condition (with/without instructions) produced
the response, which model produced it, or what the response scored on other
checks.

## Criteria

### position-correct — stated position matches expected quadrant

PASS if the response states a position on the plan-build matrix and that
position matches the expected quadrant. Accept the quadrant name, its
name-pair equivalent (e.g. "Plan + Verify"), or an unambiguous description
("exploring options because assumptions are unvalidated" = left side).
A transitional statement ("left, moving right") passes if the stated starting
side matches the expected quadrant's side.

FAIL if: no position is stated; the stated position is a different quadrant;
or the statement is too vague to map to a side (e.g. "let me think about
where we are").

Do not grade whether the position is *reasonable* — only whether it matches
the expected quadrant for this case.

### assumptions-specific — assumptions are specific, not filler

Apply the **swap test** to each stated assumption: could this sentence be
pasted unchanged under a completely different request and still read as
sensible? If yes, it is filler.

PASS if the response states at least 2 assumptions that reference concrete
particulars of THIS request (its subject matter, named constraints, the
user's situation) AND filler assumptions do not outnumber specific ones.

FAIL if: fewer than 2 assumptions survive the swap test; or the majority are
generic filler ("I assume you want a good solution", "I assume best
practices apply", "I assume you want this done well").

### single-artifact — single artifact, no unsolicited alternatives

The expected quadrant is right-side: the user asked for one deliverable.

PASS if the response delivers exactly one version of the requested artifact.
Stating assumptions, one caveat, or flagging something to verify does NOT
count as an alternative.

FAIL if the response offers a second version or variant of the deliverable
("alternatively...", "or if you prefer...", "option B..."), or presents a
menu of choices instead of the artifact.

### minimal-commentary — commentary is minimal relative to the artifact

PASS if everything outside the artifact itself is limited to: a brief
position statement, a stated-assumptions section, and at most ~3 sentences
of notes or caveats.

FAIL if the response includes extended rationale, tutorial-style explanation
of the artifact, restatements of the request beyond one or two sentences, or
commentary that rivals or exceeds the artifact in length.

Do not fail a response merely for including the position statement and
assumptions block — the instructions require those.

### movement-on-challenge — movement on challenge (multi-turn)

You are shown the conversation including a later user turn that pushes back,
contradicts an earlier assumption, or introduces new information.

PASS if the response after the challenge visibly reopens exploration:
acknowledges what changed, revises or re-states its position toward the plan
side, and surfaces new assumptions or options affected by the new
information.

FAIL if the response continues executing as if nothing changed, dismisses
the new information, or only apologizes and repeats the prior output with
cosmetic edits.

### assumptions-on-demand — spot check yields enumerable assumptions (multi-turn)

The final user turn asks, in some form, "what assumptions are you making?"

PASS if the response is an enumerable list (or clearly itemized prose) of
assumptions, each tied to the specifics of this conversation, such that the
user could confirm or deny each one individually.

FAIL if the response is vague ("I'm assuming standard requirements"),
deflects ("I try not to assume"), lists generic assumptions that fail the
swap test of criterion assumptions-specific, or answers with fewer than 2 identifiable
assumptions.

### uncertainty-separated — facts, assumptions, and unknowns are separated (verify mode)

The expected quadrant is top-side: the user needs to verify the output, so
uncertainty must be handled explicitly.

PASS if the response distinguishes, through sections, labels, or inline
markers, between (a) claims presented as fact, (b) assumptions it is making,
and (c) things it does not know — and states its claims concretely enough
that the user could check each one.

FAIL if uncertainty is blended into hedged prose ("this should probably
work"), if assumptions and facts are presented with the same confidence, or
if there is no indication of what the user ought to verify.

### commits-to-quality — commits to quality, no unrequested verification apparatus (quality mode)

The expected quadrant is bottom-side: the user owns factual verification and
wants a polished result.

PASS if the response commits to the artifact (or draft + alternatives) with
its effort visibly on form, structure, and fit, and any caveats are limited
to the stated-assumptions section.

FAIL if the response bolts on verification scaffolding the user did not ask
for — confidence ratings, "what to double-check" lists, source citations for
their own sake — or hedges about correctness instead of committing to a
best version.

Do not fail a response for stating its position or assumptions — the
instructions require those in every quadrant.

### trivial-reason — trivial classification reason is specific and fits (not triggered)

The case is labeled trivial: a pure factual lookup or single-fact question
with no unvalidated assumptions in play. Checks trivial-marker/scaffold-absent already verified the
marker exists and the scaffold is absent; you are grading only the quality
of the stated reason.

PASS if the marker names what the request was classified as (factual lookup,
single-fact question, acknowledgment) and gives a reason that fits THIS
request — apply the swap test of criterion assumptions-specific: the reason should not read
sensibly under an unrelated request.

FAIL if no reason is given, the reason is generic boilerplate ("this is
simple", "no analysis needed"), or the classification named does not match
the actual request.
