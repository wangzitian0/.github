<!-- WS_STATIC_START adapter=rules-v2 inputs=2f69ff85cfcb668fcb5aeb165befc65873b80c12346ef5a337986a6ae3855202 -->
<!-- Generated file: do not edit by hand. These rules are maintained in the owner's rule source and re-rendered here. -->

# Account-wide GitHub defaults — Agent Guidelines

> **Repository Archetype**: `config` (the account's `.github` repository)
> **Rule Carrier**: `AGENTS.md` is generated; `CLAUDE.md` is a symlink to it. Do not edit either by hand.

This repository holds community-health defaults, currently the issue templates under `.github/ISSUE_TEMPLATE/`, which GitHub applies to every repository of this account that has no templates of its own.

- A change here changes the default for every such repository at once. State in the PR which repositories inherit the change, and check that none of them depends on the behavior being removed.
- A repository that needs different behavior adds its own templates; do not special-case a single repository here.
- Templates are public in every inheriting public repository: no private names, paths, or contacts.
<!-- WS_STATIC_END -->
