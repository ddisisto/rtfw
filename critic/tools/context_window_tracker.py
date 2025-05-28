#!/usr/bin/env python3
"""
Track context window usage across clear/restore cycles in session logs
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

class ContextWindowTracker:
    def __init__(self):
        self.sessions = []  # List of context "eras" between clears
        self.current_session = {
            'start_time': None,
            'end_time': None,
            'start_line': 0,
            'end_line': 0,
            'max_context': 0,
            'final_context': 0,
            'baseline_after_restore': 0,
            'total_cost': 0,
            'operations': []
        }
        self.line_number = 0
        
    def process_line(self, line: str):
        """Process one JSONL line"""
        self.line_number += 1
        
        try:
            data = json.loads(line.strip())
        except:
            return
            
        # Check for clear command
        if self._is_clear_event(data):
            self._handle_clear(data)
            return
            
        # Extract metrics
        timestamp = data.get('timestamp', '')
        msg_type = data.get('type', '')
        
        if msg_type == 'assistant':
            message = data.get('message', {})
            usage = message.get('usage', {})
            
            if usage:
                # Calculate total context size
                input_tokens = usage.get('input_tokens', 0)
                cache_create = usage.get('cache_creation_input_tokens', 0)
                cache_read = usage.get('cache_read_input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
                
                total_context = cache_read + cache_create
                cost = data.get('costUSD', 0)
                
                # Update current session
                if not self.current_session['start_time']:
                    self.current_session['start_time'] = timestamp
                    self.current_session['start_line'] = self.line_number
                    
                self.current_session['end_time'] = timestamp
                self.current_session['end_line'] = self.line_number
                self.current_session['max_context'] = max(
                    self.current_session['max_context'], 
                    total_context
                )
                self.current_session['final_context'] = total_context
                self.current_session['total_cost'] += cost
                
                # Track operation
                self.current_session['operations'].append({
                    'line': self.line_number,
                    'time': timestamp,
                    'context_size': total_context,
                    'cost': cost,
                    'cache_create': cache_create,
                    'cache_read': cache_read
                })
                
                # Detect baseline after restore (first substantial operation after clear)
                if (len(self.sessions) > 0 and 
                    self.current_session['baseline_after_restore'] == 0 and
                    total_context > 10000):  # Threshold for "restored"
                    self.current_session['baseline_after_restore'] = total_context
    
    def _is_clear_event(self, data: Dict) -> bool:
        """Check if this is a clear command"""
        if data.get('type') == 'user':
            message = data.get('message', {})
            if isinstance(message, dict):
                content = message.get('content', '')
                if isinstance(content, str) and 'clear' in content.lower():
                    return True
                # Check for command format
                if '<command-name>clear</command-name>' in str(content):
                    return True
        return False
    
    def _handle_clear(self, data: Dict):
        """Handle a clear event"""
        # Save current session if it has data
        if self.current_session['operations']:
            self.sessions.append(self.current_session.copy())
            
        # Start new session
        self.current_session = {
            'start_time': data.get('timestamp', ''),
            'end_time': None,
            'start_line': self.line_number,
            'end_line': 0,
            'max_context': 0,
            'final_context': 0,
            'baseline_after_restore': 0,
            'total_cost': 0,
            'operations': []
        }
    
    def finalize(self):
        """Save final session if exists"""
        if self.current_session['operations']:
            self.sessions.append(self.current_session)
    
    def generate_report(self) -> str:
        """Generate analysis report"""
        report = ["# Context Window Usage Report\n"]
        
        total_cost = sum(s['total_cost'] for s in self.sessions)
        report.append(f"Total sessions (clear cycles): {len(self.sessions)}")
        report.append(f"Total cost across all sessions: ${total_cost:.4f}\n")
        
        for i, session in enumerate(self.sessions):
            report.append(f"\n## Session {i+1}")
            report.append(f"Time: {session['start_time']} to {session['end_time']}")
            report.append(f"Lines: {session['start_line']} to {session['end_line']}")
            report.append(f"Operations: {len(session['operations'])}")
            report.append(f"Max context: {session['max_context']:,} tokens")
            report.append(f"Final context: {session['final_context']:,} tokens")
            
            if session['baseline_after_restore'] > 0:
                report.append(f"Post-restore baseline: {session['baseline_after_restore']:,} tokens")
                
            report.append(f"Session cost: ${session['total_cost']:.4f}")
            
            # Show context growth
            if len(session['operations']) > 1:
                growth = session['final_context'] - session['operations'][0]['context_size']
                report.append(f"Context growth: {growth:,} tokens")
                
            # Context trajectory graph (simple ASCII)
            if session['operations']:
                report.append("\nContext trajectory:")
                max_ctx = session['max_context']
                if max_ctx > 0:
                    for j, op in enumerate(session['operations']):
                        if j % 5 == 0 or j == len(session['operations']) - 1:  # Sample every 5th
                            bar_len = int(50 * op['context_size'] / max_ctx)
                            bar = '█' * bar_len
                            report.append(f"  {op['time'][11:19]} |{bar}")
        
        return '\n'.join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: context_window_tracker.py <session.jsonl>")
        sys.exit(1)
        
    tracker = ContextWindowTracker()
    
    with open(sys.argv[1], 'r') as f:
        for line in f:
            tracker.process_line(line)
    
    tracker.finalize()
    print(tracker.generate_report())

if __name__ == '__main__':
    main()