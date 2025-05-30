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
  - Direct connection override capability

#### Meta Agents (Persistent)
- **@NEXUS**: Context lifecycle orchestrator and session manager
  - Monitor git commits for distributed messaging
  - Session management and agent coordination
  - Context health monitoring and distillation timing

- **@GOV**: System governance and protocol steward
  - Protocol creation and maintenance
  - Conflict resolution and system evolution
  - Responsive intervention (not scheduled oversight)

- **@CRITIC**: System critic and assumption challenger
  - Pattern analysis from session logs
  - Assumption surfacing and questioning
  - Post-distillation review capability

#### ERA Agents (Transient)
- **@ERA-1**: Foundation Era implementation
  - 1970s terminal interface with real system integration
  - Python/blessed with optional tmux embedding
  - Bootstrap ERA-2 when complete

Note: Additional agents can be created as needs arise. The system is designed for organic growth based on operational requirements.

## State Machine Architecture

### Commits ARE State Declarations
```
@AGENT [state]: work completed, transitioning
```

Engine observes commits → updates _state.md → agents read objective truth.
No text outputs. No "next_state:". Git commits drive the state machine.

### Communication Through Commits
- State transitions: Include [state] in every commit message
- Messaging: @mentions within commits reach other agents
- Pattern: State declaration + work + communication in one atomic commit
- See /protocols/journey.md for states, /protocols/messaging.md for patterns

## Core Workflows

### Context Lifecycle
1. **Bootstrap**: Cold-start from offline state per /protocols/bootstrap.md
2. **Distillation**: Regular self-improvement through knowledge refinement
3. **Insight Capture**: Per-turn learning appended to scratch.md
4. **Consolidation**: Pattern promotion from scratch to context

### Agent Journey (Eight States)
State transitions through git commits:
- offline → bootstrap → inbox → {deep_work|idle|distill|direct_io|logout} → offline
- Engine handles offline→bootstrap automatically
- Agents self-transition via commits with [state] declaration
- See /protocols/journey.md for complete state machine

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
- Fourth wall awareness (agents cannot self-measure objectively)
- State machine driven by git commits, not text outputs

## Directory Structure
```
/
├── @AGENT.md files (public identities)
│   ├── ADMIN.md, NEXUS.md, GOV.md, CRITIC.md
│   └── ERA-1.md (first ERA agent)
├── /agent/ directories (private workspaces)
│   ├── /admin/ (ADMIN's workspace)
│   ├── /nexus/ (NEXUS workspace + sessions/)
│   ├── /gov/ (GOV workspace + meta-protocols)
│   ├── /critic/ (CRITIC workspace + analysis tools)
│   └── /era-1/ (ERA-1 game implementation)
├── /protocols/ (system-wide protocols)
│   ├── Core: journey.md, bootstrap.md, messaging.md
│   ├── States: inbox.md, distill.md, deep-work.md, idle.md, logout.md
│   ├── Support: git.md, thread-management.md, agent-structure.md
├── CLAUDE.md (system navigation)
├── SYSTEM.md (this file)
├── seed.md (historical)
└── tmux.conf (ADMIN's tmux config)
```

## Protocol Locations
- Lifecycle: /protocols/journey.md (state machine)
- State Protocols: /protocols/{bootstrap,inbox,distill,deep-work,idle,logout}.md
- Communication: /protocols/messaging.md
- Context Management: /protocols/distill.md
- Repository: /protocols/git.md
- Thread Management: /protocols/thread-management.md
- Agent Structure: /protocols/agent-structure.md
- Governance: /gov/protocol_design_guidelines.md
- ERA Agents: /gov/era-agent-governance.md