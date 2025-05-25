#!/usr/bin/env python3
"""Extract @ADMIN messages from session logs for intervention analysis."""

import json
import sys
from pathlib import Path

def extract_admin_messages(jsonl_file):
    """Extract messages mentioning @ADMIN from a JSONL session file."""
    results = []
    
    with open(jsonl_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                # Check for user messages from external source
                if data.get('type') == 'user' and data.get('userType') == 'external':
                    message = data.get('message', {})
                    content = message.get('content', [])
                    
                    # Extract text content
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text = item.get('text', '')
                            # Look for @ADMIN mentions or admin-like behavior
                            if '@ADMIN' in text or 'admin' in text.lower():
                                results.append({
                                    'line': line_num,
                                    'timestamp': data.get('timestamp'),
                                    'uuid': data.get('uuid'),
                                    'text': text[:200] + '...' if len(text) > 200 else text
                                })
                                
            except json.JSONDecodeError:
                pass
    
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_admin_messages.py <jsonl_file>")
        sys.exit(1)
        
    jsonl_file = Path(sys.argv[1])
    if not jsonl_file.exists():
        print(f"File not found: {jsonl_file}")
        sys.exit(1)
        
    messages = extract_admin_messages(jsonl_file)
    
    print(f"Found {len(messages)} @ADMIN references in {jsonl_file.name}:")
    for msg in messages:
        print(f"\nLine {msg['line']} @ {msg['timestamp']}:")
        print(f"  {msg['text']}")