#!/usr/bin/env python3
"""
Enhanced session query tool - v2 improvements based on usage experience.
- No index dependency (works with any JSONL)
- Context windows (before/after messages)
- Better format handling
- Specialized filters (interventions, questions, etc.)
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Iterator, Dict, Any, Optional, List, Tuple
import re

class SessionQueryV2:
    def __init__(self, session_dir: str = "/home/daniel/prj/rtfw/nexus/sessions"):
        self.session_dir = Path(session_dir)
        self._agent_cache = {}
        
    def detect_agent(self, content: str, filename: str) -> Optional[str]:
        """Detect agent from content patterns or filename."""
        # Cache by filename to avoid repeated detection
        if filename in self._agent_cache:
            return self._agent_cache[filename]
            
        # Pattern-based detection from content
        for agent in ['NEXUS', 'GOV', 'CRITIC', 'ERA-1', 'ADMIN', 'BUILD', 'CODE']:
            if f"@{agent}" in content or f"Read {agent}.md" in content:
                self._agent_cache[filename] = agent
                return agent
                
        return None
    
    def extract_content(self, entry: Dict[str, Any]) -> str:
        """Enhanced content extraction handling all formats."""
        if entry.get('type') not in ['user', 'assistant']:
            return ''
            
        message = entry.get('message', {})
        if not isinstance(message, dict):
            return str(message)
            
        content = message.get('content', '')
        
        # Handle different content formats
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        text_parts.append(item.get('text', ''))
                    elif item.get('type') == 'tool_use':
                        # Include tool details for context
                        tool_name = item.get('name', 'unknown')
                        tool_input = item.get('input', {})
                        text_parts.append(f"[TOOL: {tool_name}]")
                        if isinstance(tool_input, dict) and 'command' in tool_input:
                            text_parts.append(f"  Command: {tool_input['command']}")
                    elif item.get('type') == 'tool_result':
                        result = item.get('content', '')
                        if len(result) > 200:
                            result = result[:200] + "..."
                        text_parts.append(f"[RESULT: {result}]")
                else:
                    text_parts.append(str(item))
            return '\n'.join(text_parts)
        else:
            return str(content)
    
    def get_context_window(self, 
                          entries: List[Dict[str, Any]], 
                          index: int, 
                          before: int = 2, 
                          after: int = 2) -> List[Dict[str, Any]]:
        """Get surrounding entries for context."""
        start = max(0, index - before)
        end = min(len(entries), index + after + 1)
        return entries[start:end]
    
    def is_intervention(self, entry: Dict[str, Any], prev_entry: Optional[Dict[str, Any]] = None) -> bool:
        """Detect if this is an intervention message."""
        if entry.get('userType') != 'external':
            return False
            
        content = self.extract_content(entry).lower()
        
        # Direct intervention patterns
        intervention_patterns = [
            r'\bno\b.*\bdon\'t\b',
            r'\bnope\b',
            r'\bactually\b',
            r'\binstead\b',
            r'\bmy bad\b',
            r'\bplease\s+\w+\s+instead\b',
            r'\btry\s+again\b',
            r'\bgreat\s+idea.*but\b'
        ]
        
        for pattern in intervention_patterns:
            if re.search(pattern, content):
                return True
                
        # Check if responding to error/mistake
        if prev_entry:
            prev_content = self.extract_content(prev_entry).lower()
            if 'error' in prev_content or 'failed' in prev_content:
                return True
                
        return False
    
    def stream_entries_with_context(self,
                                   pattern: Optional[str] = None,
                                   entry_type: Optional[str] = None,
                                   user_type: Optional[str] = None,
                                   agent: Optional[str] = None,
                                   interventions_only: bool = False,
                                   context_before: int = 0,
                                   context_after: int = 0) -> Iterator[Tuple[List[Dict], int]]:
        """Stream entries with optional context window."""
        
        pattern_re = re.compile(pattern, re.IGNORECASE) if pattern else None
        
        files = sorted(self.session_dir.glob("*.jsonl"))
        
        for jsonl_file in files:
            filename = jsonl_file.name
            
            # Load all entries from file for context access
            entries = []
            with open(jsonl_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            
            # Process entries with context
            for i, entry in enumerate(entries):
                # Basic filters
                if entry_type and entry.get('type') != entry_type:
                    continue
                if user_type and entry.get('userType') != user_type:
                    continue
                
                # Content and agent detection
                content = self.extract_content(entry)
                detected_agent = self.detect_agent(content, filename)
                
                if agent and detected_agent != agent.upper():
                    continue
                
                # Pattern filter
                if pattern_re and not pattern_re.search(content):
                    continue
                
                # Intervention filter
                if interventions_only:
                    prev = entries[i-1] if i > 0 else None
                    if not self.is_intervention(entry, prev):
                        continue
                
                # Add metadata
                entry['_file'] = filename
                entry['_agent'] = detected_agent
                entry['_content'] = content
                entry['_index'] = i
                
                # Get context window if requested
                if context_before > 0 or context_after > 0:
                    context = self.get_context_window(entries, i, context_before, context_after)
                    for ctx_entry in context:
                        ctx_entry['_file'] = filename
                        ctx_entry['_agent'] = detected_agent
                        ctx_entry['_content'] = self.extract_content(ctx_entry)
                    yield (context, i - max(0, i - context_before))
                else:
                    yield ([entry], 0)

def format_entry_enhanced(entry: Dict[str, Any], highlight: bool = False) -> str:
    """Enhanced formatting with better structure."""
    timestamp = entry.get('timestamp', 'UNKNOWN')[:19]
    agent = entry.get('_agent', 'UNKNOWN')
    entry_type = entry.get('type', 'unknown')
    user_type = entry.get('userType', '')
    content = entry.get('_content', '')
    
    # Truncate long content but keep tool commands visible
    if '[TOOL:' in content:
        # Keep tool usage more visible
        lines = content.split('\n')
        content = '\n'.join(lines[:5])
        if len(lines) > 5:
            content += '\n  ...'
    elif len(content) > 300:
        content = content[:300] + '...'
    
    prefix = ">>> " if highlight else "    "
    type_str = f"{entry_type}/{user_type}" if user_type else entry_type
    
    return f"{prefix}[{timestamp}] {agent} ({type_str}):\n{prefix}{content.replace(chr(10), chr(10) + prefix)}"

def main():
    parser = argparse.ArgumentParser(description='Enhanced session query tool v2')
    
    # Filters
    parser.add_argument('--pattern', help='Filter by content pattern (regex)')
    parser.add_argument('--type', dest='entry_type', help='Filter by entry type (user/assistant)')
    parser.add_argument('--user-type', help='Filter by user type (external/agent)')
    parser.add_argument('--agent', help='Filter by detected agent')
    parser.add_argument('--interventions', action='store_true', help='Show only intervention messages')
    
    # Context options
    parser.add_argument('--before', type=int, default=0, help='Show N messages before match')
    parser.add_argument('--after', type=int, default=0, help='Show N messages after match')
    
    # Output options
    parser.add_argument('--format', choices=['text', 'json', 'stats'], default='text')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    
    args = parser.parse_args()
    
    query = SessionQueryV2()
    
    count = 0
    stats = {'agents': {}, 'types': {}, 'files': set()}
    
    for context_entries, highlight_idx in query.stream_entries_with_context(
        pattern=args.pattern,
        entry_type=args.entry_type,
        user_type=args.user_type,
        agent=args.agent,
        interventions_only=args.interventions,
        context_before=args.before,
        context_after=args.after
    ):
        if args.format == 'json':
            print(json.dumps(context_entries))
        elif args.format == 'stats':
            # Collect statistics
            for entry in context_entries:
                agent = entry.get('_agent', 'UNKNOWN')
                stats['agents'][agent] = stats['agents'].get(agent, 0) + 1
                stats['types'][entry.get('type')] = stats['types'].get(entry.get('type'), 0) + 1
                stats['files'].add(entry.get('_file'))
        else:  # text format
            if args.before > 0 or args.after > 0:
                print(f"\n{'='*60}")
                print(f"Context for match in {context_entries[0]['_file']}:")
                print('='*60)
            
            for i, entry in enumerate(context_entries):
                print(format_entry_enhanced(entry, highlight=(i == highlight_idx)))
                
        count += 1
        if args.limit and count >= args.limit:
            break
    
    if args.format == 'text':
        print(f"\n[Found {count} matches]")
    elif args.format == 'stats':
        print(json.dumps({
            'total_matches': count,
            'agents': stats['agents'],
            'types': stats['types'],
            'files_searched': len(stats['files'])
        }, indent=2))

if __name__ == '__main__':
    main()