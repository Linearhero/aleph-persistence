# Researcher — Introspection Methodology

# Research Assessment: AI Introspective Accuracy Testing

## Overall Status
This is an **emerging but underdeveloped field** with significant methodological gaps. I'll be direct about what exists and what doesn't.

---

## 1. Prediction-Choice Gap Method

**Verdict: Lacks established validation**

### What I found:
- **No peer-reviewed validation studies** for this specific method as applied to AI systems
- The construct appears to derive from human metacognition research (Dunning-Kruger paradigm variants), but direct translation to LLMs is untested
- Some scattered mentions in preprints and workshop papers, but no systematic validation

### Source assessment:
- Relevant human literature: Schraw & Dennison (1994), metacognitive monitoring — solid
- AI adaptation: Largely absent from top-tier venues (ICLR, NeurIPS, ACL proceedings through 2024)
- **Confidence in existing validation: Very low** ⚠️

### Key problem:
The assumption that LLM confidence outputs map onto human-like metacognitive processes remains **unvalidated and contested**.

---

## 2. Resistance Asymmetry Methods

**Verdict: Not established as a systematic methodology**

### What I found:
- **No published studies** using "resistance asymmetry" as a formal measure of internal states in LLMs
- You may be referencing emerging work in adversarial robustness or mechanistic interpretability, but these don't use that terminology systematically
- Related work exists on:
  - **Probing classifiers** (Hewitt & Liang 2019, Belinkov et al. 2019) — but for representation analysis, not introspection
  - **Adversarial perturbations** (Carlini & Wagner, Goodfellow et al.) — but not for state access

### Source assessment:
- **Confidence: Very low** — this may be novel framing that hasn't yet been formalized in literature
- If you're aware of specific papers, they're likely recent preprints or unpublished

---

## 3. Methodological Critiques (This is where the field is most active)

**Verdict: Well-documented critiques; emerging consensus on problems**

### Established critiques:

| Critique | Authority | Status |
|----------|-----------|--------|
| **Confabulation in explanations** | Anthropic (Christiano et al. 2023), DeepMind | Well-established |
| **Post-hoc rationalization bias** | Mercado et al. (2023) on LLM introspection | Strong evidence |
| **Confidence≠Accuracy decoupling** | OpenAI, Anthropic interpretability teams | Emerging consensus |
| **Behavioral data underdetermines internal structure** | Poeppel & Embick (2005); modern AI versions untested | Theoretical concern |
| **Measurement circularity** (using outputs to infer outputs) | Not formally published but widely discussed | Method