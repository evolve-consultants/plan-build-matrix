Here are my explicit assumptions, grouped by category:

**About the project/tool:**
- It's already published to a Homebrew tap (ready to install)
- It requires exactly one API key to function
- The API key is the only setup hurdle between install and first use
- It's a command-line tool with standard CLI conventions
- The tool has a help command (`--help`)

**About the API key infrastructure:**
- An API key is something users obtain from you (not generated locally)
- There's a place where users go to get one (a dashboard, signup page, or contact method)
- The key is a string that doesn't change per invocation
- It's safe to show how to pass it in an example (not a security anti-pattern in your context)

**About how the key is used:**
- It's passed via environment variable OR config file (most common patterns)
- There's no additional authentication flow after the key is set
- One key works for everything the tool does

**About the audience:**
- They're developers (comfortable with `export`, `~/.config`, command line)
- They've never used your tool before
- They can find and follow a link to get an API key without hand-holding

**About your constraints:**
- You want this section short (Quickstart implies 4-6 steps max)
- The README already exists or follows standard structure
- You're willing to provide the missing details to refine it

**About what "quickstart" means to you:**
- Time-to-first-success is the priority over comprehensive documentation
- One happy path is better than multiple options

---

**The ones I'm most uncertain about:**
1. Where/how users get the API key (this determines step 2 entirely)
2. How it's passed to the tool (this changes the setup pattern)
3. What a realistic first command looks like (matters for step 4 credibility)

Any of these wrong? That's where I should recalibrate before drafting.