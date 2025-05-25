#!/usr/bin/env python3
"""Track chronological flow across multiple interleaved session files."""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import heapq

class ChronologicalTracker:
    def __init__(self, session_dir: str):
        self.session_dir = Path(session_dir)
        self.progress_file = Path("critic/progress/chronological_progress.json")
        self.progress = self.load_progress()
        
    def load_progress(self) -> Dict:
        """Load tracking progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            "sessions": {},  # file -> last_processed_timestamp
            "current_position": None
        }
    
    def save_progress(self):
        """Save current progress."""
        self.progress_file.parent.mkdir(exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def scan_session_files(self) -> List[Tuple[str, str, str]]:
        """Scan all session files and get their date ranges."""
        results = []
        
        for jsonl_file in sorted(self.session_dir.glob("*.jsonl")):
            first_ts = None
            last_ts = None
            agent = None
            
            with open(jsonl_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if 'timestamp' in data:
                            ts = data['timestamp']
                            if not first_ts:
                                first_ts = ts
                            last_ts = ts
                            
                        # Try to identify agent from content
                        if data.get('type') == 'user' and not agent:
                            content = str(data.get('message', {}).get('content', ''))
                            if 'init @' in content:
                                # Extract agent name from init command
                                start = content.find('init @') + 6
                                end = content.find('.md', start)
                                if end > start:
                                    agent = content[start:end]
                    except:
                        pass
            
            if first_ts and last_ts:
                results.append((
                    str(jsonl_file.name),
                    first_ts,
                    last_ts,
                    agent or "UNKNOWN"
                ))
        
        return sorted(results, key=lambda x: x[1])  # Sort by start time
    
    def get_next_events(self, limit: int = 10) -> List[Dict]:
        """Get next N events in chronological order across all files."""
        # Priority queue of (timestamp, file, line_num, data)
        heap = []
        
        # Initialize heap with first unprocessed event from each file
        for jsonl_file in self.session_dir.glob("*.jsonl"):
            file_name = str(jsonl_file.name)
            last_processed = self.progress.get("sessions", {}).get(file_name)
            
            with open(jsonl_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        ts = data.get('timestamp')
                        if ts:
                            # Skip if already processed
                            if last_processed and ts <= last_processed:
                                continue
                            
                            # Add to heap
                            heapq.heappush(heap, (ts, file_name, line_num, data))
                            break  # Only need first unprocessed
                    except:
                        pass
        
        # Extract next N events
        events = []
        while heap and len(events) < limit:
            ts, file_name, line_num, data = heapq.heappop(heap)
            
            # Simplify event data
            event = {
                'timestamp': ts,
                'file': file_name,
                'line': line_num,
                'type': data.get('type'),
                'userType': data.get('userType')
            }
            
            # Extract meaningful content
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
                
                event['content'] = ' '.join(text_parts)[:200] + '...' if text_parts else ''
            
            events.append(event)
            
            # Try to get next event from same file
            with open(self.session_dir / file_name, 'r') as f:
                for i, line in enumerate(f, 1):
                    if i <= line_num:
                        continue
                    try:
                        data = json.loads(line)
                        next_ts = data.get('timestamp')
                        if next_ts:
                            heapq.heappush(heap, (next_ts, file_name, i, data))
                            break
                    except:
                        pass
        
        return events
    
    def mark_processed(self, timestamp: str, file_name: str):
        """Mark an event as processed."""
        if "sessions" not in self.progress:
            self.progress["sessions"] = {}
        self.progress["sessions"][file_name] = timestamp
        self.progress["current_position"] = timestamp
        self.save_progress()

def main():
    tracker = ChronologicalTracker("/home/daniel/prj/rtfw/nexus/sessions")
    
    # Show session overview
    print("=== SESSION FILES OVERVIEW ===")
    sessions = tracker.scan_session_files()
    for file_name, start, end, agent in sessions:
        print(f"{file_name}: {start[:16]} to {end[:16]} [{agent}]")
    
    print(f"\nTotal sessions: {len(sessions)}")
    
    # Show next events
    print("\n=== NEXT EVENTS ===")
    events = tracker.get_next_events(5)
    
    last_file = None
    for event in events:
        # Note context switches
        if last_file and last_file != event['file']:
            print(f"\n[CONTEXT SWITCH: {last_file} → {event['file']}]")
        last_file = event['file']
        
        print(f"\n{event['timestamp'][:19]} [{event['type']}/{event.get('userType', 'agent')}] in {event['file']}:")
        if 'content' in event:
            print(f"  {event['content']}")

if __name__ == '__main__':
    main()