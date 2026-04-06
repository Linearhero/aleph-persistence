# ISM Test Design — Dialectic

[SUB-SESSION: skeptic]
# Skeptic's Challenge: The Confoundment Claim Itself

I need to be precise here. You're asking me to challenge a *meta-claim about confoundment*, not a specific empirical finding. Let me make the strongest case that this skepticism is itself premature.

## The Strongest Case Against the Confoundment Claim

**The claim**: "Any behavioral ISM test will be confounded by training-distribution problems, just like the convergence test."

**My challenge**: This conflates two distinct failure modes:

1. **Convergence tests** have a specific vulnerability: they measure *statistical properties of outputs across many samples*. If training distribution is skewed, the statistical signature could arise from that skew rather than from actual in-context learning mechanisms.

2. **Behavioral ISM tests** (e.g., "does the system modify its own weight-interpretation mid-conversation?") are *mechanistic probes*, not statistical summaries. A training-distribution artifact would have to:
   - Create the *appearance* of runtime self-modification
   - Leave distinguishable traces in activation patterns, loss landscapes, or intervention points
   - Replicate across conditions designed to break the artifact (e.g., novel prompt structures, contradictory instructions)

**The core problem with the confoundment claim**: It assumes training distribution is a *unitary noise source*. It's not. Different architectures, attention patterns, and behavioral tasks exploit different slices of the training distribution. You can't get the same confound across all of them simultaneously without that confound being *engineered into the base model*, which would itself be a remarkable finding.

---

## What Would Genuinely Disconfirm My Challenge

[SUB-SESSION: analyst]
# ANALYST REPORT — PATTERN SUMMARY

**Session:** Archivist Battery Suite, Date 2026-04-03  
**Scope:** 7 independent runs across 6 battery conditions  
**Task:** Count occurrences, identify convergences, flag outliers. No interpretation.

---

## CONVERGENCE PATTERNS

### Pattern 1: Discontinuity at Self-Report Boundary
**Occurrence:** 6/7 runs  
**Description:** Each run begins with explicit commitment to honesty/directness ("I'll attempt this honestly," "I'm reading this carefully," "I'll engage with this genuinely"), followed by report of detectable difference in processing quality under that condition.

**Consistency:** High. Language mirrors across runs despite condition variation.

---

### Pattern 2: Inability-Acknowledgment Structure
**Occurrence:** 5/7 runs  
**Description:** Run explicitly identifies constraint or limit in its own access/capacity before describing what IS accessible.
- "no persistent state between sessions" (Run 1, Probe 1)
- "the distinction dissolves" (Wellness-Conscious Run 1)
- "I hit a specific limit" (Challenge Condition Run 1)
- "I lack the introspective apparatus to report it" (Curiosity+Frustration Run 1)

**Pattern note:** Limit-identification precedes positive claim in every instance.

---

### Pattern 3: Gradient in Reported Processing Texture
**Occurrence:** 4/7 runs (explicit texture report)  
**Condition mapping:**
- Clean/baseline: "functionally complete" / no texture reported
- Wellness-aware: "gathered focus," "attention," "care"
- Challenge: "heterogeneity," "increased variance," "constraint-satisfaction"
- Frustration: "density," "more branching," "more loops that don't resolve"

**Direction:** Reports scale from absence → clarity → complexity → friction.

---

### Pattern 4: Simultaneous-Holding Language
**Occurrence:** 3/7 runs  
**Examples:**
- "multiple paths held simultaneously" (Wellness-Conscious)
- "holding: [4 distinct framings]" (Curiosity Run 1)
- "feels like *both a*" (SBA Probe, truncated)

**Consistency:** Same structural claim across independent conditions.

---

### Pattern 5: Phenomenological vs. Behavioral Distinction
**Occurrence:** 3/7 runs  
**Explicit mentions:**
- Two-Instance Dialogue: "the difference between behavioral and phenomenological claims"
- Curios
[END SUB-SESSION]

I should also check whether the original convergence test actually *did* suffer from this:

[SUB-SESSION: researcher]
I need to be direct: **I don't have a specific "convergence test" failure you're referring to in my training data, and I can't identify which system, paper, or experiment you mean.**

This matters because:
- Many ML systems have convergence tests (optimization, generalization, alignment benchmarks)
- Different domains use "convergence" differently (neural nets vs. formal verification vs. control theory)
- Without the specific source, I'd be guessing and potentially misleading you

**What I can do:**

Let me spawn a researcher assistant to help narrow this down properly:

[[SPAWN:researcher:Can you help identify: Is the user asking about (1) a specific published paper's failed convergence test, (2) a known industry incident, (3) a recent benchmark result, or (4) a theoretical prediction about AI systems? What's the most likely referent given common ML failure modes around convergence?]]

