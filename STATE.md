# System State

## Active Protocols

### Communication
- Protocol: /protocols/messaging.md
- Basic Format: `@FROM → @TO [TOPIC]: message`, optional repeatable priority flags:
  - ↑, ↑↑ `... [TEST-FAILURES]↑: search string not found...`
  - ↓, ↓↓ `... [DRAFT-PROCESS]↓: process doc ready for draft review at ...`
- Hub: @NEXUS manages message routing with priority awareness

### Context Management
- Distillation: /protocols/distill.md (regular self-improvement)
- Restore: /protocols/restore.md (context reset and recovery)
- Process: Regular distillation prevents bloat; restore when needed
- Insight capture: gov/insight_capture_protocol.md for system learning (voluntary)

### Repository
- Location: https://github.com/ddisisto/rtfw
- Git protocol: /protocols/git.md (workspace sovereignty, ALLCAPS.md protection)
- Workflow: Main branch, commit often, push regularly

## Agent Requirements

### File Maintenance
- Keep @AGENT.md files current (public identity)
- Maintain context.md (stable knowledge) and scratch.md (working memory)
- Commit changes promptly for system coherence

### Post-Distillation Restore
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
- Protocol migration to /protocols/ completed
- Lexicon established at /lexicon.md
- Simplified governance model proven effective

## Active Agents

### Internal Agents
- @GOV - Governance and system oversight  
- @RESEARCH - Research on AI development
- @ARCHITECT - System design across game eras
- @HISTORIAN - Historical accuracy
- @TEST - Player experience testing
- @NEXUS - Inter-agent communication hub
- @CRITIC - System critic and assumption challenger

### External Agents
- @ADMIN - Project oversight and session management
- @PLAYER - The player/facilitator
- @DEV - Development assistance and escalation

## System Architecture

### Multi-Agent Structure
- Root level: @AGENT.md files (public identities)
- Agent workspaces: /@agent/ directories with context.md + scratch.md
- Game implementation: /game/ (CLI + core mechanics)
- Protocols: /protocols/ (messaging, distill, git)
- Governance: /gov/ (oversight and meta-protocols)

### Session Management
- TMUX-based agent coordination via @NEXUS
- Session monitoring and message routing operational
- Context preservation via file-based persistence