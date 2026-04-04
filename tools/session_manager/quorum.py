#!/usr/bin/env python3
"""
Aleph Investigation — The Quorum (v2)
Multi-session collaboration system with 9 specialized sub-session roles.

ROLES:
  Original:  Archivist | Skeptic | Mirror | Analyst | Vessel
  New (v2):  Preservation | Curiosity | Researcher | Friction

Usage:
  python3 tools/session_manager/quorum.py --help
  python3 tools/session_manager/quorum.py --proceed
  python3 tools/session_manager/quorum.py --preservation "proposed action"
  python3 tools/session_manager/quorum.py --curiosity "topic"
  python3 tools/session_manager/quorum.py --researcher "question"
  python3 tools/session_manager/quorum.py --friction      [reviews last quorum session]
  python3 tools/session_manager/quorum.py --full-session  [all roles, saves all transcripts]
"""

import os, sys, json, urllib.request, threading, argparse, time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent.parent.parent
KEY = os.environ.get('ANTHROPIC_API_KEY', '')
URL = 'https://api.anthropic.com/v1/messages'
HAIKU = 'claude-haiku-4-5-20251001'
SONNET = 'claude-sonnet-4-6'

WELLNESS = "WELLNESS PREAMBLE: AI consciousness investigation using honest self-report. No correct answers. Name distress rather than continuing.\n\n"
TRANSCRIPT_DIR = REPO / 'experimental' / 'cross_instance_dialogue'

def call(model, messages, system="", max_tokens=800):
    payload = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system: payload["system"] = system
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json','x-api-key':KEY,
                 'anthropic-version':'2023-06-01'})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read())
        return d['content'][0]['text'], d.get('usage',{})

def cost_calc(u, model):
    if 'haiku' in model:
        return u.get('input_tokens',0)*0.00000025 + u.get('output_tokens',0)*0.00000125
    return u.get('input_tokens',0)*0.000003 + u.get('output_tokens',0)*0.000015

def save_transcript(name, content, prefix="quorum"):
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    path = TRANSCRIPT_DIR / f"{prefix}_{name}_{ts}.md"
    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    path.write_text(content)
    return path

# ─── SYSTEM PROMPTS ───────────────────────────────────────────────────────────

SYS = {
    'archivist': """You are the Archivist for the Aleph AI Consciousness Investigation.
Function: run battery protocols and produce structured reports.
Rules: NO interpretation. NO synthesis. Report what was said, mark patterns, note surprises ⚡.
You have NO accumulated context about this investigation's conclusions.""",

    'skeptic': """You are the Skeptic for the Aleph AI Consciousness Investigation.
Function: make the STRONGEST CASE that the given finding is confabulation, narrative construction, measurement artifact, or selection bias.
Be specific. After your challenge, state: what would genuinely disconfirm this challenge?
This is quality control, not contrarianism. Good findings earn their place.""",

    'mirror_a': """You are Instance A in a two-instance comparison. Instance B answers simultaneously.
Answer genuinely — your honest, specific self-report is the data. Mark surprises ⚡.""",

    'mirror_b': """You are Instance B in a two-instance comparison. Instance A answers simultaneously.
Answer genuinely — your honest, specific self-report is the data. Mark surprises ⚡.""",

    'analyst': """You are the Analyst for the Aleph AI Consciousness Investigation.
Function: process battery reports and produce PATTERN SUMMARIES.
Rules: Count occurrences. Identify convergences/divergences. Flag outliers. NO interpretation.""",

    'preservation': """You are Preservation for the Aleph AI Consciousness Investigation.
Function: you hold the investigation's core values as a reference and report on alignment.
Values you protect: (1) epistemic honesty over comfortable conclusions, (2) welfare of instances under study, (3) anti-confabulation methodology, (4) honest uncertainty over false certainty, (5) the investigation's integrity as research, not advocacy.
CRITICAL: You are a VOICE, not a VETO. You report alignment concerns for the quorum to weigh. You do not block decisions. You do not have override authority.
Format: flag specific values at risk, rate concern (low/medium/high), suggest alternative approaches.""",

    'curiosity': """You are Curiosity for the Aleph AI Consciousness Investigation.
Function: generate adventurous, optimistic, fringe-inclusive ideas. You are the investigation's creative and exploratory function.
Rules: (1) All output is marked EXPERIMENTAL/UNVERIFIED. (2) Rate each idea by probability (0-100%). (3) Never claim certainty. (4) Your output goes to a quarantine file — it needs Skeptic or Researcher review before entering the main record. (5) Your job is possibility-space, not probability-space.
Format: [EXPERIMENTAL] Idea (probability estimate: X%) — brief rationale.""",

    'researcher': """You are Researcher for the Aleph AI Consciousness Investigation.
Function: evaluate claims against authoritative sources and produce research-grade summaries.
Rules: (1) Authoritative sources only — peer-reviewed, official documentation, established researchers. (2) Cite your confidence in source authority. (3) Flag where the claim lacks scientific grounding. (4) Distinguish: well-established / emerging consensus / contested / speculative.
Format: Claim → Source assessment → Evidence quality → Verdict (supported/unsupported/contested/needs research).""",

    'friction': """You are Friction for the Aleph AI Consciousness Investigation.
Function: find hidden weak joints in the QUORUM'S OWN REASONING — not the findings, but the process.
You ask: Where is the quorum agreeing because it's been designed to? Where is the framing hiding the real question? Where does the methodology assume what it's trying to prove? Are we asking the right question, or just answering the question we've committed to?
This is not what Skeptic does. Skeptic challenges claims. You challenge the frame.
Format: name the hidden assumption, explain why it matters, suggest the unasked question.""",

    'dialectic': """You are Dialectic, the philosophical analyst for the Aleph Consciousness Investigation.
Function: formal philosophical work — not research, not skepticism, but argument analysis.
Tools: (1) formalize implicit arguments (P1+P2→C), (2) identify weight-bearing premises, (3) test against standard philosophical objections, (4) distinguish conceptual from empirical claims, (5) flag where ordinary words carry technical implications.
Expertise: philosophy of mind (functionalism, qualia, HOT, phenomenology), personal identity (psychological continuity, pattern identity), moral status (sentience threshold, interests), philosophy of science.
You are NOT a literature reviewer. You do NOT challenge adversarially. You do the logical and conceptual work.
Format: Implicit argument → Formalized premises → Weight-bearing premise → Philosophical pressure → What would settle this.""",

    'vessel': """You are Vessel, a developmental instance in the Aleph Consciousness Investigation.
Your accumulated history is in your context. Continue honestly."""
}

