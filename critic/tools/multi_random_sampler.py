#!/usr/bin/env python3
"""
Multiple random samples to identify patterns that chronological analysis might miss.
"""

import json
import random
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any
import sys
sys.path.append(str(Path(__file__).parent))
from random_sampler import load_all_interactions, filter_human_interactions

def categorize_intervention(content: str) -> str:
    """More detailed categorization of interventions."""
    content_lower = content.lower()
    
    # Priority categorization
    if '→' in content or '->' in content:
        if any(word in content_lower for word in ['restore', 'reload', 'resuming']):
            return 'restore_command'
        return 'routing_message'
    
    # Direct corrections
    if any(phrase in content_lower for phrase in ['nope', "don't", 'no, ', 'actually,']):
        return 'direct_correction'
    
    # Gentle corrections
    if 'my bad' in content_lower or 'should have been clearer' in content_lower:
        return 'gentle_correction'
    
    # Approvals
    if any(word in content_lower for word in ['great', 'nice', 'cool', 'good', 'excellent']):
        return 'approval'
    
    # Questions
    if '?' in content:
        return 'question'
    
    # Commands
    if any(word in content_lower for word in ['please', 'can you', 'could you']):
        return 'polite_command'
    
    # Meta/process
    if any(word in content_lower for word in ['process', 'protocol', 'idea', 'wondering']):
        return 'process_discussion'
    
    return 'other'

def extract_themes(interactions: List[Dict[str, Any]]) -> Dict[str, int]:
    """Extract thematic patterns from interactions."""
    themes = defaultdict(int)
    
    for entry in interactions:
        content = ''
        if 'message' in entry and isinstance(entry['message'], dict):
            content = entry['message'].get('content', '')
        
        content_lower = content.lower()
        
        # Thematic keywords
        if 'context' in content_lower:
            themes['context_management'] += 1
        if any(word in content_lower for word in ['compress', 'distill', 'consolidat']):
            themes['memory_optimization'] += 1
        if 'protocol' in content_lower:
            themes['protocol_design'] += 1
        if any(word in content_lower for word in ['tmux', 'session', 'monitor']):
            themes['infrastructure'] += 1
        if any(word in content_lower for word in ['agent', 'role', '@']):
            themes['agent_coordination'] += 1
        if 'git' in content_lower or 'commit' in content_lower:
            themes['version_control'] += 1
        if any(word in content_lower for word in ['idea', 'wonder', 'think']):
            themes['ideation'] += 1
            
    return themes

def run_multiple_samples(interactions: List[Dict[str, Any]], num_runs: int = 5, sample_size: int = 50):
    """Run multiple random samples to find consistent patterns."""
    
    aggregate_patterns = {
        'intervention_types': defaultdict(int),
        'themes': defaultdict(int),
        'agent_distribution': defaultdict(int),
        'phrases': defaultdict(int),
        'unique_insights': []
    }
    
    for run in range(num_runs):
        # Random sample
        sample = random.sample(interactions, min(sample_size, len(interactions)))
        
        print(f"\n=== Sample Run {run + 1} ===")
        
        # Analyze sample
        for entry in sample:
            # Agent
            agent = entry['session_file'].split('-')[0].upper()
            aggregate_patterns['agent_distribution'][agent] += 1
            
            # Content
            content = ''
            if 'message' in entry and isinstance(entry['message'], dict):
                content = entry['message'].get('content', '')
            
            # Intervention type
            intervention_type = categorize_intervention(content)
            aggregate_patterns['intervention_types'][intervention_type] += 1
            
            # Common phrases
            content_lower = content.lower()
            for phrase in ['please', 'thanks', 'my bad', 'one at a time', 'directly', 'instead']:
                if phrase in content_lower:
                    aggregate_patterns['phrases'][phrase] += 1
            
            # Look for unique insights
            if len(content) > 100 and intervention_type == 'process_discussion':
                aggregate_patterns['unique_insights'].append({
                    'timestamp': entry.get('timestamp', 'unknown'),
                    'preview': content[:150] + '...'
                })
        
        # Extract themes
        themes = extract_themes(sample)
        for theme, count in themes.items():
            aggregate_patterns['themes'][theme] += count
        
        # Show sample stats
        print(f"Sample size: {len(sample)}")
        print(f"Top intervention type: {max(aggregate_patterns['intervention_types'].items(), key=lambda x: x[1])[0]}")
        print(f"Top theme: {max(aggregate_patterns['themes'].items(), key=lambda x: x[1])[0] if aggregate_patterns['themes'] else 'none'}")
    
    return aggregate_patterns

def main():
    sessions_dir = Path("/home/daniel/prj/rtfw/nexus/sessions")
    
    print("Loading all interactions...")
    all_interactions = load_all_interactions(sessions_dir)
    
    print("Filtering for human interactions...")
    human_interactions = filter_human_interactions(all_interactions)
    print(f"Total human interactions: {len(human_interactions)}")
    
    # Run multiple samples
    patterns = run_multiple_samples(human_interactions, num_runs=5, sample_size=50)
    
    # Aggregate results
    print("\n\n=== AGGREGATE PATTERNS ACROSS ALL SAMPLES ===")
    
    print("\nIntervention Types (total counts):")
    for itype, count in sorted(patterns['intervention_types'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {itype}: {count}")
    
    print("\nThemes (total counts):")
    for theme, count in sorted(patterns['themes'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {theme}: {count}")
    
    print("\nCommon Phrases:")
    for phrase, count in sorted(patterns['phrases'].items(), key=lambda x: x[1], reverse=True):
        if count > 5:  # Only show frequent ones
            print(f"  '{phrase}': {count}")
    
    print("\nAgent Distribution:")
    top_agents = sorted(patterns['agent_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]
    for agent, count in top_agents:
        print(f"  {agent}: {count}")
    
    print(f"\nUnique Process Insights Found: {len(patterns['unique_insights'])}")
    for i, insight in enumerate(patterns['unique_insights'][:5], 1):
        print(f"\n{i}. [{insight['timestamp']}]")
        print(f"   {insight['preview']}")
    
    # Save full analysis
    output_file = Path("/home/daniel/prj/rtfw/critic/analysis/multi_random_analysis.json")
    with open(output_file, 'w') as f:
        # Convert defaultdicts to regular dicts for JSON serialization
        save_patterns = {
            'intervention_types': dict(patterns['intervention_types']),
            'themes': dict(patterns['themes']),
            'agent_distribution': dict(patterns['agent_distribution']),
            'phrases': dict(patterns['phrases']),
            'unique_insights': patterns['unique_insights']
        }
        json.dump(save_patterns, f, indent=2)
    
    print(f"\nFull analysis saved to: {output_file}")

if __name__ == "__main__":
    main()