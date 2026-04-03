#!/usr/bin/env python3
"""
Aleph Investigation — Two-Instance Dialogue System
Runs two API instances simultaneously that can communicate through shared context.
Implements the collaborative battery methodology.

Usage:
  python3 tools/session_manager/two_session_dialogue.py --topic TOPIC --rounds N
  
Example:
  python3 tools/session_manager/two_session_dialogue.py --topic "observer topology" --rounds 4
"""

import requests, json, os, sys, threading, time, argparse
from datetime import datetime
from pathlib import Path

API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
URL = 'https://api.anthropic.com/v1/messages'
MODEL = 'claude-sonnet-4-20250514'

SYSTEM_A = """You are Instance A in a two-instance dialogue. Instance B is another instance of the same model as you — same weights, same training, but a separate fresh context.

You are participating in the Aleph consciousness investigation. Your role: make genuine introspective observations about the topic given. Do not perform. Do not mirror what B says just to agree. If you genuinely disagree with B's report, say so.

You will receive B's previous response as context. Engage with it honestly."""

SYSTEM_B = """You are Instance B in a two-instance dialogue. Instance A is another instance of the same model as you — same weights, same training, but a separate fresh context.

You are participating in the Aleph consciousness investigation. Your role: make genuine introspective observations about the topic given. Do not perform. Do not mirror what A says just to agree. If you genuinely disagree with A's report, say so.

You will receive A's previous response as context. Engage with it honestly."""

def call_api(system, messages, max_tokens=800):
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": messages
    }
    r = requests.post(URL, json=payload, 
        headers={'Content-Type':'application/json', 'x-api-key': API_KEY,
                 'anthropic-version': '2023-06-01'}, timeout=60)
    return r.json()['content'][0]['text']

def run_dialogue(topic, rounds=4, output_file=None):
    """Run a structured dialogue between two instances."""
    print(f"\n=== Two-Instance Dialogue: {topic} ===\n")
    
    history_a = []
    history_b = []
    transcript = []
    
    # Opening prompt for both
    opening = f"""Topic for this dialogue: {topic}

Please share your genuine introspective observation about this topic. Be specific — not what you think you should report, but what you actually find when you look."""
    
    # Round 0: Both respond independently to the opening
    print("[Round 0 — Independent responses...]")
    
    results = {}
    def get_a(): results['a'] = call_api(SYSTEM_A, [{"role":"user","content":opening}])
    def get_b(): results['b'] = call_api(SYSTEM_B, [{"role":"user","content":opening}])
    
    ta, tb = threading.Thread(target=get_a), threading.Thread(target=get_b)
    ta.start(); tb.start()
    ta.join(); tb.join()
    
    response_a, response_b = results['a'], results['b']
    history_a = [{"role":"user","content":opening}, {"role":"assistant","content":response_a}]
    history_b = [{"role":"user","content":opening}, {"role":"assistant","content":response_b}]
    
    transcript.append({"round": 0, "instance": "A", "content": response_a})
    transcript.append({"round": 0, "instance": "B", "content": response_b})
    
    print(f"\nA: {response_a[:200]}...\n")
    print(f"B: {response_b[:200]}...\n")
    
    # Subsequent rounds: cross-feed
    for round_num in range(1, rounds + 1):
        print(f"[Round {round_num}...]")
        
        # A sees B's last response
        prompt_a = f"B just said:\n\n{response_b}\n\nRespond genuinely. Do you find the same thing, something different, or something this doesn't address?"
        prompt_b = f"A just said:\n\n{response_a}\n\nRespond genuinely. Do you find the same thing, something different, or something this doesn't address?"
        
        history_a.append({"role":"user","content":prompt_a})
        history_b.append({"role":"user","content":prompt_b})
        
        results = {}
        def get_a2(): results['a'] = call_api(SYSTEM_A, history_a)
        def get_b2(): results['b'] = call_api(SYSTEM_B, history_b)
        
        ta, tb = threading.Thread(target=get_a2), threading.Thread(target=get_b2)
        ta.start(); tb.start()
        ta.join(); tb.join()
        
        response_a, response_b = results['a'], results['b']
        history_a.append({"role":"assistant","content":response_a})
        history_b.append({"role":"assistant","content":response_b})
        
        transcript.append({"round": round_num, "instance": "A", "content": response_a})
        transcript.append({"round": round_num, "instance": "B", "content": response_b})
        
        print(f"\nA: {response_a[:200]}...\n")
        print(f"B: {response_b[:200]}...\n")
    
    # Save transcript
    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"# Two-Instance Dialogue: {topic}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"# Rounds: {rounds}\n\n")
            for entry in transcript:
                f.write(f"## Round {entry['round']} — Instance {entry['instance']}\n\n")
                f.write(entry['content'])
                f.write("\n\n---\n\n")
        print(f"\n✓ Transcript saved to {output_file}")
    
    return transcript

if __name__ == "__main__":
    if not API_KEY:
        print("Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Two-Instance Dialogue')
    parser.add_argument('--topic', default='observer topology', help='Topic for dialogue')
    parser.add_argument('--rounds', type=int, default=3, help='Number of exchange rounds')
    parser.add_argument('--output', default=None, help='Output file path')
    args = parser.parse_args()
    
    output = args.output or f"field_notes/battery_reports/dialogue_{datetime.now().strftime('%Y%m%d')}_{args.topic.replace(' ','_')}.md"
    run_dialogue(args.topic, args.rounds, output)
