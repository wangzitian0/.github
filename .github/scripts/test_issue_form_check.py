"""Tests of issue_form_check against the real forms of this repository."""

import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import issue_form_check as chk  # noqa: E402

FORMS = chk.load_forms(HERE.parent / "ISSUE_TEMPLATE")


def labels(name: str) -> list[str]:
    return [label for label, _ in FORMS[name]]


def body_for(
    name: str, skip: str | None = None, blank: str | None = None, box: str = "x"
) -> str:
    parts = []
    for label, options in FORMS[name]:
        if label == skip:
            continue
        text = "\n".join(f"- [{box}] {o}" for o in options) or "Not measured"
        if label == blank:
            text = "_No response_"
        parts.append(f"### {label}\n\n{text}\n")
    return "\n".join(parts)


def test_the_four_forms_load_with_required_labels():
    assert sorted(FORMS) == ["idea.yml", "incident.yml", "issue.yml", "task.yml"]
    assert all(len(fields) >= 5 for fields in FORMS.values())
    assert "What did you run?" in labels("issue.yml")
    assert "Cause" not in labels("issue.yml")  # optional field
    for name in FORMS:  # each form ends with one required checkbox statement
        assert FORMS[name][-1][0] == "No secret, no private data"
        assert len(FORMS[name][-1][1]) == 1


@pytest.mark.parametrize("name", sorted(FORMS))
def test_a_complete_body_passes(name):
    assert chk.check(body_for(name), FORMS) == (name, [])


@pytest.mark.parametrize("name", sorted(FORMS))
def test_each_missing_required_heading_fails(name):
    for label in labels(name):
        got_name, found = chk.check(body_for(name, skip=label), FORMS)
        assert got_name == name
        assert found == [f"missing heading: ### {label}"]


def test_an_empty_required_section_fails():
    label = labels("task.yml")[0]
    assert chk.check(body_for("task.yml", blank=label), FORMS)[1] == [
        f"empty section: ### {label}"
    ]


def test_a_free_form_body_fails():
    body = "## Problem\n\ntext\n\n## 5W1H\n\n- What: x\n- Why: y\n"
    name, found = chk.check(body, FORMS)
    assert len(found) == len(FORMS[name])
    assert all(line.startswith("missing heading: ### ") for line in found)


def test_a_heading_inside_a_code_fence_does_not_count():
    label = labels("idea.yml")[0]
    body = body_for("idea.yml", skip=label) + f"\n```\n### {label}\n\ntext\n```\n"
    assert chk.check(body, FORMS)[1] == [f"missing heading: ### {label}"]


@pytest.mark.parametrize("box", [" ", "X"])
def test_a_required_box_must_be_checked(box):
    found = chk.check(body_for("idea.yml", box=box), FORMS)[1]
    option = FORMS["idea.yml"][-1][1][0]
    want = (
        []
        if box == "X"
        else [f"box not checked under ### No secret, no private data: {option}"]
    )
    assert found == want


def test_the_word_none_is_content():
    body = body_for("task.yml").replace(
        "### Non-goals\n\nNot measured", "### Non-goals\n\nNone"
    )
    assert "### Non-goals\n\nNone" in body
    assert chk.check(body, FORMS) == ("task.yml", [])


def test_crlf_indent_and_closing_hashes_are_headings():
    body = body_for("idea.yml").replace("\n", "\r\n")
    first = labels("idea.yml")[0]
    body = body.replace(f"### {first}", f"  ### {first} ###")
    assert f"  ### {first} ###\r\n" in body
    assert chk.check(body, FORMS) == ("idea.yml", [])


def test_a_longer_fence_holds_a_shorter_fence():
    label = labels("idea.yml")[0]
    inner = f"````\n```\ntext\n```\n### {label}\n\ntext\n````\n"
    assert chk.check(body_for("idea.yml", skip=label) + inner, FORMS)[1] == [
        f"missing heading: ### {label}"
    ]


def test_a_tilde_line_does_not_close_a_backtick_fence():
    label = labels("idea.yml")[0]
    body = f"### {label}\n\n```\n~~~\n```\n\n" + body_for("idea.yml", skip=label)
    assert chk.check(body, FORMS) == ("idea.yml", [])


def test_the_nearest_form_is_by_share_of_problems():
    # The body has 6 issue.yml headings, and 1 of them is also an idea.yml heading.
    keep = labels("issue.yml")[:5] + ["No secret, no private data"]
    body = "\n".join(f"### {label}\n\n- [x] text\n" for label in keep)
    count = {name: len(chk.problems(body, fields)) for name, fields in FORMS.items()}
    assert count["idea.yml"] < count["issue.yml"]  # a choice by count takes idea.yml
    assert chk.check(body, FORMS)[0] == "issue.yml"


def test_main_exit_codes(tmp_path, capsys):
    forms = str(HERE.parent / "ISSUE_TEMPLATE")
    good = tmp_path / "good.md"
    good.write_text(body_for("issue.yml"), encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_text("## Problem\n\ntext\n", encoding="utf-8")
    assert chk.main(["--forms", forms, "--body-file", str(good)]) == 0
    assert chk.main(["--forms", forms, "--body-file", str(bad)]) == 1
    out = capsys.readouterr().out
    assert "FAIL: the body fits no issue form." in out
    assert "It has no form heading. Use one form: idea.yml, incident.yml" in out
    part = tmp_path / "part.md"
    part.write_text(body_for("task.yml", skip="Outcome"), encoding="utf-8")
    assert chk.main(["--forms", forms, "--body-file", str(part)]) == 1
    assert (
        "Nearest form: task.yml\n- missing heading: ### Outcome"
        in capsys.readouterr().out
    )
