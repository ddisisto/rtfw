#!/usr/bin/env python3
"""
Targeted sampling for specific patterns or time periods.
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

def load_all_interactions(sessions_dir: Path) -> List[Dict[str, Any]]:
    """Load all interactions from all session files."""
    all_interactions = []
    
    for session_file in sessions_dir.glob("*.jsonl"):
        with open(session_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry['session_file'] = session_file.name
                    all_interactions.append(entry)
                except json.JSONDecodeError:
                    continue
    
    return all_interactions

def filter_human_messages(interactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter to only real human messages (not tool results)."""
    human_messages = []
    
    for entry in interactions:
        if entry.get('type') == 'user' and entry.get('userType') == 'external':
            # Extract content
            content = ''
            if 'message' in entry and isinstance(entry['message'], dict):
                msg_content = entry['message'].get('content', '')
                if isinstance(msg_content, str):
                    content = msg_content
                elif isinstance(msg_content, dict) and 'tool_use_id' in msg_content:
                    continue  # Skip tool results
            
            # Only add if it has real text content
            if content and not content.startswith('{'):
                entry['extracted_content'] = content
                human_messages.append(entry)
    
    return human_messages

def sample_by_pattern(messages: List[Dict[str, Any]], pattern: str, sample_size: int = 10) -> List[Dict[str, Any]]:
    """Sample messages containing specific pattern."""
    matching = [msg for msg in messages if pattern.lower() in msg['extracted_content'].lower()]
    return random.sample(matching, min(sample_size, len(matching)))

def sample_by_time_period(messages: List[Dict[str, Any]], start_hour: int, end_hour: int, sample_size: int = 10) -> List[Dict[str, Any]]:
    """Sample messages from specific time period (by hour of day)."""
    time_filtered = []
    for msg in messages:
        if 'timestamp' in msg:
            try:
                dt = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                if start_hour <= dt.hour < end_hour:
                    time_filtered.append(msg)
            except:
                continue
    
    return random.sample(time_filtered, min(sample_size, len(time_filtered)))

def get_contiguous_batch(messages: List[Dict[str, Any]], start_idx: Optional[int] = None, batch_size: int = 10) -> List[Dict[str, Any]]:
    """Get contiguous messages starting from index or random."""
    if start_idx is None:
        start_idx = random.randint(0, max(0, len(messages) - batch_size))
    
    return messages[start_idx:start_idx + batch_size]

def analyze_batch(batch: List[Dict[str, Any]], batch_name: str = "Batch"):
    """Analyze and display a batch of messages."""
    print(f"\n=== {batch_name} ===")
    print(f"Size: {len(batch)}")
    
    if not batch:
        print("No messages found matching criteria")
        return
    
    # Time range
    timestamps = [msg['timestamp'] for msg in batch if 'timestamp' in msg]
    if timestamps:
        print(f"Time range: {min(timestamps)} to {max(timestamps)}")
    
    # Content analysis
    total_length = sum(len(msg['extracted_content']) for msg in batch)
    avg_length = total_length // len(batch) if batch else 0
    print(f"Average message length: {avg_length} chars")
    
    # Show messages
    print("\nMessages:")
    for i, msg in enumerate(batch[:10], 1):  # Show max 10
        content = msg['extracted_content']
        preview = content[:150] + "..." if len(content) > 150 else content
        agent = msg['session_file'].split('-')[0].upper()
        timestamp = msg.get('timestamp', 'unknown')
        
        print(f"\n{i}. [{timestamp}] Session: {agent}")
        print(f"   {preview}")
    
    return batch

# Quick analysis functions for interactive use
def get_corrections_batch(messages: List[Dict[str, Any]], size: int = 10):
    """Get batch of correction messages."""
    corrections = [msg for msg in messages 
                  if any(word in msg['extracted_content'].lower() 
                        for word in ['nope', "don't", 'actually', 'instead', 'my bad'])]
    return random.sample(corrections, min(size, len(corrections)))

def get_approvals_batch(messages: List[Dict[str, Any]], size: int = 10):
    """Get batch of approval messages."""
    approvals = [msg for msg in messages 
                if any(word in msg['extracted_content'].lower() 
                      for word in ['great', 'nice', 'cool', 'good', 'excellent', 'perfect'])]
    return random.sample(approvals, min(size, len(approvals)))

def get_questions_batch(messages: List[Dict[str, Any]], size: int = 10):
    """Get batch of question messages."""
    questions = [msg for msg in messages if '?' in msg['extracted_content']]
    return random.sample(questions, min(size, len(questions)))

def main():
    """Run targeted analysis based on command line args or interactive."""
    sessions_dir = Path("/home/daniel/prj/rtfw/nexus/sessions")
    
    print("Loading interactions...")
    all_interactions = load_all_interactions(sessions_dir)
    human_messages = filter_human_messages(all_interactions)
    print(f"Found {len(human_messages)} human messages")
    
    # Example analyses
    print("\n" + "="*50)
    
    # 1. Random contiguous batch
    batch1 = get_contiguous_batch(human_messages, batch_size=15)
    analyze_batch(batch1, "Random Contiguous Batch (15 messages)")
    
    # 2. Corrections batch
    batch2 = get_corrections_batch(human_messages)
    analyze_batch(batch2, "Corrections Sample")
    
    # 3. Morning messages (assuming UTC)
    batch3 = sample_by_time_period(human_messages, 5, 12, sample_size=10)
    analyze_batch(batch3, "Morning Messages (5am-12pm UTC)")
    
    # 4. Protocol discussions
    batch4 = sample_by_pattern(human_messages, "protocol", sample_size=10)
    analyze_batch(batch4, "Protocol Discussions")

if __name__ == "__main__":
    main()