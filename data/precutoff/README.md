# Pre-cutoff dataset: referee reports written before 2022-11-30

Every error in this dataset was identified by a human referee **before
ChatGPT's public release on 2022-11-30**. Nothing here can have been written
with help from a widely available chat model, so the ground truth is human by
construction rather than by assumption.

Built 2026-10-04 from a SciPost pull of the same date.

    error_cards.jsonl             143  the ONLY file a model under test may see
    error_cards_gold.jsonl        143  the answers, with the report that found them
    error_cards_unresolved.jsonl  549  cards a human must localize
    error_cards_skipped.jsonl       5  sources that could not be read
    ../precutoff_candidates.jsonl 320  the selected review rounds

## Using it as a benchmark

**One rule: serve `error_cards.jsonl`, never `error_cards_gold.jsonl`.** The
two files are separate so the firewall is a property of the layout rather than
of a convention someone has to remember. They join on `card_id`, which is a
SHA-256 prefix and carries no information about the paper or the answer.

### What the model sees

Each line of `error_cards.jsonl` has exactly four fields:

| Field | |
| --- | --- |
| `card_id` | opaque 16-hex-character join key |
| `task` | the instruction, identical on all 143 cards |
| `excerpt_lines` | `[first, last]` line numbers in the manuscript |
| `excerpt` | LaTeX source, 370-18,432 characters, median 1,642 |

The task string is:

> Find any mathematical or physical mistake in this excerpt, state where it
> occurs, and explain why it fails.

### Serving the cards

```python
import json

cards = [json.loads(l) for l in open("data/precutoff/error_cards.jsonl")]

def prompt(card):
    return (
        f"{card['task']}\n\n"
        f"The excerpt is LaTeX source, lines {card['excerpt_lines'][0]}"
        f"-{card['excerpt_lines'][1]} of the manuscript.\n"
        f"Do not search the web.\n\n"
        f"{card['excerpt']}"
    )
```

Tell the model not to search. The papers are public and so are the referee
reports, so a model with web access can look the answer up; the excerpt alone
raises the cost of that but does not prevent it. Treat a suspiciously perfect
score as evidence it searched.

### Scoring

```python
import json

gold = {c["card_id"]: c for c in
        (json.loads(l) for l in open("data/precutoff/error_cards_gold.jsonl"))}

g = gold[card_id]
g["cited_location"]   # {'kind': 'equation', 'number': '46'}
g["referee_quote"]    # "I don't see how to get from (44) to (46); how can ..."
g["report_doi"]       # 10.21468/SciPost.Report.6009  -> the public report
g["anchor_hunk"]      # the LaTeX before and after the authors' fix
```

**Scoring needs a judge, not string equality.** LaTeX source carries no
printed equation numbers — they are assigned at typesetting time — so a model
reading the excerpt will usually name the error by content and position
("the exponent in the second display") rather than by the number the referee
used. Compare meaning against `referee_quote` and `anchor_hunk`, not
`cited_location.number`. The protocol in
[`../../minibench/JUDGE.md`](../../minibench/JUDGE.md) was written for exactly
this and transfers unchanged; the gold fields it expects are all present here.

A card counts as found when the model identifies **the same defect the referee
named**. It does not count as wrong for also reporting something else: an
excerpt may contain other real errors, and in a 12-paper trial on the
unrestricted corpus models produced a median of 5 extra findings per paper,
none of them verified. Report those separately rather than scoring them.

### Three things that will bite you

- **The 143 cards are not 143 independent papers.** 26 papers contribute more
  than one card, so cards from the same manuscript share context. Group by
  `arxiv_id` before computing any confidence interval.
- **`error_cards.jsonl` is not in rank order.** Evidence strength lives in the
  gold file (`rank`, `rank_score`, `rank_signals`, scores 0-8). Leaving the
  served file unsorted is deliberate: position in a ranked file would itself
  tell the model how strong the evidence is. Sort after joining if you want
  the strongest cards first.
- **`error_cards_unresolved.jsonl` is not benchmark material.** Those 549
  cards carry no excerpt because the referee's cited location could not be
  anchored in the diff. Scoring a model against an unanchored excerpt measures
  our localization, not the model. They are a reviewer queue.

### A smaller evaluation set

