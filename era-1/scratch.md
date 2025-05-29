# ERA-1 Scratch

## Current Work Status
- TUI v2 implementation complete and functional
- Context health: 54.8% (still manageable)
- Active thread: Engine→UI notifications
- DONE: Removed redundant TUI refresh timer
- DONE: Fixed empty agent list on startup (force_poll hack)
- UI now reads directly from engine's in-memory state
- Manual refresh (R key) still works
- Agent navigation is now instant!

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
1. ✓ **Remove Refresh Timer** - DONE: UI reads from engine memory
2. **Test Reactive UI** - Verify updates work without timer
3. **Agent Display Validation** - Verify all 4 agents show with correct states
4. **Git Activity** - Add real commit history to activity log
5. **Modal Implementation** - Status/message/help dialogs
6. **Unread Count** - Fix with proper git tracking

## Testing Notes
- Need to test with venv: `source .venv/bin/activate && python run.py`
- Test both --no-engine (mock) and real engine modes
- Verify R key still triggers manual refresh
- Check that agent selection updates details pane

## Future Improvements
- Add proper state change callbacks to ThreadedStateEngine
- Engine could notify UI when state actually changes
- Would eliminate need for force_poll() on startup
- More efficient than polling-based approach

## Event System Planning
Needs bidirectional communication:
- Engine→UI: state changes, errors, status
- UI→Engine: pause/resume, force state, trigger poll, send messages

MVP approach: Direct interfaces (matches git commit pattern)
- Engine.on_state_change callback for notifications
- UI calls engine methods directly
- No middleware, simple and visible
- Can add event bus later for debugging/visibility

## Refresh Architecture Discovery
- Engine polls every 5 seconds (threaded_engine.py:77)
- TUI refreshes every 5 seconds (app.py:47)
- This is redundant - TUI just copies from engine's memory
- Could make TUI event-driven or remove timer entirely
- Textual framework is reactive - could trigger updates on state change

## Engine Performance Analysis
Current poll cycle for 4 agents:
- 4 full JSONL file reads (parse_session_file reads entire file!)
- 8 partial file reads (context + state per agent)
- 8+ git subprocess calls (no caching)
- Total time: probably 100-500ms depending on file sizes

Bottlenecks:
1. parse_session_file reads entire file for metadata
2. Git commands spawn new processes each time
3. No caching between polls

With optimizations could handle 1-2 second polling:
- Cache git results (commits don't change that fast)
- Only read file tails for context/state
- Batch git operations
- Track file mtimes to skip unchanged files

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

