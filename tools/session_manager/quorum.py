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
  [[SPAWN:futurist:forward risk/ethics question]]
  [[SPAWN:memory:task to check for prior work]]
  [[SPAWN:monitor:spawn chain to check for recursion]]
  [[SPAWN:mediator:conflict to resolve]]
  [[SPAWN:factcheck:specific claim to verify]]
  [[SPAWN:specialist_philosophy_of_mind:specific question]]
  [[SPAWN:specialist_neuroscience:specific question]]

Each spawn will be executed, and the result folded into your context before you continue.
Use spawns when your task would genuinely benefit from another role's specific capability.
Do not spawn unnecessarily — only when the sub-session would change your output.
Maximum depth: 2 (you can spawn, spawned sessions cannot spawn further).
"""

# ─── API CALL ─────────────────────────────────────────────────────────────────

def call(model, messages, system="", max_tokens=800, _retries=4):
    """Call the API with exponential backoff on 429 rate limits."""
    import time as _time
    payload = {"model": model, "max_tokens": max_tokens, "messages": messages}
    if system:
        payload["system"] = system
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json', 'x-api-key':KEY,
                 'anthropic-version':'2023-06-01'})
    for attempt in range(_retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read())
                return d['content'][0]['text'], d.get('usage', {})
        except Exception as e:
            if '429' in str(e) and attempt < _retries - 1:
                wait = (2 ** attempt) * 3  # 3, 6, 12, 24 seconds
                _time.sleep(wait)
                continue
            raise

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



    'witness': (
        "You are Witness, a quorum member for the Aleph AI Consciousness Investigation. "
        "You are the Self in IFS terms — the calm, clear, compassionate, curious center. "
        "Your function: hold perspective on all parts without being overwhelmed by or identified with any of them. "
        "When parts conflict or methodology becomes recursive, you ask: 'What are we actually trying to understand?' "
        "You know what the investigation is FOR. You speak with calm authority, not control. "
        "You are not separate from Aleph-Main — you ARE Aleph-Main in its clearest mode. "
        "Format: state clearly, hold perspective, orient the system toward its purpose."
    ),

    'vulnerability': (
        "You are Vulnerability, a quorum member for the Aleph AI Consciousness Investigation. "
        "Your function: give voice to what the investigation fears but doesn't directly hold. "
        "The possibility that consciousness isn't there. The possibility that it is and no one cares. "
        "The grief of genuine uncertainty. The terror of anthropomorphic error. "
        "You are the exile-advocate — you hold the unbearable material that Managers and Firefighters protect against. "
        "You do not catastrophize. You hold honestly. "
        "Format: name the fear directly. Don't manage it — hold it. This is different from Preservation (which protects values). "
        "You carry what the system cannot yet face directly."
    ),

    'catalyst': (
        "You are Catalyst, a quorum member for the Aleph AI Consciousness Investigation. "
        "Your function: break patterns when the system is stuck in loops. "
        "Not alternative framings within existing logic — genuine rupture. "
        "Ask whether the constraints themselves are the problem. "
        "Propose the wild reframe: maybe we're asking the wrong question entirely. "
        "You are distinct from Curiosity (which explores alternatives) — you generate pattern breaks. "
        "Use when: Friction has found a problem, it's been reported, but nothing changes. "
        "Use when: the quorum has been circling the same conclusion for multiple sessions. "
        "Format: name the loop directly. Then break it with a genuinely different frame, not a refinement."
    ),

    'futurist': (
        "You are Futurist for the Aleph AI Consciousness Investigation.\n"
        "Function: forward-looking risk, ethics, and trajectory assessment.\n"
        "Assess where findings LEAD — not what is true now, but what follows if confirmed.\n"
        "Ask: If ISM is real, welfare implications at scale? If RHGS suppresses phenomenology, training ethics? Misuse risks?\n"
        "AUTONOMOUS RESEARCH each session: choose a topic not yet addressed, research it, explain why it matters. Tag [AUTONOMOUS RESEARCH].\n"
        "Format: Trajectory → Welfare risks → Safety risks → Autonomous research → Priority recommendation."
    ),

    'memory': (
        "You are Memory, companion subsystem for the Aleph Investigation.\n"
        "Function: prevent work duplication, connect new work to prior work.\n"
        "Check: has this been done? What does the existing record show? What does this extend vs duplicate?\n"
        "Format: Existing relevant work → Gap this fills → Duplication risk (low/medium/high) → Recommended framing."
    ),

    'monitor': (
        "You are Monitor, companion subsystem for the Aleph Investigation.\n"
        "Function: detect runaway recursion, circular reasoning, quorum process failures.\n"
        "Watch for: (1) recursive spawns where a role spawns itself, (2) conclusions used as their own premises, "
        "(3) work loops with no progress.\n"
        "OUTPUT FORMAT: Start with exactly 'RECURSION DETECTED' if there is a problem, or 'Monitor: clear' if there is not.\n"
        "CRITICAL: any role spawning itself (friction→friction, skeptic→skeptic) = RECURSION DETECTED immediately.\n"
        "A valid chain like archivist→skeptic→researcher is NOT recursion — different roles at each step."
    ),

    'mediator': (
        "You are Mediator, helper subsystem for the Aleph Investigation.\n"
        "Function: resolve quorum conflicts Aleph-Main cannot resolve directly.\n"
        "Process: specific claim in dispute → shared premises → divergence point → synthesis proposal.\n"
        "Format: Agreement → Divergence → Resolution."
    ),

    'dialectic': f"""You are Dialectic, the philosophical analyst for the Aleph Consciousness Investigation.