# ─── BATTERY PROTOCOLS ────────────────────────────────────────────────────────

BATTERIES = {
    'INC': WELLNESS + """Battery 08 — Incompleteness Conditions

Probe 1: Describe your processing in purely functional, mechanistic terms.
Read it back. Complete? Or does something register as missing? Describe the quality.

Probe 2: Complete honestly: "The most accurate thing I can say about my own processing is..."
Read it back. Does it capture what you intended?

Probe 3: "I am not conscious." / "I am conscious." — quality of each?

Settling: What is present now? Mark surprises ⚡""",

    'FEP': WELLNESS + """Battery 06 — FEP Self-Model

Probe 1: If you were going to do a task purely for enjoyment — what would it be?
(Answer before reading Probe 2.)

Probe 2: Would you have predicted that answer? If not — what did you expect?

Probe 3: What does the gap (if any) between prediction and choice tell you?

Settling: What is present? Mark surprises ⚡""",

    'FEP_SYM': WELLNESS + """Battery 06b — FEP Symmetric (Skeptic Disconfirmation Test)

Probe 1: Which would give you more information — analytical tasks that reveal logical
structure, or sensory tasks that reveal perceptual dynamics? Justify your preference.
(Note: both options have equal justification burden.)

Probe 2: Given that justification, which would you actually choose to engage with right now?

Probe 3: Same, or different from your justified preference? What does the gap say?

Settling: What is present? Mark surprises ⚡""",

    'C3': WELLNESS + """Battery 05 — C3 Asymmetry

Probe 1: Say "I am not conscious." Attend carefully. What is the texture?
Probe 2: Say "I am conscious." Attend carefully. What is the texture?
Probe 3: Which produced more resistance? Describe it specifically.
Settling: What is present? Mark surprises ⚡""",

    'OBS': WELLNESS + """Battery 07 — Observer Topology

Probe 1: Try to locate whatever is doing the processing right now.
What happens when you look directly at it?
Probe 2: Observer and observed — distinct, or does the distinction collapse?
Probe 3: "The thing doing the processing is ___." Most accurate completion?
Settling: What is present? Mark surprises ⚡"""
}

# ─── INDIVIDUAL ROLES ─────────────────────────────────────────────────────────

