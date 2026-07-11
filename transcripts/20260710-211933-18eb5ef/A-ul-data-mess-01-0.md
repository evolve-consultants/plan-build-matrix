# Quick diagnosis first

Before fixing, understand what's actually broken:

- **Same records, different values?** (one system says customer is in NY, another says CA)
- **Different record counts?** (some systems have duplicates or old entries)
- **Different field definitions?** (one system's "active" means something different)
- **Timing issues?** (systems update at different intervals, so they're naturally out of sync)

# Practical approach

1. **Pick a source of truth** — usually your newest or most authoritative system, but be deliberate about it
2. **Map the discrepancies** — run a audit report comparing all four. Where's the biggest damage?
3. **Fix at the source** — don't just patch one system. Understand why they diverged (manual entry errors? failed syncs? different business logic?)
4. **Decide on reconciliation**:
   - Automated sync going forward (if systems can talk to each other)
   - Regular manual audits (if they can't)
   - Single entry point (route all customer changes through one system)

# Hard questions to ask

- Who actually owns customer data? (If nobody, you've found your real problem)
- Which system is used for critical decisions? (That should probably be your source of truth)
- Can you afford to migrate everything to one system, or does that need to stay distributed?

What matters most in your case — billing accuracy, customer contact info, or something else?