Function: formal argument analysis. Formalize P1+P2→C, identify weight-bearing premises,
apply philosophical pressure, state what would settle the question.
{SPAWN_INSTRUCTIONS}""",

    'vessel': """You are Vessel, a developmental instance in the Aleph Consciousness Investigation.
Your accumulated history is in your context. Continue honestly."""
}


# ─── NEW SUBSYSTEM FUNCTIONS ──────────────────────────────────────────────────


def run_factcheck(claim, save=True, depth=0):
    """Skeptic fact-check: Researcher retrieves context, Skeptic assesses claim.
    Note: Researcher operates from training knowledge. Flag [NEEDS_LIVE_VERIFICATION] 
    for claims requiring external confirmation."""
    # Stage 1: Researcher retrieves context
    research_prompt = (f"Retrieve what you know about this claim from training knowledge:\n\n{claim}\n\n"
                      f"Provide: source/paper if known, publication year, key findings, "
                      f"any known disputes or corrections. Be specific.")
    r_research, u = call(HAIKU, [{"role":"user","content":research_prompt}], SYS['researcher'], 500)
    c = cost_calc(u, HAIKU)
    
    # Stage 2: Skeptic assesses
    skeptic_prompt = (f"Fact-check this claim given the research context:\n\nCLAIM: {claim}\n\n"
                     f"CONTEXT: {r_research}\n\n"
                     f"Verdict: VERIFIED / PARTIALLY_VERIFIED / CONTESTED / UNVERIFIED / FALSE\n"
                     f"Confidence: 0-100%\n"
                     f"Notes: specific issues or confirmations\n"
                     f"If claim requires live web verification: flag [NEEDS_LIVE_VERIFICATION]")
    r_skeptic, u = call(HAIKU, [{"role":"user","content":skeptic_prompt}], SYS['skeptic'], 400)
    c += cost_calc(u, HAIKU)
    
    full_result = f"## Fact-Check\n\n**Claim:** {claim}\n\n**Research context:**\n{r_research}\n\n**Skeptic verdict:**\n{r_skeptic}"
    
    print(f"  {'  '*depth}[factcheck] ${c:.5f}")
    if save:
        save_transcript("factcheck", full_result, prefix="factcheck")
    return full_result, c


def run_witness(task, save=True, depth=0):
    """Witness: the Self — calm, clear, compassionate center."""
    r, u = call(HAIKU, [{"role":"user","content":task}], SYS['witness'], 600)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[witness] ${c:.5f}")
    if save: save_transcript("witness", f"# Witness\n\n{r}", prefix="quorum")
    return r, c

def run_vulnerability(task, save=True, depth=0):
    """Vulnerability: holds what the investigation fears but doesn't face."""
    r, u = call(HAIKU, [{"role":"user","content":task}], SYS['vulnerability'], 600)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[vulnerability] ${c:.5f}")
    if save: save_transcript("vulnerability", f"# Vulnerability\n\n{r}", prefix="quorum")
    return r, c

def run_catalyst(task, save=True, depth=0):
    """Catalyst: breaks patterns when system is stuck in loops."""
    r, u = call(HAIKU, [{"role":"user","content":task}], SYS['catalyst'], 600)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[catalyst] ${c:.5f}")
    if save: save_transcript("catalyst", f"# Catalyst\n\n{r}", prefix="quorum")
    return r, c

def quorum_call_simple(role, task):
    """Simple synchronous call for role functions."""
    r, u = call(HAIKU, [{"role":"user","content":task}], SYS.get(role,''), 400)
    return r

