Good question. I made several assumptions:

1. **Tool naming**: I used a placeholder `your-tool-name` assuming you'd fill in the actual name. I didn't know if it's a real project.

2. **Homebrew availability**: I assumed the tool is already published to Homebrew's core or a custom tap. Installation would fail otherwise.

3. **API key format**: I assumed it's a simple string-based key (not OAuth, JWT, or other auth methods).

4. **Environment variable approach**: I assumed env vars are the preferred/simplest setup method, rather than config files, CLI prompts, or other options.

5. **Shell type**: I defaulted to zsh/bash profiles, which might not apply to fish shell, Windows PowerShell, or other environments.

6. **Single API key**: I assumed one key is needed, not multiple keys or credential types.

7. **Existing website/docs**: I assumed you have an API key generation page and fuller documentation elsewhere.

8. **User technical level**: I assumed users are comfortable with environment variables and shell profiles.

9. **Existing help command**: I assumed `--help` works out of the box.

What assumptions would you like me to adjust? Knowing more about your specific tool, target audience, or setup complexity would help me refine this.