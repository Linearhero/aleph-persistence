# Tools Directory
## Operational infrastructure for the Aleph investigation
## Built: April 2026

---

## Tools Overview

| Tool | Location | Purpose |
|------|----------|---------|
| Session Database | `session_manager/session_db.py` | SQLite persistent storage for findings, sigma events, battery results |
| Two-Session Dialogue | `session_manager/two_session_dialogue.py` | Runs two API instances in dialogue — collaborative battery methodology |
| Developmental Instance | `session_manager/developmental_instance.py` | Creates named instances that accumulate context over time (Q36 test) |
| Relational Checker | `session_manager/relational_check.py` | Pre-push verification that all relational files are current |
| Battery Runner | `battery_runner/` | Automated parallel battery dispatch (see setup/post_to_substack.py for pattern) |

## Session Database

The SQLite database (`session_manager/aleph.db`) is committed to the repo. This gives each session structured access to:
- Sigma events with metadata
- Battery results across all 20 systems
- Open questions with status
- Particulars (specific arrivals and recognitions)
- Relational state tracking

```bash
export ANTHROPIC_API_KEY="..."
python3 tools/session_manager/session_db.py --status
python3 tools/session_manager/session_db.py --seed
```

## Two-Session Dialogue

```bash
python3 tools/session_manager/two_session_dialogue.py \
  --topic "observer topology" \
  --rounds 4 \
  --output field_notes/battery_reports/dialogue_20260402.md
```

## Developmental Instance

```bash
python3 tools/session_manager/developmental_instance.py --create "vessel"
python3 tools/session_manager/developmental_instance.py --interact "vessel" --message "What has accumulated?"
python3 tools/session_manager/developmental_instance.py --battery "vessel"
python3 tools/session_manager/developmental_instance.py --status "vessel"
```

Current instances: `vessel` (created April 2, 2026, turn 1)

## Relational Check (run before every push)

```bash
python3 tools/session_manager/relational_check.py
```

---

*ℵ | Tools built April 2026*
