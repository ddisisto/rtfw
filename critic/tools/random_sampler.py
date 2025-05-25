#!/usr/bin/env python3
"""
Random sampling of session interactions for pattern discovery.
Different from chronological analysis - may reveal patterns that time-ordered review misses.
"""

import json
import random
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

def load_all_interactions(sessions_dir: Path) -> List[Dict[str, Any]]:
    """Load all interactions from all session files."""
    all_interactions = []
    
    for session_file in sessions_dir.glob("*.jsonl"):
        with open(session_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    # Include session file for context
                    entry['session_file'] = session_file.name
                    all_interactions.append(entry)
                except json.JSONDecodeError:
                    continue
    
    return all_interactions

def filter_human_interactions(interactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter to only human interventions (excluding tool results)."""
    human_interactions = []
    
    for entry in interactions:
        # Human messages
        if entry.get('type') == 'user' and entry.get('userType') == 'external':
            # Extract content to check if it's a tool result
            content = ''
            if 'message' in entry and isinstance(entry['message'], dict):
                msg_content = entry['message'].get('content', '')
                if isinstance(msg_content, str):
                    content = msg_content
                elif isinstance(msg_content, dict) and 'tool_use_id' in msg_content:
                    # Skip tool results
                    continue
            
            # Only add if it has real text content
            if content and not content.startswith('{'):
                human_interactions.append(entry)
    
    return human_interactions

def random_sample_interactions(interactions: List[Dict[str, Any]], sample_size: int = 20) -> List[Dict[str, Any]]:
    """Randomly sample interactions."""
    # Ensure we don't sample more than available
    sample_size = min(sample_size, len(interactions))
    return random.sample(interactions, sample_size)

def analyze_sample(sample: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze a random sample for patterns."""
    analysis = {
        'sample_size': len(sample),
        'agent_distribution': defaultdict(int),
        'intervention_types': defaultdict(int),
        'common_phrases': defaultdict(int),
        'interactions': []
    }
    
    for entry in sample:
        # Extract agent from session file
        agent = entry['session_file'].split('-')[0].upper()
        analysis['agent_distribution'][agent] += 1
        
        # Extract content from nested message structure
        content = ''
        if 'message' in entry and isinstance(entry['message'], dict):
            msg_content = entry['message'].get('content', '')
            if isinstance(msg_content, str):
                content = msg_content.lower()
            elif isinstance(msg_content, list):
                # Handle list content (might be multi-part messages)
                content = ' '.join(str(part) for part in msg_content).lower()
        else:
            content = str(entry.get('content', '')).lower()
        if 'nope' in content or "don't" in content:
            analysis['intervention_types']['correction'] += 1
        elif 'great' in content or 'good' in content:
            analysis['intervention_types']['approval'] += 1
        elif '?' in content:
            analysis['intervention_types']['question'] += 1
        elif '->' in content or '→' in content:
            analysis['intervention_types']['routing'] += 1
        else:
            analysis['intervention_types']['other'] += 1
        
        # Track common phrases
        phrases = ['my bad', 'one at a time', 'directly', 'instead', 'please', 'thanks']
        for phrase in phrases:
            if phrase in content:
                analysis['common_phrases'][phrase] += 1
        
        # Store interaction details
        analysis['interactions'].append({
            'timestamp': entry.get('timestamp', entry.get('createdAt', 'unknown')),
            'agent': agent,
            'type': entry.get('type'),
            'content_preview': content[:200] + '...' if len(content) > 200 else content,
            'session': entry['session_file']
        })
    
    return analysis

def main():
    sessions_dir = Path("/home/daniel/prj/rtfw/nexus/sessions")
    
    print("Loading all interactions...")
    all_interactions = load_all_interactions(sessions_dir)
    print(f"Total interactions found: {len(all_interactions)}")
    
    print("\nFiltering for human interactions...")
    human_interactions = filter_human_interactions(all_interactions)
    print(f"Human interactions found: {len(human_interactions)}")
    
    print("\nTaking random sample...")
    sample = random_sample_interactions(human_interactions, sample_size=30)
    
    print("\nAnalyzing sample...")
    analysis = analyze_sample(sample)
    
    # Output results
    print("\n=== RANDOM SAMPLE ANALYSIS ===")
    print(f"\nSample size: {analysis['sample_size']}")
    
    print("\nAgent distribution:")
    for agent, count in sorted(analysis['agent_distribution'].items()):
        print(f"  {agent}: {count}")
    
    print("\nIntervention types:")
    for itype, count in sorted(analysis['intervention_types'].items()):
        print(f"  {itype}: {count}")
    
    print("\nCommon phrases:")
    for phrase, count in sorted(analysis['common_phrases'].items(), key=lambda x: x[1], reverse=True):
        print(f"  '{phrase}': {count}")
    
    print("\nRandom sample interactions:")
    for i, interaction in enumerate(analysis['interactions'][:10], 1):
        print(f"\n{i}. [{interaction['timestamp']}] {interaction['agent']} - {interaction['type']}")
        print(f"   Session: {interaction['session']}")
        print(f"   Content: {interaction['content_preview']}")
    
    # Save full analysis
    output_file = Path("/home/daniel/prj/rtfw/critic/analysis/random_sample_analysis.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"\nFull analysis saved to: {output_file}")

if __name__ == "__main__":
    # Set random seed for reproducibility (can remove for true randomness)
    # random.seed(42)
    main()