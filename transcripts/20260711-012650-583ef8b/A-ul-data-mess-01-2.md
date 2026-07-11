This is a common but serious problem. Here's a practical approach:

**First, understand the scope:**
- Map which systems hold what data and where conflicts occur
- Determine how many customers are affected and which fields disagree
- Identify which system is authoritative (or if it varies by field)

**Quick wins to attempt:**
- Check for obvious sync failures (one system just hasn't been updated lately)
- Look for data entry mistakes or formatting differences (spaces, capitalization, phone formats)
- See if some systems legitimately hold different data (e.g., billing vs. shipping addresses)

**Decide your source of truth:**
- Pick one system as primary, or designate different fields to different systems
- Document this decision—it matters for future choices
- This might not be the "best" system, just the most reliable one

**Plan a cleanup:**
- Decide how to handle conflicts (manual review for high-value accounts, rules for others)
- Don't just pick one system blindly—you may lose correct data
- Consider cleaning high-impact data first (active customers, revenue-critical fields)

**Prevent recurrence:**
- Fix whatever caused the desync (API integration, sync jobs, process gaps)
- Add monitoring/alerts for future conflicts
- Establish data governance so one person/team owns each field

**The hard question:** Are you fixing this because it's causing real problems now, or preventing future ones? That affects how much effort to spend versus moving forward with known messiness.

What's driving this—an immediate business need or general cleanup?