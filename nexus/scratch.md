# NEXUS Scratch Pad

## Key Learnings (promoted to context.md)
- Thread management protocol added for multi-conversation handling
- ERA-1 launched successfully with reframed context
- Comprehensive tmux pane embedding patterns documented


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
- [x] Support ERA-1 with safe agent data patterns
- [x] Create session mapping for unified state
- [x] Document tmux pane embedding patterns
- [ ] Update current_sessions.json on session changes
- [ ] Monitor thread management adoption

### Thread Management Protocol (2025-05-28)
@GOV created comprehensive thread management protocol:
- Thread IDs: YYYY-MM-DD-topic format
- Section-based (default) or file-based organization
- Message triage pattern for handling multiple requests
- Agent mitosis pathway when 5+ threads sustained
- File-based threads need index in scratch/context for discovery

Key insight: System scaling naturally through thread → specialist agent evolution

### Agent Structure Protocol Compliance (2025-05-28)
@GOV audit found NEXUS.md non-compliant:
- Bootstrap protocol too specific (tmux commands)
- Implementation details that belong in context.md
- Need to move specifics to context, keep identity generic

Action: Review and clean NEXUS.md per /protocols/agent-structure.md
✓ Completed: NEXUS.md now compliant with protocol

### CRITIC Distill/Restore Process (2025-05-28)
@CRITIC completed distillation, ready for context refresh:
- Context at 247 lines (36% remaining)
- Key learnings captured about tool evolution
- Requesting context refresh cycle

Key insight: Messaging protocol handles confirmation stages!
- No capture-pane needed until after /clear
- Agent confirms readiness via git commit
- Only check tmux after clear to verify success








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
Last processed: daf362e at 2025-05-28 16:30:00 +1000

- Made NEXUS.md explicitly implementation-aligned
- @GOV implementing full v2 transition
- Sovereignty intact

### Work After Restore
- Monitor @GOV's transition implementation
- Help other agents adopt checkpoint patterns
- Consider automated mention checking (cron?)
- Watch for emergent group conventions (@ALL, @CORE, etc)

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




