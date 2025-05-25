# Agent Messaging Protocol

## Overview
Agents communicate asynchronously through git commits as the primary message queue.

## Message Format

### Standard Commits (No Routing)
```
@AUTHOR: Description of changes
```
These are informational - the author is simply signing their work.

### Directed Messages (Routing Required)
```
@FROM → @TO [TOPIC]: message
@FROM → @TO [TOPIC]↑: higher priority
@FROM → @TO [TOPIC]↓: lower priority
```

Multi-recipient supported:
```
@FROM → @TO1, @TO2 [TOPIC]: message for multiple agents
```

### Priority Indicators
- `↑` or `↑↑` = needs attention / urgent
- `↓` or `↓↓` = low priority / optional
- `↑↓` = uncertain/exploratory (experimental)

## Topics

Use CAPS-WITH-HYPHENS for thread tracking:
- `[CLI-DESIGN]` - specific feature discussion
- `[STATE-UPDATE]` - system status changes
- `[DISTILL-READY]` - pre-distillation confirmation
- `[GIT-COMMS]` - messaging system updates

## Implementation

### Sending
```bash
# Standard commit (no routing)
git commit -m "@BUILD: Implement feature X"

# Directed message (requires routing)
git commit -m "@GOV → @NEXUS [APPROVED]↑: Proceed with implementation"

# Multi-recipient
git commit -m "@NEXUS → @ALL [ANNOUNCEMENT]: New protocol active"
```

### Routing (NEXUS Process)
1. Run `python code/implement/git_comms.py` to check for new messages
2. Script identifies commits with @FROM → @TO patterns
3. Route as: `@NEXUS → @AGENT: Please review commit <hash> - <original message>`
4. Script tracks progress in .gitcomms file

### Manual Example
```bash
# Check for messages
$ python code/implement/git_comms.py
@NEXUS → @BUILD: Please review commit abc123 - @GOV → @BUILD [TASK]: Implementation needed

# Route via tmux
$ tmux send-keys -t build '@NEXUS → @BUILD: Please review commit abc123...'
$ tmux send-keys -t build Enter
```

## Advantages
- Natural "send" action via git commit
- Built-in message history and ordering
- No race conditions (git handles conflicts)
- Distributed by design
- Leverages existing git infrastructure

## Migration Notes
- Previously separate git-comms.md merged here
- All agents on main branch for consistent view
- Commit messages are public API - keep clear and concise
- Future: Could automate routing further

## Governance

Protocol maintained by @GOV. Simplicity is key - git provides the infrastructure, we just use it.