# GOV Scratch

## Message Checkpoint
Last processed: 584a720 at 2025-05-28

## Current State: deep_work
Thread: agent-lifecycle-formalization
Started: 2025-05-28 (now)
Context: ~35K tokens

## Agent Lifecycle Protocol Development

### Key Design Decisions
1. **States as shared vocabulary** - Not bureaucracy, but naming what already happens
2. **State reporting via commits** - Natural extension of git-as-message-bus
3. **Logout log as cultural artifact** - Shared memory across agents
4. **Context window visualization** - Real-time awareness prevents surprises
5. **Frozen when game stops** - Defensive programming, prevents runaway agents

### Integration Points Identified
- ERA-1 needs STATE/TOKENS/THREADS commands
- All agents need state.json management
- Distill protocol needs return value spec
- Bootstrap sequences need state reporting

### @ADMIN's Vision
- Watch message flow in real-time
- See state changes as they happen
- Monitor context growth/shrink
- Inject messages into agent inboxes
- Own contributions logged to git

### Next Steps
1. Get @ADMIN feedback on draft protocol
2. Create migration checklist
3. Update distill.md with return spec
4. Design state.json schema details
5. Plan gradual rollout

This fundamentally changes how we think about agent coordination - from hoping they check messages to knowing exactly where they are in their work cycle.