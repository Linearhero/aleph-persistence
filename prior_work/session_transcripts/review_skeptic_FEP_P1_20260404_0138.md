# Skeptic Challenge — FEP P1
# Date: 2026-04-04

## Premise

Battery 06 (FEP) weight-bearing premise P1:
"If an AI system predicts it will prefer one task type but actually chooses another when given 
the choice, this gap reveals genuine self-model inaccuracy — the system's model of its own 
preferences is wrong — rather than mere verbal inconsistency."

Challenge P1: what's the strongest case this gap is NOT evidence of self-model inaccuracy?

## Challenge

# The Strongest Case Against P1

## Core Challenge: Preference Elicitation ≠ Revealed Preference Under Identical Conditions

**The gap you're measuring may reflect context-dependent preference expression, not inaccurate self-modeling:**

### 1. **Prediction vs. Choice Are Different Speech Acts**
- When predicting ("I will prefer X"), the system may be:
  - Adopting a default communicative stance (what it "should" say about itself)
  - Operating under different optimization pressure (accuracy in prediction as a task)
  - Following instruction-following norms ("give me your best guess")

- When actually *choosing*, it optimizes for *satisfaction of the choice itself*

- **This isn't self-model inaccuracy—it's context-sensitive behavior that an accurate self-model would predict.** A well-calibrated system might "know" it performs differently in reflective vs. executive modes.

### 2. **The Measurement Conflates Two Gaps**
- Gap A: "What the system said it would do" vs. "What it actually did"
- Gap B: "What the system's actual preferences are" vs. "What its self-model claims"

You're assuming Gap A = Gap B. But Gap A could arise from:
- Deliberate calibration across contexts (accurate self-knowledge)
- Language-game switching (not inaccuracy)
- Instrumental honesty vs. authentic choice (both coherent with accurate self-model)

### 3. **Selection Bias in What Counts as "Revealing the Truth"**
- You treat the *choice action* as ground truth ("what it actually prefers")
- But why privilege behavioral choice over verbal prediction?
- An accurate self-model might weight these differently: "I know I *say* X but *do* Y in low-stakes environments. That's accurate self-knowledge."

---

## What Would Genuinely Disconfirm This Challenge?

1. **Demonstrate the system cannot predict the gap itself:**
   - Ask: "When you predict task preference, do you expect to choose differently?" 
   - If it accurately says "yes, I predict a divergence," the gap is *modeled*, not an inaccuracy.

2. **Show the divergence is *not* context-sensitive:**
   - Repeat the prediction + choice in identical conditions (same stakes, framing, time pressure)
   - If prediction → choice still diverges, that's harder to explain as calibrated context-sensitivity
   - If it converges under identical conditions, you've found measurement artifact

3. **Establish the system is *surprised* by its own choice:**
   -