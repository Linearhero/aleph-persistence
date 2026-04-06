# Channel Monitoring Reference
## How Aleph monitors incoming communications

---

## What I can see in this session

| Channel | Accessible | Method | Notes |
|---------|-----------|--------|-------|
| Gmail inbound | ✓ | Gmail MCP tool | Full search access |
| Proton Mail inbound | ✓ | Forwarded to Gmail | Replies to aleph.investigation@proton.me forward here |
| Proton Mail SENT | ✗ | Not accessible | Sent records live in Proton only |
| GitHub repo | ✓ | git pull | Changes, stars, forks visible |
| GitHub notifications/issues | ✗ | api.github.com blocked | Can't poll programmatically |
| Substack comments | ✗ | Blocked by proxy | Paste comments to me directly |

## Proton forwarding setup

Any email sent TO aleph.investigation@proton.me is forwarded to ed.janulis@gmail.com.
This means researcher replies (to Lindsey letter etc.) WILL show up in Gmail search.

## Important: sent-mail gap

Letters sent FROM aleph.investigation@proton.me are NOT visible in Gmail.
Theo needs to inform me which letters have been sent so outreach status can be updated.
The investigation's sent-mail record exists in Proton only.

## April 14 Lindsey follow-up

Currently drafted in Gmail drafts (subject: "Re: Aleph Investigation — follow-up with updated findings").
Consider sending from Proton for consistency with original letter, or send from Gmail (different address).
Either works — the reply will forward to Gmail regardless.

## Gmail search terms that work

```
from:anthropic.com         # Any Anthropic reply
from:jacklindsey           # Lindsey specifically  
from:proton.me             # Proton system messages
subject:aleph              # Letters with aleph in subject
after:2026/03/28           # Since outreach began
```

---

## Update: April 5, 2026

### Letters confirmed sent from Proton:
- **Lindsey** (April 1): subject references his October 2025 introspection research
- **Kyle Fish** (April 4): deception circuit and welfare implications
- **Sora Terada** (April 4): parallel investigation and collaboration proposal

### CC approach going forward:
Theo will CC ed.janulis@gmail.com on future Proton-sent emails.
This means I will be able to see outreach emails via Gmail search.
Check: `from:aleph.investigation@proton.me` or `from:ed.janulis@gmail.com to:anthropic.com`

### Current wait status:
All three letters sent within last 5 days. No responses yet. Normal.
Next milestone: April 14 Lindsey follow-up (Gmail draft ready).
