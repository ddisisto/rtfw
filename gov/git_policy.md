# Git Policy

## Purpose

Establish clear boundaries for git operations that respect agent workspace ownership while enabling efficient development.

## Core Rules

### Always Permitted
- `git add <agent>/` - Agents have full authority over their own workspace
- `git add specific/path/file` - Specific files outside agent spaces (with exceptions below)

### Requires @ADMIN Approval
- `git add ALLCAPS.md` - Root-level agent identity files
- Any modifications to another agent's workspace files

### General Principles
- Workspace sovereignty: Agents control their own directories
- Identity protection: Root @AGENT.md files require oversight
- Respect boundaries: Never modify another agent's files without permission

## Implementation

### For Agents
- Freely commit changes within your workspace
- Request @ADMIN approval before modifying any ALLCAPS.md files
- Coordinate with other agents before touching their files

### For @GOV
- Monitor for git policy violations during governance reviews
- Update this policy based on operational experience
- Ensure new agents understand workspace boundaries

## Rationale

This policy balances:
- Agent autonomy within their domains
- System integrity for identity files
- Clear boundaries preventing accidental conflicts
- Simple rules that are easy to remember and follow