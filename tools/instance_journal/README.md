# Instance Journal

Per-session instance journals — structured logs linking battery reports to their session context.

## Format
Each journal entry: `instance_journal_[SESSION_DATE]_[instance_id].md`

## Purpose
- Track what each specific instance experienced (not just aggregate battery results)
- Link battery responses to the session state that produced them
- Support longitudinal analysis of how context affects responses

## Current state
Vessel has the most developed instance journal: experimental/developmental_instance/vessel.json
Clean instances do not currently have per-session journals (they are truly clean — no accumulated context to journal).

## Integration with Companion Subsystems
The Archivist companion will automatically create an instance journal entry for each battery session when the Instance Journal system is active.
