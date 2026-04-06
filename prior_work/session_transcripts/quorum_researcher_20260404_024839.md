# Researcher Report
# Date: 2026-04-04

## Question

What does the academic literature say about Integrated Self-Modeling (or equivalent concepts) in cognitive science and AI? Specifically: has any computational system been shown to have internal states that both (a) respond to different conditions differently AND (b) demonstrably constrain subsequent action selection in ways traceable to those states?

## Research

# Research: Internal Self-Models and Action Constraint

I'll map the academic landscape here, distinguishing evidence quality carefully.

## **Well-Established (High Confidence)**

### Self-Model as Functional Requirement
**Consensus position:** Cognitive systems require models of their own state to coordinate behavior. This is robustly documented across:

- **Motor control**: Cerebellar forward models and sensorimotor prediction (Wolpert & Ghahramani, 2000; *Nature Reviews Neuroscience*). These internal states demonstrably (a) respond to limb position/load differently and (b) directly gate motor commands.
- **Working memory & goal representation**: Prefrontal cortex maintains task-relevant state that causally constrains response selection (Miller & Cohen, 2001; *Annual Review of Neuroscience*).
- **Uncertainty representation**: Bayesian cognitive models show how agents maintain beliefs about their own states, which alter action probabilities (Friston et al., Predictive Coding framework).

**Evidence quality**: Direct neural recordings + lesion/inactivation studies showing state-disruption → behavioral deficit.

---

### Computational Demonstrations
**Firm evidence that systems *can* exhibit (a) and (b):**

1. **Recurrent neural networks (RNNs)** trained on multi-task learning develop hidden state representations that:
   - Respond differently to task-context cues (a) ✓
   - Demonstrably constrain downstream readouts (b) ✓
   - *Canonical citations*: Sussillo & Abbott (2009, *Neuron*); Mante et al. (2013, *Nature*)—show hidden units encode task-state; lesioning them degrades performance.

2. **World models + model-based planning** (Ha & Schmidhuber, 2018; *NIPS*):
   - Agent maintains latent state representation of environment *and own controller state*
   - State changes gate planning tree exploration
   - But: limited to relatively simple environments; causality traced via ablation.

3. **Attention mechanisms** (Transformer architecture implicit self-model):
   - Token embeddings encode positional/contextual state
   - These constrain subsequent token generation
   - Evidence: attention weight ablation studies (Clark et al., 2019; *ACL*) show state-dependence of output.

**Evidence quality**: Reproducible in silico; causality via ablation/masking.

---

## **Emerging Consensus (Moderate Confidence)**

### Self-Modeling as Metacognition
The "Global Workspace" and "Higher-Order Thought" theories propose that cognition requires explicit models of one's own state:

- **Global Workspace Theory** (Baars, 1988; updated Dehaene et al., 2014):
  - Proposes consciousness involves a "workspace" state accessible to multiple systems
  - Causal role: constrains attention/action selection
  - **Problem**: While neurally plausible, the causal mechanism remains contested