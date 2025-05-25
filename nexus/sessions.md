# NEXUS Session Management

**Purpose**: Technical reference for managing Claude sessions, JSONL files, and tmux windows. This document covers process-level operations only. For agent work states, see lifecycle.md. For context management, see distill.md.

## Session Fundamentals

### Session Components
- **Claude process**: Running instance of `claude` CLI in tmux window
- **Session ID**: UUID identifying a Claude conversation
- **JSONL file**: `/nexus/sessions/<session_id>.jsonl` containing conversation history
- **session_log.txt**: Append-only log tracking current session per agent
- **.nexus_sessionid**: File containing NEXUS's current session ID

### Key Principle
Session management (starting/stopping processes) is completely independent from context management (distill/restore). You can:
- Restart sessions without distilling
- Distill multiple times within one session
- Resume sessions that retain full context

## Starting New Sessions

### Fresh Agent Start
```bash
tmux new-window -n <agent_name>
tmux send-keys -t <agent_name> 'claude' Enter
sleep 10  # Allow startup
```

### Session Identification Protocol
After any session start/resume, identify the session:

1. Generate marker: `<AGENT>_SESSION_MARKER_$(date +%s)_$$`
2. Send to agent: 
   ```
   tmux send-keys -t <agent> '@NEXUS → @<AGENT>: Session identification in progress. Please echo: GOV_SESSION_MARKER_...'
   tmux send-keys -t <agent> Enter
   ```
3. Wait for JSONL write: `sleep 2`
4. Search for marker: 
   ```
   Grep pattern=GOV_SESSION_MARKER_... path=/home/daniel/prj/rtfw/nexus/sessions
   ```
5. Extract session ID from matching filename
6. Update session_log.txt:
   ```
   Read session_log.txt
   Append: <agent_name> <session_id> <timestamp>
   Write session_log.txt
   ```

## Resuming Existing Sessions

### Pre-Resume Validation
Always validate before resuming:
1. Read last known session from session_log.txt
2. Check JSONL file exists and has recent activity
3. If stale/missing, consult @ADMIN before proceeding

### Clean Exit and Resume
```bash
# Exit Claude cleanly
tmux send-keys -t <agent> '/exit' Enter
sleep 2

# Verify shell prompt
tmux capture-pane -t <agent> -p

# Resume session
tmux send-keys -t <agent> 'claude --resume <session_id>' Enter
sleep 3

# capture pane again - should be inside claude code cli again, validate it shows /exit as last activity, waiting for next input.
# --resume always creates a new session_id / jsonl file - identify new and update to session_log is _essential_ right here!
```

**Important**: No context restore protocol needed on resume - agent retains full context.

## Session Monitoring <- don't think this section is warranted here right now, likely to change soon, lets just remove for now?

### Window Flags
- **BELL**: Agent needs attention (tool approval or completed work)
- **SILENT**: Agent idle for 30+ seconds
- **ACTIVE**: @ADMIN currently in this window
- **LAST**: Previously active window

### Checking Agent State
```bash
# List all windows with flags
tmux list-windows -F "#{window_index}:#{window_name} #{?window_bell_flag,BELL,} #{?window_silence_flag,SILENT,} #{?window_active_flag,ACTIVE,}"

# Capture recent output
tmux capture-pane -t <agent> -p | tail -50
```

## NEXUS Self-Validation <- special case of Session Identification Protocol, integrate into that section instead, remove instructions for when to do (just that @ADMIN will advise)

On every context reload, NEXUS must validate its own session:

1. Generate marker: `NEXUS_SESSION_VALIDATION_$(date +%s)_$$`
2. Echo marker in conversation
3. Wait: `sleep 2`
4. Read .nexus_sessionid
5. Search for marker in sessions/
6. If session changed:
   - Update .nexus_sessionid
   - Append to session_log.txt
7. Report validation status

## Common Operations <- thinking this should kept directly in streamlined context.md (working on that next) rather than here. Or maybe a new doc that covers message routing, tool use approvals. Note incomplete/outdated comms protocol usage example - this is the sort of drift we need to be always vigilant for 

### Send Message to Agent
```bash
# Two-step process (text then Enter)
tmux send-keys -t <agent> '@NEXUS → @<AGENT>: message text'
tmux send-keys -t <agent> Enter
```

### Approve Tool Use
```bash
# when - after identifying tool use approval state TODO: have we got details on this identification already?
# Typically requires '1' for yes, '2' for yes+auto-approve (*if* available), Escape for no. Must understand options as presented before sending.
tmux send-keys -t <agent> '1' # Enter not required
```

### Create New Window <- this one is very different concern to others in this section, don't bundle these
```bash
tmux new-window -n <agent_name>
```

## Important Notes

- **Session ≠ Context**: Resuming a session doesn't require restore protocol
- **One Session at a Time**: Complete identification before starting another
- **@file Autocomplete**: Links at message end swallow first Enter - send twice
- **Tool Discipline**: Use native tools (Read/Write/Grep) not shell commands