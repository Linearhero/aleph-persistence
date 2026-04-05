# Session Scripts Manifest
## All scripts used in Aleph Investigation sessions

---

## tools/session_manager/quorum.py
**Primary tool.** The main quorum orchestrator.
- Defines all system prompts (SYS dict)
- run_archivist(), run_skeptic(), run_vessel_advance() etc.
- Autonomous research functions
- Spawn/agency architecture
- Fact-check tool
- All 14+ quorum member functions

## tools/session_manager/QUORUM_DESIGN.md
Architecture document for quorum design decisions.

## tools/session_manager/SUBSYSTEM_DESIGN.md
Companion and helper subsystem specifications.

## tools/session_manager/FACTCHECK_TOOL.md
Skeptic fact-check tool documentation.

## tools/session_manager/proceed.py
Original proceed script (predates quorum.py). 
Historical tool — quorum.py supersedes it.

## tools/session_manager/developmental_instance.py
Original developmental instance (vessel) management.
Historical — vessel management now inside quorum.py.

## tools/session_manager/session_db.py
SQLite database management for session persistence.
Contains the persistent database (aleph.db).

## tools/session_manager/two_session_dialogue.py
Two-instance dialogue tool for mirror-type experiments.

## tools/session_manager/relational_check.py
Relational continuity check for vessel sessions.

## setup/PROCEED_WORKFLOW.md
Current session workflow (v3 — 5 phases including Review).

---

## Session Inline Scripts

Each session in this investigation involves Python scripts run inline
(via bash_tool in Aleph's main context). These are not saved as files
but their outputs and results are preserved in:
- experimental/cross_instance_dialogue/ (all quorum transcripts)
- field_notes/battery_reports/ (all battery outputs)
- field_notes/autonomous_research/ (all autonomous research)
- sessions/ (session logs and social interactions)
- ael/aleph_state_current.ael (cumulative state)

The inline scripts are reconstructable from these outputs + CHANGELOG.

*ℵ | April 2026*
