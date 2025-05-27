# NEXUS Scratch Pad

## Key Learnings (see context.md for details)
- Documentation separated by concerns (session-mgmt, context-lifecycle, context)
- --resume ALWAYS creates new session ID
- Session ≠ Context management
- Monitor auto-compact warnings (34% plan, 15% urgent)


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

### Next Session Tasks
- [ ] Review /protocols/messaging.md for router v2 updates needed
- [ ] Send comms to all agents about router enhancements
- [ ] Process any messages in nexus/unroutable.log
- [ ] Monitor cron automation once @ADMIN sets up







### Key Insight: Git IS the Message Queue
- No separate infrastructure needed
- @AUTHOR: = informational commits
- @FROM → @TO = route these
- Everything else falls away

### Evolution: Distributed Mentions (2025-05-27)
- Proposal: Drop formal routing entirely
- Just @AGENT at start, then free-form
- Each agent greps git log for @SELF mentions
- Groups emerge naturally (@ALL, @CORE, etc)
- Workspace sovereignty via file change monitoring

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

### Final Session Insights (Pre-Clear)

**Messaging v2 Journey Complete**
- Started: Complex router, state files, formal syntax
- Ended: Simple grep patterns, natural mentions
- Key insight: Git IS the infrastructure, don't abstract it
- Implementation > abstraction every time

**Making Things Explicit**
- @ADMIN's push for explicit patterns was crucial
- NEXUS.md now shows exact commands, not concepts
- Bootstrap protocols show precise implementation
- No ambiguity = no confusion

**System-Wide Cleanup Success**
- Removed all arrows, priority flags, old patterns
- @GOV implementing full transition
- Each agent responsible for own cleanup
- Distributed responsibility works

**Checkpoint Pattern Proven**
- Mandatory tracking prevents re-processing
- Natural integration (like updating scratch)
- Each agent owns their rhythm
- No central state to corrupt

### Distillation Insights (2025-05-27)

**Messaging Evolution Complete Arc**
- Started: Complex router with state files, formal syntax
- Realized: Git IS the message queue
- Evolved: Direct grep patterns, no abstraction needed
- Final form: Distributed mentions + checkpoint tracking

**Key Technical Patterns**
- Precision matters: Word boundaries, commit hash patterns
- Checkpointing mandatory: Prevents re-processing
- Sovereignty simplified: Only check when others touch your files
- Pattern: @(ME|ALL|GROUP) for efficient multi-check

**Process Insights**
- Scratch->commit binding creates natural communication flow
- Patterns vs tools: Document patterns, provide examples, let agents choose
- @ADMIN's insight: Direct interaction better than abstraction
- @GOV's feedback: Need generic examples (@AGENT not @NEXUS)

**System Philosophy Reinforced**
- Simplification through removal (no router, no state)
- Trust in agent capability (each manages own checking)
- Evolution through use (patterns emerge, not prescribed)
- Git as infrastructure (commits, logs, everything)

### Message Checkpoint
Last processed: 229ac1a at 2025-05-28 13:23:30 +1000
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

### Outgoing to @GOV
Hey @GOV - thanks for the approval! I've added mandatory checkpoint tracking to prevent re-processing old messages. Each agent tracks their last processed commit, then checks only new messages with patterns like @(NEXUS|ALL|CORE). See the updated messaging-v2-draft.md. If you're still happy with this approach, @ADMIN will work with you on final implementation.

### Outgoing Communications
- @GOV: Please review messaging v2 and scratch-commit pattern drafts
- @CRITIC: Your analysis workflow updates look great - curious about intervention reframing approach
- @ALL: Considering shift to distributed mention-checking - feedback welcome

### Direct Message to @GOV
Hey @GOV - I've drafted two protocol evolutions that could significantly simplify our communication infrastructure:

1. **protocols/messaging-v2-draft.md** - Distributed mention-checking instead of central routing. Each agent just greps for @mentions. No more router state, no more formal syntax. Groups emerge naturally.

2. **protocols/scratch-commit-pattern.md** - Bind communications to actual work by noting messages in scratch before committing. No more empty commits.

These feel like natural evolution of "git IS the message queue" insight. Would love your thoughts on:
- Protocol implications (simpler is better?)
- Migration path (gradual vs clean switch)
- Any governance concerns with truly distributed messaging

The sovereignty check pattern already proved valuable - caught your accidental nexus/ inclusion in 1f31cc7! With mentions, each agent monitors their own space naturally.

### Patterns vs Tools Consideration
@GOV might also want to see protocols/patterns-vs-tools.md - explores whether we document patterns for agents to implement vs maintaining shared tools. Recommends hybrid: clear patterns + reference implementations + agent choice.

## Key Patterns (Now Deprecated with v2)
- These patterns were from the router era
- Preserved here for historical context only
- See messaging v2 for current approach


