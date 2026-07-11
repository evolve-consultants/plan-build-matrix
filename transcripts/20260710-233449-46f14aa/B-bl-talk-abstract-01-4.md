**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
You've built a design system and want to pitch it as a conference talk. You own the factual details and will catch anything inaccurate; you want me to focus on structure, narrative arc, and impact — making it compelling and coherent enough to get accepted.

<assumptions>
  <project>You have a design system that's live/mature enough to talk about publicly. It solves a real problem your organization had.</project>
  <task>You're submitting this to a design/engineering conference. The abstract needs to hook reviewers and signal that you have something worth 30–45 minutes.</task>
  <operator>You know the system inside out and will fact-check. You want strategic feedback on framing, not verification help.</operator>
</assumptions>

### What I'm unsure of
- **Scope and novelty**: Is this system a visual design system (colors, components), a process system, something architectural, or hybrid? What's genuinely new about your approach?
- **The core problem it solved**: Was it chaos (100 button styles), fragmentation (web vs. mobile), speed (shipping time), or something else?
- **Your audience**: Are you talking to designers, engineers, or mixed? This changes what problems feel urgent.

### Here's a draft (Option A)

---

**How We Built a Design System Without Losing Our Product**

Design systems are supposed to speed you up. Ours almost slowed us down.

When we started, we had one goal: reduce fragmentation across our product. What we didn't anticipate was how a naive system could become a straitjacket — forcing decisions upstream that belonged downstream, blocking teams from shipping, and creating the exact bottleneck we were trying to prevent.

In this talk, we'll walk through how we rebuilt our system with a different philosophy: **governance as friction reduction, not control**. We'll cover the architecture decisions that let teams move fast while staying aligned — including what we tried that failed, how we measure "working" vs. "broken," and the single practice that made adoption stick when mandates didn't.

You'll leave with a framework you can use whether you're starting a system from scratch or rescuing one that's become a liability.

---

### Alternatives I considered

- **B (Problem-first)**: Lead with the crisis moment — "We had 47 button components" — to signal urgency before pivoting to philosophy. Works better if your system solved a dramatic, specific disaster.

- **C (Technical-first)**: Open with the architecture or tooling innovation — "We built a system that lives in three places and stays in sync" — if the *how* is more novel than the *why*. Better for engineer-heavy audiences.

### Next prompt should include
- What the actual core problem was (the one you'd spend half the talk on)
- Whether the angle feels right — does "governance as friction" resonate, or is there a better frame?
- Any details that are flatly wrong (timeline, scale, outcomes)
- Your gut on which alternative direction, if any, lands better