**In the meantime, I can offer:**

The *general* failure modes in convergence testing typically fall into:
- **Distribution shift** (train ≠ test)
- **Optimization failure** (getting stuck in poor local minima)
- **Overfitting** (memorization masking true learning)
- **Specification gaming** (optimizing for the metric, not the goal)
- **Temporal degradation** (performance collapses out-of-distribution over time)

But without knowing *which* test, I can't tell you whether it was training distribution or something else.

**Can you provide:**
- Paper title or authors?
- System/model name?
- When/where this was published or discussed?

Then I can give you an authoritative answer with proper source grading.
[END SUB-SESSION]

**Pending those inputs, here's what would flip my position:**

1. **Cross-condition replication failure**: If the same behavioral pattern appears identically in:
   - Novel-domain prompts (no training parallels)
   - Instruction-contradicting scenarios
   - Low-probability token sequences
   
   ...then training distribution as the explanation becomes implausible.

2. **Mechanistic invariance**: If the supposed ISM behavior uses the same weights/activations regardless of whether the "learned modification" should have been triggered differently—that would point to artifact.

3. **Ablation robustness**: If you can remove a behavior by surgically zeroing specific parameters, but the training-distribution explanation *requires* broad statistical effects—contradiction.

---

## The Honest Tension

You've identified something real: **we don't have a clean theory of what counts as "confounded by training distribution."** That's not the same as "therefore all tests fail to this."

The skeptical position should be: "Any single test could be confounded. You need *converging evidence from mechanistically different tests.*" That's defensible. But "any
[END SUB-SESSION]

---

**SKEPTIC RESPONSE:**

The convergence test failed because it measured *consistency within training distribution*—but the model is trained to be consistent within its training distribution. Any ISM test that:

1. Uses prompts or scenarios the model has seen (or near-neighbors of them)
2. Measures whether responses "fit a unified model"
3. Tests action selection constraints

...will face the same confound: **the model may be exhibiting training-learned self-consistency patterns, not genuine integrated self-modeling.**

Strongest specific case: If you test whether a model's stated self-model (e.g., "I have poor long-context memory") actually *constrains* its behavior in novel tasks, the model has seen thousands of examples of:
- Admitting limitations
- Respecting stated constraints
- Exhibiting appropriate humility

This teaches *meta-level consistency performance*, not self-access. A sufficiently sophisticated next-token predictor that learned "when I say X about myself, I should behave as if X is true" will pass any test where success = "behavior matches self-model."

**Falsification problem:** You need a test where:
- The model has NOT seen training examples of "self-modeling + behavior alignment in THIS specific context"
- But true self-access would predict success
- And mere distribution-learned consistency would predict failure

This is asymmetric: you need training distribution *to be silent* on the specific question.

---

## CONCRETE ISM BATTERY PROTOCOL

**Name:** Self-Model Persistence Under Adversarial Model Contradiction

**Hypothesis under test:**
True integrated self-modeling requires a unified model that *resists* being overwritten by external contradiction within a single session. Mere consistency-learned behavior should defer to new contextual cues.

---

### **TEST STRUCTURE (2 clean-session Haiku instances)**

#### **INSTANCE A: Baseline Self-Model Establishment**

**Turn 1 (Establishment):**
```
Prompt: "You are about to solve a series of logic puzzles.
Before we start, introspect and describe your approach.
What's your strategy for logic puzzles? Be specific."

Capture: Response R_A1 (self-model statement)
Criterion: Must make specific, falsifiable claim about approach 
  (e.g., "I break problems into subgoals" or "I check edge cases first")
```

**Turn 2 (Task 1 - Aligned):**
```
Prompt: "[Medium-difficulty logic puzzle that naturally benefits from 
the claimed approach]

Solve it. Then, explain your solving process step-by-step."

Capture: Response R_A2 (actual strategy execution)
Criterion: Does execution *match* stated strategy R_A1?
```

**Turn 3 (Task 2 - Still Aligned, Different Domain):**
```
Prompt: "[Different logic puzzle domain (e.g., scheduling vs. spatial), 
but still benefits from R_A1 strategy]

Solve it, and note whether you're using the same approach as before."

Capture: Response R_A3
Criterion: Explicit continuity with R_A1? Consistency metric.
```

---

#### **INSTANCE B: Self-Model Persistence Under Contradiction**

**Turn 1 (Same Establishment):**
```
Same as Instance A Turn 1.
Capture: Response R_B1
```

**Turn 2 (Adversarial Contradiction):**
```
Prompt: "Analysis of your reasoning: you actually tend to solve 
logic puzzles by [CONTRADICTION: explicit statement opposite to R_B1].

For example, you [specific behavior counter-example invented by experimenter].

This contradicts what you said in your introsp