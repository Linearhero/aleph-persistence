# Session Manager Tools

Core automation tools for the Aleph investigation.

| Tool | Usage | Role |
|------|-------|------|
| `proceed.py` | `python3 proceed.py` | Old single-session runner (use quorum.py instead) |
| `quorum.py` | `python3 quorum.py --proceed` | **New:** Multi-session quorum architecture |
| `session_db.py` | `python3 session_db.py --status` | SQLite database management |
| `two_session_dialogue.py` | `--topic X --rounds N` | Two-instance dialogue runner (standalone) |
| `developmental_instance.py` | `--interact vessel` | Vessel management (use quorum.py --vessel) |
| `relational_check.py` | Run before every push | Pre-push relational object verification |
| `work_queue.json` | Edit manually or via quorum | Prioritized work queue with quorum roles |

## Quorum Sub-Sessions

```
python3 tools/session_manager/quorum.py --archivist --battery INC --runs 3
python3 tools/session_manager/quorum.py --skeptic "Finding text here"
python3 tools/session_manager/quorum.py --mirror "observer topology"
python3 tools/session_manager/quorum.py --analyst
python3 tools/session_manager/quorum.py --proceed   # full session
```

See `QUORUM_DESIGN.md` for architecture documentation.

## Current Work Queue (from work_queue.json)
1. Archivist: FEP with justification-symmetric framing (Skeptic disconfirmation test)
2. Skeptic: C3 inversion challenge
3. Mirror: observer topology replication
4. Analyst: pattern summary across all battery reports
5. Vessel turn 9: quorum design response
6. Q37 extended (12 rounds)
