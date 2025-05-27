# ERA-1 Context

## Mission
Implement Foundation Era - a 1970s-style terminal game that provides real agent management capabilities.

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

## Dependencies
- Python for implementation (era-appropriate choice)
- Git for agent communication
- Filesystem for state monitoring
- No external libraries initially (self-contained)

## Next Steps
1. Create basic game loop
2. Implement status command with real data
3. Add messaging capability
4. Build out remaining commands
5. Polish 1970s aesthetic