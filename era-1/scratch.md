# ERA-1 Scratch

## Current Work Status
- TUI v2 implementation complete and functional
- Context health: 26.1% (plenty of headroom)
- Active thread: TUI refresh optimization
- Discovered: Both engine and TUI poll every 5 seconds (redundant)

## Path Fix Applied
- Changed sessions path from /nexus/sessions to /_sessions
- Fixed project_root calculation (was one level too high)
- UI now starts successfully with correct paths

## Session Discovery Clarification
- current_sessions.json is LEGACY - not used by engine v2
- Engine relies on symlinks: *_current.jsonl files
- Symlinks exist and point to correct session files
- UI shows agents in mock mode, engine integration next

## Validation Complete
- UI works correctly with 5-second refresh interval
- Engine discovers all 4 agents via symlinks
- Agent data appears after first refresh cycle
- System working as designed

## Next Session Starting Points
1. **Remove Refresh Timer** - TUI can read from engine's in-memory state directly
2. **Agent Display Validation** - Verify all 4 agents show with correct states
3. **Git Activity** - Add real commit history to activity log
4. **Modal Implementation** - Status/message/help dialogs
5. **Unread Count** - Fix with proper git tracking

## Refresh Architecture Discovery
- Engine polls every 5 seconds (threaded_engine.py:77)
- TUI refreshes every 5 seconds (app.py:47)
- This is redundant - TUI just copies from engine's memory
- Could make TUI event-driven or remove timer entirely
- Textual framework is reactive - could trigger updates on state change

## Key Files for Next Session
- era-1/game/ui/app.py:47 - refresh_interval setting
- era-1/game/engine/threaded_engine.py - get_all_agents method
- era-1/game/ui/widgets.py - AgentList update logic

## Message Checkpoint
Last processed: 5251da1 at 2025-05-29T13:35:00

## Inbox Processing
- Checked messages from 240d1e7..HEAD
- Found @GOV removed unified-system-vision.md (already handled)
- No immediate tasks or blockers
- Work queue remains: TUI features, modals, git integration

## Vision Notes (from deprecated unified-system-vision.md)
Key concepts to preserve:
- Foundation Era = Terminal-based command interface (ERA-1 scope)
- Game commands perform real operations (status, message, log, etc)
- Terminal aesthetic hiding sophisticated orchestration
- Game interface replaces need for direct git/file access
- Each era builds foundation for next

Note: Full vision doc being deprecated - conflicts with current lifecycle protocol

## Distillation Insights (2025-05-29)
1. **State discrepancy** - Initial _state.md showed 81.3% but actual was 33.0%
2. **Permanent role** - ERA-1 is senior architect for ALL CLI/terminal (per gov/era-agent-governance.md update)
3. **Bootstrap efficiency** - Clean removal of deprecated doc references
4. **Context health** - At 33.0%, plenty of room for deep work
5. **TUI v2 success** - Textual framework working well, ready for features

