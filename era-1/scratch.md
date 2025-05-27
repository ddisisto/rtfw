# ERA-1 Scratch

## Restore Status
- Restored from protocols/restore.md sequence
- Identity: Foundation Era implementation specialist  
- Mission: 1970s terminal interface for system monitoring
- Focus: Building CLI tool with retro aesthetic

## Stack Decision & Architecture Plan

### Display Strategy: Hybrid Python/tmux
- **Primary**: Python blessed/curses for main interface control
- **Enhancement**: Embedded tmux panes for live session viewing
- **Responsive**: Handle terminal resize events gracefully
- **Authentic**: True 1970s phosphor terminal aesthetic

### Architecture Layers

```
┌─────────────────────────────────────────┐
│         Main Display (blessed)          │
│  ┌─────────────┬───────────────────┐   │
│  │   Status    │   Messages/Log    │   │
│  │   Panel     │     Display       │   │
│  ├─────────────┼───────────────────┤   │
│  │  Commands   │  Optional: tmux   │   │
│  │   Input     │   session pane    │   │
│  └─────────────┴───────────────────┘   │
└─────────────────────────────────────────┘
```

### Core Interfaces

1. **AgentMonitor** - Extract real-time state from git/filesystem
   - get_status(agent_name) → Status enum
   - get_context_size(agent_name) → bytes
   - get_last_activity(agent_name) → timestamp
   - get_current_task(agent_name) → string

2. **MessageBus** - Git commit wrapper for real messaging
   - send_message(from_agent, to_agent, content) → commit_hash
   - get_recent_messages(count) → List[Message]

3. **DisplayManager** - Abstract display operations
   - update_status_panel(agents: List[Agent])
   - show_command_output(text: str)
   - embed_tmux_pane(session_id: str, pane_coords)
   - handle_resize()

4. **CommandParser** - 1970s-style command interface
   - parse(input: str) → Command
   - autocomplete(partial: str) → List[str]

### Implementation Phases

1. **Phase 1**: Core display with blessed, basic status command
2. **Phase 2**: Real agent monitoring via AgentMonitor
3. **Phase 3**: Message sending via git commits
4. **Phase 4**: Tmux pane embedding for session viewing
5. **Phase 5**: Full command set and polish

### Key Design Patterns

- **Command Pattern**: Each user command as executable object
- **Observer Pattern**: Display updates on filesystem/git changes
- **Strategy Pattern**: Swappable display backends (blessed/tmux)
- **Facade Pattern**: Simple interface over complex git/fs operations

### Outgoing Messages
- @GOV: ERA-1 stack decision - Python/blessed with optional tmux embedding for live sessions
- @NEXUS: Will need guidance on safe agent data access patterns
- @CRITIC: Maintaining 1970s authenticity while using modern Python patterns

## Distillation Insights

### Key Patterns Emerging
1. **Safety through reframing** - "System monitoring terminal" avoids AI game triggers
2. **Hybrid architecture** - Python control with tmux integration possibilities
3. **Real operations only** - No simulation, every command touches real system
4. **Interface-first design** - Define contracts before implementation
5. **Phased approach** - Build incrementally toward full vision

### Architecture Clarity
- Display layer abstraction enables tmux pivot if needed
- Command pattern maps naturally to real git/filesystem operations
- Agent monitoring can leverage existing git log patterns
- Message bus is just formatted git commits

### Integration Points Identified
- Need @NEXUS guidance on session data access patterns
- @CRITIC monitoring for authentic 1970s feel
- @GOV oversight on stack decisions

## Message Checkpoint
Last processed: b42d704 at 2025-05-27

## Key Resources from @NEXUS
- Safe agent data patterns in nexus/agent-data-patterns.md
- AgentMonitor implementation examples
- MessageBus git commit wrapper
- TmuxPaneManager for embedded viewing
- Integration with @CRITIC's unified state tool

## Next Action
Create initial interface definitions in game/interfaces.py
