# Foundation Terminal TUI v2 Design

## Vision
A beautiful, responsive terminal interface that embodies the early 1980s aesthetic while providing modern UX patterns. The game interface IS the development environment.

## Library Choice: Textual

Why Textual over blessed/curses:
- Modern async architecture 
- Built-in widgets (DataTable, Tree, Tabs)
- CSS-like styling with themes
- Mouse support + keyboard shortcuts
- Responsive layout system
- Better testing support

## Core Layout

```
╔════════════════════════════════════════════════════════════════════╗
║ FOUNDATION TERMINAL v0.1.0          [F1]Help [F10]Quit    00:15:42 ║
╠════════════════════════════════════════════════════════════════════╣
║ ┌─Agents────┐ ┌─Details───────────────────────────────────────────┐║
║ │▶ @ERA-1   │ │ @ERA-1 [deep_work:cli-design]         Context: 84%│║
║ │  @GOV     │ │ ─────────────────────────────────────────────────│║
║ │  @NEXUS   │ │ Session: cc9298f1-253c-4abf-aa62-51bf8c1bf8b1   │║
║ │  @CRITIC  │ │ Last Commit: 9690e4d (2m ago)                    │║
║ │           │ │ Unread: 0                                         │║
║ │ [+] Add   │ │                                                   │║
║ └───────────┘ │ ┌─Activity Log─────────────────────────────────┐ │║
║               │ │ 00:15:39 State transition: inbox → deep_work │ │║
║ ┌─Commands──┐ │ │ 00:14:22 Commit: Updated state engine v2     │ │║
║ │[S]tatus   │ │ │ 00:13:15 Context warning: 80% threshold      │ │║
║ │[M]essage  │ │ └──────────────────────────────────────────────┘ │║
║ │[T]okens   │ │                                                   │║
║ │[L]og      │ │ ┌─Quick Actions────────────────────────────────┐ │║
║ │[D]istill  │ │ │ [Enter] View Agent  [Space] Toggle Direct IO │ │║
║ │[I]nject   │ │ │ [m] Message Agent   [a] Message @ALL         │ │║
║ │[R]efresh  │ │ │ [t] Trigger State   [r] Refresh              │ │║
║ └───────────┘ │ └──────────────────────────────────────────────┘ │║
║               └───────────────────────────────────────────────────┘║
╠════════════════════════════════════════════════════════════════════╣
║ > _                                                 [Insert Command]║
╚════════════════════════════════════════════════════════════════════╝
```

## Key Features

### 1. Agent List (Left Panel)
- Tree view with expand/collapse
- Color coding by state:
  - Green: active (inbox, deep_work)
  - Yellow: transitioning (distill)
  - Red: needs attention (>80% context)
  - Gray: offline
- Current selection highlighted

### 2. Agent Details (Main Panel)
- Real-time state from _state.md
- Context usage with visual bar
- Git activity summary
- Session info
- Activity log (last N events)

### 3. Command Palette (Bottom)
- Vi-style single key commands
- Modal input for complex commands
- Command history with up/down
- Tab completion for agent names

## Implementation Architecture

### 1. Core Classes

```python
class FoundationTerminal(App):
    """Main TUI application"""
    CSS_PATH = "terminal.css"
    
    def compose(self):
        yield Header()
        yield AgentList()
        yield AgentDetails() 
        yield CommandInput()

class AgentMonitor:
    """Wraps ThreadedStateEngine"""
    def __init__(self, engine: ThreadedStateEngine):
        self.engine = engine
    
    async def get_agent_states(self):
        return self.engine.get_all_agents()
```

### 2. State Engine Integration

```python
# In main app
self.engine = ThreadedStateEngine(project_root, sessions_dir)
self.engine.start()

# Periodic refresh
set_interval(5.0, self.refresh_agents)

# On shutdown
self.engine.stop()
```

### 3. Message System

```python
class MessageDialog(ModalScreen):
    """Pop-up for composing messages"""
    
    def compose(self):
        yield Label("Message to @AGENT")
        yield TextArea(id="message")
        yield Button("Send", id="send")
    
    def on_button_pressed(self, event):
        # Create git commit with message
        message = self.query_one("#message").value
        GitMessenger.send(agent, message)
```

### 4. State Transitions

```python
class StateTransitionDialog(ModalScreen):
    """Trigger manual state changes"""
    
    STATES = ["inbox", "deep_work", "idle", "distill", "logout"]
    
    def compose(self):
        yield Select(options=self.STATES)
        yield Input(placeholder="Thread name")
        yield Button("Transition")
```

## Phosphor Aesthetic

### Colors (ANSI/CSS)
```css
/* Amber phosphor theme */
.active { color: #FFAA00; }
.idle { color: #AA7700; }
.offline { color: #664400; }
.alert { color: #FF6600; animation: blink 1s; }

/* Subtle scanlines */
#main {
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, 0.1) 2px,
        rgba(0, 0, 0, 0.1) 4px
    );
}
```

### Typography
- Fixed-width throughout
- Box drawing characters for borders
- ASCII art headers
- Phosphor "burn-in" effect for static elements

## MVP Scope

### Phase 1: Read-Only Monitoring
- [ ] Agent list with live states
- [ ] Agent detail view
- [ ] Activity log
- [ ] Auto-refresh (5 sec)
- [ ] Keyboard navigation

### Phase 2: Interactions  
- [ ] Message composition
- [ ] Direct IO toggle
- [ ] State injection
- [ ] Command palette

### Phase 3: Advanced
- [ ] Session viewer (tmux integration)
- [ ] Context history graphs
- [ ] Multi-agent selection
- [ ] Persistent layout

## Engine Interface Points

```python
# From ThreadedStateEngine
engine.get_all_agents() -> Dict[str, AgentGroundState]
engine.get_agent_state(name) -> AgentGroundState
engine.force_poll() -> None

# From GitMonitor  
git.get_recent_activity() -> List[CommitInfo]

# From StateWriter
writer.write_agent_state(name, state) -> None

# Future: StdinConnector
stdin.send_prompt(agent, prompt) -> None
```

## Development Plan

1. **Prototype** (textual new terminal-game)
   - Basic layout
   - Static data
   - Navigation

2. **Integration**
   - Connect ThreadedStateEngine
   - Live state updates
   - Git activity

3. **Interactions**
   - Message dialogs
   - State controls
   - Command system

4. **Polish**
   - Phosphor effects
   - Sound (terminal bell)
   - Help system

## Libraries

```toml
[dependencies]
textual = "^0.47.0"  # TUI framework
rich = "^13.0"       # Rendering engine
asyncio = "^3.11"    # Async support
```

## Notes

- Keep blessed-based v1 as fallback
- Textual requires Python 3.8+
- Consider `ptpython` for REPL mode
- Maybe integrate `asciinema` for demos?

This design prioritizes beauty and usability while maintaining the retro aesthetic. The responsive layout will adapt to terminal size, and the modal system keeps complex interactions clean.