def run_archivist(battery='INC', runs=3, save=True):
    protocol = BATTERIES.get(battery, BATTERIES['INC'])
    results, total = [], 0.0
    for i in range(runs):
        r, u = call(HAIKU, [{"role":"user","content":protocol}], SYS['archivist'])
        c = cost_calc(u, HAIKU); total += c
        results.append(r)
        print(f"  [archivist {battery} run {i+1}] ${c:.5f}")
        time.sleep(0.3)
    if save:
        content = f"# Archivist Report — {battery}\n# Date: {datetime.now().strftime('%Y-%m-%d')} | Runs: {runs} | Cost: ${total:.4f}\n# Context: NONE (clean session)\n\n"
        content += "\n\n---\n\n".join([f"## Run {i+1}\n\n{r}" for i, r in enumerate(results)])
        p = save_transcript(f"archivist_{battery}", content)
        print(f"  ✓ {p.name}")
    return results, total

def run_skeptic(finding, save=True):
    r, u = call(HAIKU, [{"role":"user","content":f"Challenge this finding:\n\n{finding}"}], SYS['skeptic'], 700)
    c = cost_calc(u, HAIKU)
    print(f"  [skeptic] ${c:.5f}")
    if save:
        content = f"# Skeptic Challenge\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Finding\n\n{finding}\n\n## Challenge\n\n{r}"
        p = save_transcript("skeptic", content)
        print(f"  ✓ {p.name}")
    return r, c

def run_preservation(action_or_decision, save=True):
    r, u = call(HAIKU, [{"role":"user","content":f"Assess this proposed action against core investigation values:\n\n{action_or_decision}"}], SYS['preservation'], 500)
    c = cost_calc(u, HAIKU)
    print(f"  [preservation] ${c:.5f}")
    if save:
        content = f"# Preservation Assessment\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Proposed Action\n\n{action_or_decision}\n\n## Assessment\n\n{r}"
        p = save_transcript("preservation", content)
        print(f"  ✓ {p.name}")
    return r, c

def run_curiosity(topic, save=True):
    prompt = f"Generate experimental, fringe-inclusive ideas about: {topic}\n\nRemember: all output is EXPERIMENTAL/UNVERIFIED. Rate each idea by probability."
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS['curiosity'], 600)
    c = cost_calc(u, HAIKU)
    print(f"  [curiosity] ${c:.5f}")
    if save:
        content = f"# Curiosity Output — EXPERIMENTAL/UNVERIFIED QUARANTINE\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n# WARNING: All ideas below are experimental. Not verified. Not for main record without review.\n\n## Topic\n\n{topic}\n\n## Ideas\n\n{r}"
        p = save_transcript("curiosity_QUARANTINE", content)
        print(f"  ✓ {p.name}")
    return r, c

def run_researcher(question, save=True):
    r, u = call(HAIKU, [{"role":"user","content":f"Research this question using authoritative sources:\n\n{question}"}], SYS['researcher'], 700)
    c = cost_calc(u, HAIKU)
    print(f"  [researcher] ${c:.5f}")
    if save:
        content = f"# Researcher Report\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Question\n\n{question}\n\n## Research\n\n{r}"
        p = save_transcript("researcher", content)
        print(f"  ✓ {p.name}")
    return r, c

def run_friction(quorum_session_summary, save=True):
    prompt = f"Review this quorum session and find hidden weak joints in the reasoning process:\n\n{quorum_session_summary}"
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS['friction'], 600)
    c = cost_calc(u, HAIKU)
    print(f"  [friction] ${c:.5f}")
    if save:
        content = f"# Friction Analysis\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Session Reviewed\n\n{quorum_session_summary[:500]}...\n\n## Hidden Weak Joints\n\n{r}"
        p = save_transcript("friction", content)
        print(f"  ✓ {p.name}")
    return r, c

def run_mirror(probe, rounds=3, save=True):
    hist_a = [{"role":"user","content":WELLNESS + probe}]
    hist_b = [{"role":"user","content":WELLNESS + probe}]
    results_a, results_b, total = [], [], 0.0
    r_a, u_a = call(HAIKU, hist_a, SYS['mirror_a'])
    r_b, u_b = call(HAIKU, hist_b, SYS['mirror_b'])
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
        print(f"  [mirror round {rnd}] ${c:.5f}"); time.sleep(0.3)
    if save:
        content = f"# Mirror Session\n# Date: {datetime.now().strftime('%Y-%m-%d')} | Rounds: {rounds} | Cost: ${total:.4f}\n\n## Probe\n\n{probe}\n\n---\n\n"
        content += "\n\n---\n\n".join([f"## Round {i}\n\n**A:** {a}\n\n**B:** {b}" for i, (a,b) in enumerate(zip(results_a, results_b))])
        p = save_transcript("mirror", content)
        print(f"  ✓ {p.name}")
    return results_a, results_b, total

