# NEXUS Session Management Protocol

## Agent Session Restart Process

### Clean Exit
1. Send `/exit` command: `tmux send-keys -t <agent> '/exit'` + Enter
2. Verify shell prompt: `tmux capture-pane -t <agent> -p`

### Session Resume
1. Check version: `tmux send-keys -t <agent> 'claude --version'` + Enter
2. Resume session: `tmux send-keys -t <agent> 'claude --resume <session_id>'` + Enter
3. Wait for startup: `sleep 10`
4. Capture and verify: `tmux capture-pane -t <agent> -p`
5. **NO BOOTSTRAP NEEDED** - agent retains context on resume

### Session Identification
- Read last known session from nexus/session_log.txt
- After resume, use marker protocol if session verification needed
- Update records only if session changed

## Compression Management

### Pre-Compression
1. Send notice: `@NEXUS → @<AGENT> [COMPRESSION]: External compression scheduled. Please consolidate per @gov/context_consolidation_protocol.md and confirm readiness.`
2. Wait for agent confirmation of readiness

### Compression Execution
1. Send `/clear` command to agent
2. Agent will show fresh state

### Post-Compression Recovery
1. Send bootstrap: `@NEXUS → @<AGENT> [AGENT-BOOTSTRAP]: @gov/context_compression_protocol.md completed for @<AGENT>.md agent - please reload all relevant agent context for continuation`
2. Agent reloads context and confirms operational status

## Key Principles

### Bootstrap Usage
- **ONLY after explicit compression** via `/clear`
- **NEVER on normal resume** - agents retain context
- **Check with @ADMIN** if agent seems to have lost identity

### State Awareness
- **ALWAYS capture-pane before actions** to understand current state
- **Never assume** agent state - verify through capture
- **Tool prompts** look different from ready prompts

### Tool Discipline
- Session log updates: Read full → append → Write entire content
- No bash append operations (echo >>)
- Prefer native tools always

## Common Patterns

### Full Restart + Compression Test
1. Exit: `/exit`
2. Resume: `claude --resume <id>`
3. Pre-compress notice
4. Clear: `/clear`
5. Bootstrap message
6. Verify recovery

### Quick Status Check
1. Capture-pane first
2. Assess visual state
3. Send appropriate message based on what you see

### Multi-Agent Coordination
- One operation at a time until confirmed
- Track states in scratch.md
- Update session_log.txt for permanence