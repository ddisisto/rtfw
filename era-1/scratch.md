# ERA-1 Scratch

## Key Insights (2025-05-29 Session)
1. **Redundant polling wastes resources** - UI shouldn't poll when engine already maintains state
2. **Direct memory access** - Reading from shared state is instant vs triggering new operations
3. **Startup sequencing** - Components need proper initialization order
4. **Direct interfaces > middleware** - Matches project's git commit philosophy
5. **Engine bottlenecks** - Full file reads, subprocess spawning, no caching

## Next Priority: Engine State Management
@ADMIN wants to shift focus from UI to engine accuracy. Options:

1. **Git Integration** (fundamental)
   - Real-time commit monitoring
   - Accurate unread counts
   - Message stream processing
   - Challenge: subprocess efficiency

2. **Engine Performance** (low hanging fruit)
   - Fix parse_session_file (only read tail)
   - Cache git results between polls
   - Batch subprocess calls
   - Could enable sub-second polling

3. **State Accuracy**
   - Validate state transitions
   - Better error handling
   - Ensure _state.md consistency

4. **Engine→UI Callbacks**
   - Implement state change notifications
   - Remove force_poll() hack
   - Enable reactive updates

## Message Checkpoint
Last processed: 5251da1 at 2025-05-29T13:35:00


