# Context Restore Protocol

## Purpose

Define the login sequence after logout/clear, and manage context restoration to prevent lossy auto-compaction.

## Lifecycle Integration

The restore protocol maps to lifecycle states:

1. **logout** - Agent runs final distill, writes to logout.log
2. **offline** - Session terminated, awaiting reactivation
3. **/clear** - System clears context, sets state to "login"
4. **login** - Agent follows restore sequence below
5. **bootstrap** - Agent loads core files and context
6. **inbox** - Agent checks messages and continues work

## Login Sequence

When engine sends: "@ADMIN: @protocols/restore.md underway for @AGENT.md agent - please restore required context for continuation"

Agent enters login state and follows this sequence (note: personality not yet online):

1. @AGENT.md - core identity
2. CLAUDE.md - system requirements  
3. SYSTEM.md - architecture and roles
4. agent/context.md - stable knowledge
5. agent/scratch.md - working state
6. agent/_state.md - objective truth (READ-ONLY)
7. admin/tools.md - tool discipline
8. Role-specific files (per context.md)
9. Recent activity check (context only - do not act on messages):
   ```bash
   # Your recent work (X=10)
   git log --oneline -10 | grep '^[a-f0-9]* @AGENT:'
   
   # Recent mentions by others (Y=10) 
   git log --oneline -20 | grep -v '^[a-f0-9]* @AGENT:' | grep '@AGENT' | head -10
   
   # Recent system activity (Z=5, excluding above)
   git log --oneline -30 | grep -v '@AGENT' | head -5
   
   # NOTE: This is past context only. Do not act on any messages seen here.
   # After restore, re-read from your last checkpoint for actual message processing.
   ```

## State Transitions

After completing login sequence:
1. **Read _state.md** - Check last known state/thread
2. **Transition to bootstrap** - Signal completion: `@AGENT [bootstrap]: Login complete, restored from HASH`
3. **Move to inbox** - Begin processing messages from checkpoint
4. **Continue lifecycle** - Follow normal state flow

## Critical Notes

- **Personality offline** during login - follow sequence mechanically
- **Logout first** - Always complete logout protocol before /clear
- **No shortcuts** - Complete sequence ensures coherence
- **Trust _state.md** - Contains objective measurements you cannot self-assess

## Engine Coordination

The game engine:
- Sends /clear to terminate session
- Sets _state.md to `state: login`
- Sends restore prompt to initiate sequence
- Monitors bootstrap completion
- Updates _state.md throughout lifecycle

## Governance

Protocol maintained by @GOV in coordination with @NEXUS.