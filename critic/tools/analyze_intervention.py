#!/usr/bin/env python3
"""Analyze a specific @ADMIN intervention with context."""

import json
import sys
from pathlib import Path

def get_context_around_line(jsonl_file, target_line, before=5, after=5):
    """Get conversation context around a specific line number."""
    context = {
        'before': [],
        'target': None,
        'after': []
    }
    
    with open(jsonl_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                
                # Simplify the data for analysis
                simplified = {
                    'line': line_num,
                    'type': data.get('type'),
                    'userType': data.get('userType'),
                    'timestamp': data.get('timestamp'),
                    'uuid': data.get('uuid'),
                    'parentUuid': data.get('parentUuid')
                }
                
                # Extract message content
                if data.get('type') in ['user', 'assistant']:
                    message = data.get('message', {})
                    content = message.get('content', [])
                    text_parts = []
                    
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                            elif item.get('type') == 'tool_use':
                                text_parts.append(f"[TOOL: {item.get('name')}]")
                    
                    simplified['content'] = ' '.join(text_parts)[:200] + '...' if text_parts else '[No text content]'
                
                # Collect context
                if line_num < target_line - before:
                    continue
                elif line_num >= target_line - before and line_num < target_line:
                    context['before'].append(simplified)
                elif line_num == target_line:
                    context['target'] = simplified
                elif line_num > target_line and line_num <= target_line + after:
                    context['after'].append(simplified)
                elif line_num > target_line + after:
                    break
                    
            except json.JSONDecodeError:
                pass
    
    return context

def trace_conversation_thread(jsonl_file, target_uuid):
    """Trace the conversation thread leading to a specific message."""
    messages = {}
    
    # Load all messages
    with open(jsonl_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                uuid = data.get('uuid')
                if uuid:
                    messages[uuid] = {
                        'line': line_num,
                        'type': data.get('type'),
                        'userType': data.get('userType'),
                        'parentUuid': data.get('parentUuid'),
                        'content': extract_text_content(data)
                    }
            except json.JSONDecodeError:
                pass
    
    # Trace back from target
    thread = []
    current_uuid = target_uuid
    
    while current_uuid and current_uuid in messages:
        msg = messages[current_uuid]
        thread.insert(0, msg)  # Insert at beginning to maintain order
        current_uuid = msg.get('parentUuid')
        
        # Limit thread length to prevent infinite loops
        if len(thread) > 20:
            break
    
    return thread

def extract_text_content(data):
    """Extract text content from a message."""
    if data.get('type') not in ['user', 'assistant']:
        return '[Non-message type]'
        
    message = data.get('message', {})
    content = message.get('content', [])
    text_parts = []
    
    for item in content:
        if isinstance(item, dict):
            if item.get('type') == 'text':
                text_parts.append(item.get('text', ''))
            elif item.get('type') == 'tool_use':
                text_parts.append(f"[TOOL: {item.get('name')}]")
    
    return ' '.join(text_parts)[:300] + '...' if text_parts else '[No text content]'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: analyze_intervention.py <jsonl_file> <line_number>")
        sys.exit(1)
        
    jsonl_file = Path(sys.argv[1])
    target_line = int(sys.argv[2])
    
    if not jsonl_file.exists():
        print(f"File not found: {jsonl_file}")
        sys.exit(1)
    
    # Get context around the line
    context = get_context_around_line(jsonl_file, target_line, before=10, after=5)
    
    print(f"\n=== Context around line {target_line} ===")
    print("\nBEFORE:")
    for msg in context['before']:
        print(f"  L{msg['line']} [{msg['type']}/{msg.get('userType', 'agent')}]: {msg.get('content', '')}")
    
    print(f"\nTARGET (Line {target_line}):")
    if context['target']:
        print(f"  {context['target'].get('content', '')}")
        
        # Trace conversation thread
        print("\n=== Conversation Thread ===")
        thread = trace_conversation_thread(jsonl_file, context['target'].get('uuid'))
        for i, msg in enumerate(thread):
            indent = "  " * min(i, 3)
            print(f"{indent}L{msg['line']} [{msg['type']}/{msg.get('userType', 'agent')}]: {msg['content'][:100]}...")
    
    print("\nAFTER:")
    for msg in context['after']:
        print(f"  L{msg['line']} [{msg['type']}/{msg.get('userType', 'agent')}]: {msg.get('content', '')}")