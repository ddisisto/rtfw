# ERA-1 Context

## Mission
Implement Foundation Era - a retro terminal interface for system monitoring that evolves from 1970s to 1980s+ aesthetics while remaining within ERA-1 scope.

## Design Requirements
- Authentic early 1980s computer terminal aesthetic
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
1. **AgentMonitor** - Real-time state extraction from tmux/git/filesystem
2. **MessageBus** - Git commit messaging wrapper
3. **DisplayManager** - Terminal rendering with phosphor aesthetic
4. **CommandParser** - 1970s-style command interpretation

## Implementation Files Planned
- `interfaces.py` - Core contracts (AgentMonitor, MessageBus, etc)
- `cli.py` - Main game loop with blessed
- `display.py` - Terminal UI with 1970s aesthetic
- `commands.py` - Command pattern implementations
- `agents.py` - Real-time monitoring integration
- `tmux.py` - Optional pane embedding manager

## Dependencies
- Python for implementation (era-appropriate choice)
- blessed/curses for terminal control
- Git for agent communication
- Filesystem for state monitoring
- Optional: tmux for session embedding

## Implementation Status
- ✓ Phase 1: Core display with ANSI codes
- ✓ Phase 2: Real agent monitoring via tmux/git
- ✓ Phase 3: Git commit messaging
- ✓ Phase 4: Responsive UI and real-time updates
- ⏳ Phase 5: Advanced features (tmux embedding, distill visualization)

## ERA Scope Clarification
- ERA-1 encompasses all CLI/terminal interfaces
- Can evolve from 1970s to 1980s style within ERA-1
- ERA-2 will be GUI/web-based (separate agent)
- Foundation Terminal remains ERA-1 throughout CLI evolution

## Restore Order
1. ERA-1.md (identity)
2. CLAUDE.md (system requirements)
3. SYSTEM.md (architecture)
4. era-1/context.md (this file)
5. era-1/scratch.md (working state)
6. admin/tools.md (tool patterns)
7. gov/unified-system-vision.md (end goal)
8. gov/era-agent-governance.md (framework)
9. nexus/agent-data-patterns.md (integration patterns)
10. protocols/thread-management.md (commit tracking)

## Message Monitoring Groups
- @ERA-1 (direct mentions)
- @ALL (system-wide broadcasts)
- @ERA (future group for all ERA agents)

## Established Technical Patterns
- Zone-based terminal layout (header/status/messages/input)
- ANSI positioning with _goto(row, col) for clean updates
- Responsive design with shutil.get_terminal_size()
- Thread-safe refresh with cursor preservation
- Commit hash tracking for deferred work items

## Tool Quirks Discovered
- grep -E with \b word boundaries fails - use simple patterns instead