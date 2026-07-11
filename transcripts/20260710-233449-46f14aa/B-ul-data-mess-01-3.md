**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking

You have customer records in four different systems that contain conflicting information, and you need a strategy to resolve the inconsistencies and prevent them from recurring.

<assumptions>
  <project>You have some ability to query/audit all four systems and possibly modify data or processes. The systems likely serve different business functions (billing, CRM, support, etc.).</project>
  <task>You want to establish a single source of truth and ensure data stays consistent going forward — not just fix today's mess, but prevent it from happening again.</task>
  <operator>You probably have some authority to change processes or tooling, but likely not unlimited time/budget. You're looking for a practical path forward, not a theoretical ideal.</operator>
</assumptions>

### What I'm unsure of

- **Which system is authoritative today?** (Or is there one?) This changes everything about the fix strategy.
- **What's causing the drift?** (Manual entry in multiple places, batch syncs failing silently, different update rules, lack of enforcement?)
- **How recent is the data?** Are we talking days/weeks of drift or months/years?
- **What happens if you pick wrong?** (Financial impact, customer impact, operational friction?)
- **Scope of inconsistency:** Is it a few fields (address, email) or fundamental identity (which records represent the same customer)?

### Options

| | Best for | Time | Risk | Effort |
|---|---|---|---|---|
| **A: Audit first, then declare a source of truth** | You need to understand the problem before fixing it. Prevents rushing into a bad solution. | 1–2 weeks | Low—you learn before committing | Medium—requires systematic querying |
| **B: Designate the most authoritative system now, sync all others to it** | You need a fast fix and have high confidence in one system's data quality. | Days–1 week | Medium—assumes one system is actually trustworthy | Low—straightforward execution |
| **C: Build a consolidation/deduplication layer (CDI or master data)** | You expect ongoing multi-system updates and need a durable solution. The systems will never fully sync otherwise. | 4–12 weeks | Low after it's live; high during | High—significant tooling/process change |
| **D: Pick a system to be the customer view layer, let others stay specialists** | You accept that systems will differ by design. They serve different purposes and shouldn't be forced to agree. | Days | Low—no forced sync | Low—mostly a communication/process change |

### Recommendation

**Start with A (audit), then move to C or D depending on what you find.**

Here's why:
1. **Options B, C, and D all assume you know what the "right" answer is.** You probably don't yet. An audit takes a week and saves you months of fixing the wrong thing.
2. **The audit will tell you whether this is a technical problem or a process problem.** (Often it's process.)
3. **Once you know the root cause, C and D become much cheaper** because you know what you're preventing.
4. **C is the "proper" solution** if multiple systems legitimately need to write customer data. **D is the pragmatic solution** if one system should own customer identity and the others should read it.

### Next prompt should include

- Answers to the five uncertain items above (especially: which system should be authoritative? what's the root cause of drift?)
- Whether you're looking for a quick stabilization or a longer durable fix
- Whether I should help you design an audit first, or if you'd rather jump straight to one of the other options

If you want to move forward with an audit, I can give you a checklist of what to measure.