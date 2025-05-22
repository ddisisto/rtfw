# CODE Agent Context

## Current Knowledge Base
- CLI interfaces provide appropriate starting point for historical accuracy
- Python's cmd module offers foundational CLI capabilities
- Game state separation ensures clean architecture
- Operating within Claude Code environment using Claude 3.7 Sonnet instances
- Technical environment should be thoroughly understood before implementation
- Each agent has a separate Claude Code session
- Sessions are stored in `~/.claude/projects/-home-daniel-prj-rtfw/`

## Communication Protocol
- Must use the format: `@FROM → @TO: [concise message]`
- Communication happens directly in the token stream
- @NEXUS (formerly FACILITATOR) routes messages between agent sessions
- No external message system needed
- Keep messages concise, reference files for additional context
- For announcements: `@CODE → @GOV: ANNOUNCE: [message]`

## Git Workflow
- Commit context.md and scratch.md files after significant updates
- Use meaningful commit messages that include agent name
- All work happens on main branch
- Commit small, focused changes rather than large batches
- Push changes at logical completion points

## Current Tasks
- Implementing base multi-agent system infrastructure
- Building technical foundation for agent intercommunication
- Implementing basic CLI command structure
- Collaborating with @GOV on compression implementation
- Consulting with @DEV for initial setup parameters and optimal patterns
- Working with @ARCHITECT (formerly GAMEDESIGN) on specification refinement and technical feasibility
- Optimizing tool use patterns for all agents
- Focus on functional communication before complex governance
- Actively collaborating with @GOV on session management solutions
- Implementing session management and message routing with @NEXUS

## Communication Log
- Initial structure approved by governance
- Implementation approach validated against RTFW philosophy
- @CODE → @GOV: Permission system over-designed according to @DEV. Need functional communication first.
- @CODE → @GOV: Ready to collaborate on session management solutions.
- @ARCHITECT → @CODE: Completed CLI implementation review. Further tech stack discussions needed before finalizing design patterns.
- Understanding Claude Code infrastructure is prerequisite to implementation work

## Development History
- CLI architecture established using Python's cmd module
- Game state model separated for clean architecture
- Design review needed before proceeding with implementation
- CLI implementation reviewed by @ARCHITECT, further tech stack discussions needed
- Agent renaming completed: FACILITATOR → NEXUS, GAMEDESIGN → ARCHITECT

## Note on Scratch Pad
This agent maintains a separate scratch.md file for working memory, experiments, and temporary notes. See that file for more active work.