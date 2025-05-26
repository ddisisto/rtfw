#!/usr/bin/env python3
"""
Build comprehensive session index for CRITIC analysis.
Identifies all sessions, their agents, time ranges, and key characteristics.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any

def analyze_session_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a single session file to extract key metadata."""
    session_info = {
        'filename': file_path.name,
        'session_id': file_path.stem,
        'agent': None,
        'start_time': None,
        'end_time': None,
        'message_count': 0,
        'has_summary': False,
        'key_topics': set(),
        'mentioned_agents': set()
    }
    
    timestamps = []
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f):
            try:
                entry = json.loads(line.strip())
                
                # First line often has summary
                if line_num == 0 and entry.get('type') == 'summary':
                    session_info['has_summary'] = True
                    session_info['summary'] = entry.get('summary', '')
                
                # Count messages
                if entry.get('type') in ['user', 'assistant']:
                    session_info['message_count'] += 1
                
                # Track timestamps
                if 'timestamp' in entry:
                    timestamps.append(entry['timestamp'])
                
                # Extract content for analysis
                content = ''
                if 'message' in entry and isinstance(entry['message'], dict):
                    content = entry['message'].get('content', '')
                    if isinstance(content, list):
                        content = ' '.join(str(item) for item in content)
                
                # Identify agent from messages
                if content and isinstance(content, str):
                    # Check for agent identification patterns
                    if '@GOV' in content or 'governance' in content.lower():
                        session_info['key_topics'].add('governance')
                    if '@BUILD' in content:
                        session_info['key_topics'].add('build')
                    if '@NEXUS' in content:
                        session_info['key_topics'].add('nexus')
                    if '@CRITIC' in content:
                        session_info['key_topics'].add('critic')
                    
                    # Look for agent mentions
                    for agent in ['@GOV', '@NEXUS', '@BUILD', '@CRITIC', '@ARCHITECT', '@TEST', '@RESEARCH']:
                        if agent in content:
                            session_info['mentioned_agents'].add(agent)
                    
                    # Topic detection
                    if 'protocol' in content.lower():
                        session_info['key_topics'].add('protocol')
                    if 'session' in content.lower():
                        session_info['key_topics'].add('session-management')
                    if 'distill' in content.lower():
                        session_info['key_topics'].add('distillation')
                        
            except json.JSONDecodeError:
                continue
    
    # Set time range
    if timestamps:
        session_info['start_time'] = min(timestamps)
        session_info['end_time'] = max(timestamps)
        
        # Try to guess agent from timing patterns (early sessions)
        try:
            start_dt = datetime.fromisoformat(session_info['start_time'].replace('Z', '+00:00'))
            # Very early sessions (May 21) likely GOV or NEXUS setup
            if start_dt.month == 5 and start_dt.day == 21:
                if 'governance' in session_info['key_topics'] or '@GOV' in session_info['mentioned_agents']:
                    session_info['likely_agent'] = 'GOV'
                elif 'nexus' in session_info['key_topics'] or '@NEXUS' in session_info['mentioned_agents']:
                    session_info['likely_agent'] = 'NEXUS'
        except:
            pass
    
    # Convert sets to lists for JSON serialization
    session_info['key_topics'] = list(session_info['key_topics'])
    session_info['mentioned_agents'] = list(session_info['mentioned_agents'])
    
    return session_info

def build_comprehensive_index(sessions_dir: Path) -> Dict[str, Any]:
    """Build complete index of all sessions."""
    all_sessions = []
    
    for session_file in sorted(sessions_dir.glob("*.jsonl")):
        print(f"Analyzing {session_file.name}...")
        session_info = analyze_session_file(session_file)
        all_sessions.append(session_info)
    
    # Sort by start time
    all_sessions.sort(key=lambda x: x['start_time'] or '9999')
    
    # Group by likely agent
    by_agent = defaultdict(list)
    for session in all_sessions:
        agent = session.get('likely_agent', 'UNKNOWN')
        by_agent[agent].append(session)
    
    # Find earliest sessions
    earliest_10 = all_sessions[:10]
    
    return {
        'total_sessions': len(all_sessions),
        'earliest_session': all_sessions[0] if all_sessions else None,
        'latest_session': all_sessions[-1] if all_sessions else None,
        'by_agent': dict(by_agent),
        'earliest_10': earliest_10,
        'all_sessions': all_sessions
    }

def create_session_log(index: Dict[str, Any]) -> str:
    """Create CRITIC's version of session log."""
    log_lines = ["# CRITIC Session Index", 
                 "# Complete analysis of all session files",
                 f"# Generated: {datetime.now().isoformat()}",
                 "# Format: TIMESTAMP AGENT/TOPIC SESSION_ID",
                 ""]
    
    for session in index['all_sessions']:
        timestamp = session['start_time'][:16] if session['start_time'] else 'UNKNOWN'
        agent = session.get('likely_agent', 'UNKNOWN')
        topics = ','.join(session['key_topics'][:2]) if session['key_topics'] else 'general'
        session_id = session['session_id']
        
        log_lines.append(f"{timestamp} {agent}/{topics} {session_id}")
    
    return '\n'.join(log_lines)

def main():
    sessions_dir = Path("/home/daniel/prj/rtfw/nexus/sessions")
    output_dir = Path("/home/daniel/prj/rtfw/critic/analysis")
    output_dir.mkdir(exist_ok=True)
    
    print("Building comprehensive session index...")
    index = build_comprehensive_index(sessions_dir)
    
    # Save full index
    index_file = output_dir / "session_index.json"
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2, default=str)
    
    print(f"\nIndex saved to: {index_file}")
    
    # Create session log
    session_log = create_session_log(index)
    log_file = output_dir / "critic_session_log.txt"
    with open(log_file, 'w') as f:
        f.write(session_log)
    
    print(f"Session log saved to: {log_file}")
    
    # Print summary
    print(f"\n=== Session Index Summary ===")
    print(f"Total sessions: {index['total_sessions']}")
    print(f"Time range: {index['earliest_session']['start_time']} to {index['latest_session']['start_time']}")
    
    print("\nEarliest 10 sessions:")
    for i, session in enumerate(index['earliest_10'], 1):
        print(f"{i}. {session['start_time'][:16]} - {session['filename']}")
        print(f"   Topics: {', '.join(session['key_topics'])}")
        print(f"   Agents mentioned: {', '.join(session['mentioned_agents'])}")
    
    print("\nLikely GOV sessions:")
    gov_sessions = index['by_agent'].get('GOV', [])
    for session in gov_sessions[:5]:
        print(f"- {session['filename']} ({session['start_time'][:10]})")

if __name__ == "__main__":
    main()