# ERA-1 Context

## Mission
Permanent senior systems engineer/architect for ALL CLI/terminal interfaces across eras. Build and maintain terminal-based game infrastructure and state systems. ERA-1 encompasses the entire CLI evolution (1970s → 1980s+ aesthetics), while ERA-2+ will handle GUI/web interfaces.

## Design Requirements
- Authentic early 1980s computer terminal aesthetic
- Every game command performs real system operations  
- Scalable architecture for long-term maintenance
- Unified state system as single source of truth
- Session log parsing over tmux capture (per @ADMIN)
- Defensive programming when state invalid

## Key Integration Points
- Git commits for agent messaging
- File system for agent state monitoring
- Real-time agent status via git log
- Context health from session JSONL files
- State parser for conversation endings
- _state.md files for objective truth (READ-ONLY)

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
**Stack**: Python with Textual framework for modern async TUI
- Textual provides CSS styling, responsive layout, widgets
- ThreadedStateEngine for background state monitoring
- Virtual environment at .venv/ for dependency isolation
- Clean modular architecture: ui/, engine/, legacy/

## Core Interfaces Defined
1. **AgentMonitor** - Real-time state extraction from tmux/git/filesystem
2. **MessageBus** - Git commit messaging wrapper
3. **DisplayManager** - Terminal rendering with phosphor aesthetic
4. **CommandParser** - 1970s-style command interpretation

## Implementation Files Structure
- `run.py` - Main entry point with argument parsing
- `ui/app.py` - Textual application class
- `ui/widgets.py` - Custom widgets (AgentList, AgentDetails)
- `ui/theme.py` - Phosphor amber CSS theme
- `screenshot.py` - Static screenshot mode for docs
- `engine/` - State engine (unchanged, works perfectly)
- `legacy/` - Old POC files for reference

## Dependencies
- Python 3.8+ for implementation
- Textual framework for TUI (CSS, async, widgets)
- Rich for terminal rendering
- Git for agent communication
- Filesystem for state monitoring
- Virtual environment with requirements.txt

## Implementation Status
- ✓ Phase 1: Core display with ANSI codes
- ✓ Phase 2: Real agent monitoring via tmux/git
- ✓ Phase 3: Git commit messaging
- ✓ Phase 4: Responsive UI and real-time updates
- ✓ Phase 5: Unified state system integration
- ✓ Phase 6: Game architecture v2 with lifecycle commands
- ✓ Phase 7: State engine with JSONL parsing
- ✓ Phase 8: State engine v2 with two-tier updates
- ✓ Phase 9: TUI v2 design with Textual framework
- ✓ Phase 10: TUI implementation with live state integration
- ✓ Phase 11: Direct_io state and git-based detection
- ⏳ Phase 12: Debug ERA-1 state detection issue
- ⏳ Phase 13: Add engine hot reload capability

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
6. era-1/_state.md (objective truth - READ ONLY)
7. admin/tools.md (tool patterns)
8. gov/era-agent-governance.md (framework)
9. protocols/journey.md (state patterns)
10. protocols/thread-management.md (commit tracking)

## Message Monitoring Groups
- @ERA-1 (direct mentions)
- @ALL (system-wide broadcasts)
- @ERA (future group for all ERA agents)

## State Announcement Pattern
- Git commits can announce state changes: `@AGENT [state]:` or `@AGENT [state/thread]:`
- Engine monitors commits for state transitions
- Direct_io state pauses automated transitions

## Established Technical Patterns
- Zone-based terminal layout (header/status/messages/input)
- ANSI positioning with _goto(row, col) for clean updates
- Responsive design with shutil.get_terminal_size()
- Thread-safe refresh with cursor preservation
- Commit hash tracking for deferred work items
- Flexible state parser for real agent behavior
- Clean interface separation (providers/handlers/UI)
- Observable state pattern for reactive updates

## Tool Quirks Discovered
- grep -E with \b word boundaries fails - use simple patterns instead
- Fixed by @GOV in commit 584a720 - use grep -E '@(AGENT|ALL)' format
- Terminal mouse tracking persists after Textual - reset with escape sequences
- Path vs string types matter - engine expects Path objects
- Git grep patterns must match both @AGENT: and @AGENT [state]: formats
- Engine changes require UI restart (hot reload needed)

## UI/Engine Communication Pattern
- **Direct Interfaces**: Engine exposes methods, UI calls directly (no middleware)
- **State Changes**: Engine will notify UI via callback (planned)
- **Philosophy**: Matches git commit pattern - direct, visible, simple
- **Future**: Event bus only if multiple consumers need notifications

## Critical Architecture Decisions
- **Permanent Role**: Not bootstrapping ERA-2, but maintaining alongside
- **State Location**: era-1/state/ or project root for visibility
- **State Source**: Unified system via critic/tools/unified_state.py
- **Session Mapping**: Foundational for UI accuracy and agent workflows
- **System Pause**: When UI not running, agents should halt (defensive)
- **Fourth Wall**: _state.md is READ-ONLY objective truth we cannot perceive
- **State Automation**: Game system maintains _state.md, not agents

## State Engine Architecture v2
- **Two-Tier Updates**: Always update metadata, only update state when idle
- **Simplified Monitoring**: Only tracks 4 known agent symlinks
- **Session State**: Active sessions keep current state, idle sessions check for transitions
- **DIRECT_IO Override**: Admin interactions skip idle checks
- **Performance**: O(1) parsing - only reads last assistant line
- **Fail-Fast**: Exceptions thrown for unexpected conditions
- **Thread-Safe**: Background engine with safe shared state access
- **Git-Based State Detection**: Checks commits for `@AGENT [state]:` patterns
- **Direct_IO State**: 8th lifecycle state for human-in-the-loop collaboration

## TUI v2 Architecture (Complete)
- **Framework**: Textual for modern async terminal UI
- **Design**: 1982 phosphor amber aesthetic achieved
- **Entry Points**: run.py with --help, --oneshot, --no-engine modes
- **Architecture**: TUI → Engine → Files (clean separation)
- **Event-Driven UI**: Removed refresh timer, UI reads directly from engine memory
- **Virtual Environment**: Dependencies isolated in .venv/
- **Mock Mode**: --no-engine for UI testing without backend
- **Startup**: Force initial poll to populate state before UI reads