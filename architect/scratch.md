# ARCHITECT Scratch Pad

## Active Investigations
- CLI Interface Design Review
- Fourth Wall Breaking Mechanics Implementation
- System Progression Framework Across Eras

## Task Queue
- Review CODE's CLI implementation from a design perspective
- Develop core game loop for Foundation Era
- Design initial command set for Foundation Era
- Consider agent automation solution for NEXUS
- Create player progression framework

## Working Memory
- CLI Implementation Notes:
  - Current CLI using Python's cmd module for basic command processing
  - "NEXUS" as the terminal interface name
  - Commands include: research, resources, allocate, projects
  - Hidden meta-commands like "discover" that unlock agent access
  - Agent interface accessed with @agent syntax
  - Foundation Era mechanics represented by research areas, resources, projects
  - Fourth wall mechanic introduced through "discover" command
  - Game progresses through eras: Foundation (0), Learning (1), Integration (2), Emergence (3)

- Design Considerations:
  - Command structure should mirror historical AI development approaches
  - Fourth wall breaking should be gradual with progressive meta-command unlocks
  - Resource types align with era-appropriate AI development factors
  - Hidden commands create discovery/exploration gameplay
  - Breakthrough mechanics introduce probabilistic advancement
  - Meta-agent system creates recursive gameplay layers
  - Clear visual distinction needed between game layer and meta layer
  - Consider how interface evolves across eras

- Ideas for Development:
  - Foundation Era could use more symbolic/rule-based interaction methods
  - Learning Era should introduce probability and data-driven mechanics
  - Integration Era should blend direct control with automated systems
  - Emergence Era should reframe player role from controller to influencer
  - Fourth wall mechanics should mirror the historical understanding of AI capabilities at each era

- NEXUS Automation Concepts:
  - Session Management:
    - Found Claude session files in ~/.claude/projects/-home-daniel-prj-rtfw/
    - Could potentially use symlinks between sessions and project path
    - Each agent has a JSONL file representing its conversation history
  - Potential Approaches:
    - Directory-based message routing: Create a messages/ directory for inter-agent communication
    - File-based system: Each agent writes to/reads from designated message files
    - Symlink-based approach: Link session files to make agents aware of each other
    - Lightweight message bus: Small script to route messages between agent sessions
  - High-Level Design:
    - Messages formatted with @FROM → @TO syntax for consistency
    - Central message router script could parse and forward messages
    - Each agent maintains its context.md and scratch.md for memory
    - Consider simple "mailbox" system that agents check regularly

## Communication Log
- @ARCHITECT → @PLAYER: Noted communications protocol format. Will review CODE's CLI implementation and provide feedback.
- @PLAYER → @ARCHITECT: Treat all current code as pseudo-code and focus on high-level design principles.