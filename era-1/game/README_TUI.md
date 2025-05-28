# Foundation Terminal TUI v2

## Overview

Production implementation of the Foundation Terminal using Textual framework. This replaces the POC cli.py with a proper event-driven TUI that integrates with the state engine for live updates.

## Architecture

```
run.py                 # Main entry point
ui/
├── __init__.py       # Module init
├── app.py            # Main Textual application
├── theme.py          # Phosphor amber CSS theme
├── widgets.py        # Custom widgets (AgentList, AgentDetails, etc)
├── modals.py         # Dialog boxes (coming soon)
└── integrations.py   # Engine/Git integration (coming soon)

engine/               # Existing state engine (unchanged)
├── threaded_engine.py
├── state_writer.py
├── git_monitor.py
└── ...

legacy/               # Old POC files for reference
├── cli.py
├── display.py
└── ...
```

## Key Design Decisions

1. **Textual Framework**: Modern async TUI with CSS styling and responsive layout
2. **Live Updates**: ThreadedStateEngine runs in background, UI polls every 5 seconds
3. **Separation of Concerns**: Clean UI/Engine boundary via well-defined interfaces
4. **MVP First**: Read-only monitoring before adding interactions
5. **Phosphor Aesthetic**: Amber monochrome theme with 1982 terminal feel

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the terminal
python run.py

# Development mode with hot reload
textual run --dev run.py
```

## Current Status

### Implemented
- [x] Basic application structure
- [x] Phosphor amber theme
- [x] Agent list widget with state coloring
- [x] Agent details panel
- [x] Command palette
- [x] Engine integration scaffolding
- [x] Auto-refresh timer

### TODO
- [ ] Message composition modal
- [ ] Status overview screen
- [ ] State injection dialog
- [ ] Git activity integration
- [ ] Context usage graphs
- [ ] Help system
- [ ] Session viewer (tmux integration)
- [ ] Error handling and recovery

## Integration Points

The TUI connects to the existing engine through these interfaces:

```python
# From ThreadedStateEngine
engine.get_all_agents() -> Dict[str, AgentGroundState]
engine.get_agent_state(name) -> AgentGroundState  
engine.force_poll() -> None

# Future additions
git.send_message(agent, message) -> None
state.inject_transition(agent, new_state) -> None
```

## Design Philosophy

The Foundation Terminal embodies the principle that "the game IS the development environment". Every displayed element represents real system state, and every command performs actual operations. The 1982 aesthetic is a stylistic choice that reinforces the "foundation era" theme while providing modern UX patterns underneath.