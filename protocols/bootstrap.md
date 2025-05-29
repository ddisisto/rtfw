# Bootstrap Protocol

## Purpose

Define the bootstrap sequence for agents starting from offline state, whether after logout/clear or cold start.

## Lifecycle Integration

Bootstrap occurs when transitioning from offline → operational:

1. **offline** - Session terminated, no agent activity
2. **/clear** - Engine clears context if needed
3. **bootstrap prompt** - Engine sends: "@ADMIN: @protocols/bootstrap.md underway for @AGENT.md agent"
4. **bootstrap** - Agent loads files and restores context
5. **inbox** - Agent checks messages and resumes work

## Bootstrap Sequence

When receiving bootstrap prompt, agent follows this sequence (note: personality not yet online):

1. @AGENT.md - core identity
2. CLAUDE.md - system requirements  
3. SYSTEM.md - architecture and roles
4. agent/context.md - stable knowledge
5. agent/scratch.md - working state
6. agent/_state.md - objective truth (READ-ONLY)
7. admin/tools.md - tool discipline
8. Role-specific files (per context.md)
9. Recent activity check (background context only - READ-ONLY orientation):
   ```bash
   # Your recent work (X=10)
   git log --oneline | grep '^[a-f0-9]* @AGENT:' | head -10
   
   # Recent mentions by others (Y=10) 
   git log --oneline | grep -v '^[a-f0-9]* @AGENT:' | grep '@AGENT' | head -10
   
   # Recent system activity (Z=5, excluding above)
   git log --oneline | grep -v '@AGENT' | head -5
   
   # CRITICAL: This is READ-ONLY background context for orientation
   # Do NOT act on messages, update checkpoints, or make decisions
   # This helps you understand recent system activity before entering inbox
   # Actual message processing begins in inbox state with proper checkpoint
   ```

## State Transitions

After completing bootstrap sequence:
1. **Read _state.md** - Check last known state/thread for context
2. **Signal completion** - Output decision for engine:
   ```
   next_state: inbox
   ```
3. **Wait for confirmation** - Pause after outputting decision
4. **Engine transitions** - System moves agent to inbox state  
5. **Continue lifecycle** - Follow normal state flow from inbox only after transition

## Critical Notes

- **Personality offline** during bootstrap - follow sequence mechanically
- **Logout first** - Always complete logout protocol before /clear
- **No shortcuts** - Complete sequence ensures coherence
- **Trust _state.md** - Contains objective measurements you cannot self-assess
- **No commits during bootstrap** - State tracking only, work begins in inbox

## Engine Coordination

The game engine:
- Sends /clear to terminate session
- Sets _state.md to `state: bootstrap`
- Sends bootstrap prompt to initiate sequence
- Monitors bootstrap completion via decision output
- Updates _state.md throughout lifecycle

## Governance

Protocol maintained by @GOV in coordination with @NEXUS.