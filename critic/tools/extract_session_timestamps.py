#!/usr/bin/env python3
"""Extract first and last timestamps from each session file."""

import json
from pathlib import Path
import csv

def get_first_last_timestamps(session_file: Path):
    """Get first and last timestamps from a session file."""
    first_ts = None
    last_ts = None
    
    with open(session_file, 'r') as f:
        # Get first timestamp
        for line in f:
            try:
                entry = json.loads(line.strip())
                if 'timestamp' in entry and entry['timestamp']:
                    first_ts = entry['timestamp']
                    break
            except json.JSONDecodeError:
                continue
        
        # Get last timestamp by reading file again from end
        # More efficient than loading entire file
        f.seek(0)
        lines = f.readlines()
        
        for line in reversed(lines):
            try:
                entry = json.loads(line.strip())
                if 'timestamp' in entry and entry['timestamp']:
                    last_ts = entry['timestamp']
                    break
            except json.JSONDecodeError:
                continue
    
    return first_ts, last_ts

def main():
    session_dir = Path("/home/daniel/prj/rtfw/nexus/sessions")
    
    # Read existing CSV
    existing_data = {}
    with open('/home/daniel/prj/rtfw/critic/sessions_index.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_data[row['sessionId']] = row
    
    # Update with last timestamps
    results = []
    for session_id, data in existing_data.items():
        session_file = session_dir / f"{session_id}.jsonl"
        if session_file.exists():
            first_ts, last_ts = get_first_last_timestamps(session_file)
            data['last_ts'] = last_ts if last_ts else 'UNKNOWN'
            # Verify first_ts matches
            if first_ts and data['start_ts'] == 'UNKNOWN':
                data['start_ts'] = first_ts
        else:
            data['last_ts'] = 'UNKNOWN'
        
        results.append(data)
    
    # Sort by start timestamp
    results.sort(key=lambda x: x['start_ts'] if x['start_ts'] != 'UNKNOWN' else '9999')
    
    # Write updated CSV
    with open('/home/daniel/prj/rtfw/critic/sessions_index.csv', 'w', newline='') as f:
        fieldnames = ['sessionId', 'agent', 'start_ts', 'last_ts']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print("Updated sessions_index.csv with last timestamps")
    
    # Show summary
    print("\nSession time ranges:")
    for row in results:
        if row['start_ts'] != 'UNKNOWN' and row['last_ts'] != 'UNKNOWN':
            print(f"{row['agent']:12} {row['sessionId']}: {row['start_ts'][:16]} → {row['last_ts'][:16]}")

if __name__ == '__main__':
    main()