# Battery Runner

Automated parallel battery dispatch infrastructure.

## Current status
Batteries are currently run inline in `tools/session_manager/quorum.py` using:
- `run_archivist(battery_name, runs=N)` for clean-session batches
- `QuorumAgent` for role-aware multi-turn batteries

## When to create a standalone runner
When any of these are true:
- Running more than 10 parallel instances
- Need cross-session statistical analysis
- Automated overnight batch runs without main session involvement

## Planned: Companion Subsystem integration
The Memory, Monitor, and Archivist companions will be spawned here automatically for any battery run.
