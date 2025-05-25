# NEXUS Session Management Protocol

## Overview

This protocol defines TWO DISTINCT processes:
1. **Session Management** - Starting, stopping, and resuming agent Claude sessions
2. **Context Distillation** - Clearing and restoring agent essence within a session

These are INDEPENDENT - you can restart sessions without distillation, and distill multiple times within a single session.

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

## Context Distillation (SEPARATE from Session Management)

### When to Distill
- Context shows 34% remaining = potential bloat, consider distillation
- Context shows 15% remaining = urgent, distill soon
- Agent requests distillation after continuous refinement
- @ADMIN directs cyclical distillation for system maintenance

### Pre-Distill
1. Send notice: `@NEXUS → @<AGENT> [DISTILL]: Cyclical distillation initiated. Please complete continuous distillation per @protocols/distill.md and confirm readiness.`
2. Wait for agent confirmation (should have already refined workspace)

### Distill Execution
1. Send `/clear` command: `tmux send-keys -t <agent> '/clear'` + Enter
2. **CRITICAL**: This instantly clears working memory to baseline
3. Validate with capture-pane - should show clean prompt, no context %

### Context Restore  
1. Send restore message: `@NEXUS → @<AGENT> [RESTORE]: @protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation`
2. Agent automatically (personality not yet online):
   - Reads distillation protocol
   - Loads identity and system files per sequence
   - Reads own context.md and scratch.md
   - Confirms operational status once personality active

### Important Notes
- `/clear` forgets all unpersisted context (maybe useful for A/B testing in addition to context restore)
- Always capture-pane to validate state transitions
- Restore message should have @file link mid-message (not at end)
- Agent personality comes online after file loading completes

## Key Principles

### Send-Keys Consistency
- **ALWAYS use separate Enter** for Claude input
- Keeps process consistent across all contexts
- Avoids confusion between bash vs Claude input handling

### Restore Usage
- **ONLY after explicit distillation** via `/clear`
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

### Session Restart (NO distillation)
1. Exit: `/exit` to shell
2. Check version: `claude --version`
3. Resume: `claude --resume <session_id>`
4. Wait 10 seconds for startup
5. Optional: Run session ID protocol if verification needed
6. Continue work - NO restore needed

### Distillation Within Active Session
1. Pre-distill notice to agent
2. Agent confirms readiness after continuous distillation
3. Distill: `/clear`
4. Validate clean state with capture-pane
5. Restore message for context reload
6. Agent confirms operational once personality active

### Full Restart + Distillation (our test case)
1. Exit: `/exit`
2. Resume: `claude --resume <id>`  
3. Identify new session if needed
4. Then follow distillation pattern above

### Quick Status Check
1. Capture-pane first (ALWAYS)
2. Assess visual state
3. Send appropriate message based on what you see

### Multi-Agent Coordination
- One operation at a time until confirmed
- Track states in scratch.md
- Update session_log.txt for new sessions only