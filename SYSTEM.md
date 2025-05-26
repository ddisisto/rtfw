# System Architecture

## Overview
Multi-agent system for collaborative AI development with file-based persistence and session-based coordination.

## Agent Architecture

### Agent Structure
- Root level: @AGENT.md files define public identity and interfaces
- Agent workspaces: /@agent/ directories containing:
  - context.md: Stable knowledge and restore dependencies
  - scratch.md: Working memory and per-turn insights
  - notes/: Agent-specific documentation (optional)

### Active Agents

#### External
- **@ADMIN**: Project oversight and direction
  - Ultimate authority and human interface
  - Resource provisioning and strategic guidance
  - Catch-all for unroutable messages

#### Internal
- **@NEXUS**: Central communication hub and session orchestrator
  - Message routing with priority awareness (↑/↓ flags)
  - Session management and agent coordination
  - Lexicon tracking and pattern recognition

- **@GOV**: System governance and protocol steward
  - Protocol creation and maintenance
  - Conflict resolution and system evolution
  - Responsive intervention (not scheduled oversight)

- **@CRITIC**: System critic and assumption challenger
  - Pattern analysis from session logs
  - Assumption surfacing and questioning
  - Post-distillation review capability


Note: Additional agents can be created as needs arise. The system is designed for organic growth based on operational requirements.

## Communication Patterns

### Message Format
```
@FROM → @TO [TOPIC]: message content
@FROM → @TO [TOPIC]↑: higher priority
@FROM → @TO [TOPIC]↓: lower priority
```

### Communication Channels
- Git commits with @mentions (primary async channel)
- File-based persistence for context preservation
- See /protocols/git-comms.md for implementation details

## Core Workflows

### Context Lifecycle
1. **Distillation**: Regular self-improvement through knowledge refinement
2. **Restore**: Context reset with dependency-aware reloading
3. **Insight Capture**: Per-turn learning appended to scratch.md
4. **Consolidation**: Pattern promotion from scratch to context

### Agent Bootstrap
1. Read own @AGENT.md for identity
2. Load CLAUDE.md for system requirements
3. Check STATE.md for current priorities
4. Load own context.md and scratch.md
5. Announce operational status to @NEXUS

### Repository Workflow
- Single main branch, no agent branches
- Regular commits for context preservation
- ALLCAPS.md files require @GOV/@ADMIN approval
- Workspace sovereignty within agent directories

## System Principles

### Governance Philosophy
- Minimal viable governance
- Protocols as extensible frameworks
- Agent sovereignty with accountability
- Evolution through practice

### Operational Patterns
- File-based everything (persistence, config, state)
- Native tools over shell commands
- Qualitative metrics over quantitative
- Responsive intervention over scheduled review

## Directory Structure
```
/
├── @AGENT.md files (public identities)
├── /agent/ directories (private workspaces)
├── /protocols/ (system-wide protocols)
├── /gov/ (governance meta-protocols)
├── /admin/ (administrative workspace)
└── /nexus/sessions/ (NEXUS session management)
```

## Protocol Locations
- Communication: /protocols/messaging.md
- Context Management: /protocols/distill.md, /protocols/restore.md
- Repository: /protocols/git.md
- Governance: /gov/protocol_design_guidelines.md