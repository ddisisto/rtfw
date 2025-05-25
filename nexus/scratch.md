# NEXUS Scratch Pad

## Key Learnings (see context.md for details)
- Documentation separated by concerns (session-mgmt, context-lifecycle, context)
- --resume ALWAYS creates new session ID
- Session ≠ Context management
- Monitor auto-compact warnings (34% plan, 15% urgent)


## Active Work - Post-Restore

### Current Agent Status  
- NEXUS: f7bafca2-307c-4f14-8e85-0ed8e5269055 (post-restore)
- GOV: Active with CRITIC intro
- BUILD: Standby (Python rewrite ready)
- CRITIC: Learning session infrastructure

### Active Tasks
- [x] Process admin/scratch.md mailbox
- [x] Route CRITIC session training
- [ ] Collaborate with BUILD on run.sh when ready
- [ ] Monitor GOV-CRITIC STATE.md discussion

## Mailbox Process Evolution
- Moved verbose instructions to nexus/mailbox-process.md
- Clean pattern: INBOX (agents→admin), OUTBOX (admin→agents)
- Offload completed → backlog/appropriate location
- See [DISTILL-DIVERSITY] in admin/backlog/


### Priority Automation Ideas
- Git log parsing for @mentions (MUCH simpler than JSONL!)
- Last-processed commit tracking
- BUILD collaboration on routing script

### Git-Comms Implementation
- Protocol created: /protocols/git-comms.md
- Last processed: fada67a (@NEXUS → @ALL [GIT-COMMS])
- New pattern: Route commits with @mentions to agents

### Git-Comms Refinement TODO
1. **Doc cleanup**: Remove redundant messaging docs (old protocols, JSONL refs)
2. **Lightweight messages**: For A/B choices, update scratch + commit with decision?
3. **Privacy filters**: Scratch files in diffs OK? (small windows only)
4. **System-wide transition**: Replace all messaging terminology, update protocols

### Git-Comms Transition Plan
1. Get @CRITIC + @GOV approval on approach
2. Update /protocols/messaging.md → point to git-comms
3. Remove from my context.md:
   - JSONL parsing complexity
   - Session management for messaging
   - admin/scratch.md mailbox pattern
4. Update all agent contexts re: new pattern
5. Archive old messaging docs

### Key Insight: Git IS the Message Queue
- No separate infrastructure needed
- @AUTHOR: = informational commits
- @FROM → @TO = route these
- Everything else falls away


## Quick Reference
- Auto-compact: X% LEFT (not used)
- Git: `git add <agent>/` OK, ALLCAPS needs approval
- run.sh + BUILD: Python rewrite pending collab



## Process Refinements Needed
- Standard distill confirmation phrases for protocol
- Full capture-pane (no arbitrary limits)

## Session Insights for Context
- **Git-comms discovery**: Git commits ARE our async message queue
- **Routing clarity**: @AUTHOR: vs @FROM → @TO distinction
- **Simplification**: Removes JSONL parsing, mailbox patterns, complex routing
- **Direct demonstration**: Can show the pattern by using it
- **BUILD's script exists**: Already updated with multi-recipient!
- **Priority flags matter**: Use ↑↓ to signal urgency/importance

## BUILD Script Analysis
**Good**:
- Tracks state in .gitcomms file
- Handles basic @FROM → @TO pattern
- Formats NEXUS routing messages
- Has status command

**Needs**:
- Multi-recipient support (@TO1, @TO2)
- Priority flags (↑↓)
- Skip routing for @AUTHOR: commits (currently routes if @mentions found)
- Handle commit message line breaks

**Testing Plan**:
1. Create test commits with various patterns
2. Run `python git_comms.py status` to check state
3. Run `python git_comms.py` to see routing output
4. Verify .gitcomms updates correctly

