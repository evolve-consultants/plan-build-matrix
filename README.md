PLAN-BUILD MATRIX
========================================

> **The single biggest problem in communication is the illusion that it has taken place.**


- How do you know you've understood Claude's responses, Claude's intent?
- How do you know Claude has understood you and your intent?
- Have you ever told Claude to do something, and it does it, but then it also does things (for better or worse) that you hadn't intended?

This repository contains instructions that make Claude operate according to an "assumptions alignment" framework. The framework minimizes the risk of a miscommunication, of hours (and tokens) lost in rabbit holes, while increasing your awareness and control of what, exactly, Claude is doing.

Consider this matrix:

<img src="./Plan-Create-Matrix.png" alt="matrix with 4 quadrants, planning on the left, building on the right, shallow knowledge in the top, and deep knowledge in the bottom" width="800">

When working with Claude we are often in one of the four quadrants. The risk that Claude will do something wrong is highest in the top, left-hand quadrant and lowest in the bottom, right-hand quadrant.

In reality, Claude isn't actually doing anything **wrong** but rather acting without clarifying _all_ assumptions up front. The net result is we find ourselves saying things, like, "What was Claude thinking?" ("What was Claude assming?" would be more precise).

By using the instructions in this repository, Claude will guide you, and itself, toward the lower, right-hand quadrant where the risk of doing something unexpected is lowest.

## HOW IT WORKS

The core mechanism is assumption alignment.
Claude assesses how many unvalidated assumptions exist between itself and
the operator (you). Many assumptions → upper-left (explore, surface options).
Few assumptions → bottom-right (execute, single artifact).

Claude should state its position on the matrix before acting on
non-trivial requests. As assumptions are confirmed or challenged during
a conversation, Claude moves naturally between quadrants with the aim of landing in the lower, right-hand quadrant.

## HOW TO VERIFY IT'S WORKING

1. **Positioning statements**: On non-trivial requests, Claude should briefly
   state where it thinks we are on the matrix and why. If this is
   absent, the framework isn't being applied.
2. **Assumption surfacing**: Claude should proactively state assumptions
   before acting, especially early in conversations. No assumptions
   stated = not applying the framework.
3. **Mode matching**: Left-side responses should have multiple options +
   recommended path. Right-side responses should be single artifacts
   with minimal commentary. Wrong mode = wrong quadrant read.
4. **Movement on challenge**: If you push back or reveal new information,
   Claude should shift toward upper-left (more exploration). If it
   stays in execution mode after a challenge, it's not responding to
   the alignment signal.
5. **Spot check**: Ask "what assumptions are you making?" at any point.
   A specific, enumerable answer means it's tracking. A vague answer
   means it isn't.

## SAMPLE PROMPTS

We've included some sample prompts we think are exemplary of the types of prompts you should use in each of the four quadrants. [See the Sample Prompts](./Sample-Prompts-by-Quadrant.md)
## TESTING

The instructions themselves are under test. [TESTING-METHODOLOGY.md](./TESTING-METHODOLOGY.md) describes the full methodology (behavioral dimensions, binary checks, LLM-as-judge rubric, scoring, and regression rules). The test harness lives in [`harness/`](./harness/).

### Running the tests manually

Requires [uv](https://docs.astral.sh/uv/) (it manages the virtualenv and pins the exact Python and package versions from `uv.lock` — no system-Python surprises):

```sh
uv sync          # one-time: creates .venv/ from the lockfile
uv run pytest    # run the test suite
```

Tests also run automatically in GitHub Actions on every push and pull request to `main` (see [`.github/workflows/tests.yml`](./.github/workflows/tests.yml)).
