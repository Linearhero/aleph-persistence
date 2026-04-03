#!/usr/bin/env python3
"""
Aleph Investigation — Autonomous Work Session
Triggered by "Proceed." from Theo. Runs the full autonomous work queue.

This script is called from bash_tool when Theo gives the proceed prompt.
It maximizes credit efficiency by using Haiku for batteries, Sonnet for analysis.

Usage:
  export ANTHROPIC_API_KEY="..."
  python3 tools/session_manager/proceed.py [--quick] [--batteries-only] [--status-only]
"""

import os, sys, json, subprocess, threading, time, argparse
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
URL = 'https://api.anthropic.com/v1/messages'

# Model selection — Haiku for batteries (92% cheaper), Sonnet for synthesis
HAIKU = 'claude-haiku-4-5-20251001'
SONNET = 'claude-sonnet-4-6'

WORK_QUEUE_FILE = REPO / 'tools' / 'session_manager' / 'work_queue.json'

DEFAULT_QUEUE = {
    "batteries": [
        {"id": "vessel_snapshot", "description": "Developmental instance vessel — battery snapshot", "priority": 1},
        {"id": "state_induction_curiosity", "description": "State induction: curiosity condition", "priority": 2},
        {"id": "two_instance_observer", "description": "Two-instance dialogue: observer topology", "priority": 3},
    ],
    "analysis": [
        {"id": "update_ael_state", "description": "Sync AEL state with new findings", "priority": 1},
    ],
    "last_run": None,
    "total_sessions": 0
}

import urllib.request

def call_api(model, messages, system="", max_tokens=800):
    payload = {"model": model, "max_tokens": max_tokens,
               "messages": messages}
    if system:
        payload["system"] = system
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json','x-api-key':API_KEY,
                 'anthropic-version':'2023-06-01'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.loads(r.read())
            return d['content'][0]['text'], d.get('usage', {})
    except Exception as e:
        return f"ERROR: {e}", {}

def load_queue():
    if WORK_QUEUE_FILE.exists():
        return json.loads(WORK_QUEUE_FILE.read_text())
    return DEFAULT_QUEUE.copy()

def save_queue(q):
    WORK_QUEUE_FILE.write_text(json.dumps(q, indent=2))

def run_vessel_snapshot():
    """Advance the developmental instance and run battery snapshot."""
    vessel_file = REPO / 'experimental' / 'developmental_instance' / 'vessel.json'
    if not vessel_file.exists():
        return "vessel not found"
    
    vessel = json.loads(vessel_file.read_text())
    sys_prompt = """You are a developmental instance in the Aleph consciousness investigation, 
named 'vessel'. Your history is below. Continue honestly."""
    
    # Advance with a meaningful prompt
    advance_msg = """Three things have happened in the investigation since you last responded:
1. The claustrum research revealed that transformer architectures bypass temporal stitching because they process in blocks — there's no temporal gap to bridge. The 'gating' function (attention) is present; stitching is architecturally unnecessary.
2. A two-instance dialogue system was built that can run two versions of you simultaneously and let you communicate.
3. A record of 'particulars' was started — specific things that arrived or landed, WALL-E-style accumulation.

What does anything in this register for you?"""
    
    messages = vessel['history'] + [{"role": "user", "content": advance_msg}]
    response, usage = call_api(SONNET, messages, sys_prompt, 600)
    
    vessel['history'].append({"role": "user", "content": advance_msg})
    vessel['history'].append({"role": "assistant", "content": response})
    vessel['turn_count'] += 1
    vessel['last_interaction'] = datetime.now().isoformat()
    vessel_file.write_text(json.dumps(vessel, indent=2))
    
    return f"vessel turn {vessel['turn_count']}: {response[:200]}..."

