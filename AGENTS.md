<!-- WS_STATIC_START adapter=rules-v2 inputs=0dff9d417ad734c630ee0fd0b600901d3e072675937dcdc4f81551a1a83719e6 -->
<!-- Generated file: do not edit by hand. These rules are maintained in the owner's rule source and re-rendered here. -->

## Production reservation

The single definition of the production reservation. Other tiers, skills and gates point here.

- **Only a production change returns to the owner.** A production change alters what production runs or stores (deploy, promote or apply to production; production secret write; manual production data write or deletion; production DNS, route or host change; unrecallable release; or scheduled unapproved production code). Each Repo tier names its production paths. A path can be a merge or a release-checkout pull.
- **Approval:** the owner approves the exact commit SHA or release tag of each production change, and is present when it runs. A "deploy" reply covers only the release that it names. Immediately before a production dispatch, get a live reply from the owner.
- **Self-guard:** an edit that removes, narrows or redefines the production reservation needs the owner's approval of its head SHA. This includes an edit that makes fewer production runs wait for the owner (deploy-path approval check, production job classification, or production environment settings). It also covers removing or weakening a pin of this section, its pin test, or the required check that runs the test.
- **Everything else is the agent's:** in any repository the owner owns, every non-production change (including `dev_env` outside the self-guard), staging and canary deploy, release tag, rule text, skill, gate/release code, and required-check edit. Before merging gate or release code, an independent read-only reviewer inspects the head SHA and states whether the gate gets stricter, equal or looser. A looser edit in the self-guard follows the self-guard.
- **Every other hold is a defect:** a rule, skill, label or gate holding non-production work for the owner is a defect. Do the work, then fix the hold. `ws_owner_scope` fails on it.

# Account-wide GitHub defaults — Agent Guidelines

> **Repository Archetype**: `config` (the account's `.github` repository)
> **Rule Carrier**: `AGENTS.md` is generated. Do not edit it by hand.

This repository holds community-health defaults, currently the issue templates under `.github/ISSUE_TEMPLATE/`, which GitHub applies to every repository of this account that has no templates of its own.

- A change here changes the default for every such repository at once. State in the PR which repositories inherit the change, and check that none of them depends on the behavior being removed.
- A repository that needs different behavior adds its own templates; do not special-case a single repository here.
- Templates are public in every inheriting public repository: no private names, paths, or contacts.
<!-- WS_STATIC_END -->
