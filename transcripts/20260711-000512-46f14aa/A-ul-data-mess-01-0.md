# Fixing Disagreeing Customer Data Across Systems

This is a common but genuinely tricky problem. Here's how to approach it systematically:

## 1. Diagnose Before You Fix

Before reconciling anything, figure out *why* they disagree:
- **Different update cadences** (one system syncs nightly, another real-time)
- **Different sources of truth** (sales team edits CRM, support edits helpdesk, no sync between them)
- **Different data models** (one stores full name, another first/last split differently)
- **Manual entry errors** vs. **integration/sync bugs**
- **Duplicate records** within individual systems (not just across them)

The fix is very different if this is a sync problem vs. a governance problem vs. a data quality problem.

## 2. Establish a System of Record

Pick one system as the **authoritative source** for each data type (this might differ by field):
- CRM might own "company name, deal stage"
- Billing system might own "legal entity name, payment terms"
- Support system might own "product usage, ticket history"

Not every system needs to own everything — but every *field* needs exactly one owner.

## 3. Assess the Damage (Scope the Problem)

Before building pipelines, sample the data:
- Pick 50-100 customers and manually compare across systems
- Categorize the conflict types (missing data, stale data, contradictory data, formatting differences)
- This tells you whether you need fuzzy matching, simple sync, or a full MDM (Master Data Management) initiative

## 4. Choose Your Reconciliation Approach

Depending on scale/budget:

| Approach | When it fits |
|---|---|
| Manual cleanup + spreadsheet | <500 customers, one-time fix |
| ETL/reverse-ETL tool (Fivetran, Census, Hightouch) | You have several SaaS tools and want ongoing sync |
| Customer Data Platform (CDP) | You need unified profiles for marketing/analytics |
| Master Data Management (MDM) | Large enterprise, many systems, compliance needs |
| iPaaS + custom matching logic | Complex business rules, unusual data shapes |

## 5. Build the Matching/Merge Logic

- Define a matching key (email, customer ID, phone+name fuzzy match)
- Decide **conflict resolution rules** (most recent wins? System of record wins? Manual review for high-value accounts?)
- Flag irreconcilable conflicts for human review rather than silently guessing

## 6. Fix the Root Cause, Not Just the Symptom

Once cleaned, prevent re-drift:
- Set up one-way or bi-directional syncs between systems
- Add validation rules at data entry points
- Assign data governance ownership (who's allowed to edit what, where)
- Schedule periodic audits (quarterly spot-checks)

---

**A few questions that would help me give more specific advice:**
- What are the four systems (CRM, billing, support, ERP, etc.)?
- Roughly how many customer records are we talking about?
- Is this a one-time cleanup or do you need ongoing sync?
- Do you have engineering resources, or does this need to be low-code/manual?