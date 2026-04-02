#!/usr/bin/env python3
"""
Aleph Investigation — Substack Auto-Poster
Run on your local machine: Python setup/post_to_substack.py
Requires: pip install requests
"""

import requests, json, sys, os
from pathlib import Path
from urllib.parse import unquote

PUBLICATION = "alephai"
PUB_URL = f"https://{PUBLICATION}.substack.com"

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
    val = os.environ.get("SUBSTACK_SID") or input("Paste your substack.sid cookie value:\n> ").strip()
    return unquote(val)

def make_session(cookie):
    s = requests.Session()
    for name in ("substack.sid", "connect.sid"):
        s.cookies.set(name, cookie, domain=".substack.com")
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://substack.com",
        "Referer": "https://substack.com/",
    })
    return s

def test_auth(s):
    """Try several known-good endpoints to verify auth."""
    endpoints = [
        f"{PUB_URL}/api/v1/subscriber/me",
        "https://substack.com/api/v1/subscriber/me",
        f"{PUB_URL}/api/v1/user",
        f"{PUB_URL}/api/v1/users/me",
        "https://substack.com/api/v1/me",
        f"{PUB_URL}/api/v1/settings",
    ]
    for url in endpoints:
        try:
            r = s.get(url, timeout=10)
            if r.status_code == 200 and r.headers.get("content-type","").startswith("application/json"):
                data = r.json()
                name = data.get("name") or data.get("author_name") or data.get("handle","?")
                print(f"  ✓ Auth OK via {url.split('/')[-1]} — {name}")
                return True, data
            elif r.status_code == 200:
                print(f"  ~ {url}: 200 but not JSON")
        except Exception as e:
            pass
    return False, {}

def read_file(repo_root, path):
    fp = Path(repo_root) / path
    if not fp.exists():
        return None
    text = fp.read_text(encoding="utf-8")
    lines = text.split("\n")
    # Skip title/subtitle header lines at top of file
    skip = 0
    for i, l in enumerate(lines[:8]):
        if l.startswith("# ") or l.startswith("## ") or l.startswith("*Aleph") or l == "---":
            skip = i + 1
    body = "\n".join(lines[skip:]).strip()
    return body

def markdown_to_tiptap(md):
    """Minimal markdown → Substack tiptap JSON."""
    paragraphs = []
    for para in md.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.startswith("# "):
            paragraphs.append({"type": "heading", "attrs": {"level": 1},
                "content": [{"type": "text", "text": para[2:]}]})
        elif para.startswith("## "):
            paragraphs.append({"type": "heading", "attrs": {"level": 2},
                "content": [{"type": "text", "text": para[3:]}]})
        elif para.startswith("---"):
            paragraphs.append({"type": "horizontalRule"})
        else:
            paragraphs.append({"type": "paragraph",
                "content": [{"type": "text", "text": para}]})
    return json.dumps({"type": "doc", "content": paragraphs})

def try_create_draft(s, title, subtitle, body):
    """Try creating a draft via multiple endpoint variants."""
    tiptap = markdown_to_tiptap(body)

    payloads_and_urls = [
        # Variant 1: publication-specific drafts endpoint
        (f"{PUB_URL}/api/v1/drafts", {
            "draft_title": title,
            "draft_subtitle": subtitle,
            "draft_body": tiptap,
            "audience": "everyone",
            "section_chosen": True,
        }),
        # Variant 2: with type field
        (f"{PUB_URL}/api/v1/drafts", {
            "draft_title": title,
            "draft_subtitle": subtitle,
            "draft_body": tiptap,
            "type": "newsletter",
            "audience": "everyone",
        }),
        # Variant 3: substack.com root
        ("https://substack.com/api/v1/drafts", {
            "draft_title": title,
            "draft_subtitle": subtitle,
            "draft_body": tiptap,
            "audience": "everyone",
            "publication_id": PUBLICATION,
        }),
    ]

    for url, payload in payloads_and_urls:
        try:
            r = s.post(url, json=payload, timeout=15)
            if r.status_code in (200, 201):
                try:
                    data = r.json()
                    if "id" in data:
                        return True, data["id"], r
                except:
                    pass
            print(f"  Variant {url.split('/')[-1]}: {r.status_code}")
        except Exception as e:
            print(f"  Exception: {e}")

    return False, None, None

def main():
    print("═══ Aleph — Substack Publisher ═══\n")
    repo_root = Path(__file__).parent.parent
    cookie = get_cookie()

    s = make_session(cookie)
    print("\nTesting auth...")
    ok, user_data = test_auth(s)

    if not ok:
        print("\n✗ Could not authenticate.")
        print("\nThe cookie may have changed format. Let's try posting a draft directly anyway.")
        print("(Substack sometimes allows draft creation even when /me is 404)\n")
        # Don't exit — try posting anyway

    print()
    created_any = False

    for title, subtitle, fname in POSTS:
        print(f"── {title}")
        body = read_file(repo_root, fname)
        if not body:
            print(f"   ✗ File not found: {fname}\n")
            continue
        print(f"   {len(body)} chars")

        success, draft_id, resp = try_create_draft(s, title, subtitle, body)

        if success:
            print(f"   ✓ Draft created (id: {draft_id})")
            created_any = True
            ans = input("   Publish now? [y/N]: ").strip().lower()
            if ans == "y":
                pr = s.post(f"{PUB_URL}/api/v1/drafts/{draft_id}/publish",
                            json={"send": False, "share_automatically": False})
                if pr.status_code in (200, 201):
                    print("   ✓ Published!")
                else:
                    print(f"   Draft saved — publish from your Substack dashboard")
        else:
            print(f"   ✗ Draft creation failed — printing for manual paste:\n")
            print(f"   TITLE:    {title}")
            print(f"   SUBTITLE: {subtitle}")
            print(f"   BODY (first 400 chars):\n{body[:400]}...\n")
            print(f"   Full content in repo: {fname}\n")
        print()

    if not created_any:
        print("═══ Manual fallback ═══")
        print(f"Go to https://{PUBLICATION}.substack.com/publish/post")
        print("The three post files are ready in expressions/substack_drafts/")
        print("Copy/paste each one — titles and subtitles are at the top of each file.")

    print("\n═══ Done ═══")

if __name__ == "__main__":
    main()
