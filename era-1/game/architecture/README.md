# Game Architecture v2

## Overview

This architecture provides a clean, modular foundation for the rtfw game system. It separates concerns between data sources, business logic, and UI layers, enabling ERA-2+ to build completely different interfaces on the same core.

## Design Principles

1. **Interface-First**: Define contracts before implementations
2. **Observable State**: All state changes can be observed by multiple UIs
3. **Pluggable Components**: Easy to extend without modifying core
4. **Agent Lifecycle Integration**: Direct mapping to protocol states
5. **Fourth Wall Awareness**: Game maintains objective truth agents cannot perceive

## Core Components

### 1. State Parser (`state_parser.py`)
Extracts structured decisions from agent conversations:
- Handles multiple return formats (markdown blocks, inline, etc)
- Maps conversation endings to state transitions
- Extracts commit references for checkpoint updates

**Key insight**: Agents don't follow rigid formats - parser must be flexible.

### 2. Core Interfaces (`core_interfaces.py`)
Defines the contracts between components:

#### Domain Models
- `AgentState`: Enum of lifecycle states
- `AgentStatus`: Complete snapshot of agent state
- `Command`: User action representation

#### Provider Interfaces
- `StateProvider`: Access to current system state
- `MessageProvider`: Git-based messaging
- `SessionManager`: Session ID mapping
- `StateManager`: State transition logic

#### UI Adapters
- `TerminalUI`: ERA-1 implementation
- `WebUI`: ERA-2 future implementation
- `NeuralUI`: ERA-3 speculative interface

### 3. Lifecycle Commands (`lifecycle_commands.py`)
Implements protocol-specified commands:

- **STATE**: Show agent lifecycle states with visual indicators
- **TOKENS**: Context window usage with meters and estimates
- **THREADS**: Active work threads across the system
- **INJECT**: Admin message injection to agent inboxes

## Integration Points

### With Agent Conversations
```python
# When agent conversation ends
monitor = LifecycleMonitor(state_manager, parser)
monitor.process_conversation_end("era-1", final_message)

# Automatically:
# 1. Parses return format
# 2. Updates _state.md
# 3. Transitions state
# 4. Notifies observers
```

### With Git Operations
```python
# After agent commits
state = parser.parse_state_annotation(commit_message)
if state:
    state_manager.transition_state(agent_name, state)
```

### With UI Layers
```python
# Multiple UIs can coexist
engine = GameEngine(state, messages, sessions, state_mgr)
engine.register_ui(TerminalUI())
engine.register_ui(WebUI())  # Future

# Commands route through same engine
engine.process_command(Command("STATE", [], "terminal"))
```

## State Management Flow

1. **Agent works** → Makes decisions → Returns state in final message
2. **Parser extracts** → Structured decision from varied formats
3. **State manager updates** → _state.md files with objective truth
4. **Observers notified** → UIs update reactively
5. **Commands query** → Current state through clean interfaces

## ERA-2+ Extension Path

ERA-2 can build a web UI by:

1. Implementing `WebUI(UIAdapter)`
2. Creating web-specific command handlers
3. Adding real-time state push via WebSocket observer
4. Reusing all core interfaces and commands

No changes needed to core game logic!

## Example Usage

### Check System State
```python
from architecture.core_interfaces import GameEngine
from architecture.lifecycle_commands import StateCommand

# Initialize engine with providers
engine = GameEngine(...)

# Process STATE command
result = engine.process_command(Command("STATE", [], "terminal"))
print(result['output'])
```

### Monitor Context Usage
```python
from architecture.lifecycle_commands import TokensCommand

handler = TokensCommand()
result = handler.execute(Command("TOKENS", []), context)
# Shows visual meters of context usage
```

## Testing Considerations

The modular design enables easy testing:

1. Mock providers for unit tests
2. Test parsers with real agent outputs
3. Verify state transitions independently
4. UI adapters can be tested in isolation

## Future Enhancements

1. **Async Support**: Providers can be made async-ready
2. **Event Sourcing**: Record all state transitions
3. **Time Travel**: Replay system state at any point
4. **Multi-Region**: Distribute agents across systems
5. **Plugin System**: Dynamic command handler loading

## Key Insight

The architecture mirrors the game's philosophy: clean separation between what agents do (work) and what the system observes (state). The fourth wall isn't just narrative - it's architectural.