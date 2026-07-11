**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
You have customer data in four systems with conflicting values, and you need a strategy for resolving or managing this inconsistency. You want to know what to do about it.

<assumptions>
  <project>The systems are likely operational/legacy (not easily replaceable) and the conflicts are actively causing problems or creating risk.</project>
  <task>You're trying to establish a single source of truth or at least make the conflicts manageable and visible.</task>
  <operator>You have authority to make decisions about data architecture but may have constraints around system changes, downtime, or integration complexity.</operator>
</assumptions>

### What I'm unsure of
- **How much the systems disagree**: Are we talking about different values for the same field, missing data in some systems, or genuinely incompatible schemas?
- **Which system (if any) is authoritative**: Do you know which one is correct, or is this a "all four are partially wrong" situation?
- **What's driving the conflicts**: Are these sync failures, different business rules, manual entry errors, or legacy migration debt?
- **Scope and urgency**: Are you trying to fix this for a specific use case (e.g., billing, support) or across the whole organization? Is this causing active customer issues today?
- **What you can change**: Can you modify the systems themselves, or do you need a solution that works around them as-is?

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Audit & Assign Authority** | Determines which system is source of truth; gives you a clear target state. Relatively low effort upfront. | Doesn't solve the immediate conflict; requires picking a winner that may not be the most complete. | You have time to plan; conflicts aren't causing urgent customer harm; you want a long-term fix. |
| **B: Build a Unified Layer** | Creates a single view for downstream consumers; lets you apply consistent rules. Isolates the conflicts behind an API. | Requires investment in a new system; doesn't fix the root data conflicts; adds a maintenance burden. | You have engineering resources and conflicts are blocking multiple teams from working independently. |
| **C: Implement Real-Time Sync** | Keeps all systems in sync going forward; prevents new conflicts. Reduces long-term manual effort. | Doesn't address *existing* conflicts; requires identifying the authoritative system first; complex to implement well. | The conflicts are from drift over time, not systematic disagreement; you have a clear source of truth. |
| **D: Quarantine & Migrate** | Forces a clean break; eliminates the problem entirely once complete. Guarantees future accuracy. | Highest cost and risk; requires downtime or parallel running; long timeline. | One system is clearly the best and you can retire the others; conflicts are severe enough to justify the lift. |
| **E: Accept & Document** | Lowest effort; reduces false confidence in bad data; unblocks teams. | Doesn't fix anything; embeds the inconsistency in your processes; creates long-term liability. | This is genuinely a known acceptable tradeoff (rare); a temporary holding pattern while planning A, B, or C. |

### Recommendation
Start with **Option A (Audit & Assign Authority)** because:
1. It's the fastest way to understand the problem deeply enough to pick the right long-term approach.
2. It creates a clear decision point for whether you need B, C, D, or a hybrid.
3. You learn which system is closest to ground truth, which informs everything downstream.
4. It's low-cost and low-risk — it doesn't commit you to anything.

After the audit, you'll likely move to **C or B** depending on what you find.

### Next prompt should include
- Which system is most critical to your business? (That's where I'd start the audit.)
- Are specific fields in conflict, or is the disagreement scattered across the schema?
- Do you have access to ground truth outside the systems (e.g., transaction logs, customer-confirmed data)?
- Is there a team that owns "customer data" or does each system have its own owner?
- What's your appetite for engineering work vs. process/manual work?