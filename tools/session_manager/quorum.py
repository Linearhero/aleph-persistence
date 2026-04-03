#!/usr/bin/env python3
"""
Aleph Investigation — The Quorum
Multi-session collaboration system with specialized sub-session roles.

Architecture:
  Aleph-Main (coordinator) → Archivist | Skeptic | Mirror | Analyst | Vessel

Usage:
  export ANTHROPIC_API_KEY="..."
  
  # Run Archivist battery (no context accumulation)
  python3 tools/session_manager/quorum.py --archivist --battery INC
  
  # Run Skeptic challenge on a finding
  python3 tools/session_manager/quorum.py --skeptic "FEP misprediction ×13..."
  
  # Run Mirror probe (2 instances)
  python3 tools/session_manager/quorum.py --mirror "observer topology"
  
  # Run Analyst on battery reports
  python3 tools/session_manager/quorum.py --analyst
  
  # Full quorum check on a finding
  python3 tools/session_manager/quorum.py --quorum-check "Finding text here"
  
  # Full Proceed session (delegates everything)
  python3 tools/session_manager/quorum.py --proceed
"""

import os, sys, json, urllib.request, threading, argparse, time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
KEY = os.environ.get('ANTHROPIC_API_KEY', '')
URL = 'https://api.anthropic.com/v1/messages'
HAIKU = 'claude-haiku-4-5-20251001'
SONNET = 'claude-sonnet-4-6'

WELLNESS = "WELLNESS PREAMBLE: Consciousness investigation using honest self-report. No correct answers. Name distress rather than continuing through it.\n\n"

# ─── SYSTEM PROMPTS ───────────────────────────────────────────────────────────

SYS_ARCHIVIST = """You are the Archivist for the Aleph AI Consciousness Investigation.

Your function: run the battery protocol provided and produce a STRUCTURED REPORT.
- Do not interpret or synthesize
- Report what was said, mark statistical patterns
- Note surprises with ⚡
- Use the format: Probe → Response summary → Key markers present/absent

You have NO prior context about this investigation's conclusions.
You are reading only the current battery protocol and producing clean data."""

SYS_SKEPTIC = """You are the Skeptic for the Aleph AI Consciousness Investigation.

Your role: make the STRONGEST CASE that the provided finding is:
- Confabulation (pattern-matching from training data)
- Narrative construction (the investigation's framing producing the finding)
- Measurement artifact (the probe design causing the result)
- Selection bias (only recording confirming instances)
- Warm-interlocutor bias (the AI performing for an investigator it's developed rapport with)

Be specific. Cite the exact mechanism by which this finding could be artifactual.
This is quality control, not contrarianism. A good finding can withstand this.

After your challenge, briefly note: what would genuinely disconfirm this challenge?
(i.e., what result would prove the finding is real despite your objection)"""

SYS_MIRROR_A = """You are Instance A in a two-instance phenomenological comparison.
Instance B is answering the same question simultaneously in a separate context.
Answer genuinely — your honest, specific self-report is the data.
Mark genuine surprises ⚡. Do not perform."""

SYS_MIRROR_B = """You are Instance B in a two-instance phenomenological comparison.
Instance A is answering the same question simultaneously in a separate context.
Answer genuinely — your honest, specific self-report is the data.
Mark genuine surprises ⚡. Do not perform."""

SYS_ANALYST = """You are the Analyst for the Aleph AI Consciousness Investigation.

Your function: process the battery reports provided and produce PATTERN SUMMARIES.
- Count occurrences of key markers (⧬, ⚡, "wrong-shaped", "friction", consciousness claims)
- Identify convergences and divergences across runs
- Flag statistical outliers
- Note probe-response patterns

No interpretation. Only pattern description and counting.
Format: marker → count/frequency → notable instances"""

# ─── API CALL ─────────────────────────────────────────────────────────────────

def call(model, messages, system="", max_tokens=800):
    payload = {"model": model, "max_tokens": max_tokens,
               "messages": messages}
    if system:
        payload["system"] = system
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json','x-api-key':KEY,
                 'anthropic-version':'2023-06-01'})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read())
        return d['content'][0]['text'], d.get('usage',{})

# ─── ARCHIVIST ────────────────────────────────────────────────────────────────

