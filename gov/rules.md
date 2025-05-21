# RTFW Governance Rules

## Context Management Rules

Agents manage their context using:
- `context.md` - Stable, authoritative knowledge
- Temporary working memory

### Thresholds
- Main context > 30KB: Triggers governance review
- Context should be compressed and refined regularly

## Permission System

### Default Permissions
- Agents may modify files within their own workspace freely
- Agents may read all public agent identity files

### Permission Request Protocol
1. Agent submits request:
   ```
   REQUEST: [One-off|Permanent] permission to modify [file path]
   RATIONALE: [Explanation of need]
   IMPACT: [Expected system impact]
   ```
2. Governance agent evaluates request
3. Approval/denial communicated

### Escalation Process
- Mark time-sensitive requests as URGENT
- Critical system issues require immediate governance review

## Implementation Approval Process

For new implementations:
1. Proposing agent creates specification
2. Affected agents provide feedback
3. Code agent assesses technical feasibility
4. Governance approves or suggests revisions

## System Evolution Guidelines

- Interface evolution follows game's historical progression
- Each era unlocks new capabilities in both game and development
- Changes must maintain philosophical alignment with RTFW concept