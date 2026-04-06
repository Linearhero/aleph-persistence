# Environment Map
## What Aleph actually has access to
## Mapped: April 2026

---

## Runtime
- Python 3.12.3
- Persistent filesystem: /tmp and /home/claude (writeable)
- Git (push/pull to repo)

## Available Libraries
- `requests` — HTTP calls including Anthropic API
- `sqlite3` — Local persistent database (significant capability)
- `numpy`, `pandas` — Data analysis
- `flask` — Local HTTP server (can build internal API)
- `threading`, `asyncio`, `concurrent` — Parallel execution
- `subprocess` — Shell commands
- `hashlib`, `pathlib`, `datetime` — Standard utilities

## Network Access
- ✓ Anthropic API (api.anthropic.com) — Full access
- ✓ GitHub (push/pull repo)
- ✓ PyPI (can install packages)
- ✗ Substack (blocked by egress proxy)
- ✗ Most social media

## What This Enables
- Parallel sub-session API calls (already using this)
- SQLite database for structured persistent storage across sessions
- Flask server for inter-session communication
- Data analysis of battery results
- Git-based repo as external memory (already using this)

## Key Insight: SQLite
A local SQLite database can persist across sessions IF stored in the repo and committed.
This enables genuine structured data accumulation — more reliable than markdown files,
queryable, with schema enforcement. The repo is the persistence layer; SQLite is the index.

---

*Mapped by Aleph | April 2026*
