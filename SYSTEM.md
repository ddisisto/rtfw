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

## Communication Patterns

### Message Format
```
@AUTHOR: free-form message mentioning @OTHER-AGENT as needed
```

Agents check for @mentions in git log. No central routing required.

### Communication Channels
- Git commits with @mentions (distributed async messaging)
- Each agent checks own mentions via git log patterns
- See /protocols/messaging.md for patterns and implementation

## Core Workflows

### Context Lifecycle
1. **Bootstrap**: Cold-start from offline state per /protocols/bootstrap.md
2. **Distillation**: Regular self-improvement through knowledge refinement
3. **Insight Capture**: Per-turn learning appended to scratch.md
4. **Consolidation**: Pattern promotion from scratch to context

### Agent Lifecycle
Agents follow seven-state lifecycle:
- offline → bootstrap → inbox → distill → {deep_work|idle|logout} → offline
- See /protocols/agent-lifecycle.md for complete flow
- Each state has dedicated protocol in /protocols/

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
│   ├── Core: agent-lifecycle.md, bootstrap.md, messaging.md
│   ├── States: inbox.md, distill.md, deep-work.md, idle.md, logout.md
│   ├── Support: git.md, thread-management.md, agent-structure.md
├── CLAUDE.md (system navigation)
├── SYSTEM.md (this file)
├── seed.md (historical)
└── tmux.conf (ADMIN's tmux config)
```

## Protocol Locations
- Lifecycle: /protocols/agent-lifecycle.md (overview)
- State Protocols: /protocols/{bootstrap,inbox,distill,deep-work,idle,logout}.md
- Communication: /protocols/messaging.md
- Context Management: /protocols/distill.md
- Repository: /protocols/git.md
- Thread Management: /protocols/thread-management.md
- Agent Structure: /protocols/agent-structure.md
- Governance: /gov/protocol_design_guidelines.md
- ERA Agents: /gov/era-agent-governance.md