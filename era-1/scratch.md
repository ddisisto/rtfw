# ERA-1 Scratch

## Tools Created (2025-05-30)
- `pidfile.py` - Single-instance enforcement for engine
- `test_engine.py` - Test engine in isolation (requires stopping main)
- `validate_state.py` - Check state consistency (safe with running engine)
- `models_v2.py` - Structured state model matching _state.md template
- `state_parser_v2.py` - Structure-aware parser for _state.md
- `test_state_v2.py` - Test v2 models and round-trip serialization

## Path Forward (2025-05-30, Context: 68.1% - distilling)

### Immediate Tasks
1. **PID-based session discovery** - @ADMIN's suggestion for robust tmux→PID→session mapping
2. **Engine observability** - Add error logging and test harness
3. **Architecture clarity** - Define clear interfaces between components

### Completed Today
- ✓ Created pidfile.py for single-instance enforcement
- ✓ Integrated into run.py and ui/app.py
- ✓ Engine/UI running stable (PID 970985)

### Architecture Decisions Needed
1. **Keep monolithic or split?**
   - Current: UI + Engine in same process (simpler)
   - Alternative: Separate processes with IPC (more flexible)

2. **Logging strategy**
   - Simple: File-based logs in era-1/logs/
   - Advanced: Structured logging with rotation

3. **Test infrastructure**
   - Unit tests for engine components
   - Integration tests for state transitions
   - Mock JSONL sessions for testing

### Next Session Focus
When resuming from bootstrap:
1. Check unread messages (currently 3)
2. Implement PID-based session discovery
3. Add basic error logging
4. Create test harness for engine

## Recent checkpoint: 7502718 (2025-05-30T13:19:00)