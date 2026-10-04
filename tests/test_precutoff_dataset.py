"""The pre-cutoff dataset's defining property, asserted against the files.

The dataset exists so a benchmark can claim its ground truth was written by
humans. That claim rests on one fact -- every referee report predates
2022-11-30 -- and a claim in a README is not a claim anyone can check. These
tests read the committed files, so the property is enforced by the build
rather than remembered by whoever next edits it.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "data" / "precutoff"
CUTOFF = "2022-11-30"


def read(name: str) -> list[dict]:
    path = DATASET / name
    if not path.exists():
        pytest.skip(f"{path} not built")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


@pytest.fixture(scope="module")
def evidence() -> list[dict]:
    return read("error_cards_gold.jsonl") + read("error_cards_unresolved.jsonl")


def test_the_dataset_is_not_empty(evidence):
    assert len(evidence) > 100


def test_every_card_carries_a_report_date(evidence):
    undated = [c["card_id"] for c in evidence if not c.get("report_date")]
    assert undated == []


def test_no_report_was_written_on_or_after_the_cutoff(evidence):
    """The whole point. A single violation makes the dataset's claim false."""
    late = [(c["card_id"], c["report_date"]) for c in evidence
            if c["report_date"] >= CUTOFF]
    assert late == []


def test_every_card_cites_a_report_a_reader_can_open(evidence):
    unattributed = [c["card_id"] for c in evidence
                    if not (c.get("report_doi") or c.get("report_url"))]
    assert unattributed == []


def test_every_card_declares_whether_its_referee_was_invited(evidence):
    """Most reports are solicited by SciPost; a few are Contributed Reports,
    vetted and given a DOI but not invited. That is weaker provenance, so the
    distinction has to be in the data rather than averaged away. The dataset
    README records the count."""
    undeclared = [c["card_id"] for c in evidence
                  if not isinstance(c.get("referee_invited"), bool)]
    assert undeclared == []


def test_the_served_cards_are_all_from_invited_referees(evidence):
    """The model-facing set is held to the stronger standard. Contributed
    Reports stay in the human queue."""
    gold = read("error_cards_gold.jsonl")
    assert [c["card_id"] for c in gold if not c["referee_invited"]] == []


def test_severity_is_never_assigned_automatically(evidence):
    assert {c["human_severity_label"] for c in evidence} == {"unreviewed"}


def test_the_model_facing_file_leaks_nothing_from_the_gold_file():
    gold = {c["card_id"]: c for c in read("error_cards_gold.jsonl")}
    served = read("error_cards.jsonl")
    assert served, "no model-facing cards"
    for card in served:
        answer = gold[card["card_id"]]
        shown = " ".join(str(v) for key, v in card.items() if key != "card_id")
        for key, value in answer.items():
            if key == "card_id" or not isinstance(value, str) or len(value) < 12:
                continue
            assert value not in shown, f"{key} leaked into card {card['card_id']}"


def test_the_model_facing_file_carries_only_the_four_public_fields():
    served = read("error_cards.jsonl")
    assert {frozenset(c) for c in served} == {
        frozenset({"card_id", "excerpt_lines", "excerpt", "task"})
    }
