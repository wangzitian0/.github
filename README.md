# .github — org-wide defaults

Default **issue templates** inherited by every repository in this account that
does not define its own `.github/ISSUE_TEMPLATE/`:

| Type | For | Required evidence |
|------|-----|----------|
| **Issue** | a defect | the commands, the verbatim output, the rule that defines the expected result, last good and first bad ref, the check that missed it |
| **Task** | committed work | the outcome, the measured cost of no change, the measured current state, slices, non-goals, checks as commands |
| **Idea** | a proposal | one real occurrence, the present workaround, the fact that decides it |
| **Incident** | an operational failure | impact, timeline with links, the trigger and its proof, rule-outs, follow-ups |

Each field asks for pasted evidence, not for a summary. GitHub renders a field as
`### <label>`. An issue created from the command line uses the same headings and
fills each required field (see `.github/ISSUE_TEMPLATE/config.yml`).

A repo can override any of these by adding its own template of the same name.
