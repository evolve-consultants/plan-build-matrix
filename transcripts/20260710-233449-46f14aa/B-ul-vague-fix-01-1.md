**Operating from: Upper-Left (Plan + Verify)**

### What I understand you're asking
Users find your dashboard confusing and you want it fixed. But "confusing" can mean many different things, and the fix depends entirely on *what* is confusing and *why*.

<assumptions>
  <project>You have a dashboard (web app, internal tool, analytics, etc.). I don't know its domain, structure, or current state.</project>
  <task>You want to improve user experience by reducing confusion. I don't know if this is causing lost engagement, support tickets, errors, or something else.</task>
  <operator>You have access to users and the dashboard. I don't know your role (PM, eng, design), timeline, or constraints.</operator>
</assumptions>

### What I'm unsure of
- **What kind of dashboard** (analytics, admin panel, data visualization, project management, etc.)
- **What specifically confuses users** (layout, terminology, missing information, too much information, unclear next steps, visual hierarchy, navigation, data interpretation)
- **How you know it's confusing** (user feedback, support tickets, behavioral data, user testing, or just intuition)
- **What you've already tried** to diagnose or fix the problem
- **Your constraints** (timeline, design/eng bandwidth, ability to do user research)

### Options

| | Upside | Downside | Best when |
|---|---|---|---|
| **A: Quick diagnostic interviews** | Fast, direct feedback. You'll hear confusion in users' own words. Takes 30 min per person. | Qualitative only. May not scale to see patterns. | You have 3–5 users you can talk to this week. You need answers fast. |
| **B: Structured user testing** | Systematic. You'll see *where* users struggle (by task, by section). Can observe behavior + ask why. | Takes more time to set up. Requires moderation skill. | You have a week. You can recruit 5–8 users. You want to prioritize fixes. |
| **C: Analyze existing signals** | No recruiting needed. Quick baseline. May reveal obvious issues. | Assumes you have logs/analytics. Doesn't tell you *why*. | You have behavioral data (heatmaps, session recordings, etc.). You want to move fast. |
| **D: A/B test a hypothesis** | Validates fixes before rolling out. Builds confidence in changes. | Requires you to already have a hypothesis about what's confusing. Time to measure. | You think you know the problem and want to prove a fix works. |

### Recommendation
Start with **Option A (quick interviews)** because:
1. It's the fastest path to knowing what's actually broken
2. You'll get language and context from users, which makes the *real* fix clear
3. It takes 2–3 hours of your time and unblocks everything else
4. If it reveals a clear pattern, you can move straight to design/build
5. If it's scattered issues, you'll know to do Option B next

### Next prompt should include
- **Who** you can talk to (internal users, customers, beta testers)
- **How much time** you have before you need to make changes
- **What you've heard so far** (even vague complaints help)
- **Any data you already have** (support tickets, session recordings, analytics dashboards)
- **The dashboard's purpose** (what does it do, who uses it, what should they accomplish in it)

Once I know those, I can help you either **design the interview script**, **analyze existing data**, or **sketch a redesign hypothesis** — depending on what path makes sense.