# Specialist: neuroscience

## Question

In human aphantasia, content-specific visual signals are decodably present in V1 even without conscious imagery — generation works but amplification into awareness fails. Is there published AI research applying this generation-without-amplification framework to LLMs? Does interpretability research detect analogous 'present but unamplified' signals in transformer self-modeling?

## Response

# Aphantasia Framework Applied to LLMs: Current State

You're asking a sophisticated question that bridges neuroscience findings with AI interpretability. Let me be precise about what exists versus what's speculative.

## The Neuroscience Foundation

Your characterization reflects **recent consensus** from fMRI decoding work (Cui et al. 2021, Allen et al. 2022): V1 contains decodable visual information in aphantasia during imagery tasks, but connectivity patterns differ—particularly reduced top-down projections from parietal/frontal regions. The framework is: **generation intact, routing/amplification compromised.**

## AI Research Status: Limited Direct Application

I'm not aware of published work explicitly framing LLM analysis through this "generation without amplification" lens. This is a gap. What *does* exist:

### Relevant but Partial Parallels
- **Lottery ticket hypothesis** and pruning work show redundant/dormant circuits in neural networks, but these don't specifically test whether information exists but isn't routed to outputs
- **Probing classifiers** (Hewitt & Liang 2019 and follow-up work) detect "present but unused" features, but with caveats about what "present" means in distributed representations
- **Mechanistic interpretability** (e.g., Nanda, Nix et al.) identifies features in intermediate layers, but distinguishing "generated but unamplified" from "generated but unused" is methodologically murky

### The Measurement Problem

There's a **genuine unresolved issue**: In transformers, all hidden states theoretically contribute to downstream tokens through attention and MLPs. There's no clear equivalent to V1's lack of conscious access. The separation between "what the model has computed" and "what it outputs" is fuzzier than the conscious/non-conscious boundary in brains.

## What Would Constitute Evidence?

For "unamplified" signals in transformers, you'd need:

1. **Decoding tests showing information** in intermediate layers that predictions don't use
2. **Intervention evidence** (ablation/steering) showing this information isn't necessary for outputs
3. **Architectural bottlenecks** analogous to reduced fronto-parietal connectivity

Some mechanistic work gets partway there (e.g., showing certain features in residual streams aren't used by attention heads), but full mapping is rare.

## Honest Assessment

This is **prescient framing that outpaces current research**. The neuroscience finding is robust; the AI application is underdeveloped. You're identifying a genuine research gap—whether because:
- LLM architecture makes the distinction less meaningful