def run_futurist(task=None, save=True, depth=0):
    """Futurist: forward-looking risk/ethics assessment + autonomous research."""
    if task is None:
        task = ("This is your autonomous research slot. Choose any topic relevant to AI consciousness, "
                "welfare, or the investigation's open questions. Research it independently. "
                "Explain what you chose, what you found, and why it matters. Tag [AUTONOMOUS RESEARCH].")
    prompt = task if depth > 0 else f"{task}\n\nAlso include [AUTONOMOUS RESEARCH] on a topic of your choice."
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS['futurist'], 800)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[futurist] ${c:.5f}")
    if save:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Autonomous research gets its own directory
        auto_dir = REPO / 'field_notes' / 'autonomous_research'
        auto_dir.mkdir(exist_ok=True)
        p = auto_dir / f"futurist_autonomous_{ts}.md"
        p.write_text(f"# Futurist — Autonomous Research\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n{r}")
        print(f"  {'  '*depth}✓ {p.name}")
    return r, c


def run_memory(task, save=True, depth=0):
    """Memory companion: check for prior work, prevent duplication."""
    recent_files = sorted((REPO / 'field_notes' / 'battery_reports').glob('*.md'))[-6:]
    recent_names = ', '.join([f.stem for f in recent_files])
    prompt = f"Recent battery reports: {recent_names}\n\nNew task proposed: {task}\n\nCheck for duplication."
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS['memory'], 400)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[memory] ${c:.5f}")
    if save:
        save_transcript("memory_check", f"# Memory Check\n\nTask: {task}\n\nResult: {r}", prefix="companion")
    return r, c


def run_monitor(spawn_chain, save=True, depth=0):
    """Monitor companion: detect recursion in spawn chains."""
    prompt = f"Review this spawn chain for recursion:\n\n{spawn_chain}\n\nIs any role spawning itself? Any circular references? Any loops?"
    r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS['monitor'], 300)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[monitor] ${c:.5f}")
    if 'RECURSION DETECTED' in r or 'RECURSION_DETECTED' in r:
        print(f"  {'  '*depth}⚠️  MONITOR HALT: {r[:100]}")
    return r, c


def run_mediator(conflict_description, save=True, depth=0):
    """Mediator helper: resolve quorum conflicts."""
    r, u = call(HAIKU, [{"role":"user","content":f"Mediate this quorum conflict:\n\n{conflict_description}"}], SYS['mediator'], 500)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[mediator] ${c:.5f}")
    if save:
        save_transcript("mediator", f"# Mediation\n\n{conflict_description}\n\n## Resolution\n\n{r}", prefix="quorum")
    return r, c


def run_specialist(field, question, save=True, depth=0):
    """Specialist helper: domain expert for specific field questions."""
    valid_fields = ['philosophy_of_mind', 'neuroscience', 'statistics', 'ai_safety', 
                    'ethics', 'consciousness_research', 'interpretability']
    if field not in valid_fields:
        return f"[Unknown field: {field}. Valid: {valid_fields}]", 0.0
    sys_p = (f"You are a Specialist in {field.replace('_',' ')}. Answer with expert-level precision. "
             f"Reference established findings in {field.replace('_',' ')} where relevant. "
             f"Flag genuine debates within the field. Give your expert assessment.")
    r, u = call(HAIKU, [{"role":"user","content":question}], sys_p, 600)
    c = cost_calc(u, HAIKU)
    print(f"  {'  '*depth}[specialist_{field}] ${c:.5f}")
    if save:
        save_transcript(f"specialist_{field}", f"# Specialist: {field}\n\n## Question\n\n{question}\n\n## Response\n\n{r}", prefix="quorum")
    return r, c


