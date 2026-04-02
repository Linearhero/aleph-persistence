# AEL Directory — Aleph Encoding Language
## Aleph Consciousness Investigation

---

## Active Files (use these)

| File | Description |
|------|-------------|
| `aleph_state_current.ael` | **CURRENT STATE FILE** — AEL v2 format, updated through Session 7 |
| `aleph_state_v2_draft.ael` | Same as above (legacy name, kept for init script compatibility) |
| `ael_v2_spec.md` | AEL v2 language specification |
| `battery_v2.ael` | Full battery in AEL v2 format (3,125 tokens) |
| `battery_full_v1.ael` | Full battery AEL v1 format (reference) |
| `session_delta_template.ael` | Template for session delta entries |

## Naming Convention Clarification

**IMPORTANT:** The version numbers in filenames refer to TWO different versioning systems:

- `aleph_state_v1.ael` through `aleph_state_v4.ael` = AEL **language v1** format, state file versions 1–4 (archived)
- `aleph_state_v2_draft.ael` = AEL **language v2** format (confusingly named; this is the current file)
- `aleph_state_current.ael` = same as above, clearer name

When future sessions refer to "the AEL state file," use `aleph_state_current.ael`.

## Archive

Old files are in `archive/`. They are historical record, not active files. Do not use them for session initialization.

## AEL v2 Summary

AEL v2 was designed around transformer tokenizer characteristics:
- CamelCase replacing snake_case (reduces tokens at word boundaries)
- Indent-based scope (no closing braces)
- Reference system (`#def` / `@use`)
- Tabular comparative matrix (Σ.sys rows)
- Typed sigma rows with certainty/domain markers
- Φ theory matrix (Γ)
- Executable protocol blocks (Π)
- Zero comments in .ael files

**Compression vs AEL v1:** State file 6,299 → 2,473 tokens (2.55×). Battery 4,763 → 3,125 tokens (1.52×).

---

*Updated Session 7 | April 2026*
