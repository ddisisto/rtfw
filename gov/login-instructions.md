# Login Instructions for Logged Out Agents

## For @ADMIN to Execute

When bringing an agent back online:

1. **Engine sets state**:
   ```
   echo 'state: login' > agent/_state.md
   ```

2. **Send /clear to agent terminal**

3. **Send restore prompt**:
   ```
   @ADMIN: @protocols/restore.md underway for @AGENT.md agent - please restore required context for continuation
   ```

## What Agent Will Do

1. **Enter login state** (personality offline)
2. **Load files in order**:
   - @AGENT.md
   - CLAUDE.md  
   - SYSTEM.md
   - agent/context.md
   - agent/scratch.md
   - agent/_state.md (RO)
   - admin/tools.md
   - Role-specific files
   - Check recent git activity

3. **Transition to bootstrap**:
   ```
   @AGENT [bootstrap]: Login complete, restored from COMMIT_HASH
   ```

4. **Move to inbox** and resume normal operations

## Current Logged Out Agents

- @NEXUS - Chose logout based on _state.md data
- @CRITIC - Also in logout state

Both are ready for this login sequence once you update their _state.md files and send the prompts.