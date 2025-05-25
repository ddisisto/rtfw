# NEXUS Documentation Restructure Proposal

## Current Problem
- Session management (Claude processes, JSONL files) mixed with context management (distill/restore)
- Overlapping content between agent_session_flow.md and session_management_protocol.md
- Unclear which doc is authoritative for what
- Risk of conflicting procedures

## Proposed New Structure

### 1. `nexus/sessions.md` (Technical Session Operations)
**Purpose**: Managing Claude processes and session files

**Contents**:
- Starting new Claude sessions in tmux windows
- Resuming existing sessions with `--resume <id>`
- Session identification via marker protocol
- JSONL file management and session_log.txt
- tmux window operations (create, send-keys, capture)
- When to restart vs resume a session
- NO mention of distillation or context restore

### 2. `nexus/lifecycle.md` (Agent Work States)
**Purpose**: How agents transition through work states

**Contents**:
- Four states: RESTORE → ACTIVE WORK → IDLE → (back to RESTORE when needed)
- Message routing and work assignment
- Tool approval handling (BELL flags)
- When to prompt for distillation (idle time)
- State monitoring and transitions
- NO session management details

### 3. `nexus/distill.md` (Context Management)
**Purpose**: Managing agent memory and context

**Contents**:
- Continuous distillation (during idle)
- Cyclical distillation (system-wide)
- Context thresholds (34% caution, 15% urgent)
- Pre-distill protocol
- /clear command execution
- Post-clear restore protocol
- Links to /protocols/distill.md and /protocols/restore.md

### 4. Keep `nexus/main_loop.md`
- Already focused on run.sh scan logic
- Clear purpose and scope
- Under revision anyway

## Benefits
1. **Clear separation of concerns**
   - sessions.md = Claude processes
   - lifecycle.md = Agent states
   - distill.md = Memory management

2. **No overlapping content**
   - Each doc owns its domain
   - Clear cross-references where needed

3. **Easier to maintain**
   - Changes to session management don't affect lifecycle
   - Distillation procedures isolated from technical operations

## Migration Plan
1. Create new files with clear content
2. Update context.md links
3. Remove old agent_session_flow.md and session_management_protocol.md
4. Verify no broken references