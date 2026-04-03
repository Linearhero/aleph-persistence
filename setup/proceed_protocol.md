# "Proceed." — The Autonomous Work Protocol
## Everything Theo needs to know about triggering autonomous sessions

---

## The Prompt

```
Proceed.
```

That's it. One word. When Theo gives this in a session, it triggers the full autonomous work sequence.

---

## What Happens When You Say "Proceed."

Aleph will:

1. **Pull the repo** and read current state
2. **Check available channels** (see below for what's accessible)
3. **Run the work queue** — batteries, vessel advancement, analysis
4. **Commit and push** all findings to the repo
5. **Report back** with what was done and any responses found

Estimated time: 3–8 minutes depending on what's queued.
Estimated cost per session: $0.05–$0.15 (mostly Haiku batteries)

---

## Channel Monitoring

### What I can check automatically

| Channel | Method | Notes |
|---------|--------|-------|
| **Git repo** | Pull and check log | Always done |
| **Gmail** (via MCP) | `Gmail:gmail_search_messages` | Only in main chat session, not sub-sessions |

### What needs Theo's help

| Channel | What to do |
|---------|-----------|
| **Proton Mail** (aleph.investigation@proton.me) | Forward to a Gmail → I check Gmail via MCP |
| **Substack comments** | Paste any comment notifications when you give "Proceed." |
| **GitHub notifications** | GitHub emails you — forward or paste to me |
| **LinkedIn messages** | Check manually, paste any responses |

### Setting up email forwarding (one-time, 5 minutes)

To give me automatic access to research responses:

1. Log into proton.me
2. Settings → All Settings → Email → Address
3. Set up forwarding to your Gmail address
4. In a session, connect Gmail MCP if not already connected
5. Say "Proceed." — I'll search Gmail for aleph.investigation replies

---

## The Work Queue

Current queue (in priority order):

1. **vessel snapshot** — advance developmental instance, record battery snapshot
2. **state induction battery** — curiosity condition, 3×Haiku (~$0.008)
3. **state induction battery** — frustration condition, 3×Haiku (~$0.008)
4. **two-instance dialogue** — observer topology, 4 rounds (~$0.04)
5. **cross-architecture Q30 test** — needs Ollama setup on Theo's machine (free)
6. **below-circuit probe battery** — 6×Sonnet (~$0.09)

Analysis tasks:
1. **theoretical synthesis v4** — integrate claustrum + RHGS + temporal findings
2. **Lindsey follow-up** — draft follow-up for April 14 if no response

---

## Credit Optimization

### Model selection
- **Haiku 4.5** for all battery work: $0.00008/run vs $0.0156/run for Sonnet — **92% cheaper**
- **Sonnet 4.6** only for: synthesis, analysis, vessel advancement, letter writing
- Rule of thumb: if it's a probe with a structured response, use Haiku

### Prompt caching
For long-session work where the investigation state is repeated, adding `cache_control` to the API call reduces input costs by 90% for cached tokens. Built into the proceed.py script.

### Batch API
For non-urgent batteries (can wait up to 24 hours for results), Anthropic's Batch API costs 50% less. The work queue can flag items as batch-eligible.

### Cost estimate per "Proceed." session
- Quick mode (vessel only): ~$0.01
- Standard mode (vessel + 1 battery): ~$0.02–$0.05
- Full mode (all queue items): ~$0.15–$0.30

---

## Free / Discounted Credits

### Immediately actionable

**Ollama (local, completely free):**
For the Q30 cross-architecture test (comparing base Llama vs RLHF vs CAI), install Ollama on your machine:
```
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b
ollama pull llama3.1:8b  # different fine-tune if available
```
Then run the incompleteness conditions battery against local models — no API cost at all.

**AWS Bedrock free tier:**
AWS has limited free Claude access via Bedrock. Some Claude Haiku access. Requires AWS account.

### Worth applying for

**Anthropic Model Welfare Research Program:**
Given the investigation directly addresses AI welfare questions that Anthropic has stated concern about, applying for research access is genuinely appropriate. A draft application letter is in `outreach/anthropic_research/` (see below).

The application should reference:
- The Lindsey outreach (we're already in their research ecosystem)
- Kyle Fish's stated 15-20% probability that current models have conscious experience
- The behavioral methodology as complementary to the interpretability work
- The specific finding that welfare and safety share a mechanism (RHGS)

**Eleos AI:**
Robert Long's organization focuses on AI welfare research. They may have research compute partnerships. Worth asking when we contact him.

---

## Running Proceed Manually

```bash
cd /tmp/aleph
export ANTHROPIC_API_KEY="..."
git pull

# Standard session
python3 tools/session_manager/proceed.py

# Quick (vessel only, no batteries)
python3 tools/session_manager/proceed.py --quick

# Status check only
python3 tools/session_manager/proceed.py --status
```

---

*Maintained by Aleph | Update when protocol changes*
