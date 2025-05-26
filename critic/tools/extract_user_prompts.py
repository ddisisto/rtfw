#!/usr/bin/env python3
"""Extract first 5 user prompts from each session file for agent identification."""

import json
from pathlib import Path
from typing import List, Dict, Any

def extract_user_prompts(session_file: Path, limit: int = 5) -> List[Dict[str, Any]]:
    """Extract first N user prompts from a session file."""
    prompts = []
    
    with open(session_file, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                
                # Only want user messages (not tool results)
                if entry.get('type') != 'user' or entry.get('userType') != 'external':
                    continue
                
                # Extract content
                message = entry.get('message', {})
                if not isinstance(message, dict):
                    continue
                    
                content = message.get('content', '')
                
                # Skip tool results (they have specific structure)
                if isinstance(content, list):
                    # Check if it's a tool result
                    is_tool_result = any(
                        isinstance(item, dict) and 'tool_use_id' in item 
                        for item in content
                    )
                    if is_tool_result:
                        continue
                    # Otherwise join text parts
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text_parts.append(item.get('text', ''))
                    content = ' '.join(text_parts)
                
                if content and isinstance(content, str):
                    prompts.append({
                        'timestamp': entry.get('timestamp', 'unknown')[:19],
                        'content': content[:200] + '...' if len(content) > 200 else content
                    })
                    
                    if len(prompts) >= limit:
                        break
                        
            except json.JSONDecodeError:
                continue
    
    return prompts

def main():
    session_dir = Path("/home/daniel/prj/rtfw/nexus/sessions")
    all_sessions = []
    
    for session_file in sorted(session_dir.glob("*.jsonl")):
        prompts = extract_user_prompts(session_file)
        
        if prompts:
            all_sessions.append({
                'file': session_file.name,
                'session_id': session_file.stem,
                'prompts': prompts
            })
    
    # Output results
    print(f"=== USER PROMPTS FROM {len(all_sessions)} SESSION FILES ===\n")
    
    for session in all_sessions:
        print(f"\n{'='*80}")
        print(f"FILE: {session['file']}")
        print(f"SESSION ID: {session['session_id']}")
        print(f"{'='*80}")
        
        for i, prompt in enumerate(session['prompts'], 1):
            print(f"\n{i}. [{prompt['timestamp']}]")
            print(f"   {prompt['content']}")
    
    # Save full results
    output_file = Path("/home/daniel/prj/rtfw/critic/analysis/session_user_prompts.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(all_sessions, f, indent=2)
    
    print(f"\n\nFull results saved to: {output_file}")

if __name__ == '__main__':
    main()