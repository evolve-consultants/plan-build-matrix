**Operating from: Bottom-Left (Plan + Quality)**

### What I understand you're asking
Your four systems each hold customer records that have drifted out of sync (different values, maybe different identifiers for the same person), and you want a path toward reconciling them.

<assumptions>
  <project>The four systems are likely separate functional silos (e.g. CRM, billing, support, marketing) that were never integrated with a shared identity or sync process</project>
  <task>You want a practical way to get to a trustworthy, consistent view of customer data — likely because something downstream (reporting, ops, a migration, a compliance ask) is being blocked by the disagreement</task>
  <operator>Unclear whether you're technical, whether there's budget for tooling, and whether this is a one-time cleanup or a recurring pain</operator>
</assumptions>

### What I'm unsure of
- What actually disagrees — different values for the same fields (address, status), or different *identifiers* for the same customer (harder problem: identity resolution)?
- Scale — hundreds of customers or millions? Manual fixes are viable at one scale and absurd at another.
- Is this a one-time cleanup, or do these systems need to stay in sync going forward?
- Is there a forcing function (compliance, a merger, a migration) or is this general hygiene?
- Any existing appetite/budget for tooling (MDM/CDP platforms), or is this expected to be a process fix?

### Here's a rough draft (Option A)
A lightweight starting approach, assuming this is closer to "messy but fixable" than "deep identity resolution problem":

1. **Audit before you fix.** Pull a sample of customers that exist in all four systems and catalog *where* they disagree — which fields, how often, and why (stale sync, manual entry, different definitions of "customer"). Don't build a solution before you know the shape of the problem.
2. **Establish a source-of-truth hierarchy per field**, not per system. E.g., billing system wins for legal name/address, CRM wins for contact preferences, support system wins for status flags. Few orgs have one system that's authoritative for everything.
3. **Pick or generate a stable identifier** to join records across systems (email, customer ID, or a probabilistic match if keys don't line up cleanly). This is usually the actual hard part — worth confirming early whether you already have this.
4. **Decide one-time vs. ongoing.** If these systems will keep diverging, a manual cleanup just resets the clock. If it's ongoing, you're looking at a sync process or MDM tool, not just a project.

### Alternatives I considered
- **B — Adopt an MDM/Customer Data Platform**: right call if this is a recurring, growing problem across an org where new systems will keep getting added. Overkill if this is a one-time mess with four fixed systems.
- **C — Full one-time data cleanup project (dedupe + standardize) with no new infrastructure**: right call if this is a known, bounded, one-time mess (e.g., pre-migration) and you don't expect the four systems to keep operating independently afterward.

### Next prompt should include
- What kind of disagreement you're seeing (value conflicts vs. identity/matching problems)
- Rough scale of customer records
- Whether this needs to be solved once or needs to stay solved
- Whether tooling is on the table or this needs to be a process-only fix