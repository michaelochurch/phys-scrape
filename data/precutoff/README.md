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
