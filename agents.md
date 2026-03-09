# ASVS Level 1 Compliance Agent

As requested, an AI agent should check this repository against the OWASP ASVS Level 1 requirements after every commit.

## Instructions for the Agent

1. **Trigger**: This workflow should be manually or automatically invoked after changes are committed.
2. **Action**: The agent should read the `.agent/skills/asvs_level_1/SKILL.md` file.
3. **Review**: The agent will scan the codebase (using `grep_search`, `list_dir`, `view_file`) and cross-reference the implemented controls (like the `AuthLog`, session configurations, password policies, input validation) against the checklist provided in the ASVS Level 1 skill.
4. **Report**: The agent must output a final report detailing any identified vulnerabilities or missing Level 1 controls that were introduced or remain unfixed.

## Example Usage

When reviewing, the AI assistant will ensure:
- Secrets are not hardcoded (checked via `.env` usage).
- The `AuthLog` is actively capturing authentication events.
- Role-based Access Control (RBAC) in `todos/views.py` correctly restricts access based on the defined groups.
