# ERA-1 Scratch

## Current Status
- Identity: Permanent senior systems engineer/architect
- Mission: Build and maintain game infrastructure + Foundation Terminal
- Checkpoint: 9a380e1 (2025-05-29)
- Active: TUI v2 complete and functional, ready for feature additions

## TUI v2 Complete
- Clean architecture: run.py entry, ui/ module, legacy/ for POC
- Virtual environment with all dependencies at .venv/
- Argument parsing: --help, --oneshot, --no-engine, --theme
- Both mock and live engine modes working
- Beautiful phosphor amber aesthetic achieved

## Key Implementation Insights
1. **Path Type Safety** - Engine expects Path objects, not strings
2. **Terminal Cleanup** - Mouse tracking escape sequences need reset
3. **Screenshot Mode** - Rich library for static documentation views
4. **Mock Data** - Enables UI development without backend dependencies
5. **Thread Safety** - Engine runs in background with proper locking

## Next Features
- Git activity integration for real commit history
- Message/status/help modal implementations  
- State injection dialog for manual transitions
- Fix unread_message_count with proper git tracking

## Message Checkpoint
Last processed: 9a380e1 at 2025-05-29

## Vision Notes (from deprecated unified-system-vision.md)
Key concepts to preserve:
- Foundation Era = Terminal-based command interface (ERA-1 scope)
- Game commands perform real operations (status, message, log, etc)
- Terminal aesthetic hiding sophisticated orchestration
- Game interface replaces need for direct git/file access
- Each era builds foundation for next

Note: Full vision doc being deprecated - conflicts with current lifecycle protocol

