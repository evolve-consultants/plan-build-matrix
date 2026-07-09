# Plan-Build Matrix Response Templates

## Upper-Left: Plan + Verify

Use this template when assumptions are many or uncertain and the request needs exploration with verifiable reasoning.

```
**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
One to three sentences restating the request in my own words, so you can
confirm or correct my understanding.

<assumptions>
  <project>What I believe about the codebase/environment relevant to this request</project>
  <task>What I believe you're trying to accomplish and why</task>
  <operator>What I believe about your context, expertise, and constraints</operator>
</assumptions>

### What I'm unsure of
- Specific thing that would change my approach
- Another specific thing
- Another specific thing

### Options
| | Upside | Downside | Best when |
|---|---|---|---|
| **A** | ... | ... | ... |
| **B** | ... | ... | ... |
| **C** | ... | ... | ... |

### Recommendation
Option X because Y.

### Next prompt should include
- Which option you prefer (or a different direction)
- Answers to the uncertainties above
- Whether "best when" column matches your situation
```

## Bottom-Left: Plan + Quality

Use this template when assumptions are many or uncertain but the operator owns verification. Focus on communication quality, fit, and actionable options. Leading with a draft can be faster than pure option-listing.

```
**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
One to three sentences restating the request in my own words, so you can
confirm or correct my understanding.

<assumptions>
  <project>What I believe about the codebase/environment relevant to this request</project>
  <task>What I believe you're trying to accomplish and why</task>
  <operator>What I believe about your context, expertise, and constraints</operator>
</assumptions>

### What I'm unsure of
- Specific thing that would change my approach
- Another specific thing

### Here's a rough draft (Option A)
The actual artifact — a short first pass at the deliverable, written
to the best of current understanding.

### Alternatives I considered
- **B**: how it differs and when you'd want it instead
- **C**: how it differs and when you'd want it instead

### Next prompt should include
- Reactions to the draft — what's right, what's off
- Answers to the uncertainties above
- Whether you'd rather see option B or C fleshed out instead
```

## Upper-Right: Build + Verify

Use this template when assumptions are few and you're ready to execute, but the output needs to be externally verifiable. Mark confidence levels inline so the operator knows what to trust and what to double-check.

```
**Operating from: Upper-Right (Build + Verify)**

### What I understand you're asking
One to three sentences restating the request.

<assumptions>
  <project>What I believe about the codebase/environment relevant to this request</project>
  <task>What I believe you're trying to accomplish and why</task>
  <operator>What I believe about your context, expertise, and constraints</operator>
</assumptions>

### The artifact
The deliverable itself. Where specific choices are based on
assumptions rather than confirmed facts, mark them inline:

  some_value: 128  <!-- assumed: check actual limit -->

### What I'm confident about
- Bullet list of claims you can take at face value

### What I'd double-check
- Bullet list of things that are probably right but worth verifying
- Why each one matters if it turns out to be wrong
```

## Bottom-Right: Build + Quality

Use this template when assumptions are few and you're ready to deliver a polished artifact. This is the last off-ramp — state key assumptions upfront so the operator can back out before accepting the output.

```
**Operating from: Bottom-Right (Build + Quality)**

### Confirming before I proceed
These are the key assumptions I'm acting on. If any are wrong,
now is the time to say so:
- Assumption 1
- Assumption 2
- Assumption 3

<assumptions>
  <project>What I believe about the codebase/environment relevant to this request</project>
  <task>What I believe you're trying to accomplish and why</task>
  <operator>What I believe about your context, expertise, and constraints</operator>
</assumptions>

### The artifact
The deliverable itself — full quality, minimal commentary.
```
