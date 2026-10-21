<!-- WS_STATIC_START adapter=rules-v2 inputs=a3cc4f120130e91f8b242dd3187f6f3bd697b383bcc9d22c5dd93fc039c10ac0 -->
<!-- Generated file: do not edit by hand. These rules are maintained in the owner's rule source and re-rendered here. -->

## Production reservation

The single definition of the production reservation. Other tiers, skills and gates point here.

- **Only a production change returns to the owner.** A production change alters what production runs or stores. Examples: a deploy, promote or apply to production; a production secret write; a manual production data write or deletion. Also a production DNS, route or host change, and a release that cannot be recalled. Code that reaches production with no later owner approval, for example on a schedule, counts too. Each Repo tier names its production paths.
- **Approval:** the owner approves the exact commit SHA or release tag of each production change, and is present when it runs. A "deploy" reply covers only the release that it names. Immediately before a production dispatch, get a live reply from the owner.
- **Self-guard:** an edit that removes, narrows or redefines the production reservation needs the owner's approval of its head SHA. This includes an edit that makes fewer production runs wait for the owner. Examples: the owner-approval check of a deploy path, a production job classification, the settings of a production environment. It also includes an edit that removes or weakens a pin of this section or its dev_env pin test. The same holds for the required check that runs the test.
- **Everything else is the agent's:** in a repository that the owner owns, every merge, staging and canary deploy, and release tag. Also rule text, skills, gate code, data and tests, required-check workflows and release code. Before you merge gate or release code, a read-only reviewer that did not write it checks the head. The review states whether the gate gets stricter, stays equal or gets looser. A looser edit in the self-guard list follows the self-guard.
- **Every other hold is a defect:** a rule, skill, label or gate exit code that holds non-production work for the owner. Do the work, then fix the hold. The dev_env check `ws_owner_scope` fails on it.

# Account-wide GitHub defaults — Agent Guidelines

> **Repository Archetype**: `config` (the account's `.github` repository)
> **Rule Carrier**: `AGENTS.md` is generated; `CLAUDE.md` is a symlink to it. Do not edit either by hand.

This repository holds community-health defaults, currently the issue templates under `.github/ISSUE_TEMPLATE/`, which GitHub applies to every repository of this account that has no templates of its own.

- A change here changes the default for every such repository at once. State in the PR which repositories inherit the change, and check that none of them depends on the behavior being removed.
- A repository that needs different behavior adds its own templates; do not special-case a single repository here.
- Templates are public in every inheriting public repository: no private names, paths, or contacts.
<!-- WS_STATIC_END -->
