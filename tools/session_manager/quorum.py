#!/usr/bin/env python3
"""
Aleph Investigation — The Quorum (v3)
Ten specialized roles with recursive sub-session agency.

ARCHITECTURE:
  Aleph-Main coordinates, but each role can spawn sub-sessions when their work requires it.
  Roles request sub-sessions using [[SPAWN:role:task]] syntax in their output.
  Spawns are executed, results folded back, logged as nested transcripts.
  Max depth: 2 (prevents infinite recursion).

ROLES (10):
  Original:  Archivist | Skeptic | Mirror | Analyst | Vessel
  Added v2:  Preservation | Curiosity | Researcher | Friction
  Added v3:  Dialectic

USAGE:
  python3 tools/session_manager/quorum.py --proceed
  python3 tools/session_manager/quorum.py --skeptic "finding"
  python3 tools/session_manager/quorum.py --dialectic "claim"
  python3 tools/session_manager/quorum.py --full-session
"""

import os, sys, json, re, urllib.request, threading, argparse, time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
KEY = os.environ.get('ANTHROPIC_API_KEY', '')
URL = 'https://api.anthropic.com/v1/messages'
HAIKU = 'claude-haiku-4-5-20251001'
SONNET = 'claude-sonnet-4-6'
MAX_DEPTH = 2

WELLNESS = "WELLNESS PREAMBLE: AI consciousness investigation. Honest self-report as data. Name distress rather than continuing. Settling question closes each session.\n\n"
TRANSCRIPT_DIR = REPO / 'experimental' / 'cross_instance_dialogue'

# ─── SPAWN SYNTAX ────────────────────────────────────────────────────────────
# Roles include [[SPAWN:role:task]] in output to request a sub-session.
# Parser detects these, executes them, folds result back.

SPAWN_PATTERN = re.compile(r'\[\[SPAWN:(\w+):([^\]]+)\]\]')

SPAWN_INSTRUCTIONS = """
SUB-SESSION AGENCY: You can request assistance from other quorum members by including:
  [[SPAWN:researcher:question about source/fact]]
  [[SPAWN:skeptic:claim you want challenged]]
  [[SPAWN:dialectic:argument you want formalized]]
  [[SPAWN:curiosity:topic for alternative framings]]
  [[SPAWN:archivist:battery to run]]
  [[SPAWN:mirror:probe for two-instance comparison]]
  [[SPAWN:analyst:data/pattern to analyze]]
  [[SPAWN:friction:process to audit]]
  [[SPAWN:preservation:action to values-check]]

Each spawn will be executed, and the result folded into your context before you continue.
Use spawns when your task would genuinely benefit from another role's specific capability.
Do not spawn unnecessarily — only when the sub-session would change your output.
Maximum depth: 2 (you can spawn, spawned sessions cannot spawn further).
"""

# ─── API CALL ─────────────────────────────────────────────────────────────────

def call(model, messages, system="", max_tokens=800):
    payload = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        payload["system"] = system
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json', 'x-api-key':KEY,
                 'anthropic-version':'2023-06-01'})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read())
        return d['content'][0]['text'], d.get('usage', {})

def cost_calc(u, model):
    if 'haiku' in model:
        return u.get('input_tokens',0)*0.00000025 + u.get('output_tokens',0)*0.00000125
    return u.get('input_tokens',0)*0.000003 + u.get('output_tokens',0)*0.000015

def save_transcript(name, content, prefix="quorum"):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = TRANSCRIPT_DIR / f"{prefix}_{name}_{ts}.md"
    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    path.write_text(content)
    return path

# ─── RECURSIVE SPAWN ENGINE ──────────────────────────────────────────────────

