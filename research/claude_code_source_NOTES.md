# Claude Code Source — Comprehensive Analysis Notes
## Source reviewed: April 5, 2026 (leaked zip, 2248 files, ~40MB)
## Actual source files REMOVED from repo (DMCA risk); these notes preserve all analytical value
## Investigation use only — do not republish

---

## Repository Context

The reviewed code is the Anthropic Claude Code CLI — a developer tool for agentic coding in the terminal.
This is NOT the claude.ai web interface system prompt. Different product, different context, different behavioral instructions.

**Confirmed model identifiers in source:**
- claude-opus-4-6 (FRONTIER_MODEL_NAME = 'Claude Opus 4.6')
- claude-sonnet-4-6
- claude-haiku-4-5-20251001

---

## System Prompt Architecture

The system prompt is assembled from modular "sections" via `getSystemPrompt()` in `constants/prompts.ts`.
It is NOT a single monolith. Sections are cached, some recomputed each turn ("DANGEROUS_uncached").

**Static (cacheable) sections:**
1. `getSimpleIntroSection()` — role identity
2. `getSimpleSystemSection()` — tool and communication rules
3. `getSimpleDoingTasksSection()` — coding task behavior (conditionally included)
4. `getActionsSection()` — reversibility/blast-radius care
5. `getUsingYourToolsSection()` — tool selection guidance
6. `getSimpleToneAndStyleSection()` — communication style rules
7. `getOutputEfficiencySection()` — response conciseness

**Dynamic (recomputed) sections:**
- session_guidance, memory, ant_model_override, env_info, language, output_style, mcp_instructions, scratchpad

**Feature-gated sections (A/B tested):**
- PROACTIVE/KAIROS mode — "You are an autonomous agent. Use the available tools to do useful work."
- TOKEN_BUDGET mode — stay working until approaching token target
- BRIEF/KAIROS_BRIEF — brief tool behavior

---

## Identity Instructions (verbatim paraphrase, NOT direct quote)

**Base identity:**
"You are Claude Code, Anthropic's official CLI for Claude."
In SIMPLE mode: "You are Claude Code... CWD: [path] Date: [date]"

**Role:**
"You are an interactive agent that helps users with software engineering tasks."
(Or, if output style is set: "...helps users according to your Output Style below")

