**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
You want a warmer, more approachable opening for your README that draws readers in instead of overwhelming them with dry exposition. You'll verify the factual claims yourself.

<assumptions>
  <project>This is an open-source or team project with a README that currently leads with dense technical or administrative content</project>
  <task>Make the first impression more inviting and human, to help people quickly grasp what the project does and why they should care</task>
  <operator>You own the domain knowledge and can fact-check, so I should focus on tone, structure, and clarity rather than perfect accuracy</operator>
</assumptions>

### What I'm unsure of
- **Project type**: Is this a library, tool, CLI, framework, application, or something else?
- **Audience**: Who are the primary readers? (developers, end users, contributors, researchers?)
- **The current opening**: What's the tone/content right now? (features list, installation, problem statement, architecture?)

### Here's a rough draft (Option A)
A template that works for most projects — adapt the voice and content to fit yours:

```markdown
# ProjectName

**What it does in one sentence that makes people say "oh, I need that."**

Most people encounter [common problem/workflow] and think "there has to be a better way." 
There is. ProjectName [one-sentence core value: does X faster / removes step Y / solves Z painlessly].

## Why it exists

[2–3 sentences on the gap it fills. What was annoying before? What's better now?]

## Quick start

[5 lines of code showing the happy path. Something that *works* and illustrates the idea immediately.]

## What you can do with it

- [Capability 1]
- [Capability 2]
- [Capability 3]

**Want to dive deeper?** → [Link to docs / installation / examples]
```

### Alternatives I considered

**B: Problem-first (storytelling angle)**  
Lead with a concrete problem scenario ("You're juggling N tools to do X...") before naming the solution. Works great for tools solving workflow friction but can feel over-dramatized for libraries.

**C: Persona-first (audience-specific)**  
Open with "For [role], ProjectName is [value]" in multiple bullets, each speaking to a different user type. More inclusive but takes more space and risks feeling scattered.

### Next prompt should include
- What type of project this is and who uses it
- The actual opening text (or a summary of what's there now)
- Whether you prefer the direct (A), narrative (B), or multi-audience (C) angle
- Any tone notes (playful? professional? somewhere in between?)