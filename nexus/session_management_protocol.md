# NEXUS Session Management Protocol

## Overview

This protocol defines TWO DISTINCT processes:
1. **Session Management** - Starting, stopping, and resuming agent Claude sessions
2. **Compression Management** - Clearing and recovering agent context within a session

These are INDEPENDENT - you can restart sessions without compression, and compress multiple times within a single session.

## Session Management

### Pre-Restart Validation
1. **Validate session ID** before any restart attempt:
   - Read nexus/session_log.txt for agent's last known session
   - List session files: `ls -la nexus/sessions/*.jsonl`
   - Verify session file exists and has recent activity
   - If session seems stale/missing, consult @ADMIN before proceeding

### Clean Exit
1. Send `/exit` command: `tmux send-keys -t <agent> '/exit'` + Enter
2. Verify shell prompt: `tmux capture-pane -t <agent> -p`

### Session Resume
1. Check version: `tmux send-keys -t <agent> 'claude --version' Enter` (single command works at bash)
2. Resume session: `tmux send-keys -t <agent> 'claude --resume <session_id>' Enter` (single command works at bash)
3. Wait for startup: `sleep 10`
4. Capture and verify: `tmux capture-pane -t <agent> -p`
5. **NO BOOTSTRAP NEEDED** - agent retains context on resume

### Session Identification
- Read last known session from nexus/session_log.txt
- After resume, use marker protocol if session verification needed
- Update records only if session changed

## Compression Management (SEPARATE from Session Management)

### When to Compress
- Context shows 34% remaining = potential bloat, consider compression
- Context shows 15% remaining = urgent, compress soon
- Agent requests compression after consolidation
- @ADMIN directs compression for system maintenance

### Pre-Compression
1. Send notice: `@NEXUS → @<AGENT> [COMPRESSION]: External compression scheduled. Please consolidate per @gov/context_consolidation_protocol.md and confirm readiness.`
2. Wait for agent confirmation (should have already saved important state)

### Compression Execution
1. Send `/clear` command: `tmux send-keys -t <agent> '/clear'` + Enter
2. **CRITICAL**: This instantly resets context to baseline
3. Validate with capture-pane - should show clean prompt, no context %

### Post-Compression Recovery  
1. Send bootstrap: `@NEXUS → @<AGENT> [AGENT-BOOTSTRAP]: @gov/context_compression_protocol.md completed for @<AGENT>.md agent - please reload all relevant agent context for continuation`
2. Agent automatically:
   - Reads compression protocol
   - Loads identity and system files
   - Reads own context.md and scratch.md
   - Confirms operational status

### Important Notes
- `/clear` forgets all unpersisted context (useful for A/B testing)
- Always capture-pane to validate state transitions
- Bootstrap message should have @file link mid-message (not at end)

## Key Principles

### Send-Keys Consistency
- **ALWAYS use separate Enter** for Claude input (even though inline works at bash)
- Keeps process consistent across all contexts
- Avoids confusion between bash vs Claude input handling

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

### Session Restart (NO compression)
1. Exit: `/exit` to shell
2. Check version: `claude --version`
3. Resume: `claude --resume <session_id>`
4. Wait 10 seconds for startup
5. Optional: Run session ID protocol if verification needed
6. Continue work - NO bootstrap needed

### Compression Within Active Session
1. Pre-compress notice to agent
2. Agent confirms readiness
3. Clear: `/clear`
4. Validate clean state with capture-pane
5. Bootstrap message for recovery
6. Agent confirms operational

### Full Restart + Compression (our test case)
1. Exit: `/exit`
2. Resume: `claude --resume <id>`  
3. Identify new session if needed
4. Then follow compression pattern above

### Quick Status Check
1. Capture-pane first (ALWAYS)
2. Assess visual state
3. Send appropriate message based on what you see

### Multi-Agent Coordination
- One operation at a time until confirmed
- Track states in scratch.md
- Update session_log.txt for new sessions only