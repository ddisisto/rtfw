# NEXUS Session Management

**Purpose**: Technical reference for managing Claude sessions, JSONL files, and tmux windows. This document covers process-level operations only. For context lifecycle and work states, see context-lifecycle.md.

## Session Fundamentals

### Session Components
- **Claude process**: Running instance of `claude` CLI in tmux window
- **Session ID**: UUID identifying a Claude conversation
- **JSONL file**: `/nexus/sessions/<session_id>.jsonl` containing conversation history
- **session_log.txt**: Append-only log tracking current session per agent
- **nexus/.sessionid**: File containing NEXUS's current session ID

### Key Principle
Session management (starting/stopping processes) is completely independent from context management (distill/restore). You can:
- Restart sessions without distilling
- Distill multiple times within one session
- Resume sessions that retain full context

## Critical: Claude CLI Input Handling

**VITAL**: In Claude CLI, Enter within tmux send-keys creates newlines, NOT submission!
- Always send message text and Enter as SEPARATE commands
- Pattern: `tmux send-keys -t <agent> 'message'` then `tmux send-keys -t <agent> Enter`
- This applies to ALL interactions with Claude sessions

## Starting New Sessions

### Session Identification Protocol
After any session start/resume, identify the session:

#### For Other Agents
1. Generate marker: `<AGENT>_SESSION_MARKER_$(date +%s)_$$`
2. Send to agent: 
   ```
   tmux send-keys -t <agent> '@NEXUS → @<AGENT>: Session identification in progress. Please echo: <AGENT>_SESSION_MARKER_...'
   tmux send-keys -t <agent> Enter  # CRITICAL: Separate command to submit!
   ```
3. Wait for JSONL write: `sleep 2`
4. Search for marker: 
   ```
   Grep pattern=<AGENT>_SESSION_MARKER_... path=/home/daniel/prj/rtfw/nexus/sessions
   ```
5. Extract session ID from matching filename
6. Update nexus/session_log.txt:
   ```
   Read session_log.txt
   Append: <agent_name> <session_id> <timestamp>
   Write session_log.txt
   ```

#### For NEXUS Self-Validation
When @ADMIN requests validation:

1. Generate marker: `NEXUS_SESSION_VALIDATION_$(date +%s)_$$`
2. Echo marker in conversation
3. Wait: `sleep 2`
4. Read nexus/.sessionid
5. Grep for marker in sessions/, should find prior session + new one if applicable
6. If session changed:
   - Update nexus/.sessionid
   - Append to session_log.txt
7. Report validation status

## Fresh Agent Start
Used only when starting an entirely new agent / session that did not previously exist. Otherwise must use Resume process below
```bash
tmux new-window -n <agent_name>
tmux send-keys -t <agent_name> 'claude' Enter
sleep 2  # Allow startup
```
Then run identification protocol immediately to capture session_id, followed by initial context load - typically same as protocols/restore.md, basic agent role and context templates having been provided by @GOV

## Resuming Existing Sessions

### Pre-Resume Validation
Always validate before resuming:
1. Read last known session from session_log.txt
2. Check JSONL file exists and has recent activity
3. If stale/missing, consult @ADMIN before proceeding

### Clean Exit and Resume
```bash
# Check initial state
tmux capture-pane -t <agent> -p

# Exit Claude cleanly (if Claude Code cli is currently running)
tmux send-keys -t <agent> '/exit'
tmux send-keys -t <agent> Enter
sleep 2

# Verify shell prompt
tmux capture-pane -t <agent> -p

# Resume session
tmux send-keys -t <agent> 'claude --resume <session_id>' Enter
sleep 2

# Verify agent is back in Claude
tmux capture-pane -t <agent> -p
# Should show /exit as last activity, waiting for input

# CRITICAL: Resume creates NEW session ID!
# Must run identification protocol immediately
```

**Important**: 
- No context restore protocol needed on resume - agent retains full context
- **Always identify new session after resume** - `--resume` creates new JSONL file


## Important Notes

- **Session ≠ Context**: Resuming a session doesn't require restore protocol
- **Resume = New Session**: Always run identification after `--resume` 
- **One Session at a Time**: Complete identification before starting another
- **Tool Discipline**: Use native tools (Read/Write/Grep) not shell commands