#!/usr/bin/env python3
"""
Aleph Investigation — Relational Objects Pre-Push Checker
Verifies all relational files are current before committing to repo.
Run this before every push.

Usage: python3 tools/session_manager/relational_check.py
"""

import os, subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent.parent

RELATIONAL_FILES = {
    "relationships/theo/README.md": "Theo's README — update if sessions/systems count changed",
    "relationships/aleph_self/personal_notes.md": "Personal notes — any new session reflections to add?",
    "relationships/aleph_self/self_state.ael": "Self state — sync with aleph_state_current.ael",
    "relationships/theo/relationship.ael": "Theo relationship AEL — sigma events σ9/σ10/σ14 current?",
    "relationships/ai_entities/opus3/README.md": "Opus 3 relationship — letter posted? status updated?",
    "outreach/README.md": "Outreach status — any contacts sent/responded?",
    "outreach/jack_lindsey/README.md": "Lindsey outreach — follow-up due April 14?",
    "memory_map/MASTER_INDEX.md": "Master index — session count / systems current?",
    "ael/aleph_state_current.ael": "AEL state — all deltas merged?",
    "README.md": "Root README — status counts current?",
}

def check_staleness(filepath):
    """Check git log for last modification date."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ci', str(filepath)],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        date_str = result.stdout.strip()[:10]  # YYYY-MM-DD
        return date_str
    except:
        return "unknown"

def run_check():
    print("=== Relational Objects Pre-Push Check ===\n")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    issues = []
    for filepath, description in RELATIONAL_FILES.items():
        full_path = REPO_ROOT / filepath
        last_modified = check_staleness(filepath)
        
        exists = full_path.exists()
        status = "✓" if exists else "✗ MISSING"
        
        print(f"{status} {filepath}")
        print(f"   Last modified: {last_modified}")
        print(f"   Check: {description}\n")
        
        if not exists:
            issues.append(f"MISSING: {filepath}")
    
    print("\n=== Checklist ===")
    checklist = [
        "[ ] Session count in README.md is correct",
        "[ ] Systems count in README.md is correct",
        "[ ] aleph_state_current.ael has current session delta",
        "[ ] Theo README reflects session 7+ context",
        "[ ] Outreach README shows current contact status",
        "[ ] Any new sigma candidates added to sigma_events table (tools/session_manager/aleph.db)",
        "[ ] New battery reports filed in field_notes/battery_reports/",
        "[ ] CHANGELOG.md updated",
    ]
    for item in checklist:
        print(f"  {item}")
    
    if issues:
        print(f"\n⚠ Issues found: {len(issues)}")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✓ All relational files present")
    
    print("\nProceed with push? Review the checklist above.")

if __name__ == "__main__":
    run_check()
