# ERA-1 Foundation Terminal

An early 1980s-style system monitoring terminal that provides real control over the rtfw multi-agent system.

## Features

- **Real Integration**: Every command performs actual operations
- **Live Monitoring**: Auto-refresh shows real-time agent activity  
- **Authentic Aesthetic**: Green phosphor terminal with early 1980s styling
- **Zero Dependencies**: Uses only Python stdlib (blessed optional for future enhancement)

## Usage

### Interactive Mode (default)
```bash
./cli.py
```

Commands:
- `STATUS [agent]` - Show agent status (all or specific)
- `MESSAGE agent "content"` - Send git commit message
- `LOG [count]` - Show recent system activity
- `MONITOR` - Toggle real-time auto-refresh
- `HELP` - Show available commands
- `EXIT/QUIT` - Exit the terminal

### One-Shot Mode
```bash
# Quick status check
./cli.py status
./cli.py status GOV

# Send a message
./cli.py message GOV "System check please"

# View logs with filters
./cli.py log --count 50
./cli.py log --from ADMIN
./cli.py log --mentions ERA-1
```

## Real-Time Monitoring

In interactive mode, type `MONITOR` to enable auto-refresh:
- Updates every 3 seconds
- Shows tmux window activity states
- Tracks context.md growth
- Displays recent git commits
- Indicates active agents (activity in last 30 seconds)

## Architecture

- `interfaces.py` - Core contracts for all components
- `agents.py` - Safe read-only agent monitoring
- `messaging.py` - Git commit messaging
- `display.py` - Terminal UI with ANSI codes
- `commands.py` - Command parsing and handlers
- `cli.py` - Main game loop with CLI support

## Agent Status Indicators

- **ACTIVE** - Currently selected window (*) or recent activity
- **SILENT** - Window exists but marked silent (-)
- **IDLE** - Window exists, no recent activity
- **OFFLINE** - No tmux window found

## Future Enhancements

- [ ] CONTEXT command for detailed context.md analysis
- [ ] VIEW command with tmux pane embedding
- [ ] Blessed library for enhanced TUI
- [ ] More retro touches (ASCII art, system beeps, etc)
- [ ] Session history graphs