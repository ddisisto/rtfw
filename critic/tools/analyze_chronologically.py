#!/usr/bin/env python3
"""Analyze sessions chronologically, tracking interventions and context switches."""

import json
import sys
from pathlib import Path
from datetime import datetime
from chronological_tracker import ChronologicalTracker

def analyze_event_batch(events, session_dir):
    """Analyze a batch of chronological events."""
    analysis = {
        'context_switches': [],
        'interventions': [],
        'agent_activity': {}
    }
    
    last_file = None
    last_agent = None
    
    for event in events:
        # Detect context switches
        if last_file and last_file != event['file']:
            # Try to determine agents involved
            from_agent = extract_agent_from_file(last_file, session_dir)
            to_agent = extract_agent_from_file(event['file'], session_dir)
            
            analysis['context_switches'].append({
                'timestamp': event['timestamp'],
                'from_file': last_file,
                'to_file': event['file'],
                'from_agent': from_agent,
                'to_agent': to_agent
            })
        
        # Look for external interventions
        if event.get('userType') == 'external' and event.get('type') == 'user':
            content = event.get('content', '')
            
            # Check for intervention patterns
            if any(marker in content.lower() for marker in [
                'wait', 'actually', 'instead', 'no,', 'stop', 
                'better idea', 'please', 'don\'t', 'should'
            ]):
                analysis['interventions'].append({
                    'timestamp': event['timestamp'],
                    'file': event['file'],
                    'line': event['line'],
                    'preview': content[:100] + '...' if len(content) > 100 else content
                })
        
        # Track agent activity
        agent = extract_agent_from_file(event['file'], session_dir)
        if agent not in analysis['agent_activity']:
            analysis['agent_activity'][agent] = {
                'first_seen': event['timestamp'],
                'last_seen': event['timestamp'],
                'event_count': 0
            }
        analysis['agent_activity'][agent]['last_seen'] = event['timestamp']
        analysis['agent_activity'][agent]['event_count'] += 1
        
        last_file = event['file']
        last_agent = agent
    
    return analysis

def extract_agent_from_file(file_name, session_dir):
    """Try to extract agent name from session file."""
    # Quick scan for init commands
    file_path = Path(session_dir) / file_name
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('type') == 'user':
                    content = str(data.get('message', {}).get('content', ''))
                    if 'init @' in content:
                        start = content.find('init @') + 6
                        end = content.find('.md', start)
                        if end > start:
                            return content[start:end]
            except:
                pass
    return "UNKNOWN"

def main():
    tracker = ChronologicalTracker("/home/daniel/prj/rtfw/nexus/sessions")
    
    # Get next batch of events
    print("=== CHRONOLOGICAL ANALYSIS - NEXT 20 EVENTS ===\n")
    events = tracker.get_next_events(20)
    
    if not events:
        print("No unprocessed events found.")
        return
    
    # Analyze the batch
    analysis = analyze_event_batch(events, "/home/daniel/prj/rtfw/nexus/sessions")
    
    # Report findings
    print(f"Time Range: {events[0]['timestamp'][:19]} to {events[-1]['timestamp'][:19]}")
    print(f"Events Processed: {len(events)}")
    
    print(f"\n--- Context Switches: {len(analysis['context_switches'])} ---")
    for switch in analysis['context_switches']:
        print(f"{switch['timestamp'][:19]}: {switch['from_agent']} → {switch['to_agent']}")
    
    print(f"\n--- Potential Interventions: {len(analysis['interventions'])} ---")
    for interv in analysis['interventions']:
        print(f"{interv['timestamp'][:19]} in {interv['file']}:")
        print(f"  Line {interv['line']}: {interv['preview']}")
    
    print(f"\n--- Agent Activity ---")
    for agent, activity in analysis['agent_activity'].items():
        print(f"{agent}: {activity['event_count']} events")
    
    # Mark last event as processed
    if events:
        last_event = events[-1]
        tracker.mark_processed(last_event['timestamp'], last_event['file'])
        print(f"\n✓ Progress saved. Last processed: {last_event['timestamp']}")

if __name__ == '__main__':
    main()