Good catch — let me be more granular.

<assumptions>
  <project>
    - The tool is distributed via Homebrew (confirmed by you)
    - It requires an API key to function (confirmed)
    - Beyond those two things, I know nothing: name, purpose, architecture, whether it reads from env vars or config files, whether setup is 30 seconds or 10 minutes, what the first command should be
    - I'm assuming it's self-contained (no database setup, no additional services to run) but I haven't verified this
  </project>
  <task>
    - You want a Quickstart section in the README (confirmed)
    - The goal is to get new users from zero to functional as quickly as possible (assumed)
    - You want it positioned early in the README, before deeper docs (assumed but not confirmed)
    - The section should be short enough to scan in under a minute (assumed)
    - You're not asking me to write the whole README, just this one section (confirmed)
  </task>
  <operator>
    - You maintain this README and own decisions about tone, structure, and what goes in it (assumed)
    - You know your typical user better than I do (assumed)
    - You have the tool locally or know how it works in detail (assumed)
    - You're not looking for me to guess — you want to provide the missing context yourself (inferred from your question)
    - You prefer I state assumptions explicitly rather than silently filling gaps (confirmed by asking this question)
  </operator>
</assumptions>

The biggest gap is **what happens between "install" and "working"** — what's the actual sequence of commands, and what does success look like to a first-time user?

What matters most for me to know before drafting?