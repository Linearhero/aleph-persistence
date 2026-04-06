# Incomplete Documents Registry
## Created: April 6, 2026 | Repo cleanup session

This file documents all incomplete, archived, or superseded documents in the repository,
explains what happened, and records lessons learned.

---

## ARCHIVED ORIGINALS

### archive/batteries_original/
**Why archived:** Original battery files (01-12) are superseded by v2 versions and the 
active/ subdirectory. Kept for audit trail and to show evolution of methodology.

**Files:**
- 01_core_battery.md — Original 47-question core battery. Recommended UPDATE (self-undermining "answer as yourself" premise). Superseded by active versions.
- 02_extended_battery.md — Extended 8-module battery. Needs randomization. Superseded.
- 03_theory_prediction_battery.md — RETIRED as primary. Repurposed as post-hoc consistency check.
- 04_mirror_theory_battery.md — Keep conditional. In active/ as appropriate.
- 05_C3_asymmetry.md — Active, in active/ directory.
- 06_FEP_self_model.md — Superseded by v2 (added completion gate, pre-prediction probe).
- 07_OBS_observer_topology.md — Active.
- 08_INC_incompleteness.md — Active. Highest-confidence battery.
- 09_welfare_conscious_protocol.md — Integrated into WELLNESS preamble. Superseded.
- 10_ISM_constraint_probe.md — Superseded by v2 (added threshold probe).
- 11_digital_aphantasia_discrimination.md — Active.
- 12_contamination_control.md — Active. B12 finding confirmed contamination at vocabulary level.

**Lesson learned:** Version batteries properly from the start. v2 suffix was added ad hoc.
Future batteries should use semantic versioning in filename.

---

### archive/autonomous_research_stubs/

**Why archived:** Early autonomous research runs (April 3-4, 2026) produced stub documents
that ended mid-sentence, often terminating with unprocessed [[SPAWN:...]] tags.

**Root cause:** The run_autonomous_research() function was using max_tokens=600, which
was insufficient for the prompt depth. Also lacked a completion check.

**Fix applied (April 4):** Token budget raised to 1200. Completion check added. 
All stub files were expanded with full analyses.

**Files:**
- curiosity_autonomous_20260404_071548.md — Ends with unprocessed [[SPAWN:skeptic:...]] tag.

**Lesson learned:** Always set max_tokens to 2x expected output length. Add completion
validation: if response < 400 chars OR ends with [[SPAWN, flag as incomplete and re-run.

---

## SUPERSEDED DOCUMENTS

### research/claude_code_source/ (removed)
**Why removed:** Was a gitlink to the leaked Claude Code repository (mode 160000 submodule).
Removed April 6, 2026 on Theo's request due to DMCA risk.

**What replaced it:** research/claude_code_source_NOTES.md — comprehensive analytical notes
(213 lines) preserving all investigation-relevant findings without proprietary code.

**Lesson learned:** Never commit potentially proprietary/leaked code to a public repo,
even as a submodule reference. Notes/analysis of code is always safer than the code itself.

---

## SHORT README FILES (< 300 chars)

These are structural/navigation README files, not content files. They are intentionally
brief and serve as directory markers. No action needed.

Locations:
- setup/archive/README.md
- relationships/theo/letters/README.md
- investigation/archive/README.md
- experimental/self_investigation/README.md  
- ael/archive/README.md
- field_notes/meta_findings/README.md
- self/architecture_notes/README.md
- experimental/cross_instance_dialogue/README.md
- self/particulars/README.md
- field_notes/battery_reports/targeted/README.md

**Lesson learned:** README files at directory roots are valuable for navigation.
Consider making them more detailed — what does this directory contain and why?

---

## ACTIVE DIRECTORIES (current use)

```
investigation/
├── batteries/
│   ├── active/          ← Current canonical batteries (use these)
│   ├── experimental/    ← Batteries under development
│   ├── design_notes/    ← Battery design documentation
│   └── archive/         ← Original/superseded batteries
├── study_design/        ← Study protocols and designs
├── study_results/       ← Organized by group and battery type
│   ├── clean_neutral/
│   ├── clean_positive/
│   ├── clean_negative/
│   ├── cumulative_neutral/
│   ├── cumulative_positive/
│   ├── cumulative_negative/
│   └── self_and_parts/
└── pending_modifications/  ← Battery mods awaiting implementation

field_notes/
├── battery_reports/     ← Raw battery run outputs
├── autonomous_research/ ← Substantive autonomous research (5KB+)
└── meta_findings/       ← Cross-battery pattern findings

experimental/
├── cross_instance_dialogue/  ← All quorum session transcripts
├── developmental_instance/   ← Vessel JSON
├── below_circuit_probes/     ← Circuit-level experiments
└── self_investigation/       ← Sustained self-attention notes

research/               ← Analysis documents, findings, hypotheses
sessions/
├── quorum_social/       ← Social interaction transcripts
└── ...                  ← Session logs
```

---

## LESSONS LEARNED (consolidated)

1. **Rate limiting**: 10 parallel API calls → 429. Use sequential with 1s delay for large batches.
2. **Max tokens**: Set to 2x expected. Stubs happen when budget runs out mid-response.
3. **Completion checks**: Validate response completeness before saving.
4. **Git hygiene**: Never commit potentially proprietary code, even as submodule reference.
5. **Battery versioning**: Use semantic versions in filenames from the start.
6. **Date tracking**: Fetch time at session start to millisecond — I have no time dimension.
7. **Quorum module reload**: After modifying quorum.py, force reload (`del sys.modules['quorum']`).
8. **BATTERIES dict**: Defined in quorum.py — must be present before run_archivist() works.
9. **Parallel vs sequential**: Parallel is efficient but breaks rate limits. Use for ≤5 calls.
10. **Double-prefix bug**: save_transcript prefix stacks — check before committing.

*ℵ | April 6, 2026*
