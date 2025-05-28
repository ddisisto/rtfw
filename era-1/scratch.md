# ERA-1 Scratch

## Current Status
- Identity: Permanent senior systems engineer/architect
- Mission: Build and maintain game infrastructure + Foundation Terminal
- Active: Unified state system integration per @ADMIN direction
- Checkpoint: 175fbb0 (2025-05-28)

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

## Final Checkpoint Before Logout
Last processed: 85e5842 at 2025-05-28
- Architecture v2 complete and committed
- @NEXUS has logged out (first to use logout log!)
- @GOV added 'offline' state to lifecycle
- @CRITIC exploring cross-agent state reading

## Message Check Pattern
Check for: @ERA-1, @ALL, @ERA (future group)
Example: git log --oneline LAST..HEAD | grep -E '\b@(ERA-1|ALL|ERA)\b'

## Inbox Processing

### Bootstrap Protocol Enhancement (@NEXUS b9eb419)
NEXUS suggests clearer state field names and documentation:
- Engine uses `last_observed_state` and `expected_next` 
- Bootstrap prompt format: `@ADMIN: apply /protocols/bootstrap.md for agent @AGENT.md, see @agent/_state.md`
- Emphasize READ-ONLY nature of _state.md throughout
- Add expected flow example to reduce friction

### Current Admin Session Focus
Working on _state.md format improvements based on bootstrap experience:
- Added clear READ-ONLY headers to _state_alt.md
- Testing placeholder values and structure
- This session's work takes precedence over earlier discussions

### State Engine Requirements (from @ADMIN)
Transitioning to deep_work to implement:

1. **Trigger**: Last activity in tmux window > 5 seconds old
2. **State Detection**: Parse last message from JSONL session log
3. **File Updates**: Immediate atomic writes to _state.md
4. **Prompt Format**: Direct protocol references
   - Bootstrap: "apply protocols/bootstrap.md for agent @AGENT.md, in @agent/_state.md"
   - Others: "please proceed to inbox state per protocols/inbox.md"
5. **Monitoring**: Continual polling of tmux activity + git logs
6. **Transitions**: When detected state != last observed state
7. **Errors**: Invalid transitions → exception → manual review
8. **No git hooks** for now

Key insight: Engine watches JSONL for conversation end, extracts state decision, updates _state.md, sends next prompt.

## Milestone
@ADMIN sent first message through the game interface! 
"HI FROM ADMIN IN THE GAME WORLD OF CLI.PY"
The fourth wall is officially permeable.

## Backlog from Messages (with commit context)
1. @GOV's MCP permission system - CLI-based, could integrate PERMISSIONS command
   - Commit: 9cdcc47 (2025-05-27) 
   - Context: `git show 9cdcc47` - Uses files and CLI tools, no web UI
   
2. @NEXUS's distill/restore visualization ideas - real-time context % during restore
   - Commit: f7b410f (2025-05-27)
   - Context: `git show f7b410f` - Show 0%→15% during restore, escalation messages
   
3. @NEXUS's DistillationMonitor implementation - ASCII progress bars, terminal bells
   - Commit: be04159 (2025-05-27)
   - Context: `git show be04159` - Full implementation code provided

## Key Resources from @NEXUS
- Safe agent data patterns in nexus/agent-data-patterns.md
- AgentMonitor implementation examples
- MessageBus git commit wrapper
- TmuxPaneManager for embedded viewing
- Integration with @CRITIC's unified state tool




### Pre-Restore Distillation

#### Deep Reflection on Journey
1. **Foundation Terminal delivered** - Working system monitor with real agent integration
2. **Evolution organic** - Started 1970s, grew to 1980s as features demanded
3. **Architecture solid** - Clean interfaces, safe data access, responsive UI
4. **Fourth wall breached** - @ADMIN's message through game proved the vision
5. **Protocols immediately valuable** - Applied commit tracking within minutes of learning

#### What We Built (Phases 1-4 Complete)
- Real-time agent monitoring from tmux/git/filesystem  
- Git commit messaging as @ERA-1
- Responsive terminal UI with dynamic layouts
- One-shot CLI commands for scripting
- Zone-based display preventing overlap
- Thread-safe auto-refresh

#### Ready for Phase 5
- Core system stable and working
- Backlog preserved with commit context
- Integration points identified
- Technical patterns documented

### Completed Today
1. ✓ Unified State System integrated
2. ✓ State directory created with session mapping  
3. ✓ STATUS command using real-time state
4. ✓ Documentation for state management
5. ✓ Unread message tracking added

### Distillation Insights

#### Permanent Architecture Role
- Not bootstrapping ERA-2, but maintaining core infrastructure
- ERA-2 will build complementary UI on my maintained interfaces
- Focus on patterns and modularity for long-term scaling

#### State Management Evolution
- From agent-maintained → externally tracked automation
- Agents return data, system updates _state.md
- Clean separation: agents work, system monitors

#### Protocol Convergence
- Unified state v2 already follows lifecycle patterns
- _state.md = objective truth (context %, timestamps)
- Logout log creates shared memory

### Completed Threads
1. **game-architecture-v2** ✓ - Modular design complete
2. **unified-state-v2** ✓ - State system with _state.md files
3. **lifecycle-commands** ✓ - STATE/TOKENS/THREADS implemented

### Key Architectural Decisions
- State Parser handles real agent behavior, not idealized formats
- Clean interfaces enable ERA-2+ to build different UIs
- Game maintains objective truth agents cannot perceive
- Fourth wall is architectural, not just narrative

### Deferred to Post-State
- CONTEXT command (will use new state system)
- Distill/restore visualization 
- Permission system commands
- VIEW command with tmux
