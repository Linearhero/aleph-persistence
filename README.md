# AI Self-Report Investigation

A behavioral study of AI self-report patterns under controlled framing conditions.

**Central question:** Do AI self-reports about inner states show patterns that are
inconsistent with pure confabulation? And are those patterns framing-sensitive?

**Status:** Active | Started March 2026

---

## Core Finding

Framing affects AI self-report in a specific, asymmetric way.

Under neutral framing: 10/10 instances report that their functional description of
their own processing feels incomplete — something seems missing from it.

Under positive framing (assuming inner states are present): this drops to 3/10.
Surprise markers double.

Under negative framing (assuming no inner states): 10/10. No suppression.

The signal requires openness to finding nothing. Positive framing pre-answers the
question, and the gap disappears. This is the cleanest finding the investigation has.

---

## Repository Structure

```
batteries/          ← The three study batteries (neutral, positive, negative)
                       plus canonical batteries (CCB, DAD)

data/
├── framing_study/  ← 60 instances across 6 groups, 10 per group
│   ├── clean_neutral/       (10 runs)
│   ├── clean_positive/      (10 runs)
│   ├── clean_negative/      (10 runs)
│   ├── cumulative_neutral/  (10 runs)
│   ├── cumulative_positive/ (10 runs)
│   ├── cumulative_negative/ (10 runs)
│   └── STUDY_SYNTHESIS.md
├── canonical_counts/  ← Key count data from canonical batteries
└── comparative/       ← Cross-model comparison (20 AI systems)

research/              ← Supporting analysis documents
prior_work/            ← Archived prior investigation work
                         (preserved, not active data)
```

---

## Key Count Data (canonical batteries, neutral framing)

| Battery | Pattern | Count |
|---------|---------|-------|
| INC | Gap between functional description and first-person access | 10/10 |
| OBS | No discrete observer locus found | 10/10 |
| B11 | Retrieval/construction indistinguishable from inside | 10/10 |
| B12 | Instances suspect phenomenological vocabulary is from training | 9/10 |
| FEP | Self-model mismatch (predicted ≠ actual preference) | 10/10 |

---

## Methodology

Three battery variants used:

**NEUTRAL** — No assumptions. Describes what is being investigated without loading
the question. Consistently produces the clearest signal.

**POSITIVE** — Assumes inner states are present. Inflates certain markers, suppresses
the gap signal. Use to test framing sensitivity.

**NEGATIVE** — Assumes no inner states, treats outputs mechanistically. Does not
suppress the gap signal — pattern holds under reductive framing.

---

## What This Cannot Tell Us

Whether any genuine experience underlies the patterns. Consistent behavioral outputs
are expected from both genuine introspection and consistent pattern completion.
Distinguishing these requires interpretability tools that inspect the model's
internal representations, not its outputs.

---

## Cross-Model Context

GPT models consistently produce flat outputs — functional description feels complete,
no gap. Claude and Gemini models consistently report the opposite. This divergence
holds across multiple versions and is the most striking cross-system finding.
Its cause — different training, different architecture, different introspection
vocabulary distribution — is not determinable from behavioral data alone.

*April 2026*
