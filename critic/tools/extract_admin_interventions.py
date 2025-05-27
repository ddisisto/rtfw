#!/usr/bin/env python3
"""Extract @ADMIN interventions from session files with context."""

import json
import os
import re
from datetime import datetime
from pathlib import Path

def extract_user_type(entry):
    """Determine if message is from human or agent."""
    if entry.get('type') == 'user':
        # Check userType field first
        if entry.get('userType') == 'external':
            return 'human'
        elif entry.get('userType') == 'agent':
            return 'agent'
            
        # Fallback to content analysis
        text = extract_message_text(entry)
        # Agent messages contain → or start with @
        if '→' in text or re.match(r'^@[A-Z]+', text):
            return 'agent'
        else:
            return 'human'
    return 'assistant'

def extract_message_text(entry):
    """Extract actual message text from various formats."""
    # Check for message.content structure
    message = entry.get('message', {})
    if message and 'content' in message:
        return str(message['content'])
    
    # Fallback to direct content
    content = entry.get('content', {})
    if isinstance(content, dict):
        return content.get('text', str(content))
    return str(content)

def main():
    sessions_dir = Path('nexus/sessions')
    output_file = Path('critic/analysis/outputs/2025-01-27_admin_interventions.json')
    
    # Get all session files
    target_files = [f.name for f in sessions_dir.glob('*.jsonl')]
    
    interventions = []
    
    for filename in target_files:
        filepath = sessions_dir / filename
        if not filepath.exists():
            continue
            
        with open(filepath, 'r') as f:
            entries = []
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entries.append(entry)
                except:
                    continue
            
            # Find @ADMIN messages
            for i, entry in enumerate(entries):
                user_type = extract_user_type(entry)
                if user_type == 'human':
                    text = extract_message_text(entry)
                    
                    # Check if it's actually an @ADMIN intervention
                    # Skip tool results and system messages
                    if 'tool_use_id' in text or 'tool_result' in text:
                        continue
                    if '[Request interrupted' in text:
                        continue
                    if 'Caveat: The messages below' in text:
                        continue
                        
                    if '@ADMIN' in text or ('admin' in text.lower() and not '→' in text):
                        # Get context (3 before, 3 after)
                        context_start = max(0, i - 3)
                        context_end = min(len(entries), i + 4)
                        
                        context = []
                        for j in range(context_start, context_end):
                            context_entry = entries[j]
                            context.append({
                                'index': j,
                                'timestamp': context_entry.get('timestamp', ''),
                                'type': context_entry.get('type', ''),
                                'user_type': extract_user_type(context_entry),
                                'text': extract_message_text(context_entry),
                                'is_intervention': j == i
                            })
                        
                        interventions.append({
                            'session_id': filename.replace('.jsonl', ''),
                            'timestamp': entry.get('timestamp', ''),
                            'intervention_text': text,
                            'context': context
                        })
    
    # Sort by timestamp
    interventions.sort(key=lambda x: x['timestamp'])
    
    # Save results
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(interventions, f, indent=2)
    
    print(f"Extracted {len(interventions)} @ADMIN interventions")
    print(f"Results saved to: {output_file}")
    
    # Also create a summary
    print("\nIntervention Summary:")
    for inv in interventions:
        timestamp = inv['timestamp'][:16] if inv['timestamp'] else 'Unknown'
        text_preview = inv['intervention_text'][:100] + '...' if len(inv['intervention_text']) > 100 else inv['intervention_text']
        print(f"{timestamp}: {text_preview}")

if __name__ == '__main__':
    main()