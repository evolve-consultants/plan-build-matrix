**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
Rewrite your README's opening section to be warmer, more inviting, and less dense—while keeping the substance intact. You'll verify technical accuracy separately.

<assumptions>
  <project>This is a software project with an existing README that starts with standard boilerplate (problem statement, features, installation, etc.)</project>
  <task>You want the first thing readers see to feel less intimidating and more human, so they're more likely to actually engage with the project</task>
  <operator>You know the project well enough to catch any factual slips I make, so I can prioritize voice and structure over defensive hedging</operator>
</assumptions>

### What I'm unsure of
- **Tone level**: are you aiming for conversational-but-professional, or can it be more playful?
- **Project category**: is this a library, tool, framework, or something else? (affects how I frame the "why you should care" angle)
- **Primary audience**: developers shipping features fast? DevOps? Data practitioners? (affects what pain points to lead with)

### Here's a rough draft (Option A)

```markdown
# [Project Name]

**[One-line hook that says what problem this solves, not what it does.]**

Most [relevant context] projects struggle with [specific friction point]. 
[Project Name] fixes that by [one clear benefit]. You get [concrete outcome] 
without [thing you'd normally have to deal with].

#### Why this matters
- **[Benefit 1]**: [Why it saves time/money/sanity]
- **[Benefit 2]**: [Why it's better than the alternative]
- **[Benefit 3]**: [Why people actually use it]

#### Quick start
```bash
# Get it running in 30 seconds
npm install [package-name]
```

See the [full setup guide](docs/setup.md) if you need more detail.

---

Everything else (features, API, examples, contributing) lives in the sections below.
```

### Alternatives I considered
- **B**: Lead with a 2-3 sentence narrative story (e.g., "We built this because...") — warmer but slower to get to the point; works well if your origin story is genuinely interesting
- **C**: Lead with a visual (diagram, screenshot, short GIF) — highest engagement but requires you already have one; I'd draft text to pair with it

### Next prompt should include
- Which of these feels closest to the tone you want
- Answers to the three uncertainties above (especially project category and audience)
- The actual opening text you're replacing, so I can keep project-specific details accurate
- Whether you'd rather I flesh out option B or C instead