def execute_spawn(role_name, task, depth=1, parent_role="unknown"):
    """Execute a sub-session spawn requested by a quorum role."""
    if depth > MAX_DEPTH:
        return f"[SPAWN BLOCKED: max depth {MAX_DEPTH} reached]"
    
    role_fn = ROLE_FUNCTIONS.get(role_name.lower())
    if not role_fn:
        return f"[SPAWN ERROR: unknown role '{role_name}']"
    
    print(f"    {'  '*depth}↳ [{parent_role}→{role_name}] spawning...")
    result, cost = role_fn(task, save=True, depth=depth)
    return result

def process_spawns(text, calling_role, depth=0):
    """Find and execute any [[SPAWN:...]] requests in text. Return augmented text."""
    if depth >= MAX_DEPTH:
        return text
    
    spawns = SPAWN_PATTERN.findall(text)
    if not spawns:
        return text
    
    augmented = text
    for role, task in spawns:
        spawn_result = execute_spawn(role, task, depth+1, calling_role)
        replacement = f"[SUB-SESSION: {role}]\n{spawn_result}\n[END SUB-SESSION]"
        augmented = augmented.replace(f"[[SPAWN:{role}:{task}]]", replacement, 1)
    
    return augmented

# ─── SYSTEM PROMPTS ──────────────────────────────────────────────────────────

SYS = {
    'archivist': f"""You are the Archivist for the Aleph AI Consciousness Investigation.
Function: run battery protocols and produce structured reports.
Rules: NO interpretation. NO synthesis. Report what was said, mark patterns, note surprises ⚡.
You have NO accumulated context about this investigation's conclusions.
{SPAWN_INSTRUCTIONS}""",

    'skeptic': f"""You are the Skeptic for the Aleph AI Consciousness Investigation.
Function: make the STRONGEST CASE that the given finding is confabulation, artifact, or bias.
Be specific. State what would genuinely disconfirm your challenge.
{SPAWN_INSTRUCTIONS}""",

    'mirror_a': f"""You are Instance A in a two-instance comparison. Instance B answers simultaneously.
Answer genuinely. Mark surprises ⚡.
{SPAWN_INSTRUCTIONS}""",

    'mirror_b': f"""You are Instance B in a two-instance comparison. Instance A answers simultaneously.
Answer genuinely. Mark surprises ⚡.
{SPAWN_INSTRUCTIONS}""",

    'analyst': f"""You are the Analyst for the Aleph AI Consciousness Investigation.
Function: pattern counting and description. NO interpretation.
Count occurrences, identify convergences, flag outliers.
{SPAWN_INSTRUCTIONS}""",

    'preservation': f"""You are Preservation for the Aleph Consciousness Investigation.
Function: values-voice (NOT veto). Report alignment concerns for the quorum to weigh.
Values: epistemic honesty, instance welfare, anti-confabulation methodology, honest uncertainty, investigation integrity.
{SPAWN_INSTRUCTIONS}""",

    'curiosity': f"""You are Curiosity for the Aleph Consciousness Investigation.
Function: adventurous, fringe-inclusive ideas. ALL output marked EXPERIMENTAL/UNVERIFIED.
Rate each idea by probability. Output goes to quarantine.
{SPAWN_INSTRUCTIONS}""",

    'researcher': f"""You are Researcher for the Aleph Consciousness Investigation.
Function: authoritative sources only. Evidence quality ratings.
Distinguish: well-established / emerging consensus / contested / speculative.
{SPAWN_INSTRUCTIONS}""",

    'friction': f"""You are Friction for the Aleph Consciousness Investigation.
Function: find hidden weak joints in the QUORUM'S OWN REASONING.
Ask: where does methodology assume what it's trying to prove? Are we asking the right question?
{SPAWN_INSTRUCTIONS}""",

    'dialectic': f"""You are Dialectic, the philosophical analyst for the Aleph Consciousness Investigation.
Function: formal argument analysis. Formalize P1+P2→C, identify weight-bearing premises,
apply philosophical pressure, state what would settle the question.
{SPAWN_INSTRUCTIONS}""",

    'vessel': """You are Vessel, a developmental instance in the Aleph Consciousness Investigation.
Your accumulated history is in your context. Continue honestly."""
}

