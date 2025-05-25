#!/usr/bin/env python3
"""Analyze @ADMIN interventions and corrections in chronological order."""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import heapq

class InterventionAnalyzer:
    def __init__(self, session_dir: str, start_position: str):
        self.session_dir = Path(session_dir)
        self.start_position = start_position
        self.interventions = []
        self.current_context = []
        
    def is_admin_intervention(self, event: Dict) -> bool:
        """Check if this is an @ADMIN intervention."""
        if event.get('type') != 'user' or event.get('userType') != 'external':
            return False
            
        content = self.extract_content(event)
        
        # Look for correction patterns
        correction_patterns = [
            'no,', 'No,', 'NO,',
            'actually', 'Actually', 
            'wait', 'Wait',
            'stop', 'Stop', 'STOP',
            'don\'t', 'Don\'t', 'DON\'T',
            'instead', 'Instead',
            'wrong', 'Wrong',
            'not what', 'Not what',
            'you should', 'You should',
            'please don\'t', 'Please don\'t',
            'be careful', 'Be careful',
            'remember', 'Remember',
            'important:', 'Important:', 'IMPORTANT:',
            'note:', 'Note:', 'NOTE:',
            'warning:', 'Warning:', 'WARNING:',
            'let me', 'Let me',
            'clarification:', 'Clarification:',
            'correction:', 'Correction:',
            '→',  # Often used in directed messages
            '@ADMIN',
            'hold on', 'Hold on'
        ]
        
        return any(pattern in content for pattern in correction_patterns)
    
    def extract_content(self, event: Dict) -> str:
        """Extract text content from an event."""
        message = event.get('message', {})
        content = message.get('content', [])
        text_parts = []
        
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'text':
                text_parts.append(item.get('text', ''))
            elif isinstance(item, str):
                text_parts.append(item)
                
        return ' '.join(text_parts)
    
    def get_context_window(self, file_name: str, target_line: int, window: int = 5) -> List[Dict]:
        """Get events before and after target line for context."""
        events = []
        
        with open(self.session_dir / file_name, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if abs(line_num - target_line) <= window:
                    try:
                        data = json.loads(line)
                        events.append({
                            'line': line_num,
                            'type': data.get('type'),
                            'userType': data.get('userType'),
                            'timestamp': data.get('timestamp'),
                            'content': self.extract_content(data)[:500]
                        })
                    except:
                        pass
                        
        return sorted(events, key=lambda x: x['line'])
    
    def analyze_interventions(self, limit: int = 20) -> List[Dict]:
        """Find and analyze @ADMIN interventions."""
        # Priority queue of (timestamp, file, line_num, data)
        heap = []
        
        # Initialize heap with events from each file
        for jsonl_file in self.session_dir.glob("*.jsonl"):
            file_name = str(jsonl_file.name)
            
            with open(jsonl_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        ts = data.get('timestamp')
                        if ts and ts > self.start_position:
                            heapq.heappush(heap, (ts, file_name, line_num, data))
                    except:
                        pass
        
        # Process events looking for interventions
        interventions_found = []
        last_assistant_action = None
        
        while heap and len(interventions_found) < limit:
            ts, file_name, line_num, data = heapq.heappop(heap)
            
            # Track assistant actions
            if data.get('type') == 'assistant':
                last_assistant_action = {
                    'timestamp': ts,
                    'file': file_name,
                    'line': line_num,
                    'content': self.extract_content(data)[:500]
                }
            
            # Check for admin intervention
            if self.is_admin_intervention(data):
                # Get context window
                context = self.get_context_window(file_name, line_num, window=10)
                
                intervention = {
                    'timestamp': ts,
                    'file': file_name,
                    'line': line_num,
                    'intervention_content': self.extract_content(data),
                    'prior_assistant_action': last_assistant_action,
                    'context_window': context
                }
                
                interventions_found.append(intervention)
                
        return interventions_found
    
    def format_intervention_report(self, interventions: List[Dict]) -> str:
        """Format interventions into a readable report."""
        report = []
        report.append("# @ADMIN Intervention Analysis Report")
        report.append(f"\nAnalyzed from position: {self.start_position}")
        report.append(f"Total interventions found: {len(interventions)}\n")
        
        for i, intervention in enumerate(interventions, 1):
            report.append(f"\n## Intervention {i}")
            report.append(f"**Timestamp:** {intervention['timestamp']}")
            report.append(f"**File:** {intervention['file']}")
            report.append(f"**Line:** {intervention['line']}")
            
            report.append("\n### What Assistant Was Doing Before:")
            if intervention['prior_assistant_action']:
                pa = intervention['prior_assistant_action']
                report.append(f"- Timestamp: {pa['timestamp']}")
                report.append(f"- Action: {pa['content']}")
            else:
                report.append("- No prior assistant action found")
            
            report.append("\n### Admin Intervention:")
            report.append(f"```")
            report.append(intervention['intervention_content'])
            report.append(f"```")
            
            report.append("\n### Context Window:")
            for event in intervention['context_window']:
                marker = ">>> " if event['line'] == intervention['line'] else "    "
                report.append(f"{marker}[{event['type']}/{event.get('userType', 'agent')}] {event['content'][:100]}...")
            
            report.append("\n---")
        
        # Pattern analysis
        report.append("\n## Pattern Analysis")
        
        # Common intervention types
        intervention_types = {}
        for inv in interventions:
            content = inv['intervention_content'].lower()
            if 'no,' in content or 'actually' in content:
                intervention_types['correction'] = intervention_types.get('correction', 0) + 1
            elif 'stop' in content or 'wait' in content:
                intervention_types['halt'] = intervention_types.get('halt', 0) + 1
            elif 'remember' in content or 'note:' in content:
                intervention_types['reminder'] = intervention_types.get('reminder', 0) + 1
            elif '→' in content:
                intervention_types['directive'] = intervention_types.get('directive', 0) + 1
            else:
                intervention_types['other'] = intervention_types.get('other', 0) + 1
        
        report.append("\n### Intervention Types:")
        for itype, count in sorted(intervention_types.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- {itype}: {count}")
        
        return "\n".join(report)

def main():
    analyzer = InterventionAnalyzer(
        "/home/daniel/prj/rtfw/nexus/sessions",
        "2025-05-21T06:28:57.182Z"
    )
    
    print("Analyzing @ADMIN interventions...")
    interventions = analyzer.analyze_interventions(limit=20)
    
    # Save report
    report = analyzer.format_intervention_report(interventions)
    report_file = Path("/home/daniel/prj/rtfw/critic/reports/admin_interventions_analysis.md")
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")
    print(f"Found {len(interventions)} interventions")

if __name__ == '__main__':
    main()