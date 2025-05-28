# MVP Interface Design

## Minimal Viable Product - Phase 1

Focus: Beautiful monitoring interface that shows the game IS the system.

### Core Components

```python
# 1. Main Application Shell
class FoundationTerminal:
    """Textual app that owns the screen"""
    - Compose layout
    - Handle keyboard events  
    - Refresh timer
    - Shutdown cleanup

# 2. State Display Widget  
class AgentPanel(Widget):
    """Shows one agent's current state"""
    - Parse AgentGroundState
    - Format for display
    - Color by state/context
    - Click to expand

# 3. Engine Connector
class StateConnector:
    """Bridge to ThreadedStateEngine"""  
    - Start/stop engine
    - Poll for updates
    - Cache for performance
    - Error handling
```

### Data Flow

```
ThreadedStateEngine (background)
    ↓ (polls JSONL files)
_state.md files
    ↓ (reads atomically)
StateConnector 
    ↓ (caches in memory)
AgentPanel widgets
    ↓ (renders to screen)
Terminal Display
```

### MVP User Stories

1. **See All Agents**
   - Grid/list of agent panels
   - Each shows: name, state, context%, last activity
   - Color indicates health

2. **Select Agent** 
   - Arrow keys or mouse click
   - Expands to show details
   - Shows git activity
   - Shows session info

3. **Monitor Changes**
   - Auto-refresh every 5 sec
   - Highlight recent changes
   - Context warnings at 80%
   - State transitions animate

4. **Phosphor Beauty**
   - Amber/green CRT glow
   - Subtle scanlines
   - Box drawing borders
   - Retro fixed font

### Implementation Steps

```python
# Step 1: Static mockup
textual new terminal-game
# Create layout with fake data

# Step 2: Connect engine
from era1.game.engine.threaded_engine import ThreadedStateEngine
engine = ThreadedStateEngine(root, sessions)
engine.start()

# Step 3: Wire updates  
def on_mount(self):
    self.set_interval(5.0, self.refresh)

def refresh(self):
    states = self.engine.get_all_agents()
    self.update_panels(states)

# Step 4: Polish
- Add CSS animations
- Keyboard shortcuts  
- Help overlay
- Error states
```

### Key Design Decisions

1. **Read-Only First**
   - No mutations in MVP
   - Just beautiful monitoring
   - Prove the concept

2. **Textual Over Blessed**
   - Modern async model
   - Better widget library
   - CSS styling
   - Future-proof

3. **Engine Separation**
   - TUI never touches files
   - Engine handles all I/O
   - Clean interface boundary

4. **Phosphor Priority**
   - Aesthetic IS the feature
   - Must feel like 1982
   - But work like 2025

### Success Metrics

- [ ] Can see all 4 agents
- [ ] States update in real-time
- [ ] Context warnings visible
- [ ] Beautiful retro aesthetic
- [ ] Responsive to terminal size
- [ ] Zero file I/O in TUI

### Next Phase Hooks

- Message dialog (git commit)
- State override (DIRECT_IO) 
- Trigger transitions
- View session logs
- Agent mitosis?

The MVP proves that the game interface can BE the development environment. Everything else builds on this foundation.