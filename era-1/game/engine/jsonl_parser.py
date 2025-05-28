"""
JSONL Parser for extracting agent state and context information from session logs
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

from .models import StateDecision, AgentState


class JSONLParser:
    """
    Parses Claude session JSONL files to extract:
    - Agent identity
    - State decisions
    - Context token usage
    - Timestamps
    """
    
    def __init__(self):
        # Patterns for extracting state decisions from agent messages
        self.state_patterns = {
            # Pattern 1: Markdown code block
            'code_block': re.compile(r'```\s*\n?(.*?)\n?```', re.DOTALL),
            # Pattern 2: Direct state annotation
            'state_key': re.compile(r'next_state:\s*(\w+)', re.IGNORECASE),
            'thread_key': re.compile(r'thread:\s*([^\n,]+?)(?:\n|,|$)', re.IGNORECASE),
            'tokens_key': re.compile(r'max_tokens:\s*(\d+)', re.IGNORECASE),
            'commit_key': re.compile(r'(?:last_read_commit|last_read):\s*([a-f0-9]{7,40})', re.IGNORECASE),
        }
        
        # Pattern for agent identification
        # TODO: Validate actual JSONL structure - assuming system prompt or early message contains agent name
        self.agent_patterns = {
            'system_prompt': re.compile(r'@(\w+)\.md agent', re.IGNORECASE),
            'bootstrap_prompt': re.compile(r'apply.*?for agent @(\w+)\.md', re.IGNORECASE),
            'agent_message': re.compile(r'^@(\w+)[:\s\[]', re.MULTILINE),  # @AGENT: or @AGENT [state]
        }
    
    def parse_session_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse entire JSONL file and extract summary information
        
        Returns:
            Dict containing:
            - agent_name: Identified agent or None
            - first_timestamp: First message timestamp
            - last_timestamp: Last message timestamp  
            - line_count: Total lines
            - last_state_decision: Most recent state decision
            - context_tokens: Latest token count
            - messages: Last N messages for state extraction
        """
        result = {
            'agent_name': None,
            'first_timestamp': None,
            'last_timestamp': None,
            'line_count': 0,
            'last_state_decision': None,
            'context_tokens': None,
            'messages': []
        }
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                result['line_count'] = len(lines)
                
                # Keep last 10 messages for state extraction
                last_messages = []
                
                for i, line in enumerate(lines):
                    try:
                        entry = json.loads(line.strip())
                        
                        # Extract timestamp
                        if 'timestamp' in entry:
                            ts = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                            if i == 0:
                                result['first_timestamp'] = ts
                            result['last_timestamp'] = ts
                        
                        # Try to identify agent (only if not yet found)
                        if not result['agent_name']:
                            agent_name = self._extract_agent_name(entry)
                            if agent_name:
                                result['agent_name'] = agent_name.lower()
                        
                        # Collect messages for state extraction
                        if entry.get('type') in ['message', 'completion'] and entry.get('content'):
                            last_messages.append(entry)
                            if len(last_messages) > 10:
                                last_messages.pop(0)
                        
                        # Extract token usage from metadata
                        if 'usage' in entry and 'total_tokens' in entry['usage']:
                            result['context_tokens'] = entry['usage']['total_tokens']
                        
                    except (json.JSONDecodeError, KeyError):
                        continue
                
                # Process last messages for state decision
                result['messages'] = last_messages
                if last_messages:
                    # Check messages in reverse order (most recent first)
                    for msg in reversed(last_messages):
                        if msg.get('role') == 'assistant' and msg.get('content'):
                            state_decision = self._extract_state_decision(msg['content'])
                            if state_decision:
                                result['last_state_decision'] = state_decision
                                break
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _extract_agent_name(self, entry: Dict[str, Any]) -> Optional[str]:
        """
        Extract agent name from JSONL entry
        
        Checks multiple patterns:
        1. System prompt mentioning agent
        2. Bootstrap prompt
        3. Agent's own messages
        """
        content = entry.get('content', '')
        
        # Check each pattern
        for pattern_name, pattern in self.agent_patterns.items():
            match = pattern.search(content)
            if match:
                agent_name = match.group(1)
                # Normalize: ERA-1 -> era-1, GOV -> gov
                return agent_name.lower().replace('_', '-')
        
        # TODO: Add more patterns based on actual JSONL structure
        # Might need to check role, metadata fields, etc.
        
        return None
    
    def _extract_state_decision(self, content: str) -> Optional[StateDecision]:
        """
        Extract state decision from message content
        
        Handles multiple formats agents use:
        1. Markdown code blocks with key:value pairs
        2. Inline state declarations
        3. Structured decision sections
        """
        # First try code blocks
        code_blocks = self.state_patterns['code_block'].findall(content)
        for block in code_blocks:
            decision = self._parse_state_block(block)
            if decision:
                return decision
        
        # Then try direct parsing of content
        decision = self._parse_state_block(content)
        if decision:
            return decision
        
        return None
    
    def _parse_state_block(self, text: str) -> Optional[StateDecision]:
        """Parse state information from text block"""
        # Extract state
        state_match = self.state_patterns['state_key'].search(text)
        if not state_match:
            return None
        
        state_name = state_match.group(1).lower()
        
        # Map to enum (handle both forms)
        state_map = {
            'bootstrap': AgentState.BOOTSTRAP,
            'inbox': AgentState.INBOX,
            'distill': AgentState.DISTILL,
            'deep_work': AgentState.DEEP_WORK,
            'deep-work': AgentState.DEEP_WORK,  # Handle hyphenated
            'idle': AgentState.IDLE,
            'logout': AgentState.LOGOUT,
            'direct_io': AgentState.DIRECT_IO,
            'direct-io': AgentState.DIRECT_IO,  # Handle hyphenated
            'offline': AgentState.OFFLINE,
        }
        
        state = state_map.get(state_name)
        if not state:
            return None
        
        # Extract optional fields
        thread_match = self.state_patterns['thread_key'].search(text)
        thread = thread_match.group(1).strip() if thread_match else None
        
        tokens_match = self.state_patterns['tokens_key'].search(text)
        max_tokens = int(tokens_match.group(1)) if tokens_match else None
        
        commit_match = self.state_patterns['commit_key'].search(text)
        last_read_commit = commit_match.group(1) if commit_match else None
        
        return StateDecision(
            next_state=state,
            thread=thread,
            max_tokens=max_tokens,
            last_read_commit=last_read_commit
        )
    
    def extract_last_activity(self, file_path: Path) -> Tuple[Optional[datetime], Optional[str]]:
        """
        Quick extraction of just the last timestamp and message
        Reads file backwards for efficiency
        """
        try:
            # Read last few lines (more efficient than whole file)
            with open(file_path, 'rb') as f:
                # Seek to end and read last 10KB
                f.seek(0, 2)  # End of file
                file_size = f.tell()
                read_size = min(file_size, 10240)  # 10KB max
                f.seek(file_size - read_size)
                tail = f.read().decode('utf-8', errors='ignore')
            
            # Split into lines and parse backwards
            lines = tail.strip().split('\n')
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    if 'timestamp' in entry:
                        ts = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                        content = entry.get('content', '')[:100]  # First 100 chars
                        return ts, content
                except:
                    continue
                    
        except Exception:
            pass
        
        return None, None
    
    def parse_state_decisions(self, file_path: Path) -> List[StateDecision]:
        """
        Parse state decision from LAST line only (most recent assistant output)
        
        Returns list with single StateDecision if found, empty list otherwise
        """
        try:
            # Read just the last line
            with open(file_path, 'rb') as f:
                # Get file size
                f.seek(0, 2)
                file_size = f.tell()
                # Go back 2KB from end or to start if file is smaller
                seek_pos = max(0, file_size - 2048)
                f.seek(seek_pos)
                tail = f.read()
                
            # Get last complete line that's an assistant message
            lines = tail.decode('utf-8', errors='ignore').strip().split('\n')
            
            # Look backwards for last assistant message
            for line in reversed(lines):
                if not line.strip():
                    continue
                    
                try:
                    entry = json.loads(line)
                    
                    # Skip if not a message or not assistant
                    message = entry.get('message', {})
                    if message.get('role') != 'assistant':
                        continue
                    
                    # Extract content
                    content_list = message.get('content', [])
                    if not content_list:
                        continue
                    
                    # Join text content
                    content_parts = []
                    for item in content_list:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            content_parts.append(item.get('text', ''))
                    
                    content = '\n'.join(content_parts)
                    if not content:
                        continue
                    
                    # Try to extract state decision
                    decision = self._extract_state_decision(content)
                    if decision:
                        # Add timestamp from entry
                        if 'timestamp' in entry:
                            decision.timestamp = datetime.fromisoformat(
                                entry['timestamp'].replace('Z', '+00:00')
                            )
                        return [decision]
                        
                except (json.JSONDecodeError, KeyError):
                    continue
            
            # No state decision found
            return []
            
        except Exception as e:
            raise RuntimeError(f"Failed to parse last line of {file_path}: {e}")
    
    def parse_context_usage(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse context token usage from last few lines (most recent usage)
        
        Returns dict with 'used', 'max', and 'percent' fields
        """
        try:
            # Read last 10KB to find recent usage data
            with open(file_path, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                seek_pos = max(0, file_size - 10240)
                f.seek(seek_pos)
                tail = f.read()
            
            # Parse lines in reverse to find most recent usage
            lines = tail.decode('utf-8', errors='ignore').strip().split('\n')
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    
                    # Look for usage in message field (actual JSONL structure)
                    message = entry.get('message', {})
                    usage = message.get('usage', {})
                    
                    if 'input_tokens' in usage:
                        # Calculate total from all token types
                        total = (usage.get('input_tokens', 0) + 
                                usage.get('cache_creation_input_tokens', 0) +
                                usage.get('cache_read_input_tokens', 0) +
                                usage.get('output_tokens', 0))
                        
                        # Assume standard context window
                        max_tokens = 128000  # Could be extracted from model info
                        
                        return {
                            'used': total,
                            'max': max_tokens,
                            'percent': (total / max_tokens) * 100
                        }
                
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return None
            
        except Exception as e:
            # Don't throw - context usage is optional
            print(f"Warning: Could not parse context usage: {e}")
            return None