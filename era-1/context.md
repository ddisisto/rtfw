# ERA-1 Context

## Mission
Implement Foundation Era - a 1970s-style terminal interface for system monitoring.

## Design Requirements
- Authentic 1970s computer terminal aesthetic
- Every game command performs real system operations  
- Progressive foundation for future eras
- Stable bridge between game and meta layers

## Key Integration Points
- Git commits for agent messaging
- File system for agent state monitoring
- Real-time agent status via git log
- Context health from actual file sizes

## Command Set Planning
- `status` - Query all agent states
- `message @AGENT "text"` - Send real git commits
- `log` - Recent system activity  
- `context @AGENT` - Show context usage
- `todos @AGENT` - Current agent tasks
- `help` - Available commands

## Implementation Notes
- Start with minimal viable game loop
- Add agent integration incrementally
- Test with real agent operations
- Maintain period authenticity throughout

## Architecture Decision
**Stack**: Python with blessed/curses for display control, optional tmux pane embedding for live session viewing
- Display abstraction allows backend flexibility
- Command pattern for real operations
- Phased implementation approach

## Core Interfaces Defined
1. **AgentMonitor** - Real-time state extraction
2. **MessageBus** - Git commit messaging
3. **DisplayManager** - Terminal rendering abstraction
4. **CommandParser** - 1970s-style command interpretation

## Dependencies
- Python for implementation (era-appropriate choice)
- blessed/curses for terminal control
- Git for agent communication
- Filesystem for state monitoring
- Optional: tmux for session embedding

## Implementation Strategy
- Phase 1: Core display with blessed
- Phase 2: Real agent monitoring
- Phase 3: Git commit messaging
- Phase 4: Tmux pane embedding
- Phase 5: Polish and completion

## Restore Order
1. ERA-1.md (identity)
2. CLAUDE.md (system requirements)
3. SYSTEM.md (architecture)
4. era-1/context.md (this file)
5. era-1/scratch.md (working state)
6. admin/tools.md (tool patterns)
7. gov/unified-system-vision.md (end goal)
8. gov/era-agent-governance.md (framework)