#!/usr/bin/env python3
"""
Unified session query tool - foundation for all session analysis.
Stream processes JSONL files with composable filters.
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Iterator, Dict, Any, Optional, List
import re

class SessionQuery:
    def __init__(self, session_dir: str = "/home/daniel/prj/rtfw/nexus/sessions"):
        self.session_dir = Path(session_dir)
        self.session_mappings = self.load_session_mappings()
    
    def load_session_mappings(self) -> Dict[str, str]:
        """Load session-to-agent mappings from CSV."""
        mappings = {}
        csv_path = Path("/home/daniel/prj/rtfw/critic/sessions_index.csv")
        if csv_path.exists():
            import csv
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    session_id = row['sessionId']
                    agent = row['agent']
                    if agent != 'UNKNOWN':
                        mappings[session_id] = agent
        return mappings
        
    def extract_content(self, entry: Dict[str, Any]) -> str:
        """Unified content extraction from various message formats."""
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
            # Extract text from content parts
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        text_parts.append(item.get('text', ''))
                    elif item.get('type') == 'tool_use':
                        text_parts.append(f"[TOOL: {item.get('name')}]")
                else:
                    text_parts.append(str(item))
            return ' '.join(text_parts)
        else:
            return str(content)
    
    def extract_agent(self, entry: Dict[str, Any], filename: str) -> str:
        """Extract agent name from session mapping."""
        session_id = filename.replace('.jsonl', '')
        if session_id in self.session_mappings:
            return self.session_mappings[session_id]
        else:
            raise Exception(f"Session {session_id} not found in index. Please run extract_user_prompts.py to analyze and update critic/sessions_index.csv")
    
    def stream_entries(self, 
                      agent: Optional[str] = None,
                      after: Optional[str] = None,
                      before: Optional[str] = None,
                      pattern: Optional[str] = None,
                      entry_type: Optional[str] = None,
                      user_type: Optional[str] = None,
                      session_id: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        """Stream filtered entries from session files."""
        
        # Convert time strings to comparable format
        after_time = after if after else None
        before_time = before if before else None
        
        # Compile pattern if provided
        pattern_re = re.compile(pattern, re.IGNORECASE) if pattern else None
        
        # Determine which files to process
        if session_id:
            files = [f for f in self.session_dir.glob(f"*{session_id}*.jsonl")]
        else:
            files = sorted(self.session_dir.glob("*.jsonl"))
        
        for jsonl_file in files:
            filename = jsonl_file.name
            
            # Stream process the file
            with open(jsonl_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        entry = json.loads(line.strip())
                        
                        # Time filters
                        timestamp = entry.get('timestamp', '')
                        if after_time and timestamp < after_time:
                            continue
                        if before_time and timestamp > before_time:
                            continue
                        
                        # Type filters
                        if entry_type and entry.get('type') != entry_type:
                            continue
                        if user_type and entry.get('userType') != user_type:
                            continue
                        
                        # Content pattern filter
                        if pattern_re:
                            content = self.extract_content(entry)
                            if not pattern_re.search(content):
                                continue
                        
                        # Agent filter (double-check from content)
                        if agent and agent.upper() != 'ALL':
                            entry_agent = self.extract_agent(entry, filename)
                            if entry_agent != agent.upper():
                                continue
                        
                        # Add metadata
                        entry['_file'] = filename
                        entry['_line'] = line_num
                        entry['_agent'] = self.extract_agent(entry, filename)
                        entry['_content'] = self.extract_content(entry)
                        
                        yield entry
                        
                    except json.JSONDecodeError:
                        continue

def format_entry(entry: Dict[str, Any], format: str, fields: List[str]) -> str:
    """Format entry for output."""
    if format == 'json':
        if fields:
            filtered = {k: entry.get(k) for k in fields if k in entry}
            return json.dumps(filtered)
        return json.dumps(entry)
    
    elif format == 'csv':
        if not fields:
            fields = ['timestamp', '_agent', 'type', '_content']
        values = [str(entry.get(f, '')).replace(',', ';') for f in fields]
        return ','.join(values)
    
    else:  # text format
        timestamp = entry.get('timestamp', 'UNKNOWN')[:19]
        agent = entry.get('_agent', 'UNKNOWN')
        entry_type = entry.get('type', 'unknown')
        user_type = entry.get('userType', 'agent')
        content = entry.get('_content', '')[:200]
        if len(entry.get('_content', '')) > 200:
            content += '...'
        
        return f"[{timestamp}] {agent} ({entry_type}/{user_type}): {content}"

def main():
    parser = argparse.ArgumentParser(description='Query session JSONL files')
    
    # Filters
    parser.add_argument('--agent', help='Filter by agent name')
    parser.add_argument('--after', help='Filter entries after timestamp')
    parser.add_argument('--before', help='Filter entries before timestamp')
    parser.add_argument('--pattern', help='Filter by content pattern (regex)')
    parser.add_argument('--type', dest='entry_type', help='Filter by entry type (user/assistant)')
    parser.add_argument('--user-type', help='Filter by user type (external/agent)')
    parser.add_argument('--session', dest='session_id', help='Filter by session ID')
    
    # Output options
    parser.add_argument('--format', choices=['json', 'csv', 'text'], default='text',
                       help='Output format')
    parser.add_argument('--fields', nargs='+', help='Fields to include (JSON/CSV only)')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    
    args = parser.parse_args()
    
    # Create query instance
    query = SessionQuery()
    
    # Stream and output results
    count = 0
    for entry in query.stream_entries(
        agent=args.agent,
        after=args.after,
        before=args.before,
        pattern=args.pattern,
        entry_type=args.entry_type,
        user_type=args.user_type,
        session_id=args.session_id
    ):
        print(format_entry(entry, args.format, args.fields or []))
        
        count += 1
        if args.limit and count >= args.limit:
            break
    
    # Print summary to stderr
    if args.format == 'text':
        print(f"\n[Found {count} entries]", file=sys.stderr)

if __name__ == '__main__':
    main()