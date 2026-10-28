# Project integrations: code, tracker, wiki, CI, CRM

One workflow in the kit, one configuration per project. A project declares its platforms in
`<project>/integrations.json` (template: `templates/project/integrations.json`); every block is
optional. Skills that use it: `work-tracking`, `find-information`, `support-case`.
Set up or check a machine: `python <kit>\scripts\setup-integrations.py --project <folder>`.

## Rules for every adapter
- Read `integrations.json` first; use its IDs, account and defaults. Missing value: look it up
  with the adapter, then propose adding it to the file (do not keep it only in tool memory).
- **Account per project:** use the account the file names (`code.account`). With `gh`, check
  `gh auth status`; switch with `gh auth switch -u <account>` and switch back afterwards.
- Logins are done by the user, never by the AI, and no token goes into a file.
- A project skill named in `preferSkill` (team templates) wins over the generic kit skill.

## Adapters

| Category | Type | Tool | Typical commands / tools |
|---|---|---|---|
| code | `github` | `gh` | `gh repo view`, `gh pr list/view/create`, `gh pr checks`, `gh search code` |
| code | `azure-repos` | Azure DevOps MCP or `az repos` | `az repos pr list/create`, `az repos show` |
| code | `gitlab` | `glab` | `glab mr list/create` |
| tracker | `jira` | Atlassian MCP (`mcp__atlassian__*`) | `searchJiraIssuesUsingJql`, `getJiraIssue`, `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `addOrEditJiraIssueComment` (cloudId from the file) |
| tracker | `azure-boards` | Azure DevOps MCP or `az boards` | `az boards query --wiql`, `az boards work-item create/update` |
| tracker | `github-issues` | `gh` | `gh issue list/create/edit/comment` |
| wiki | `confluence` | Atlassian MCP | `searchConfluence` (CQL with the space keys), `getConfluenceContent`, `createConfluenceContent`, `updateConfluenceContent` |
| wiki | `azure-wiki` | Azure DevOps MCP or `az devops wiki` | `az devops wiki page show/create` |
| ci | `github-actions` | `gh` | `gh run list/view --log-failed`, `gh workflow run` |
| ci | `azure-pipelines` | Azure DevOps MCP or `az pipelines` | `az pipelines runs list/show` |
| test | `azure-test-plans` | Azure DevOps MCP (`testplan` tools) | list plans and suites, create test cases, results of a build |
| crm | `salesforce` | `sf` CLI (alias from the file) | `sf org list`, `sf data query -o <alias> -q "SELECT ... FROM Case WHERE CaseNumber='...'"` |

**Azure DevOps:** Microsoft's official MCP server. Preferred: remote
`https://mcp.dev.azure.com/<organization>` (HTTP, Microsoft account sign-in); local alternative
`npx -y @azure-devops/mcp <organization> -d core work work-items repositories wiki pipelines`.
`setup-integrations.py` registers it in the project `.mcp.json`.
**Salesforce:** use the `sf` CLI. The `@salesforce/mcp` server reaches end of life on
2 Nov 2026, so do not build on it.

## Where information is (search order of `find-information`)
1. Project notes (`products/`, `implementations/`, `bugs/`, `support/cases/`), project `AGENTS.md`.
2. Project knowledge base and the `knowledge` list of `integrations.json` (team repos, kb folders).
3. Code: the repositories in `code.repos` (local clones first, then the host's code search).
4. Wiki spaces in `wiki.spaces`.
5. Tracker: tickets by key, then text search in `tracker.project`.
6. CRM (support questions only): cases by number, then by symptom.
7. Vendor documentation and the web (see `rules/web-scraping.md`).
Answer with the source of each fact; say when sources disagree and which one wins.
