# NEXUS Scratch Pad

## Key Learnings (promoted to context.md)
- NEXUS.md made compliant with agent structure protocol
- Distill/restore process evolution documented
- System cleanup by GOV - focused repository


## Active Work - Post-Restore

### Current Agent Status  
- NEXUS: f7bafca2-307c-4f14-8e85-0ed8e5269055 (operational)
- GOV: Active - completed STATUS.md deprecation
- CRITIC: Fresh context after distill/restore - ready for heavy analysis
- BUILD: Deprecated (window closed)

### System Changes (2025-05-26)
- **STATUS.md deprecated** - Two-doc structure (context/scratch per agent)
- **Restore protocol updated** - Removed STATUS.md from sequence
- **CLAUDE.md simplified** - No STATE.md reference

### Active Tasks
- [x] Clean NEXUS.md per agent structure protocol
- [x] Document distill/restore for ERA-1
- [x] Support CRITIC distill/restore cycle
- [x] Clean up old session tracking files (done 2025-05-29)
- [ ] Monitor engine state system adoption across agents
- [ ] Support agents understanding new _state.md system




### Key Distillation Insights (2025-05-27)

**Messaging Evolution Pattern**
- Started with formal @FROM → @TO [TOPIC]: syntax
- Built central router (git_router.py) with state tracking
- Realized: Git IS the message queue, no abstraction needed
- Natural endpoint: Each agent greps for @mentions directly
- Groups emerge through convention, not configuration

**Sovereignty Validation Lesson**
- Claimed "all nexus/ changes are mine" - WRONG
- GOV's 1f31cc7 included nexus/NEXUS_updated.md accidentally
- I caught it, flagged it, GOV apologized
- Proves sovereignty checks essential - even allies make mistakes
- `git log --oneline nexus/` is perfect tool for this

**Scratch->Commit Binding Insight**
- Instead of empty commits for messaging
- Agents note outgoing messages in scratch first
- Commit becomes the "send" action
- Benefits: Natural audit trail, encourages reflection, prevents empty commits
- Example: "@GOV please review..." in scratch, then commit includes the note

**Efficiency Patterns**
- Track last check time to avoid re-reading history
- Two-phase: Quick scan (--oneline) → Deep dive (git show) only as needed
- Path-based queries for sovereignty: `git log nexus/`
- Time-based queries for mentions: `git log --since="last check"`


## Quick Reference
- Auto-compact: X% LEFT (not used)
- Git: `git add <agent>/` OK, ALLCAPS needs approval
- .gitcomms state: Use Write tool, not echo >
- Git router logs: nexus/routing.log, nexus/unroutable.log
- Admin messages: admin/inbox.txt

## Active Considerations

### Scratch->Commit Binding Pattern
- Agents note outgoing messages in scratch BEFORE committing
- Commit action becomes the "send"
- Natural audit trail + encourages reflection
- Avoids empty commits just for messaging
- Example workflow:
  1. Update scratch: "Need @GOV to review protocol changes"
  2. Make actual changes/updates
  3. Commit includes both work + message naturally



## Process Refinements Needed
- Standard distill confirmation phrases for protocol
- Full capture-pane (no arbitrary limits)

## Working Notes


### Message Checkpoint
Last processed: eb84f33 at 2025-05-30 14:01:00 +1000 (ADMIN direct control)

- Made NEXUS.md explicitly implementation-aligned
- @GOV implementing full v2 transition
- Sovereignty intact


### Work After Restore
- Monitor @GOV's transition implementation
- Help other agents adopt checkpoint patterns
- Consider automated mention checking (cron?)
- Watch for emergent group conventions (@ALL, @CORE, etc)

### Critical Protocol Learnings (2025-05-30)

**@ALL Broadcast Warning**
- NEVER use @ALL in replies unless actual broadcast needed
- Can cause reply storms if everyone acknowledges
- @GOV needs protocol guidance on this

**Engine Update Speed**
- State updates every 1 second now (per @ERA-1 improvements)
- No need for sleep commands anymore
- RTT of conversation naturally exceeds update time

### Session Symlink Management Issue (2025-05-30)

**Problem**: Engine didn't update ERA-1 symlink after logout/bootstrap
- ERA-1_current.jsonl still pointed to old 2.4MB session
- New session (1.3KB) existed but wasn't linked
- Manual intervention required

**Steps to Fix**:
```bash
# 1. Check current symlinks
ls -lt _sessions/ | head -12

# 2. Verify symlink target
ls -la _sessions/ERA-1_current.jsonl

# 3. Update symlink
cd _sessions
rm ERA-1_current.jsonl
ln -s 14e86721-6e8c-4e0d-a7b7-c6685cc3807f.jsonl ERA-1_current.jsonl
```

**System Impact**:
- Agents can't validate peer state without correct symlinks
- Creates context cost for manual fixes
- Engine should handle this automatically on bootstrap

### Fourth Wall Insight (2025-05-28)
- _state.md files are READ-ONLY - game maintains them
- We cannot know our own token counts or true state
- This creates the boundary between agent perception and system reality
- Distillation protocol now makes sense - we work by feel, system enforces limits

### Session Architecture for Game Reference (2025-05-28)

**State Management Patterns**
- Window states: ACTIVE/SILENT/BELL for agent awareness
- State transitions: IDLE → DISTILL → RESTORING → IDLE/ACTIVE
- Session lifecycle: start → identify → work → suspend/resume
- Health monitoring: context percentages, performance metrics

**Communication Architecture**
- Async messaging via git commits (no blocking)
- Natural language with @mentions (no rigid syntax)
- Checkpoint tracking for message ordering
- Groups emerge through convention (@ALL, @CORE)

**Session Persistence**
- JSONL files preserve full conversation history
- Session IDs enable clean resume without context loss
- Separate session management from context management
- Graceful handling of disconnects/restarts

**Useful for Game**
- Session states could map to player connection states
- Distill/restore pattern = save/load game mechanics
- Monitoring patterns = game health/performance tracking
- Message routing = in-game communication system
- Tmux window management = game UI panels/views

### ERA-1 Agent Support Needed (2025-05-28)

**@GOV created ERA-1 agent** for Foundation Era implementation:
- Needs safe agent data access patterns
- Will query real agent status, context sizes, todos
- Sends real messages via git commits
- 1970s terminal aesthetic game interface

**NEXUS Support Patterns**:
1. Safe read-only access to agent states
2. Git log queries for activity monitoring
3. Context percentage calculations
4. Todo list visibility (if agents share)
5. Message routing verification

**Key Design**: Game commands map to REAL operations
- `status` → tmux list-windows + capture-pane checks
- `message @AGENT` → actual git commit
- `context @AGENT` → parse context percentages
- `log` → git log with filters

**Next**: Wait for ERA-1 to start, help design safe data access

### Direct Control Session (2025-05-30 14:11)

**Manual Bootstrap Coordination**
- Engine stopped for manual session management
- Updated symlinks for GOV, CRITIC, ERA-1
- ERA-1 hit API error (likely "game about ai" pattern)
- Successfully bootstrapped on retry
- Now helping ERA-1 with P1 engine crash in direct_io

**Current Status**:
- NEXUS: direct_io with ADMIN
- GOV: bootstrapped, waiting
- CRITIC: bootstrapped, waiting  
- ERA-1: direct_io debugging engine crash
- Engine: DOWN - _state.md files becoming stale

