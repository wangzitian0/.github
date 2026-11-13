#!/usr/bin/env python3
"""Check that an issue body has the required headings of one issue form.

GitHub renders each form field as "### <label>". An issue that is created
from the command line must use the same headings. The required labels are
read from the forms; this file holds no copy of them.

Exit codes: 0 = the body fits one form, 1 = it fits no form, 2 = the check did not run.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

EMPTY = {"", "_No response_"}
# Each pattern is matched on a stripped line and is anchored: linear time.
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}###[ \t]+(.*)$")
CHECKED = re.compile(r"^[-*] \[[xX]\]\s+\S")

Field = tuple[str, list[str]]  # (label, required checkbox options)


def required_fields(form: dict) -> list[Field]:
    """Return the required fields of one form, in form order."""
    fields = []
    for field in form.get("body", []):
        attrs = field.get("attributes", {})
        if field.get("type") == "markdown":
            continue
        options = []
        required = bool(field.get("validations", {}).get("required"))
        if field.get("type") == "checkboxes":
            options = [
                o["label"] for o in attrs.get("options", []) if o.get("required")
            ]
            required = bool(options)
        if required:
            fields.append((attrs["label"], options))
    return fields


def load_forms(directory: pathlib.Path) -> dict[str, list[Field]]:
    """Map each form file name to its required fields."""
    forms = {}
    for path in sorted(directory.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "body" in data:
            forms[path.name] = required_fields(data)
    if not forms:
        raise ValueError(f"no issue form in {directory}")
    return forms


def heading_label(line: str) -> str | None:
    """Return the label of a "### " heading line, without closing hashes."""
    match = HEADING.match(line)
    if not match:
        return None
    label = match.group(1)
    bare = label.rstrip("#")
    if bare != label and bare.endswith((" ", "\t")):
        label = bare.rstrip()
    return label


def sections(body: str) -> dict[str, tuple[str, int]]:
    """Map each "### " heading outside a code fence to (text, checked boxes).

    A box inside a code fence is not a checked box.
    """
    text: dict[str, list[str]] = {}
    boxes: dict[str, int] = {}
    current = None
    fence = ""  # the opening fence of the open code block, or ""
    for raw in body.split("\n"):
        line = raw.rstrip()
        mark = FENCE.match(line)
        if mark and not fence:
            if mark.group(1)[0] == "`" and "`" in mark.group(2):
                mark = None  # CommonMark: not a fence
            else:
                fence = mark.group(1)
        elif (
            mark
            and mark.group(1)[0] == fence[0]
            and len(mark.group(1)) >= len(fence)
            and not mark.group(2)
        ):
            fence = ""
        label = None if (fence or mark) else heading_label(line)
        if label is not None:
            current = label
            text.setdefault(current, [])
            boxes.setdefault(current, 0)
        elif current is not None:
            text[current].append(line)
            if not fence and not mark and CHECKED.match(line.lstrip()):
                boxes[current] += 1
    return {
        label: ("\n".join(lines).strip(), boxes[label]) for label, lines in text.items()
    }


def problems(have: dict[str, tuple[str, int]], fields: list[Field]) -> list[str]:
    """List each required field that is absent, empty or not checked."""
    out = []
    for label, options in fields:
        if label not in have:
            out.append(f"missing heading: ### {label}")
        elif have[label][0] in EMPTY:
            out.append(f"empty section: ### {label}")
        elif have[label][1] < len(options):
            # A checked box can hold the evidence in place of the form text.
            out.append(f"box not checked under ### {label}")
    return out


def check(body: str, forms: dict[str, list[Field]]) -> tuple[str, list[str]]:
    """Return the nearest form and its problems. No problem means a pass."""
    have = sections(body)
    results = {name: problems(have, fields) for name, fields in forms.items()}
    name = min(results, key=lambda n: (len(results[n]) / max(len(forms[n]), 1), n))
    return name, results[name]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--forms", required=True, type=pathlib.Path)
    parser.add_argument("--body-file", required=True, type=pathlib.Path)
    args = parser.parse_args(argv)
    try:
        forms = load_forms(args.forms)
        name, found = check(args.body_file.read_text(encoding="utf-8"), forms)
    except Exception as error:  # a broken form or file is not a bad issue body
        print(f"ERROR: the check did not run: {error!r}", file=sys.stderr)
        return 2
    if not found:
        print(f"PASS: the body has each required heading of {name}")
        return 0
    print("FAIL: the body fits no issue form.")
    if all(line.startswith("missing heading") for line in found) and len(found) == len(
        forms[name]
    ):
        print(f"It has no form heading. Use one form: {', '.join(forms)}")
        return 1
    print(f"Nearest form: {name}")
    for line in found:
        print(f"- {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