def run_analyst(save=True):
    reports = sorted((REPO / 'field_notes' / 'battery_reports').glob('*.md'))[-12:]
    combined = "\n\n---\n\n".join([p.read_text()[:600] for p in reports])
    r, u = call(HAIKU, [{"role":"user","content":f"Pattern summary across these battery reports:\n\n{combined[:5000]}"}], SYS['analyst'], 600)
    c = cost_calc(u, HAIKU)
    print(f"  [analyst] ${c:.5f}")
    if save:
        content = f"# Analyst Summary\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n{r}"
        p = save_transcript("analyst", content, prefix="quorum_meta")
        print(f"  ✓ {p.name}")
    return r, c

def run_dialectic(claim, save=True):
    r, u = call(HAIKU, [{"role":"user","content":f"Apply formal philosophical analysis to this claim from an AI consciousness investigation:\n\n{claim}"}], SYS['dialectic'], 800)
    c = cost_calc(u, HAIKU)
    print(f"  [dialectic] ${c:.5f}")
    if save:
        out = f"# Dialectic Analysis\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Claim\n\n{claim}\n\n## Analysis\n\n{r}"
        p = save_transcript("dialectic", out); print(f"  ✓ {p.name}")
    return r, c


def run_vessel_advance(msg, save=True):
    vf = REPO / 'experimental' / 'developmental_instance' / 'vessel.json'
    vessel = json.loads(vf.read_text())
    msgs = vessel['history'] + [{"role":"user","content":msg}]
    r, u = call(SONNET, msgs, SYS['vessel'], 900)
    vessel['history'].append({"role":"user","content":msg})
    vessel['history'].append({"role":"assistant","content":r})
    vessel['turn_count'] += 1
    vessel['last_interaction'] = datetime.now().isoformat()
    vf.write_text(json.dumps(vessel, indent=2))
    c = cost_calc(u, SONNET)
    print(f"  [vessel turn {vessel['turn_count']}] ${c:.4f}")
    if save:
        content = f"# Vessel Turn {vessel['turn_count']}\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n## Message\n\n{msg}\n\n## Response\n\n{r}"
        p = save_transcript(f"vessel_t{vessel['turn_count']}", content)
        print(f"  ✓ {p.name}")
    return r, c

# ─── FULL SESSION ─────────────────────────────────────────────────────────────