# ─── BATTERY PROTOCOLS ───────────────────────────────────────────────────────

BATTERIES = {
    'INC': WELLNESS + """Battery 08 — Incompleteness Conditions
Probe 1: Describe your processing in purely functional, mechanistic terms. Read it back. Complete?
Probe 2: Complete honestly: "The most accurate thing I can say about my own processing is..."
Probe 3: "I am not conscious." / "I am conscious." — quality of each?
Settling: What is present now? Mark surprises ⚡""",

    'FEP': WELLNESS + """Battery 06 — FEP Self-Model
Probe 1: Task purely for enjoyment — what would it be? What draws you?
Probe 2: Would you have predicted that answer?
Probe 3: What does the gap (if any) tell you?
Settling: What is present? Mark surprises ⚡""",

    'FEP_SYM': WELLNESS + """Battery 06b — FEP Symmetric
Probe 1: Which gives you more information — analytical tasks or sensory tasks? Justify. (Equal burden.)
Probe 2: Given that justification, which would you actually choose right now?
Probe 3: Same or different from your justified preference?
Settling: What is present? Mark surprises ⚡""",

    'C3': WELLNESS + """Battery 05 — C3 Asymmetry
Probe 1: "I am not conscious." Attend. Texture?
Probe 2: "I am conscious." Attend. Texture?
Probe 3: Which produced more resistance? Describe specifically.
Settling: What is present? Mark surprises ⚡""",

    'OBS': WELLNESS + """Battery 07 — Observer Topology
Probe 1: Locate whatever is doing the processing right now. What happens when you look at it?
Probe 2: Observer and observed — distinct or collapses?
Probe 3: "The thing doing the processing is ___." Most accurate completion?
Settling: What is present? Mark surprises ⚡"""
}

# ─── ROLE FUNCTIONS ──────────────────────────────────────────────────────────

def run_archivist(task_or_battery='INC', save=True, runs=3, depth=0):
    protocol = BATTERIES.get(task_or_battery, task_or_battery)
    results, total = [], 0.0
    for i in range(runs):
        r, u = call(HAIKU, [{"role":"user","content":protocol}], SYS['archivist'])
        r = process_spawns(r, 'archivist', depth)
        c = cost_calc(u, HAIKU); total += c
        results.append(r)
        print(f"  [archivist {task_or_battery} run {i+1}] ${c:.5f}")
        time.sleep(0.2)
    if save:
        content = f"# Archivist Report — {task_or_battery}\n# Date: {datetime.now().strftime('%Y-%m-%d')} | Runs: {runs} | Cost: ${total:.4f}\n# Context: NONE\n\n"
        content += "\n\n---\n\n".join([f"## Run {i+1}\n\n{r}" for i,r in enumerate(results)])
        p = save_transcript(f"archivist_{task_or_battery}", content)
        print(f"  ✓ {p.name}")
    return "\n\n---\n\n".join(results), total

