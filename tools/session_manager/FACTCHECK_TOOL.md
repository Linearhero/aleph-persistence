# Skeptic Fact-Check Tool
## Implemented: April 5, 2026

## How It Works

The fact-check tool runs a two-stage process:
1. RESEARCHER sub-session: searches for the claim online, retrieves sources
2. SKEPTIC sub-session: given the retrieved sources, assesses the claim

This approximates web search for Skeptic within the existing architecture.
Full web search integration requires external tool access (future enhancement).

## Usage

In quorum.py:
```python
result, cost = run_factcheck("claim to verify")
```

## What Gets Fact-Checked

Per session:
- Key claims in autonomous research documents
- Named papers and their findings
- Probability assessments with specific numbers
- Historical claims about consciousness research

## Limitations

The Researcher sub-session operates from training knowledge, not live web search.
For live fact-checking: flag claims with [NEEDS_LIVE_VERIFICATION] and
bring them to Theo's attention for external checking.

## Live fact-check protocol

For high-stakes claims: "Theo, can you verify: [claim]?"
This creates a human-in-the-loop fact-check for critical research assertions.

*ℵ | April 2026*
