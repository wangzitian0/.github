"""Tests of issue_form_check against the real forms of this repository."""
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import issue_form_check as chk  # noqa: E402

FORMS = chk.load_forms(HERE.parent / "ISSUE_TEMPLATE")


def body_for(name: str, skip: str | None = None, blank: str | None = None) -> str:
    parts = []
    for label in FORMS[name]:
        if label == skip:
            continue
        text = "_No response_" if label == blank else "Not measured"
        parts.append(f"### {label}\n\n{text}\n")
    return "\n".join(parts)


def test_the_four_forms_load_with_required_labels():
    assert sorted(FORMS) == ["idea.yml", "incident.yml", "issue.yml", "task.yml"]
    assert all(len(labels) >= 5 for labels in FORMS.values())
    assert "What did you run?" in FORMS["issue.yml"]
    assert "Cause" not in FORMS["issue.yml"]  # optional field


@pytest.mark.parametrize("name", sorted(FORMS))
def test_a_complete_body_passes(name):
    assert chk.check(body_for(name), FORMS) == (name, [])


@pytest.mark.parametrize("name", sorted(FORMS))
def test_each_missing_required_heading_fails(name):
    for label in FORMS[name]:
        got_name, found = chk.check(body_for(name, skip=label), FORMS)
        assert got_name == name
        assert found == [f"missing heading: ### {label}"]


def test_an_empty_required_section_fails():
    label = FORMS["task.yml"][0]
    assert chk.check(body_for("task.yml", blank=label), FORMS)[1] == [
        f"empty section: ### {label}"
    ]


def test_a_free_form_body_fails():
    body = "## Problem\n\ntext\n\n## 5W1H\n\n- What: x\n- Why: y\n"
    name, found = chk.check(body, FORMS)
    assert len(found) == len(FORMS[name])
    assert all(line.startswith("missing heading: ### ") for line in found)


def test_a_heading_inside_a_code_fence_does_not_count():
    label = FORMS["idea.yml"][0]
    body = body_for("idea.yml", skip=label) + f"\n```\n### {label}\n\ntext\n```\n"
    assert chk.check(body, FORMS)[1] == [f"missing heading: ### {label}"]


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
    assert "Nearest form: task.yml\n- missing heading: ### Outcome" in capsys.readouterr().out
