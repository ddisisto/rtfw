#!/usr/bin/env python3
"""
Analyze session JSONL for context window usage patterns
"""

import json
import sys
from pathlib import Path

def extract_content_preview(message):
    """Extract first 200 chars of content"""
    if isinstance(message, dict):
        content = message.get('content', '')
        if isinstance(content, list) and content:
            # Handle tool use or mixed content
            first_item = content[0]
            if isinstance(first_item, dict):
                return first_item.get('text', str(first_item))[:200]
            return str(first_item)[:200]
        elif isinstance(content, str):
            return content[:200]
    return "NA"

def analyze_session_line(line):
    """Parse one JSONL line and extract key metrics"""
    try:
        data = json.loads(line.strip())
        
        # Basic info
        entry_type = data.get('type', 'unknown')
        timestamp = data.get('timestamp', 'NA')[:19]  # Just date/time
        
        # Message details
        message = data.get('message', {})
        if not isinstance(message, dict):
            message = {}
            
        role = message.get('role', 'NA')
        
        # Usage metrics
        usage = message.get('usage', {})
        if not isinstance(usage, dict):
            usage = {}
            
        input_tokens = usage.get('input_tokens', 0)
        cache_create = usage.get('cache_creation_input_tokens', 0)
        cache_read = usage.get('cache_read_input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        
        # Cost
        cost = data.get('costUSD', 0)
        
        # Content preview
        content_preview = extract_content_preview(message)
        
        # Calculate totals
        total_input = input_tokens + cache_create + cache_read
        
        return {
            'timestamp': timestamp,
            'type': entry_type,
            'role': role,
            'input': input_tokens,
            'cache_create': cache_create,
            'cache_read': cache_read,
            'output': output_tokens,
            'total_input': total_input,
            'cost': cost,
            'content': content_preview
        }
    except Exception as e:
        return {
            'timestamp': 'ERROR',
            'type': 'error',
            'role': 'NA',
            'input': 0,
            'cache_create': 0,
            'cache_read': 0,
            'output': 0,
            'total_input': 0,
            'cost': 0,
            'content': f"Parse error: {str(e)}"
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_session_context.py <session.jsonl>")
        sys.exit(1)
        
    session_file = sys.argv[1]
    
    # Read last N lines if specified
    lines_to_read = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    with open(session_file, 'r') as f:
        if lines_to_read:
            lines = f.readlines()[-lines_to_read:]
        else:
            lines = f.readlines()
    
    # Header
    print(f"{'Time':<19} {'Type':<10} {'Role':<10} {'Input':<6} {'C-New':<7} {'C-Read':<7} {'Output':<7} {'Total':<7} {'Cost':<8} Content")
    print("-" * 120)
    
    # Track running totals
    total_cost = 0
    total_cache = 0
    
    for line in lines:
        data = analyze_session_line(line)
        
        # Update running totals
        total_cost += data['cost']
        total_cache += data['cache_create']
        
        # Format output
        print(f"{data['timestamp']} {data['type']:<10} {data['role']:<10} "
              f"{data['input']:<6} {data['cache_create']:<7} {data['cache_read']:<7} "
              f"{data['output']:<7} {data['total_input']:<7} ${data['cost']:<7.4f} "
              f"{data['content']}")
    
    print("\n" + "=" * 120)
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Total cache created: {total_cache} tokens")

if __name__ == '__main__':
    main()