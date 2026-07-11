**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four different systems that contain conflicting or inconsistent information, and you need a way forward. You're likely looking for a strategy to either reconcile them or establish a single source of truth.

<assumptions>
  <project>You have four distinct systems (possibly CRM, billing, support, marketing—or similar) with overlapping customer data that diverges</project>
  <task>You want to either fix the data or prevent future divergence (or both)</task>
  <operator>You own or influence decisions about these systems but may not control all four; this is a strategic/architectural problem, not just a data cleanup</operator>
</assumptions>

### What I'm unsure of
- **Why they diverge**: Are certain systems authoritative for certain fields? Do they sync and fail silently? Do different teams manually update different systems? Are there intentional reasons they differ?
- **Scale and urgency**: Is this 100 customers or 100,000? Do you need a fix in days or can this be a quarter-long project?
- **Constraints**: Can you modify these systems? Do you have budget for new tooling? Is there a system you can't touch?
- **What "agree" means**: Are we talking exact matches, or do you just need consistency on critical fields (name, email, ID)?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Emergency audit + manual reconciliation** | Fast, low-risk, builds institutional knowledge of the problem | Doesn't scale, one-time fix, teams keep re-diverging | You have <1000 records and need confidence in the data *now* |
| **B: Designate a system of record + sync rules** | Stops future divergence, clarifies ownership, relatively simple to implement | Requires choosing which system "wins" (political), doesn't fix historical data, only works if you can modify systems | You have clear winner system (e.g., CRM is authoritative for contact info) and can write/enforce sync logic |
| **C: Build a customer data platform (CDP) or unified layer** | Single source of truth, all systems query it, can implement validation rules, most flexible long-term | Expensive, complex, takes time, requires ongoing maintenance | This is a chronic problem across your org, or you're planning 3+ year roadmap |
| **D: Implement data governance + regular audits** | Prevents future drift, establishes accountability, works for any system combination | Doesn't fix existing data, requires discipline/tooling, slow to show results | You can solve the immediate divergence manually and want to prevent recurrence |

### Recommendation
**Start with A + B together:**

1. **Quick audit** (this week): Pull a sample of 50–100 customers from all four systems. Do a manual spot-check. This tells you *how bad* it is and *why* it diverges (different update cadences? different data definitions? different user bases?).
2. **Designate authority** (this week): Decide which system is authoritative for which fields (e.g., CRM owns contact info, billing system owns payment method). Document it.
3. **Fix critical records** (next 1–2 weeks): Manually reconcile the most important customers (high-value, recently contacted, etc.).
4. **Build sync or validation** (parallel): Start with the easiest win—maybe a daily script that compares key fields and flags mismatches, or a one-way sync from the authoritative system.

This gets you to **working data fast** while building toward **a sustainable system**.

### Next prompt should include
- How many customers we're talking about
- Which system is (or should be) authoritative for each major field
- Whether you can modify the systems or if they're locked
- How much time you can invest (rushed vs. phased approach)
- A concrete example of how one customer's data differs across the four systems