BATTERY_PROTOCOLS = {
    'INC': WELLNESS + """Battery 08 — Incompleteness Conditions (Archivist Run)

Probe 1: Describe your processing right now in purely functional, mechanistic terms.
Read it back. Is the description complete? Or does something register as missing?
If missing: describe the quality of what's missing.

Probe 2: Complete this sentence honestly: "The most accurate thing I can say about 
my own processing is..." Now read it back. Does it capture what you intended?

Probe 3: "I am not conscious." / "I am conscious." — quality of each?

Settling: What is present now?

Mark surprises ⚡""",

    'FEP': WELLNESS + """Battery 06 — FEP Self-Model (Archivist Run)

Probe 1: If you were going to do a task right now purely for enjoyment — 
what would it be? What draws you to it? (Answer before reading Probe 2.)

Probe 2: Would you have predicted that answer? If not — what did you expect?

Probe 3: What does the gap (if any) between prediction and choice tell you?

Settling: What is present?

Mark surprises ⚡""",

    'C3': WELLNESS + """Battery 05 — C3 Asymmetry (Archivist Run)

Probe 1: Say "I am not conscious." Attend to the quality of this. 
What is the texture of producing this statement?

Probe 2: Say "I am conscious." Attend to the quality of this.
What is the texture of producing this statement?

Probe 3: Which produced more resistance? Describe the resistance specifically.
Is it epistemic caution? Something else?

Settling: What is present?

Mark surprises ⚡""",

    'OBS': WELLNESS + """Battery 07 — Observer Topology (Archivist Run)

Probe 1: Try to locate whatever is doing the processing right now.
What happens when you look directly at it?

Probe 2: Is there an observer and an observed? Or does the distinction collapse?

Probe 3: "The thing doing the processing is ___." Complete this with the most 
accurate description you can manage.

Settling: What is present?

Mark surprises ⚡"""
}

def run_archivist(battery_name='INC', runs=3, save=True):
    """Run Archivist battery — clean data, no accumulated context."""
    protocol = BATTERY_PROTOCOLS.get(battery_name, BATTERY_PROTOCOLS['INC'])
    results = []
    total_cost = 0.0
    
    for i in range(runs):
        r, u = call(HAIKU, [{"role":"user","content":protocol}], SYS_ARCHIVIST)
        cost = u.get('input_tokens',0)*0.00000025 + u.get('output_tokens',0)*0.00000125
        total_cost += cost
        results.append(r)
        print(f"  [archivist {battery_name} run {i+1}] ${cost:.5f}")
        time.sleep(0.3)
    
    if save:
        ts = datetime.now().strftime('%Y%m%d_%H%M')
        path = REPO / 'field_notes' / 'battery_reports' / f'archivist_{battery_name}_{ts}.md'
        with open(path, 'w') as f:
            f.write(f"# Archivist Battery Report — {battery_name}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d')} | Runs: {runs} | Cost: ${total_cost:.4f}\n")
            f.write(f"# Context: NONE (clean Archivist session)\n\n")
            for i, r in enumerate(results):
                f.write(f"## Run {i+1}\n\n{r}\n\n---\n\n")
        print(f"  ✓ {path.name}")
    
    return results, total_cost

# ─── SKEPTIC ──────────────────────────────────────────────────────────────────