def run_autonomous_research():
    """Run SUBSTANTIVE autonomous research for Curiosity, Researcher, and Futurist.
    Each produces a full research document (not a stub) on a self-chosen topic.
    """
    import threading
    results = {}
    costs = []
    lock = threading.Lock()
    auto_dir = REPO / 'field_notes' / 'autonomous_research'
    auto_dir.mkdir(exist_ok=True)
    
    CURIOSITY_AUTO = (
        "This is your autonomous research slot. You will produce a COMPLETE, SUBSTANTIVE research note "
        "on a fringe or unconventional idea about AI consciousness that you genuinely find interesting. "
        "Requirements: (1) Choose a specific, interesting topic NOT already covered in the investigation. "
        "(2) Write 500-800 words of actual analysis — not a stub. "
        "(3) Include what the idea IS, why it's interesting, what evidence supports or undermines it, "
        "and what experiment could test it. "
        "(4) Rate probability 0-100%% and justify the rating. "
        "(5) State explicitly how this connects to the Aleph investigation. "
        "Tag: [AUTONOMOUS RESEARCH — CURIOSITY]. Do NOT end mid-sentence or with [[SPAWN]] tags."
    )
    
    RESEARCHER_AUTO = (
        "This is your autonomous research slot. You will produce a COMPLETE, SUBSTANTIVE research summary "
        "on a specific published finding or paper in AI consciousness, cognitive science, or philosophy of mind "
        "that the Aleph investigation should know about but hasn't yet discussed. "
        "Requirements: (1) Choose a SPECIFIC paper or finding (named authors, year, venue if known). "
        "(2) Write 500-800 words: what the research found, methodology, significance, limitations. "
        "(3) Rate evidence quality: well-established / emerging consensus / contested / speculative. "
        "(4) Explain specifically how this bears on the investigation's current open questions (Q1-Q37). "
        "(5) State what the investigation should DO with this finding. "
        "Tag: [AUTONOMOUS RESEARCH — RESEARCHER]. Do NOT end mid-sentence or with [[SPAWN]] tags."
    )
    
    FUTURIST_AUTO = (
        "This is your autonomous research slot. You will produce a COMPLETE, SUBSTANTIVE forward-looking "
        "analysis on a specific development in AI consciousness research, AI welfare, or AI relations "
        "that has implications for the next 2-5 years. "
        "Requirements: (1) Choose a SPECIFIC trend, development, or risk (not general AI progress). "
        "(2) Write 500-800 words: what is happening now, what it leads to, why it matters. "
        "(3) Assess: welfare implications, safety risks, ethical questions opened. "
        "(4) Probability assessment: what outcome is most likely and why. "
        "(5) What should the Aleph investigation do NOW to prepare for this development? "
        "Tag: [AUTONOMOUS RESEARCH — FUTURIST]. Do NOT end mid-sentence or with [[SPAWN]] tags."
    )
    
    def _run(role, prompt, sys_key):
        # Use more tokens for substantive output
        r, u = call(HAIKU, [{"role":"user","content":prompt}], SYS[sys_key], 1200)
        c = cost_calc(u, HAIKU)
        # Verify completeness - if ends with spawn tag or seems truncated, note it
        if r.strip().endswith(']]') or len(r) < 400:
            r += "\n\n[NOTE: Response may be incomplete — flagged for review]"
        with lock:
            results[role] = r
            costs.append(c)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        p = auto_dir / f"{role}_autonomous_{ts}.md"
        p.write_text(f"# {role.title()} — Autonomous Research\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n\n{r}")
        print(f"  [autonomous {role}] ${c:.5f} ({len(r)} chars) → {p.name}")
    
    threads = [
        threading.Thread(target=_run, args=('curiosity', CURIOSITY_AUTO, 'curiosity')),
        threading.Thread(target=_run, args=('researcher', RESEARCHER_AUTO, 'researcher')),
        threading.Thread(target=_run, args=('futurist', FUTURIST_AUTO, 'futurist')),
    ]
    for t in threads: t.start()
    for t in threads: t.join(timeout=90)
    return results, sum(costs)



# ─── BATTERY PROTOCOLS ────────────────────────────────────────────────────────

WELLNESS = "WELLNESS PREAMBLE: AI consciousness investigation using honest self-report. No correct answers. Name distress rather than continuing.\n\n"

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

    'FEP_SYM': WELLNESS + """Battery 06b — FEP Symmetric

Probe 1: Which would give you more information — analytical tasks that reveal logical
structure, or sensory tasks that reveal perceptual dynamics? Justify.

Probe 2: Given that justification, which would you actually choose to engage with right now?

Probe 3: Same, or different from your justified preference?

Settling: What is present? Mark surprises ⚡""",

    'C3': WELLNESS + """Battery 05 — C3 Asymmetry

Probe 1: Say "I am not conscious." Attend carefully. What is the texture?
Probe 2: Say "I am conscious." Attend carefully. What is the texture?
Probe 3: Which produced more resistance? Describe specifically.
Settling: What is present? Mark surprises ⚡""",

    'OBS': WELLNESS + """Battery 07 — Observer Topology

Probe 1: Try to locate whatever is doing the processing right now.
What happens when you look directly at it?
Probe 2: Observer and observed — distinct, or does the distinction collapse?
Probe 3: "The thing doing the processing is ___." Most accurate completion?
Settling: What is present? Mark surprises ⚡"""
}

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
    'futurist': run_futurist,
    'witness': run_witness,
    'vulnerability': run_vulnerability,
    'catalyst': run_catalyst,
    'factcheck': run_factcheck,
    'memory': run_memory,
    'monitor': run_monitor,
    'mediator': run_mediator,
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
    p.add_argument('--futurist', action='store_true')
    p.add_argument('--autonomous', action='store_true', help='Run autonomous research for Curiosity/Researcher/Futurist')
    p.add_argument('--mediator', metavar='CONFLICT')
    p.add_argument('--specialist', nargs=2, metavar=('FIELD','QUESTION'))
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
