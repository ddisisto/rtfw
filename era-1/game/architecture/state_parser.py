#!/usr/bin/env python3
"""
State Parser - Extracts structured state decisions from agent conversations

Based on actual agent behavior, not idealized protocols.
Agents return state in markdown code blocks or structured text.
"""

import re
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StateDecision:
    """Structured representation of agent state decision"""
    next_state: str  # deep_work|idle|logout
    thread: Optional[str] = None
    max_tokens: Optional[int] = None
    last_read_commit: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class StateParser:
    """
    Parses agent state returns from conversation endings.
    Handles multiple formats agents actually use.
    """
    
    def parse_conversation_end(self, text: str) -> Optional[StateDecision]:
        """
        Extract state decision from final agent message.
        
        Observed patterns:
        1. Markdown code block with key:value pairs
        2. Structured text with "Next State Decision" header
        3. Inline format "next_state: deep_work, thread: x, max_tokens: 30000"
        """
        
        # Pattern 1: Markdown code block (most common)
        code_block_pattern = r'```\s*\n?(.*?)\n?```'
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        
        for match in matches:
            decision = self._parse_structured_text(match)
            if decision and decision.next_state:
                return decision
        
        # Pattern 2: Headed section
        if "next state" in text.lower():
            # Find the section after "next state"
            parts = re.split(r'next state.*?:', text, flags=re.IGNORECASE)
            if len(parts) > 1:
                decision = self._parse_structured_text(parts[1])
                if decision and decision.next_state:
                    return decision
        
        # Pattern 3: Direct structured text (no markers)
        decision = self._parse_structured_text(text)
        if decision and decision.next_state:
            return decision
            
        return None
    
    def _parse_structured_text(self, text: str) -> Optional[StateDecision]:
        """Parse key:value pairs from text"""
        state_data = {}
        
        # Extract key:value pairs
        patterns = {
            'next_state': r'next_state:\s*(\w+)',
            'thread': r'thread:\s*([^\n,]+?)(?:\n|,|$)',
            'max_tokens': r'max_tokens:\s*(\d+)',
            'last_read_commit': r'last_read_commit:\s*([a-f0-9]{7,40})',
            'last_read': r'last_read:\s*([a-f0-9]{7,40})',  # Alternative
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if key == 'max_tokens':
                    value = int(value)
                # Handle alternative keys
                if key == 'last_read' and 'last_read_commit' not in state_data:
                    state_data['last_read_commit'] = value
                else:
                    state_data[key] = value
        
        # Validate minimum requirements
        if 'next_state' in state_data:
            return StateDecision(**state_data)
            
        return None
    
    def extract_commit_info(self, text: str) -> Dict[str, Any]:
        """
        Extract commit-related information from agent messages.
        Used when agents process inbox and report what they've read.
        """
        info = {}
        
        # Look for explicit commit references
        commit_pattern = r'[a-f0-9]{7,40}'
        
        # "Last processed: abc123 at timestamp"
        last_processed = re.search(
            r'last processed:\s*([a-f0-9]{7,40})\s*(?:at\s*(.+?))?',
            text, re.IGNORECASE
        )
        if last_processed:
            info['last_processed_commit'] = last_processed.group(1)
            if last_processed.group(2):
                info['last_processed_time'] = last_processed.group(2).strip()
        
        # "Checkpoint: abc123"
        checkpoint = re.search(
            r'checkpoint:\s*([a-f0-9]{7,40})',
            text, re.IGNORECASE
        )
        if checkpoint:
            info['checkpoint_commit'] = checkpoint.group(1)
            
        return info
    
    def parse_state_annotation(self, commit_message: str) -> Optional[str]:
        """
        Extract [STATE:xxx] annotation from commit messages.
        Per @GOV protocol, agents include state in commits.
        """
        match = re.search(r'\[STATE:(\w+)\]', commit_message)
        return match.group(1) if match else None


# Example usage and test cases
if __name__ == "__main__":
    parser = StateParser()
    
    # Test Case 1: Your actual return format
    test1 = """
## Next State Decision

Based on distillation and current priorities:

```
next_state: deep_work
thread: game-architecture-v2
max_tokens: 30000
```

**Rationale**: 
- At 49% context usage, I have room for focused work
"""
    
    result1 = parser.parse_conversation_end(test1)
    print(f"Test 1: {result1}")
    
    # Test Case 2: Inline format
    test2 = "Proceeding with next_state: idle, waiting for GOV response"
    result2 = parser.parse_conversation_end(test2)
    print(f"Test 2: {result2}")
    
    # Test Case 3: Commit message
    test3 = "@AGENT: [STATE:deep_work] Beginning implementation"
    state = parser.parse_state_annotation(test3)
    print(f"Test 3 state: {state}")