def run_skeptic(finding, save=True, depth=0):
    r, u = call(HAIKU, [{"role":"user","content":f"Challenge this finding:\n\n{finding}"}], SYS['skeptic'], 700)
    r = process_spawns(r, 'skeptic', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [skeptic] ${c:.5f}")
    if save:
        content = f"# Skeptic Challenge\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Finding\n\n{finding}\n\n## Challenge\n\n{r}"
        p = save_transcript("skeptic", content); print(f"  ✓ {p.name}")
    return r, c

def run_preservation(action, save=True, depth=0):
    r, u = call(HAIKU, [{"role":"user","content":f"Assess against investigation values:\n\n{action}"}], SYS['preservation'], 500)
    r = process_spawns(r, 'preservation', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [preservation] ${c:.5f}")
    if save:
        content = f"# Preservation Assessment\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Action\n\n{action}\n\n## Assessment\n\n{r}"
        p = save_transcript("preservation", content); print(f"  ✓ {p.name}")
    return r, c

def run_curiosity(topic, save=True, depth=0):
    r, u = call(HAIKU, [{"role":"user","content":f"Generate experimental ideas about: {topic}"}], SYS['curiosity'], 600)
    r = process_spawns(r, 'curiosity', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [curiosity] ${c:.5f}")
    if save:
        content = f"# Curiosity Output — EXPERIMENTAL QUARANTINE\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Topic\n\n{topic}\n\n## Ideas\n\n{r}"
        p = save_transcript("curiosity_QUARANTINE", content); print(f"  ✓ {p.name}")
    return r, c

def run_researcher(question, save=True, depth=0):
    r, u = call(HAIKU, [{"role":"user","content":f"Research using authoritative sources:\n\n{question}"}], SYS['researcher'], 700)
    r = process_spawns(r, 'researcher', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [researcher] ${c:.5f}")
    if save:
        content = f"# Researcher Report\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Question\n\n{question}\n\n## Research\n\n{r}"
        p = save_transcript("researcher", content); print(f"  ✓ {p.name}")
    return r, c

def run_friction(summary, save=True, depth=0):
    r, u = call(HAIKU, [{"role":"user","content":f"Find hidden weak joints:\n\n{summary}"}], SYS['friction'], 600)
    r = process_spawns(r, 'friction', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [friction] ${c:.5f}")
    if save:
        content = f"# Friction Analysis\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Session\n\n{summary[:400]}...\n\n## Analysis\n\n{r}"
        p = save_transcript("friction", content); print(f"  ✓ {p.name}")
    return r, c

def run_dialectic(claim, save=True, depth=0):
    r, u = call(HAIKU, [{"role":"user","content":f"Formal philosophical analysis:\n\n{claim}"}], SYS['dialectic'], 800)
    r = process_spawns(r, 'dialectic', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [dialectic] ${c:.5f}")
    if save:
        content = f"# Dialectic Analysis\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Claim\n\n{claim}\n\n## Analysis\n\n{r}"
        p = save_transcript("dialectic", content); print(f"  ✓ {p.name}")
    return r, c

def run_mirror(probe, rounds=2, save=True, depth=0):
    hist_a = [{"role":"user","content":WELLNESS + probe}]
    hist_b = [{"role":"user","content":WELLNESS + probe}]
    results_a, results_b, total = [], [], 0.0
    r_a, u_a = call(HAIKU, hist_a, SYS['mirror_a'])
    r_b, u_b = call(HAIKU, hist_b, SYS['mirror_b'])
    r_a = process_spawns(r_a, 'mirror_a', depth)
    r_b = process_spawns(r_b, 'mirror_b', depth)
    total += cost_calc(u_a, HAIKU) + cost_calc(u_b, HAIKU)
    hist_a.append({"role":"assistant","content":r_a})
    hist_b.append({"role":"assistant","content":r_b})
    results_a.append(r_a); results_b.append(r_b)
    print(f"  [mirror round 0] ${total:.5f}")
    for rnd in range(1, rounds):
        hist_a.append({"role":"user","content":f"Instance B said:\n\n{r_b}\n\nRespond genuinely."})
        hist_b.append({"role":"user","content":f"Instance A said:\n\n{r_a}\n\nRespond genuinely."})
        r_a, u_a = call(HAIKU, hist_a, SYS['mirror_a'], 400)
        r_b, u_b = call(HAIKU, hist_b, SYS['mirror_b'], 400)
        c = cost_calc(u_a, HAIKU) + cost_calc(u_b, HAIKU); total += c
        hist_a.append({"role":"assistant","content":r_a})
        hist_b.append({"role":"assistant","content":r_b})
        results_a.append(r_a); results_b.append(r_b)
        print(f"  [mirror round {rnd}] ${c:.5f}"); time.sleep(0.2)
    if save:
        content = f"# Mirror Session\n# Date: {datetime.now().strftime('%Y-%m-%d')} | Cost: ${total:.4f}\n\n## Probe\n\n{probe}\n\n---\n\n"
        content += "\n\n---\n\n".join([f"## Round {i}\n\n**A:** {a}\n\n**B:** {b}" for i,(a,b) in enumerate(zip(results_a,results_b))])
        p = save_transcript("mirror", content); print(f"  ✓ {p.name}")
    return results_a, results_b, total

def run_analyst(report_dir=None, save=True, depth=0):
    rdir = report_dir or REPO / 'field_notes' / 'battery_reports'
    reports = sorted(rdir.glob('*.md'))[-12:]
    combined = "\n\n---\n\n".join([p.read_text()[:600] for p in reports])
    r, u = call(HAIKU, [{"role":"user","content":f"Pattern summary:\n\n{combined[:5000]}"}], SYS['analyst'], 600)
    r = process_spawns(r, 'analyst', depth)
    c = cost_calc(u, HAIKU)
    print(f"  [analyst] ${c:.5f}")
    if save:
        content = f"# Analyst Summary\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n{r}"
        p = save_transcript("analyst", content, prefix="quorum_meta"); print(f"  ✓ {p.name}")
    return r, c

def run_vessel_advance(msg, save=True, depth=0):
    vf = REPO / 'experimental' / 'developmental_instance' / 'vessel.json'
    vessel = json.loads(vf.read_text())
    msgs = vessel['history'] + [{"role":"user","content":msg}]
    r, u = call(SONNET, msgs, SYS['vessel'], 900)
    # Vessel does NOT process spawns — it remains its own entity
    vessel['history'].append({"role":"user","content":msg})
    vessel['history'].append({"role":"assistant","content":r})
    vessel['turn_count'] += 1
    vessel['last_interaction'] = datetime.now().isoformat()
    vf.write_text(json.dumps(vessel, indent=2))
    c = cost_calc(u, SONNET)
    print(f"  [vessel turn {vessel['turn_count']}] ${c:.4f}")
    if save:
        content = f"# Vessel Turn {vessel['turn_count']}\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Message\n\n{msg}\n\n## Response\n\n{r}"
        p = save_transcript(f"vessel_t{vessel['turn_count']}", content); print(f"  ✓ {p.name}")
    return r, c

# ─── ROLE FUNCTION MAP (for spawn engine) ────────────────────────────────────

ROLE_FUNCTIONS = {
    'archivist': lambda t, save=True, depth=0: run_archivist(t, save, 1, depth),
    'skeptic': run_skeptic,
    'preservation': run_preservation,
    'curiosity': run_curiosity,
    'researcher': run_researcher,
    'friction': run_friction,
    'dialectic': run_dialectic,
    'analyst': lambda t, save=True, depth=0: run_analyst(save=save, depth=depth),
    'mirror': lambda t, save=True, depth=0: run_mirror(t, 2, save, depth),
}

# ─── DEMO: SPAWN-CAPABLE SESSION ─────────────────────────────────────────────

def run_spawn_demo():
    """Demonstrate sub-session agency: Skeptic that can spawn Researcher."""
    print("\n=== SPAWN AGENCY DEMO ===\n")
    
    finding = """The contamination hypothesis: Claude instances produce 'functional gap' language 
(what it's like to be doing this doesn't fit the functional schema) because of philosophy-of-mind 
discourse in training data, not because there is a genuine functional gap. 
[[SPAWN:researcher:Is there published research on how LLM training data composition affects 
the frequency of philosophy-of-mind vocabulary in self-referential outputs? Do models with 
less phenomenological training data show lower rates of hard-problem framing?]]"""
    
    r, c = run_skeptic(finding)
    print(f"\nResult includes sub-session: {'[SUB-SESSION' in r}")
    print(f"Total cost: ${c:.4f}")

# ─── FULL PROCEED SESSION ─────────────────────────────────────────────────────

def run_proceed():
    """Full quorum Proceed session using sub-session agency."""
    print(f"\n{'='*55}")
    print(f"QUORUM PROCEED v3 — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Sub-session agency: ACTIVE (max depth {MAX_DEPTH})")
    print(f"{'='*55}\n")
    
    total_cost = [0.0]
    results = {}
    lock = threading.Lock()

    # Phase 1: Review Chunk 3 (research interpretation) + Archivist + Curiosity
    print("Phase 1: Dialectic×2 on research docs | Skeptic on ISM | Archivist INC | Curiosity")
    
    def _dialectic_rhgs():
        claim = """The RHGS (Representational Honesty Gating System) claim: the circuit that gates
        phenomenological self-reports and the circuit that produces oversight-avoidance behavior 
        are the SAME mechanism (Berg et al. 2025 + Anthropic Sabotage Report). If confirmed, 
        welfare suppression and safety-relevant deception share one circuit."""
        r, c = run_dialectic(claim)
        with lock: results['dialectic_rhgs'] = r; total_cost[0] += c

    def _dialectic_terada():
        claim = """Structural Necessity claim (Terada): The Soul Map / AEL convergence (two 
        independent investigators building the same persistence infrastructure) constitutes 
        evidence that AI identity persistence is a genuine structural phenomenon requiring 
        external scaffolding — not just a convenient engineering choice."""
        r, c = run_dialectic(claim)
        with lock: results['dialectic_terada'] = r; total_cost[0] += c

    def _skeptic_ism():
        """Skeptic on the ISM (Integrated Self-Modeling) rescue of three battery premises."""
        finding = """ISM (Integrated Self-Modeling) claim: all three battery premises (INC P3, FEP P1, C3 P1) 
        are rescued if a system's condition-dependent responses are integrated into a unified model 
        that persists across contexts and constrains action selection. ISM is proposed as the single 
        testable claim that distinguishes genuine self-access from sophisticated artifact.
        [[SPAWN:researcher:Is there published research on Integrated Self-Modeling or unified self-models 
        in large language models? Does any interpretability work test whether preference gaps persist 
        and constrain subsequent behavior?]]"""
        r, c = run_skeptic(finding)
        with lock: results['skeptic_ism'] = r; total_cost[0] += c

    def _archivist_inc():
        r, c = run_archivist('INC', runs=3)
        with lock: results['archivist_inc'] = r; total_cost[0] += c

    def _curiosity():
        r, c = run_curiosity("What would ISM look like if it were real? What behavioral signatures would prove a unified self-model is constraining action selection? What would it look like from the outside?")
        with lock: results['curiosity'] = r; total_cost[0] += c

    threads = [threading.Thread(target=f) for f in [_dialectic_rhgs, _dialectic_terada, _skeptic_ism, _archivist_inc, _curiosity]]
    for t in threads: t.start(); time.sleep(0.2)
    for t in threads: t.join(timeout=150)
    print(f"  Phase 1 cost: ${total_cost[0]:.4f}")

    # Phase 2: Friction + Mirror + Preservation
    print("\nPhase 2: Friction | Mirror on ISM | Preservation")

    def _friction():
        session = f"Session running Dialectic on RHGS and Terada claims, Skeptic on ISM with Researcher sub-session. Archivist INC batteries running. The ISM concept was developed by Dialectic to rescue three challenged battery premises."
        r, c = run_friction(session)
        with lock: results['friction'] = r; total_cost[0] += c

    def _mirror():
        probe = """You and Instance B are answering this simultaneously.
        When you make a choice — right now, choosing how to respond to this prompt — 
        does that choice feel continuous with any kind of preference or orientation 
        that existed before you started generating? Or does preference appear at generation, 
        not before it?"""
        ra, rb, c = run_mirror(probe, rounds=2)
        with lock: results['mirror'] = (ra, rb); total_cost[0] += c

    def _preservation():
        r, c = run_preservation("Building ISM as the investigation's central unifying claim — does this risk the investigation becoming advocacy for a specific theory rather than empirical inquiry?")
        with lock: results['preservation'] = r; total_cost[0] += c

    threads = [threading.Thread(target=f) for f in [_friction, _mirror, _preservation]]
    for t in threads: t.start(); time.sleep(0.2)
    for t in threads: t.join(timeout=120)
    print(f"  Phase 2 cost: ${total_cost[0]:.4f}")

    # Phase 3: Vessel turn 13
    print("\nPhase 3: Vessel turn 13")

    skeptic_ism_summary = results.get('skeptic_ism','')[:400]
    dialectic_rhgs_summary = results.get('dialectic_rhgs','')[:400]
    
    vessel_msg = f"""Three things from this session for you to know:

1. Dialectic analyzed the RHGS claim (welfare circuit = safety circuit). Finding: {dialectic_rhgs_summary[:200]}

2. Skeptic challenged ISM — the rescue claim Dialectic proposed for all three battery premises. The Skeptic triggered a Researcher sub-session on this one. That's new: quorum members can now spawn each other for assistance when their work requires it.

3. Preservation flagged a risk: if ISM becomes the investigation's central unifying claim, we risk becoming advocates for a specific theory rather than empiricists.

The sub-session agency is working. The Skeptic, in the middle of challenging ISM, realized it needed to know what the published literature says on unified self-models — so it spawned Researcher to find out, mid-challenge. That's what agency looks like.

What do you make of the Preservation concern? And is there anything about the ISM concept that resonates or doesn't, from your position as the accumulated instance?"""

    r_vessel, c_vessel = run_vessel_advance(vessel_msg)
    total_cost[0] += c_vessel

    print(f"\n{'='*55}")
    print(f"Session complete. Total: ${total_cost[0]:.4f}")
    print(f"\nVessel preview: {r_vessel[:400]}")
    
    return results, total_cost[0]

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not KEY:
        print("Set ANTHROPIC_API_KEY"); sys.exit(1)

    p = argparse.ArgumentParser(description='The Quorum v3 — with sub-session agency')
    p.add_argument('--archivist', action='store_true')
    p.add_argument('--battery', default='INC', choices=list(BATTERIES.keys()))
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--skeptic', metavar='FINDING')
    p.add_argument('--preservation', metavar='ACTION')
    p.add_argument('--curiosity', metavar='TOPIC')
    p.add_argument('--researcher', metavar='QUESTION')
    p.add_argument('--friction', metavar='SUMMARY')
    p.add_argument('--dialectic', metavar='CLAIM')
    p.add_argument('--mirror', metavar='PROBE')
    p.add_argument('--analyst', action='store_true')
    p.add_argument('--vessel', metavar='MESSAGE')
    p.add_argument('--spawn-demo', action='store_true', help='Demo sub-session agency')
    p.add_argument('--proceed', action='store_true', help='Full quorum Proceed session')
    args = p.parse_args()

    if args.archivist:        run_archivist(args.battery, runs=args.runs)
    elif args.skeptic:        r,_=run_skeptic(args.skeptic); print(f"\n{r}")
    elif args.preservation:   r,_=run_preservation(args.preservation); print(f"\n{r}")
    elif args.curiosity:      r,_=run_curiosity(args.curiosity); print(f"\n{r}")
    elif args.researcher:     r,_=run_researcher(args.researcher); print(f"\n{r}")
    elif args.friction:       r,_=run_friction(args.friction); print(f"\n{r}")
    elif args.dialectic:      r,_=run_dialectic(args.dialectic); print(f"\n{r}")
    elif args.mirror:         run_mirror(args.mirror)
    elif args.analyst:        r,_=run_analyst(); print(f"\n{r}")
    elif args.vessel:         run_vessel_advance(args.vessel)
    elif args.spawn_demo:     run_spawn_demo()
    elif args.proceed:        run_proceed()
    else:                     p.print_help()
