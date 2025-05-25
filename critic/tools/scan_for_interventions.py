#!/usr/bin/env python3
"""Scan all sessions for @ADMIN interventions with context."""

import json
from pathlib import Path
from datetime import datetime

def scan_all_interventions(session_dir):
    """Scan all sessions for interventions chronologically."""
    all_interventions = []
    
    for jsonl_file in Path(session_dir).glob("*.jsonl"):
        with open(jsonl_file, 'r') as f:
            prev_content = None
            prev_type = None
            
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line)
                    
                    # Track previous assistant message
                    if data.get('type') == 'assistant':
                        message = data.get('message', {})
                        content = message.get('content', [])
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                        prev_content = ' '.join(text_parts)
                        prev_type = 'assistant'
                    
                    # Look for external interventions
                    if data.get('type') == 'user' and data.get('userType') == 'external':
                        message = data.get('message', {})
                        content = message.get('content', [])
                        
                        # Skip tool results
                        if any(item.get('type') == 'tool_result' for item in content if isinstance(item, dict)):
                            continue
                        
                        # Extract text
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                        
                        user_text = ' '.join(text_parts)
                        
                        # Skip empty or command messages
                        if not user_text or '<command-message>' in user_text:
                            continue
                        
                        # Intervention patterns
                        intervention_markers = [
                            'wait', 'actually', 'instead', 'no,', 'stop',
                            'better idea', 'please', "don't", 'should',
                            'correction', 'wrong', 'not quite', 'hold on',
                            'let me', "that's not", '@admin', 'prefer'
                        ]
                        
                        if any(marker in user_text.lower() for marker in intervention_markers):
                            all_interventions.append({
                                'timestamp': data.get('timestamp'),
                                'file': jsonl_file.name,
                                'line': line_num,
                                'text': user_text[:300] + '...' if len(user_text) > 300 else user_text,
                                'context': (prev_content[:200] + '...') if prev_content and len(prev_content) > 200 else prev_content
                            })
                    
                except json.JSONDecodeError:
                    pass
    
    # Sort by timestamp
    all_interventions.sort(key=lambda x: x['timestamp'])
    return all_interventions

def main():
    interventions = scan_all_interventions("/home/daniel/prj/rtfw/nexus/sessions")
    
    print(f"=== FOUND {len(interventions)} INTERVENTIONS ===\n")
    
    for i, interv in enumerate(interventions[:10]):  # First 10
        print(f"--- Intervention {i+1} ---")
        print(f"Time: {interv['timestamp'][:19]}")
        print(f"File: {interv['file']}")
        print(f"Line: {interv['line']}")
        if interv.get('context'):
            print(f"Context: {interv['context']}")
        print(f"Intervention: {interv['text']}")
        print()

if __name__ == '__main__':
    main()