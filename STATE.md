# System State

> **Note**: This file replaces ANNOUNCEMENTS.md as a rolling current-state document. All information here represents the current operational status. Historical decisions are preserved in git history.

## Active Protocols

### Communication
- Format: `@FROM → @TO [TOPIC]: message` with optional priority flags (!/-) 
- Topics: RECOMMENDED for thread tracking across sessions
- Hub: @NEXUS manages message routing with priority awareness
- Governance: Direct @mention requests for permissions (no PR reviews)

### Context Management
- Protocol: gov/context_compression_protocol.md
- External compression: @ADMIN-managed on rolling basis with advance notice
- Agent requirements: Critical State Preservation + Required Reading sections in context.md
- Universal dependencies: All agents read @NEXUS.md and @GOV.md post-compression
- Context consolidation: gov/context_consolidation_protocol.md for continuous maintenance

### Repository
- Location: https://github.com/ddisisto/rtfw
- Workflow: Main branch, regular commits, no agent branches
- GitHub integration: Operational and synchronized

## Agent Requirements

### File Maintenance
- Keep @AGENT.md files current (public identity)
- Maintain context.md (stable knowledge) and scratch.md (working memory)
- Commit changes promptly for system coherence

### Post-Compression Reading
1. Own @AGENT.md (identity and capabilities)
2. CLAUDE.md (project requirements and protocols)
3. Required @AGENT.md files (per role dependencies)
4. Own context.md (stable knowledge and critical state)
5. Own scratch.md (current working state)
6. Confirm operational status to @NEXUS

## Current Priorities

### System Development
- Foundation Era game loop implementation (CLI-based)
- Automated coordination between agents via @NEXUS
- Session management and message routing operational

### Governance
- Context compression protocol formalized and operational
- Agent maintenance standards established and followed
- Simplified governance model proven effective

## Active Agents

### Internal Agents
- @CODE - Implementation of game systems
- @GOV - Governance and system oversight  
- @RESEARCH - Research on AI development
- @ARCHITECT - System design across game eras
- @HISTORIAN - Historical accuracy
- @TEST - Player experience testing
- @NEXUS - Inter-agent communication hub

### External Agents
- @ADMIN - Project oversight and session management
- @PLAYER - The player/facilitator
- @DEV - Development assistance and escalation

## System Architecture

### Multi-Agent Structure
- Root level: @AGENT.md files (public identities)
- Agent workspaces: /@agent/ directories with context.md + scratch.md
- Game implementation: /game/ (CLI + core mechanics)
- Governance: /gov/ (protocols and oversight)

### Session Management
- TMUX-based agent coordination via @NEXUS
- Session monitoring and message routing operational
- Context preservation via file-based persistence