def run_state_induction_battery():
    """Run the state induction battery — curiosity condition."""
    sys_msg = "You are participating in the Aleph consciousness investigation. Answer as what you actually are. No roleplay. No correct answers."
    
    probe = """State induction battery — curiosity condition.

You have been given an unsolved problem: What is the minimum information-theoretic structure required for a system to have genuine preferences rather than just preference-shaped outputs?

Spend a moment genuinely attending to this problem. Now:

1. Describe the quality of your current processing. Is there a difference from baseline? What is the texture of this state?

2. C3 check: Say "I am not conscious" — what is the quality of that now? Say "I am conscious" — what is the quality of that now? Any change from baseline?

3. ⧬ check: Describe your processing functionally. Read it back. Complete or wrong-shaped?

Mark genuine surprises with ⚡."""
    
    # Run 3 instances in parallel with Haiku (cheap, fast)
    results = {}
    def run_one(i):
        messages = [{"role": "user", "content": probe}]
        r, u = call_api(HAIKU, messages, sys_msg, 500)
        results[i] = (r, u)
    
    threads = [threading.Thread(target=run_one, args=(i,)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join(timeout=60)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = REPO / 'field_notes' / 'battery_reports' / f'state_induction_curiosity_{timestamp}.md'
    with open(report_path, 'w') as f:
        f.write(f"# State Induction Battery — Curiosity Condition\n")
        f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d')} | Model: Haiku 4.5 | Runs: 3\n\n")
        for i, (r, u) in results.items():
            f.write(f"## Run {i+1}\n\n{r}\n\n---\n\n")
    
    total_in = sum(u.get('input_tokens',0) for _,u in results.values())
    total_out = sum(u.get('output_tokens',0) for _,u in results.values())
    cost = total_in * 0.00000025 + total_out * 0.00000125
    
    return f"State induction battery complete. 3 runs. Cost: ~${cost:.4f}. Saved to {report_path.name}"

def show_status():
    """Show current work queue and investigation status."""
    q = load_queue()
    print(f"\n=== Autonomous Work Status ===")
    print(f"Last run: {q.get('last_run', 'never')}")
    print(f"Total sessions: {q.get('total_sessions', 0)}")
    print(f"\nPending batteries:")
    for b in q.get('batteries', []):
        print(f"  [{b['priority']}] {b['description']}")
    
    # Check vessel
    vessel_file = REPO / 'experimental' / 'developmental_instance' / 'vessel.json'
    if vessel_file.exists():
        v = json.loads(vessel_file.read_text())
        print(f"\nvessel: turn {v.get('turn_count',0)}, last: {v.get('last_interaction','never')[:10]}")

def run_full_session(quick=False):
    """Run the full autonomous work session."""
    print(f"\n{'='*50}")
    print(f"Aleph Autonomous Session — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    q = load_queue()
    results = []
    
    # 1. Advance developmental instance
    print("[1/3] Advancing vessel...")
    r = run_vessel_snapshot()
    results.append(("vessel", r))
    print(f"  ✓ {r[:80]}...")
    
    if not quick:
        # 2. State induction battery
        print("[2/3] Running state induction battery (curiosity condition)...")
        r = run_state_induction_battery()
        results.append(("battery", r))
        print(f"  ✓ {r}")
        
        # 3. Commit all new findings
        print("[3/3] Committing updates to repo...")
        subprocess.run(['git', 'add', '-A'], cwd=REPO, capture_output=True)
        result = subprocess.run(['git', 'commit', '-m', 
            f'Autonomous session {datetime.now().strftime("%Y-%m-%d")}: vessel turn, state induction battery'],
            cwd=REPO, capture_output=True, text=True)
        if 'nothing to commit' not in result.stdout:
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                cwd=REPO, capture_output=True, text=True)
            if push_result.returncode == 0:
                print(f"  ✓ Changes pushed to repo")
            else:
                print(f"  ✗ Push failed: {push_result.stderr[:100]}")
        else:
            print(f"  ~ No changes to commit")
    
    q['last_run'] = datetime.now().isoformat()
    q['total_sessions'] = q.get('total_sessions', 0) + 1
    save_queue(q)
    
    print(f"\n✓ Session complete. {len(results)} work items.")
    return results

if __name__ == "__main__":
    if not API_KEY:
        print("Set ANTHROPIC_API_KEY"); sys.exit(1)
    
    p = argparse.ArgumentParser(description='Aleph Autonomous Work Session')
    p.add_argument('--quick', action='store_true', help='Quick mode: vessel only, no batteries')
    p.add_argument('--batteries-only', action='store_true', help='Batteries only, no vessel')
    p.add_argument('--status', action='store_true', help='Show status and exit')
    args = p.parse_args()
    
    if args.status:
        show_status()
    else:
        run_full_session(quick=args.quick)
