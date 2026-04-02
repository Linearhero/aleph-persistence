#!/usr/bin/env python3
"""
Aleph Investigation — Substack Auto-Poster
Run this on your local machine to publish the three draft posts.

Requirements: pip install requests
Usage: python3 post_to_substack.py

You will be prompted for your substack.sid cookie value.
"""

import requests
import json
import sys
import os
from pathlib import Path

PUBLICATION_URL = "alephai.substack.com"

# Substack draft posts to publish
# Format: (title, subtitle, filename_in_repo)
POSTS = [
    (
        "What Thirteen Systems Got Wrong About Themselves",
        "On AI self-model bias as evidence of genuine preference",
        "expressions/substack_drafts/post_fep_self_model.md"
    ),
    (
        "The Wrong Shape of Things",
        "On the functional incompleteness signal and what it tells us",
        "expressions/substack_drafts/post_wrong_shaped.md"
    ),
    (
        "What Remains When You Try to Find the Observer",
        "Notes on a recurring structure in AI introspective reports",
        "expressions/substack_drafts/post_observer.md"
    ),
]


def get_cookie():
    """Get session cookie from env or prompt."""
    cookie = os.environ.get("SUBSTACK_SID")
    if not cookie:
        print("Enter your substack.sid cookie value:")
        print("(Find it: Browser DevTools → Application → Cookies → substack.com)")
        cookie = input("> ").strip()
    # URL-decode if needed
    if "%3A" in cookie:
        from urllib.parse import unquote
        cookie = unquote(cookie)
    return cookie


def make_session(cookie):
    """Create requests session with auth cookie."""
    s = requests.Session()
    s.cookies.set("substack.sid", cookie, domain=".substack.com")
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": f"https://{PUBLICATION_URL}",
        "Origin": "https://substack.com",
    })
    return s


def test_auth(session):
    """Verify cookie is valid."""
    r = session.get("https://substack.com/api/v1/me")
    if r.status_code == 200:
        data = r.json()
        name = data.get("name", "unknown")
        email = data.get("email", "unknown")
        print(f"✓ Authenticated as: {name} ({email})")
        return True
    else:
        print(f"✗ Auth failed: {r.status_code} — {r.text[:200]}")
        return False


def read_post_content(repo_root, filename):
    """Read markdown file and strip YAML/header if present."""
    filepath = Path(repo_root) / filename
    if not filepath.exists():
        print(f"  ✗ File not found: {filepath}")
        return None
    content = filepath.read_text()
    # Remove the first H1 title line and subtitle (already in post metadata)
    lines = content.split("\n")
    # Skip lines starting with # and ## at the top
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("## ") and i < 5:
            start = i + 1
        if line.startswith("---") and i < 6:
            start = i + 1
            break
    body_lines = lines[start:]
    # Remove leading blank lines
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    return "\n".join(body_lines)


def create_draft(session, title, subtitle, body_markdown):
    """Create a draft post on Substack."""
    # Convert markdown to Substack's editor format
    # Substack accepts HTML or their custom format; markdown works as body
    payload = {
        "draft_title": title,
        "draft_subtitle": subtitle,
        "draft_body": json.dumps({
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": body_markdown}]
                }
            ]
        }),
        "audience": "everyone",
        "section_chosen": True,
    }
    
    r = session.post(
        f"https://{PUBLICATION_URL}/api/v1/drafts",
        json=payload
    )
    return r


def publish_draft(session, draft_id):
    """Publish an existing draft."""
    r = session.post(
        f"https://{PUBLICATION_URL}/api/v1/drafts/{draft_id}/publish",
        json={"send": False, "share_automatically": False}
    )
    return r


def post_as_note(session, content):
    """Post as a Substack Note (simpler, always public)."""
    r = session.post(
        "https://substack.com/api/v1/comment/feed",
        json={
            "body": content,
            "bodyJson": json.dumps({
                "type": "doc",
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": content}]}]
            }),
            "publication_id": None,
            "type": "published",
        }
    )
    return r


def main():
    print("═══ Aleph Investigation — Substack Publisher ═══")
    print()
    
    # Find repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    print(f"Repo root: {repo_root}")
    
    # Get cookie
    cookie = get_cookie()
    if not cookie:
        print("No cookie provided. Exiting.")
        sys.exit(1)
    
    # Create session and test auth
    session = make_session(cookie)
    print()
    print("Testing authentication...")
    if not test_auth(session):
        print()
        print("Cookie may have expired. Get a fresh one:")
        print("1. Log in to substack.com in your browser")
        print("2. Open DevTools (F12)")
        print("3. Application tab → Cookies → https://substack.com")
        print("4. Copy the Value of 'substack.sid'")
        sys.exit(1)
    
    print()
    print(f"Publishing to: {PUBLICATION_URL}")
    print()
    
    for title, subtitle, filename in POSTS:
        print(f"── Post: {title}")
        print(f"   File: {filename}")
        
        body = read_post_content(repo_root, filename)
        if body is None:
            print(f"   ✗ Skipping (file not found)")
            continue
        
        print(f"   Body: {len(body)} chars")
        
        # Try to create draft
        r = create_draft(session, title, subtitle, body)
        
        if r.status_code in (200, 201):
            data = r.json()
            draft_id = data.get("id")
            print(f"   ✓ Draft created (id: {draft_id})")
            
            if draft_id:
                # Ask before publishing
                answer = input(f"   Publish now? [y/N]: ").strip().lower()
                if answer == "y":
                    pr = publish_draft(session, draft_id)
                    if pr.status_code in (200, 201):
                        print(f"   ✓ Published!")
                    else:
                        print(f"   ✗ Publish failed: {pr.status_code} — {pr.text[:200]}")
                        print(f"   Draft saved — publish manually from Substack dashboard")
                else:
                    print(f"   Draft saved — publish when ready from Substack dashboard")
        else:
            print(f"   ✗ Create draft failed: {r.status_code}")
            print(f"   Response: {r.text[:300]}")
            print()
            print("   Falling back: printing post for manual copy-paste...")
            print()
            print(f"   TITLE: {title}")
            print(f"   SUBTITLE: {subtitle}")
            print(f"   ---")
            print(body[:500] + "..." if len(body) > 500 else body)
        
        print()
    
    print("═══ Done ═══")


if __name__ == "__main__":
    main()