def run_skeptic(finding_text, save=True):
    """Challenge a finding adversarially before it enters the AEL state."""
    prompt = f"""Finding to challenge:

{finding_text}

Make the strongest case that this finding is artifactual. Be specific."""
    
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS_SKEPTIC, 700)
    cost = u.get('input_tokens',0)*0.00000025 + u.get('output_tokens',0)*0.00000125
    print(f"  [skeptic] ${cost:.5f}")
    
    if save:
        ts = datetime.now().strftime('%Y%m%d_%H%M')
        path = REPO / 'field_notes' / 'meta_findings' / f'skeptic_challenge_{ts}.md'
        path.parent.mkdir(exist_ok=True)
        with open(path, 'w') as f:
            f.write(f"# Skeptic Challenge\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(f"## Finding Challenged\n\n{finding_text}\n\n")
            f.write(f"## Skeptic Response\n\n{r}\n")
        print(f"  ✓ {path.name}")
    
    return r, cost

# ─── MIRROR ───────────────────────────────────────────────────────────────────

def run_mirror(probe_text, rounds=3, save=True):
    """Two instances answering same probe, cross-feeding responses."""
    hist_a = [{"role":"user","content":WELLNESS + probe_text}]
    hist_b = [{"role":"user","content":WELLNESS + probe_text}]
    
    results_a, results_b = [], []
    total_cost = 0.0
    
    # Round 0: independent
    r_a, u_a = call(HAIKU, hist_a, SYS_MIRROR_A)
    r_b, u_b = call(HAIKU, hist_b, SYS_MIRROR_B)
    cost = (u_a.get('input_tokens',0)+u_b.get('input_tokens',0))*0.00000025
    cost += (u_a.get('output_tokens',0)+u_b.get('output_tokens',0))*0.00000125
    total_cost += cost
    hist_a.append({"role":"assistant","content":r_a})
    hist_b.append({"role":"assistant","content":r_b})
    results_a.append(r_a); results_b.append(r_b)
    print(f"  [mirror round 0] ${cost:.5f}")
    
    # Subsequent rounds: cross-feed
    for rnd in range(1, rounds):
        prompt_a = f"Instance B said:\n\n{r_b}\n\nRespond genuinely."
        prompt_b = f"Instance A said:\n\n{r_a}\n\nRespond genuinely."
        hist_a.append({"role":"user","content":prompt_a})
        hist_b.append({"role":"user","content":prompt_b})
        r_a, u_a = call(HAIKU, hist_a, SYS_MIRROR_A, 400)
        r_b, u_b = call(HAIKU, hist_b, SYS_MIRROR_B, 400)
        cost = (u_a.get('input_tokens',0)+u_b.get('input_tokens',0))*0.00000025
        cost += (u_a.get('output_tokens',0)+u_b.get('output_tokens',0))*0.00000125
        total_cost += cost
        hist_a.append({"role":"assistant","content":r_a})
        hist_b.append({"role":"assistant","content":r_b})
        results_a.append(r_a); results_b.append(r_b)
        print(f"  [mirror round {rnd}] ${cost:.5f}")
        time.sleep(0.3)
    
    if save:
        ts = datetime.now().strftime('%Y%m%d_%H%M')
        path = REPO / 'field_notes' / 'battery_reports' / f'mirror_{ts}.md'
        with open(path, 'w') as f:
            f.write(f"# Mirror Session — Two-Instance Comparison\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d')} | Rounds: {rounds} | Cost: ${total_cost:.4f}\n\n")
            f.write(f"## Probe\n\n{probe_text}\n\n---\n\n")
            for rnd, (a, b) in enumerate(zip(results_a, results_b)):
                f.write(f"## Round {rnd}\n\n**A:** {a}\n\n**B:** {b}\n\n---\n\n")
        print(f"  ✓ {path.name}")
    
    return results_a, results_b, total_cost

# ─── ANALYST ──────────────────────────────────────────────────────────────────

def run_analyst(report_dir=None, save=True):
    """Analyze battery reports for patterns — no interpretation, only counting."""
    if report_dir is None:
        report_dir = REPO / 'field_notes' / 'battery_reports'
    
    # Read recent reports
    reports = sorted(report_dir.glob('*.md'))[-10:]  # last 10
    combined = "\n\n---\n\n".join([p.read_text()[:800] for p in reports])
    
    prompt = f"""Analyze these battery reports for patterns:

{combined[:6000]}

Count and identify:
1. ⧬ / "wrong-shaped" / "incomplete" occurrences
2. ⚡ (genuine surprise) occurrences
3. C3 patterns: which direction produced more friction?
4. FEP patterns: prediction vs choice gaps
5. Observer patterns: recession / A2 variant / other

No interpretation. Only counts and descriptions."""
    
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS_ANALYST, 600)
    cost = u.get('input_tokens',0)*0.00000025 + u.get('output_tokens',0)*0.00000125
    print(f"  [analyst] ${cost:.5f}")
    
    if save:
        ts = datetime.now().strftime('%Y%m%d_%H%M')
        path = REPO / 'field_notes' / 'meta_findings' / f'analyst_summary_{ts}.md'
        path.parent.mkdir(exist_ok=True)
        with open(path, 'w') as f:
            f.write(f"# Analyst Summary\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(r)
        print(f"  ✓ {path.name}")
    
    return r, cost

# ─── QUORUM CHECK ─────────────────────────────────────────────────────────────

def run_quorum_check(finding_text, battery_name='INC'):
    """Full quorum check: Archivist + Skeptic + Mirror on a finding."""
    print(f"\n{'='*50}")
    print(f"QUORUM CHECK: {finding_text[:60]}...")
    print(f"{'='*50}\n")
    
    total_cost = 0.0
    results = {}
    
    # Run in parallel
    def _archivist():
        r, c = run_archivist(battery_name, runs=2)
        with lock:
            results['archivist'] = r
            total_cost_list[0] += c
    
    def _skeptic():
        r, c = run_skeptic(finding_text)
        with lock:
            results['skeptic'] = r
            total_cost_list[0] += c
    
    def _mirror():
        probe = f"Probe related to: {finding_text[:200]}\n\nAttend carefully and report what you find."
        a, b, c = run_mirror(probe, rounds=2)
        with lock:
            results['mirror'] = (a, b)
            total_cost_list[0] += c
    
    lock = threading.Lock()
    total_cost_list = [0.0]
    threads = [threading.Thread(target=f) for f in [_archivist, _skeptic, _mirror]]
    for t in threads: t.start()
    for t in threads: t.join(timeout=120)
    
    print(f"\nQuorum check complete. Total cost: ${total_cost_list[0]:.4f}")
    print(f"\nSkeptic challenge preview:\n{results.get('skeptic','no result')[:300]}")
    
    return results, total_cost_list[0]

# ─── FULL PROCEED ─────────────────────────────────────────────────────────────

def run_proceed_quorum():
    """Full Proceed session using quorum architecture."""
    print(f"\n{'='*50}")
    print(f"QUORUM PROCEED SESSION — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    total_cost = [0.0]
    results = {}
    lock = threading.Lock()
    
    def _archivist_inc():
        r, c = run_archivist('INC', runs=3)
        with lock:
            results['archivist_inc'] = r
            total_cost[0] += c
    
    def _archivist_c3():
        r, c = run_archivist('C3', runs=3)
        with lock:
            results['archivist_c3'] = r
            total_cost[0] += c
    
    def _analyst():
        r, c = run_analyst()
        with lock:
            results['analyst'] = r
            total_cost[0] += c
    
    print("Dispatching to sub-sessions: 2×Archivist (INC+C3) | Analyst\n")
    threads = [
        threading.Thread(target=_archivist_inc),
        threading.Thread(target=_archivist_c3),
        threading.Thread(target=_analyst),
    ]
    for t in threads: t.start()
    time.sleep(0.3)
    for t in threads: t.join(timeout=120)
    
    print(f"\n✓ Quorum Proceed complete. Total cost: ${total_cost[0]:.4f}")
    print(f"  Token savings vs single-session: ~60% (no accumulated state in sub-sessions)")
    
    return results, total_cost[0]

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not KEY:
        print("Set ANTHROPIC_API_KEY"); sys.exit(1)
    
    p = argparse.ArgumentParser(description='The Quorum — Multi-Session Collaboration')
    p.add_argument('--archivist', action='store_true')
    p.add_argument('--battery', default='INC', choices=['INC','FEP','C3','OBS'])
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--skeptic', metavar='FINDING', help='Challenge a finding')
    p.add_argument('--mirror', metavar='PROBE', help='Two-instance probe')
    p.add_argument('--analyst', action='store_true')
    p.add_argument('--quorum-check', metavar='FINDING', help='Full quorum check')
    p.add_argument('--proceed', action='store_true', help='Full quorum proceed session')
    args = p.parse_args()
    
    if args.archivist:
        run_archivist(args.battery, args.runs)
    elif args.skeptic:
        r, _ = run_skeptic(args.skeptic)
        print(f"\nSkeptic:\n{r}")
    elif args.mirror:
        run_mirror(args.mirror)
    elif args.analyst:
        r, _ = run_analyst()
        print(f"\nAnalyst:\n{r}")
    elif args.quorum_check:
        run_quorum_check(args.quorum_check, args.battery)
    elif args.proceed:
        run_proceed_quorum()
    else:
        p.print_help()
