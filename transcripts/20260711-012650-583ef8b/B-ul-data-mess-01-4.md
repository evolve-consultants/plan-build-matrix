**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer records in four different systems with conflicting information, and you need a strategy to resolve the inconsistencies and establish a reliable single source of truth.

<assumptions>
  <project>You have ongoing access to all four systems; they're not legacy/read-only. You have some ability to modify data or establish new processes.</project>
  <task>You want to fix this systematically rather than manually reconcile one customer at a time. This is blocking downstream work (reporting, operations, customer experience).</task>
  <operator>You're technically empowered to make architectural decisions but probably don't own all four systems independently (they belong to different teams or vendors).</operator>
</assumptions>

### What I'm unsure of
- **Scope of disagreement**: Is it a few key fields (address, email, phone) or everything? Do the disagreements follow a pattern (one system always more recent, or random conflicts)?
- **System ownership**: Do you control all four systems, or do different teams own them? This drastically changes your options.
- **Data volume**: Are we talking hundreds of customers or millions? This affects whether manual spot-checking is viable.
- **Criticality of accuracy**: Do conflicts cause immediate business problems (orders failing, billing errors) or is this more of a data hygiene issue?
- **Existing sync mechanisms**: Are any of these systems already supposed to be talking to each other? Or is this four silos you're discovering now?

### Options

| | Approach | Upside | Downside | Best when |
|---|---|---|---|---|
| **A: Audit first** | Catalog exactly what disagrees, by field and customer segment. Pick one system as temporary truth. Don't touch data yet. | You understand the problem before acting. Low risk. Gives you data to negotiate with teams. | Takes time. Doesn't fix anything immediately. | You're unsure how bad it is or don't control all systems. This is almost always the right first move. |
| **B: Master data management layer** | Build (or buy) an MDM system as the authoritative source. Sync all four systems to it. Establish governance for conflicts going forward. | Solves the root cause. Creates a single source of truth. Scales. | Expensive. Time-consuming. Requires buy-in from multiple teams. High risk of disruption during migration. | You control all four systems and have budget. This is the "proper" solution. |
| **C: Establish a consolidation process** | Pick the most reliable system as primary. Weekly/daily automated sync (where possible) with manual reconciliation for conflicts. Freeze non-primary systems from direct customer edits. | Faster than MDM. Lower cost. Fixes most of the problem. | Doesn't eliminate root cause — you're managing the symptom. The "primary" system becomes a bottleneck. | You need a quick fix and can enforce that teams edit one system. Medium-term bridge to B. |
| **D: Distributed trust with conflict resolution** | Define which system is authoritative for which fields (e.g., billing system owns payment info, CRM owns contact history). Establish reconciliation rules for the rest. | Respects team ownership. Lighter weight than MDM. | Complex to implement. Hard to explain to stakeholders. Conflicts still require manual review. | Systems have natural, clear domains of authority and disagreements are rare. |

### Recommendation
**Start with Option A (Audit)**, then move to either C or B depending on what you find.

Here's why: An audit takes days, costs nothing, and gives you leverage. You'll discover whether this is fixable with process changes (Option C) or whether you genuinely need infrastructure (Option B). Most teams guess wrong about how bad data misalignment is until they measure it. Once you have that data, the decision between C and B becomes obvious.

### Next prompt should include
- Which of the four systems do you control? Which do other teams own?
- What fields are conflicting most often? (names, contact info, payment details, identifiers?)
- What's the customer count in each system?
- Is this blocking something urgent, or is it more of a "we should fix this" project?