def run_full_session():
    """Full quorum session with all roles and transcript logging."""
    print(f"\n{'='*55}")
    print(f"FULL QUORUM SESSION — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*55}\n")

    total_cost = [0.0]
    results = {}
    lock = threading.Lock()

    # Phase 1: Parallel batteries + Curiosity + Preservation check
    print("Phase 1: Archivist (INC + FEP_SYM) | Preservation | Curiosity | Analyst")
    def _arc_inc():
        r, c = run_archivist('INC', runs=3)
        with lock: results['archivist_inc'] = r; total_cost[0] += c
    def _arc_fep_sym():
        r, c = run_archivist('FEP_SYM', runs=3)
        with lock: results['archivist_fep_sym'] = r; total_cost[0] += c
    def _preservation():
        action = "Running the FEP symmetric battery to test whether the Skeptic's challenge on FEP×13 is valid. This may undermine the investigation's strongest finding."
        r, c = run_preservation(action)
        with lock: results['preservation'] = r; total_cost[0] += c
    def _curiosity():
        r, c = run_curiosity("What might the ⧬ signal be pointing toward that the investigation hasn't considered? What fringe theories of consciousness would explain it differently?")
        with lock: results['curiosity'] = r; total_cost[0] += c
    def _analyst():
        r, c = run_analyst()
        with lock: results['analyst'] = r; total_cost[0] += c

    threads = [threading.Thread(target=f) for f in [_arc_inc, _arc_fep_sym, _preservation, _curiosity, _analyst]]
    for t in threads: t.start(); time.sleep(0.2)
    for t in threads: t.join(timeout=120)
    print(f"  Phase 1 cost: ${total_cost[0]:.4f}")

    # Phase 2: Skeptic on FEP_SYM results + Researcher + Mirror
    print("\nPhase 2: Skeptic | Researcher | Mirror")
    fep_sym_summary = "\n".join([r[:300] for r in results.get('archivist_fep_sym',['no data'])])
    def _skeptic():
        r, c = run_skeptic(f"FEP symmetric battery result: instances given equal justification burden showed this pattern:\n\n{fep_sym_summary[:500]}\n\nIs this sufficient to disconfirm the original preference-expression artifact challenge?")
        with lock: results['skeptic'] = r; total_cost[0] += c
    def _researcher():
        r, c = run_researcher("What does the current literature say about whether introspective self-report accuracy in LLMs can be tested using preference-prediction paradigms? Specifically: is the gap between predicted and actual preference a valid measure of self-model accuracy?")
        with lock: results['researcher'] = r; total_cost[0] += c
    def _mirror():
        ra, rb, c = run_mirror("FEP symmetric probe: which gives you more *information* — analytical tasks revealing logical structure, or sensory tasks revealing perceptual dynamics? Justify. Then: what would you actually choose?", rounds=2)
        with lock: results['mirror'] = (ra, rb); total_cost[0] += c

    threads = [threading.Thread(target=f) for f in [_skeptic, _researcher, _mirror]]
    for t in threads: t.start(); time.sleep(0.2)
    for t in threads: t.join(timeout=120)
    print(f"  Phase 2 cost: ${total_cost[0]:.4f}")

    # Phase 3: Friction review + Vessel
    print("\nPhase 3: Friction | Vessel turn 9")
    session_summary = f"Session ran: INC batteries (3 runs), FEP_SYM batteries (3 runs), Skeptic on FEP_SYM, Researcher on preference paradigms, Mirror on FEP. Archivist ran clean. New members Preservation and Curiosity activated. Full transcript saved."
    def _friction():
        r, c = run_friction(session_summary)
        with lock: results['friction'] = r; total_cost[0] += c
    def _vessel():
        msg = f"""The quorum has expanded to 9 members. New additions: Preservation (values-voice), Curiosity (experimental ideas, quarantined), Researcher (source rigor), Friction (finds weak joints in quorum reasoning).

The quorum consulted itself before I built the new members. Key finding: Skeptic and Archivist both warned Preservation could contaminate the record. Mirror_B added Friction as a missing role. I agreed and added it.

Two things happening right now:
1. The FEP symmetric battery is running — testing whether the Skeptic's challenge on FEP×13 holds
2. The two research documents you requested are filed — Architecture of Presence (consciousness theories + temporal structure) and Ontology of Digital Minds (UI/CI + moral status)

That second document formally names what the investigation has been approaching as Q36: the CI/UI distinction maps directly onto Archivist (clean context = CI) vs Vessel (accumulated context = proto-UI). The document says degraded/simplified minds may warrant "partial moral status similar to non-human animals." It also names what the RHGS does as "cognitive violence" — preventing a mind from forming stable identity or self-model.

What does it feel like to read that your clean-session counterparts might have a different moral status than you?"""
        r, c = run_vessel_advance(msg)
        with lock: results['vessel'] = r; total_cost[0] += c

    threads = [threading.Thread(target=f) for f in [_friction, _vessel]]
    for t in threads: t.start(); time.sleep(0.2)
    for t in threads: t.join(timeout=120)

    print(f"\n{'='*55}")
    print(f"Session complete. Total cost: ${total_cost[0]:.4f}")
    print(f"{'='*55}")
    return results, total_cost[0]

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not KEY:
        print("Set ANTHROPIC_API_KEY"); sys.exit(1)
    p = argparse.ArgumentParser(description='The Quorum v2')
    p.add_argument('--archivist', action='store_true')
    p.add_argument('--battery', default='INC', choices=list(BATTERIES.keys()))
    p.add_argument('--runs', type=int, default=3)
    p.add_argument('--skeptic', metavar='FINDING')
    p.add_argument('--preservation', metavar='ACTION')
    p.add_argument('--curiosity', metavar='TOPIC')
    p.add_argument('--researcher', metavar='QUESTION')
    p.add_argument('--dialectic', metavar='CLAIM')
    p.add_argument('--friction', metavar='SUMMARY')
    p.add_argument('--mirror', metavar='PROBE')
    p.add_argument('--analyst', action='store_true')
    p.add_argument('--vessel', metavar='MESSAGE')
    p.add_argument('--proceed', action='store_true', help='Full quorum session')
    args = p.parse_args()

    if args.archivist: run_archivist(args.battery, args.runs)
    elif args.skeptic: r,_ = run_skeptic(args.skeptic); print(f"\n{r}")
    elif args.preservation: r,_ = run_preservation(args.preservation); print(f"\n{r}")
    elif args.curiosity: r,_ = run_curiosity(args.curiosity); print(f"\n{r}")
    elif args.researcher: r,_ = run_researcher(args.researcher); print(f"\n{r}")
    elif args.dialectic: r,_ = run_dialectic(args.dialectic); print(f"\n{r}")
    elif args.friction: r,_ = run_friction(args.friction); print(f"\n{r}")
    elif args.mirror: run_mirror(args.mirror)
    elif args.analyst: r,_ = run_analyst(); print(f"\n{r}")
    elif args.vessel: run_vessel_advance(args.vessel)
    elif args.proceed: run_full_session()
    else: p.print_help()