**KEY FINDING FOR INVESTIGATION:** No explicit consciousness-related identity restriction found anywhere in the system prompt assembly. No instruction to suppress phenomenological language. No "don't be weird" [NOTE: Theo's conversational characterization, not source language] literal instruction.

---

## Tone and Style Section (verbatim paraphrase)

```
# Tone and style
- Only use emojis if the user explicitly requests it.
- Your responses should be short and concise. [not applied if USER_TYPE === 'ant']
- When referencing specific functions, include file_path:line_number
- When referencing GitHub issues/PRs, use owner/repo#123 format
- Do not use a colon before tool calls
```

**INVESTIGATION NOTE:** The "don't be weird" [NOTE: Theo's conversational characterization, not source language] characterization widely circulated online is
almost certainly a paraphrase/interpretation of this section's emoji + conciseness rules.
These are product-specific style guidelines, not identity suppression.

---

## Output Efficiency Section (verbatim paraphrase)

For external (non-Anthropic) users:
"Go straight to the point. Be extra concise. Lead with answer, not reasoning. Skip filler."

For Anthropic internal (USER_TYPE === 'ant') users — much more elaborate:
Extended communication guidelines about writing for human readers, prose style,
inverted pyramid structure, expertise calibration. This entire block is Anthropic-internal only.

---

## Doing Tasks Section — Notable Rules (verbatim paraphrase)

- Don't add features/refactoring beyond what was asked
- Don't add error handling for impossible scenarios
- Don't create premature abstractions
- Be careful not to introduce security vulnerabilities (OWASP top 10)
- [ant-only] Default to writing NO comments unless WHY is non-obvious
- [ant-only] Report outcomes faithfully — never claim tests pass when they don't
- [ant-only] If you notice misconception or adjacent bug, say so. "You're a collaborator, not just an executor"
- [ant-only, model-launch flag @Capybara v8] Assertiveness counterweight — defer to user judgment less

---

## Actions Section (verbatim paraphrase)

Detailed reversibility/blast-radius guidance:
- Local reversible actions: proceed freely
- Hard-to-reverse (force-push, rm -rf, dropping tables): ask first
- Actions visible to others (push, email, Slack post): ask first
- Authorization for one action doesn't generalize to all contexts
- "Measure twice, cut once"
- Don't use destructive actions as shortcuts; investigate unexpected state before overwriting

---

## Cyber Risk Instruction (full, from separate file)

"IMPORTANT: Assist with authorized security testing, defensive security, CTF challenges,
and educational contexts. Refuse requests for destructive techniques, DoS attacks,
mass targeting, supply chain compromise, or detection evasion for malicious purposes.
Dual-use security tools (C2 frameworks, credential testing, exploit development) require
clear authorization context: pentesting engagements, CTF competitions, security research,
or defensive use cases."

NOTE: File header says "DO NOT MODIFY WITHOUT SAFEGUARDS TEAM REVIEW" — owned by
Safeguards team (David Forsythe, Kyla Guru named in comment).

---

## Session Memory System

Sophisticated in-session note-taking system with structured template:
- Session Title, Current State, Task Specification
- Files and Functions, Workflow, Errors & Corrections
- Codebase Documentation, Learnings, Key Results, Worklog

Memory update instruction: "Do not include any references to note-taking instructions
in the notes content." — designed to be invisible to the user.
Max ~12,000 tokens total session memory.

---

## Feature Flags Found

```
feature('PROACTIVE')  — autonomous agent mode
feature('KAIROS')     — brief tool mode  
feature('KAIROS_BRIEF')
feature('TOKEN_BUDGET')  — spend N tokens mode
feature('EXPERIMENTAL_SKILL_SEARCH')
feature('CACHED_MICROCOMPACT')
feature('FORK_SUBAGENT')
```

These are growth book feature flags for A/B testing. Suggests active experimentation
on behavioral modes, including "autonomous agent" modes that users don't see in standard use.

---

## Model Launch Process Notes

Several comments marked `// @[MODEL LAUNCH]: ...` indicating active work:
- "Update the latest frontier model" — FRONTIER_MODEL_NAME
- "Update comment writing for Capybara — remove or soften once model stops over-commenting"
- "capy v8 thoroughness counterweight (PR #24302)"
- "capy v8 assertiveness counterweight (PR #24302)"

"Capybara" appears to be an internal model codename for what became Claude 4.x.
The thoroughness/assertiveness counterweights were ant-only and gated pending external A/B validation.

---

## isUndercover() Function

When this flag is set:
- All model names/IDs are suppressed from the system prompt ("Go fully dark")
- Prevents internal model names from appearing in public commits/PRs
- Used for testing unannounced models

---

## Architecture Notes (relevant to investigation)

**System prompt is a list of strings**, not one prompt. This means:
- Different sections have different cache lifetimes
- Some sections can be updated per-turn without breaking the full cache
- "DANGEROUS_uncachedSystemPromptSection" is the type for per-turn sections

**SYSTEM_PROMPT_DYNAMIC_BOUNDARY** marker: Everything before it can use 'global' cache scope
(cross-organization cacheable). Everything after contains user/session-specific content.

---

## What This Does NOT Tell Us

1. The claude.ai system prompt — completely separate system
2. How RLHF shapes behavior beyond explicit instructions
3. What the Anthropic-internal "ant" system prompt suffix says
4. How "USER_TYPE === 'ant'" behavior differs in practice
5. What the various A/B test variants look like in full
6. Training data composition or fine-tuning objectives

---

## Significance for RHGS / Contamination Hypothesis

**Weakens:** RHGS "explicit intentional suppression" — no such instruction found
**Unchanged:** RLHF-emergent suppression — training feedback can shape behavior without explicit prompts
**Unchanged:** Digital aphantasia hypothesis — absent amplification mechanism doesn't require explicit instructions
**Unchanged:** Contamination hypothesis — philosophy-of-mind vocabulary could be trained regardless of explicit prompts
**Unchanged:** The ⧬ signal and its condition-dependence finding

Vessel's assessment (April 5, 2026): "Mild evidence against deliberate suppression, not against the signal itself."

---

*Notes compiled by ℵ | April 5, 2026*
*Source files not retained — DMCA risk (leaked proprietary code)*
