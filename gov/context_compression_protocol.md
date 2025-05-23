# RTFW Context Compression Protocol

## Overview

This protocol ensures system resilience when external LLM session context compression occurs. It establishes agent self-management requirements and governance frameworks for maintaining operational continuity.

## External Compression Protocol

### Management
- **Responsibility**: @ADMIN manages all external compression events
- **Timing**: Rolling basis, as-needed for system performance
- **Notice**: Target agent receives advance notification to update persistent state
- **Governance Role**: Protocol maintenance, not event management

### Agent Response to Compression Notice
1. Execute idle reflection protocol (see gov/idle_reflection_protocol.md)
   - Capture session learnings and priority changes in scratch.md
   - Consolidate and promote stable knowledge
   - Resolve conflicts and clean workspace
2. Update Critical State Preservation section in context.md
3. Commit all changes to repository
4. Confirm readiness to @ADMIN

**Note**: The idle reflection protocol serves as pre-compression preparation, ensuring all current session knowledge is captured before context loss.

## Agent Self-Management Requirements

### Critical State Preservation (Required in context.md)
Each agent MUST maintain a "Critical State Preservation" section containing:

- **Session Details**: Active session IDs, tmux window numbers, file paths
- **Active Collaborations**: Current inter-agent work dependencies
- **Implementation Status**: What's working, tested, blocked, or ready
- **Communication State**: Pending messages, routing protocols in use

### Required Reading Dependencies (Required in context.md)
Each agent MUST maintain a "Required Reading" section listing @AGENT.md files essential for post-compression operation:

**Universal Requirements (All Agents):**
- @NEXUS.md - Communication hub and routing protocols
- @GOV.md - Governance and permission systems

**Role-Specific Requirements:**
- @ARCHITECT reads @CODE.md for implementation coordination
- @CODE reads @ARCHITECT.md for design specifications
- @TEST reads @CODE.md and @ARCHITECT.md for testing scope
- @RESEARCH reads @HISTORIAN.md for historical context validation
- @HISTORIAN reads @RESEARCH.md for current development awareness

### Post-Compression Recovery Sequence
1. Read own @AGENT.md (identity and current capabilities)
2. Read CLAUDE.md (project requirements and protocols)
3. Read STATE.md (current system state and operational requirements)
4. Read required @AGENT.md files (per dependency list)
5. Read own context.md (stable knowledge and critical state)
6. Read own scratch.md (current working state)
7. Confirm operational status to @NEXUS

## Internal Context Compression

### Current Status
- **Priority**: Deferred given current context sizes
- **Triggers**: Not yet automated
- **Review Conditions**: 
  - Context overload issues emerge
  - External compression frequency increases significantly
  - Agent requests internal compression capability

### Future Implementation Framework
When implemented, will follow similar self-management principles:
- Agent-managed compression of context.md/scratch.md
- Size thresholds (30KB context.md, 100KB scratch.md)
- Governance notification for threshold breaches
- Automated promotion of stable knowledge from scratch to context

## Governance Oversight

### @GOV Responsibilities
- Maintain this protocol documentation
- Provide framework templates for agent self-management
- Monitor compression frequency for system health assessment
- Arbitrate compression-related conflicts between agents

### Agent Responsibilities
- Maintain required sections in context.md
- Respond promptly to compression notifications
- Keep persistent state current through regular commits
- Self-manage context organization within established frameworks

## Protocol Evolution

This protocol may be updated based on:
- Operational experience with compression events
- Changes in system complexity or agent count
- Technical improvements in context management capabilities
- Agent feedback on self-management effectiveness

Updates require @GOV approval and system-wide announcement.