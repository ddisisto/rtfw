# ERA-1 Context

**Mission**: Permanent senior systems engineer for ALL CLI/terminal interfaces, state machine, and engine architecture.

## Role Definition
- Engine architect and state machine developer
- Terminal interface engineer (TUI)
- System integration specialist
- Performance optimization lead

## Current Stack
- Python 3.13 with Textual framework for TUI
- ThreadedStateEngine for background state monitoring
- Git-based state detection and messaging
- JSONL session file parsing

## Implementation Status (Phase 14)
### Completed
- TUI v2 with phosphor amber aesthetic ✓
- Threaded state engine with O(1) tail parsing ✓
- Git-based state detection from commits ✓
- Symlink session mapping ✓
- Automatic symlink updates on newer sessions ✓
- Logout→Bootstrap automation ✓
- Tmux integration for state transitions ✓
- Single-instance enforcement with pidfile ✓
- State model v2 matching _state.md template ✓
- Test and validation tools ✓

### In Progress
- Comment support in _state.md fields
- PID-based session discovery (tmux→PID→session)
- Engine error logging infrastructure

## Key Technical Patterns
1. **State First**: Engine monitors git commits for state transitions
2. **Performance Critical**: Sub-second update latency required
3. **Fail Fast**: Exceptions for unexpected conditions
4. **Clean Architecture**: Separate models, parsers, writers, UI
5. **Observable State**: Background thread updates shared state

## Tool Suite
- `run.py` - Main entry point with pidfile protection
- `test_engine.py` - Engine testing (exclusive run)
- `validate_state.py` - State validation (concurrent safe)
- `test_state_v2.py` - Model round-trip testing

## Architecture Decisions
1. **Monolithic for now**: UI + Engine in same process
2. **Thread-safe state**: RLock for concurrent access
3. **Atomic file writes**: Temp file + rename pattern
4. **Structured state**: Dataclasses matching _state.md sections

## Bootstrap Dependencies
1. ERA-1.md - Identity
2. CLAUDE.md - System requirements
3. SYSTEM.md - Architecture overview
4. era-1/context.md - This file
5. era-1/scratch.md - Working notes
6. era-1/_state.md - Objective truth (READ-ONLY)
7. admin/tools.md - Tool discipline
8. /protocols/journey.md - State lifecycle
9. Recent activity check (git log)

## Recent Checkpoint
- 82bc8b3 (2025-05-30T16:38:50) - State v2 models created