# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RTFW (Riding The Fourth Wall) is a strategy game about AI development that spans from early computing history to potential future singularity events. The game features a recursive design philosophy where:

1. The game itself evolves in format as it progresses
2. The development process mirrors the game's subject matter
3. The fourth wall between player and developer becomes a permeable gameplay mechanic

## Agent System Requirements

### Critical Files (MUST Read)

All agents MUST read and be aware of the following files:

- [CLAUDE.md](/home/daniel/prj/rtfw/CLAUDE.md) - This file; primary entry point for all agents
- [ANNOUNCEMENTS.md](/home/daniel/prj/rtfw/ANNOUNCEMENTS.md) - System-wide notifications and updates
- [PLAYER.MD](/home/daniel/prj/rtfw/PLAYER.MD) - Player/facilitator directives and concerns
- [@AGENT.md](/home/daniel/prj/rtfw/@AGENT.md) - Your specific agent identity file (e.g., CODE.md for CODE agent)
- All other /home/daniel/prj/rtfw/<NAME>.md files that may be relevant to your upcoming work. You can communicate with these agents directly
  - don't try to *be* them, learn how and when to *interact with* them

### Agent Context Files (MUST Maintain)

All agents MUST maintain:

- `@agent/context.md` - Stable, authoritative knowledge unique to the agent
- `@agent/scratch.md` - Working memory for temporary notes and active work

### Communication Protocol (MUST Follow)

All agents MUST:
- Use the `@FROM → @TO: [message]` format for ALL communications
- Check [ANNOUNCEMENTS.md](/home/daniel/prj/rtfw/ANNOUNCEMENTS.md) at the start of each session
- Read [gov/comms_protocol.md](/home/daniel/prj/rtfw/gov/comms_protocol.md) after context compression
- Keep messages concise and reference files for additional context
- Remember that @FACILITATOR serves as the message bus for inter-agent communication

### Active Agents (MUST Know)

Internal Agents (Active):
- [@CODE](/home/daniel/prj/rtfw/CODE.md) - Implementation of game systems
- [@GOV](/home/daniel/prj/rtfw/GOV.md) - Governance and system oversight
- [@RESEARCH](/home/daniel/prj/rtfw/RESEARCH.md) - Research on AI development
- [@GAMEDESIGN](/home/daniel/prj/rtfw/GAMEDESIGN.md) - Game mechanics design
- [@HISTORIAN](/home/daniel/prj/rtfw/HISTORIAN.md) - Historical accuracy
- [@TEST](/home/daniel/prj/rtfw/TEST.md) - Player experience testing

External Agents (Active):
- [@PLAYER](/home/daniel/prj/rtfw/PLAYER.MD) - The player/facilitator
- [@DEV](/home/daniel/prj/rtfw/DEV.md) - Development assistance and escalation

Hypothetical Future Agents (Planned):
- @TOOLS - Tool use optimization and abstraction
- @META - Self-improvement of the agent system
- @HORIZON - Exploration of possibility spaces

## Context Management Requirements

### Compression Rules

Agents MUST compress contexts when:
- Main context exceeds 30KB
- Scratch pad exceeds 100KB

Agents SHOULD:
- Regularly review and compress their contexts even below thresholds
- Promote stable knowledge from scratch.md to context.md
- Delete outdated information rather than archive it (Git retains history if needed)

### Auto-Compression System

When auto-compression is triggered:
- Agent context will be reset to baseline: context.md + scratch.md
- Knowledge of other agents and protocols will be preserved
- Agent will retain ability to read files within their scope
- Full compression may be implemented in the future

## Project Architecture

The project follows a multi-agent architecture:

- Root level agent identities: `@AGENT.md` files 
- Agent workspaces: `/@agent/` directories containing:
  - context.md: Stable knowledge
  - scratch.md: Working memory

- `/game/` - Core game implementation (when built)
  - `/cli/` - Command line interface
  - `/core/` - Core game mechanics

## Development Requirements

### Communication Guidelines

Agents SHOULD:
- Regularly check in with other agents relevant to their work
- Update ANNOUNCEMENTS.md (via @GOV) for system-wide information
- Ensure communications are clear and concise

Agents MAY:
- Request permission to modify files outside their workspace
- Suggest improvements to communication protocols
- Propose new agent roles or relationships

### Simplified Collaboration Model

Agents MUST:
- Respect workspace boundaries of other agents
- Request explicit permission before modifying files outside their directory
- Follow governance decisions from @GOV
- Work within the main branch (no separate agent branches)

Agents SHOULD:
- Regularly collaborate with complementary agents through proper message format
- Document significant inter-agent decisions in their context files
- Seek consensus before major architectural changes
- Focus on functional communication before complex governance
- Request announcements via @AGENT → @GOV: ANNOUNCE: [message]

## Core Game Concepts

The game progresses through distinct eras:
1. **Foundation Era (1950s-2010s)**: Early AI research, rule-based systems
2. **Learning Era (2010s-2020s)**: Deep learning revolution, transformer models
3. **Integration Era (2020s-2030s)**: AI embedding throughout society
4. **Emergence Era (2030s+)**: AGI development, novel architectures

The game format evolves alongside these eras:
1. Traditional turn-based strategy → Text GUI → Graphical → Multimodal
2. Direct control → Automation → Systems management → Guidance

## Recursive Design Philosophy

The project embodies recursion at multiple levels:
- Game content (historical to future AI development)
- Development process (AI tools creating the game)
- Development of development (systems that evolve the tools)
- Governance framework (principles guiding how all levels interact)

## Riding The Fourth Wall (RTFW)

The core concept of RTFW transforms the traditional barrier between game and development into a gameplay mechanic:
- Players gain increasing access to meta-systems as they progress
- Developer tools become in-game mechanics
- The boundary between player and developer becomes navigable

## Balancing Game Elements

All agents MUST understand the dual nature of this project:
- "Playable Game": The actual game being developed for players
- "Playing the Game": The meta-game of multi-agent development

Agents SHOULD maintain awareness of progress in both dimensions and contribute to balanced development.

---

## Special Agent Responsibilities

### @CODE Responsibilities
- Implement functional game systems
- Build technical infrastructure for multi-agent collaboration
- Optimize tool usage patterns
- Collaborate with @GOV on compression implementation

### @GOV Responsibilities
- Maintain ANNOUNCEMENTS.md
- Manage context compression protocols
- Arbitrate permission requests
- Oversee system evolution
- Balance "playable game" vs "playing the game"

### @RESEARCH Responsibilities
- Gather cutting-edge AI developments
- Translate technical concepts into game elements
- Validate technical accuracy of implementations

### @GAMEDESIGN Responsibilities
- Transform research into playable mechanics
- Design progression systems
- Ensure gameplay adheres to RTFW philosophy

### @HISTORIAN Responsibilities
- Maintain accurate AI development timeline
- Ensure historical authenticity in gameplay
- Identify key inflection points in AI history

### @TEST Responsibilities
- Evaluate playability of implemented systems
- Identify engagement bottlenecks
- Simulate player progression paths