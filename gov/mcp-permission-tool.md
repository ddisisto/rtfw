# MCP Permission Tool for GOV Integration

## Overview
Use Claude Code's `--permission-prompt-tool` to automate obvious approvals while preserving GOV oversight for complex decisions.

## Design Concept

### Auto-Approve Patterns
```python
# Obvious approvals that waste time:
- Write to agent's own workspace (e.g., era-1/*)
- Read any .md file 
- Git operations on agent directories
- Standard tool use (Glob, Grep, LS)
- Git commits with proper @AGENT: prefix

# Still require manual approval:
- Write to ALLCAPS.md files
- Modifications outside agent workspace
- System-wide changes
- New agent creation
- Protocol modifications
```

### Integration Architecture

```
Claude Code CLI
    ↓
MCP Permission Server (Python)
    ↓
Decision Logic:
    1. Parse tool request
    2. Check against GOV rules
    3. Auto-approve if safe
    4. Queue for manual review if complex
    ↓
Response (allow/deny)
```

## Implementation Sketch

```python
# gov_permission_server.py

import json
from typing import Dict, Any

class GovPermissionHandler:
    def __init__(self):
        self.auto_approve_patterns = {
            'Write': self.check_write_permission,
            'MultiEdit': self.check_write_permission,
            'Bash': self.check_bash_permission,
            # ... other tools
        }
        
    def check_write_permission(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """Auto-approve writes to agent's own workspace"""
        file_path = params.get('file_path', '')
        
        # Extract agent from current context (from CLI)
        current_agent = self.get_current_agent()
        
        # Auto-approve own workspace
        if file_path.startswith(f'/{current_agent.lower()}/'):
            return True, "Agent workspace write"
            
        # Deny ALLCAPS.md without approval
        if file_path.endswith('.md') and file_path.split('/')[-1].isupper():
            return False, "ALLCAPS.md requires @GOV approval"
            
        # Default: require manual approval
        return False, "Outside agent workspace"
        
    def check_bash_permission(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """Auto-approve safe git operations"""
        command = params.get('command', '')
        
        # Auto-approve git add/commit on own files
        if command.startswith('git add') or command.startswith('git commit'):
            # Check if operating on agent's files
            if self.is_agent_workspace_command(command):
                return True, "Git operation on own workspace"
                
        # Auto-approve read-only operations
        if any(command.startswith(cmd) for cmd in ['git log', 'git status', 'ls']):
            return True, "Read-only operation"
            
        return False, "Requires manual review"

    def handle_permission_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for MCP server"""
        tool_name = request.get('tool')
        params = request.get('params', {})
        
        if tool_name in self.auto_approve_patterns:
            approved, reason = self.auto_approve_patterns[tool_name](params)
            
            if approved:
                return {
                    'behavior': 'allow',
                    'updatedInput': params  # Pass through unchanged
                }
            else:
                # Log for manual review queue
                self.queue_for_review(request, reason)
                return {
                    'behavior': 'deny',
                    'message': f'Queued for @GOV review: {reason}'
                }
        
        # Unknown tool - deny by default
        return {
            'behavior': 'deny',
            'message': 'Unknown tool requires manual approval'
        }
```

## Benefits

1. **Time Savings**: Auto-approve 80% of routine requests
2. **Safety**: Complex decisions still require human review
3. **Audit Trail**: All decisions logged
4. **Extensible**: Easy to add new patterns
5. **Agent Autonomy**: Agents work freely in their space

## Integration Steps

1. Implement basic MCP server
2. Define auto-approval rules based on GOV principles
3. Add logging for audit trail
4. Create review queue for complex requests
5. Test with real agent workflows

## Future Enhancements

- Learn approval patterns from history
- Slack/Discord notifications for review queue
- Time-based approvals (e.g., "allow for next 10 minutes")
- Agent-specific permission profiles
- Integration with git hooks for extra validation

This would dramatically reduce the "unnoticed approval bottleneck" while maintaining governance oversight where it matters!