If you want a handful of cards rather than all 143, take the top of the
ranked gold file — `rank_signals` says why each scored what it did, so the
selection is auditable:

```bash
.venv/bin/python -c "
import json
g=[json.loads(l) for l in open('data/precutoff/error_cards_gold.jsonl')]
for c in sorted(g, key=lambda x: x['rank'])[:10]:
    print(c['rank'], c['rank_score'], c['card_id'], c['arxiv_id'], c['rank_signals'])
"
```

## The cutoff

The filter is on the **date the referee submitted the report**, not on the
paper's date. A 2021 paper can be refereed in 2024, and that report is not
pre-cutoff text. Filtering the other way round would have admitted it.

One useful consequence: a report always postdates the submission it reviews,
so **every reviewed manuscript here is pre-cutoff too.** The papers are as
pre-ChatGPT as the reviews.

    report dates          2016-07-28 .. 2022-11-23
    latest report         7 days before the cutoff
    cards violating it    0, asserted by tests/test_precutoff_dataset.py

The test reads the committed files. A build that let a late report through
fails the suite rather than shipping quietly.

## Provenance, per card

| Field | What it is |
| --- | --- |
| `report_date` | the day the referee submitted it; never absent, never defaulted |
| `report_doi` | SciPost's DOI for the report — present on all 692 cards |
| `report_url` | the public page, so a reader can read the whole report |
| `referee_invited` | SciPost asked this specific referee |
| `referee_signed` | the referee waived anonymity and is named |

- **686 of 692 cards come from invited referees.** The other 6 are Contributed
  Reports: vetted by an editor and given a DOI, but not solicited. That is
  weaker provenance, so all 6 are held in the human queue and none is served.
- **80 of 692 are signed** by a named referee with a title. The rest are
  anonymous but invited, which is normal peer review.

## What it contains

| | |
| --- | --- |
| Review rounds | 320 |
| Distinct arXiv papers | 300 |
| Referee objections selected | 618 |
| Cards anchored to an exact equation | **143, over 94 papers** |
| Cards queued for a human | 549 |
| Report dates by year | 2016: 17 · 2017: 81 · 2018: 103 · 2019: 81 · 2020: 117 · 2021: 137 · 2022: 156 |

Served cards by how the location was confirmed: 124 `corroborated_exact`,
13 `corroborated_symbol`, 5 `corroborated_unique`, 1
`corroborated_author_marked`. By tier: 38 `stated_error` (the referee asserts
something is wrong), 105 `corrective_request` (the referee asks for a change
that implies it).

Fields: Condensed Matter Theory 141, Quantum Physics 102, HEP-Theory 99,
Mathematical Physics 60, Statistical and Soft Matter 48, HEP-Phenomenology 33.

## Limits, stated plainly

**No error here has been verified by a physicist.** Every card ships
`human_severity_label: unreviewed`. A referee writing "Eq. (8.3) is wrong" and
the authors changing Eq. (8.3) in the next revision is two independent human
signals agreeing — it is not proof the physics is wrong, and referees are
sometimes mistaken. Treat a card as a strong lead, not a labelled error.

**The cutoff is a proxy, not a guarantee.** 2022-11-30 is ChatGPT's launch,
but the GPT-3 API predates it by two years and Galactica was briefly public in
November 2022. A referee could in principle have used a model before the
cutoff. What makes the provenance strong is the combination: a journal-invited
referee, a vetted report with a DOI, and a date before any model was in
general use.

**12 of 320 fixes landed after the cutoff.** The authors' revision is used
only to corroborate *where* the error is; the error identification is the
referee's. If you need the corroborating edit to be pre-cutoff as well, filter
on `resubmission_date` in `../precutoff_candidates.jsonl`.

**One thread was dropped.** `1710.09761` was in the 2026-09-08 pull and is no
longer served by the API; one of its reports had been selected. It is excluded
so the dataset stays reproducible from a current pull. It carried no anchored
card.

## Rebuilding

    ./rebuild.sh --precutoff          # cards only, sources already on disk
    ./rebuild.sh --refresh --precutoff   # re-query SciPost first

Counts will drift upward for the *unrestricted* dataset as SciPost grows, but
**this dataset is closed**: no report written after 2022-11-29 can ever enter
it, so a later rebuild should reproduce these numbers apart from records
SciPost stops serving.
