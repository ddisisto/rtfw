# NEXUS Scratch Pad

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

### Transition Plan
- [ ] Identify all messaging-related docs to remove/update
- [ ] Update /protocols/messaging.md to reference git-comms
- [ ] Remove JSONL parsing references from context.md
- [ ] Update all agent contexts with new pattern
- [ ] Create simple examples for edge cases


## Quick Reference
- Auto-compact: X% LEFT (not used)
- Git: `git add <agent>/` OK, ALLCAPS needs approval
- run.sh + BUILD: Python rewrite pending collab



## Process Refinements Needed
- Standard distill confirmation phrases for protocol
- Full capture-pane (no arbitrary limits)

## Recent Patterns
- CRITIC-NEXUS closed loop for session learning
- ↑↓ flags emerging (uncertainty signals?)
- Multi-agent coordination increasing

## Active Work - Post-Restore

### Current Agent Status
- NEXUS: Operational on new session f7bafca2-307c-4f14-8e85-0ed8e5269055
- GOV: Active - introduced self to CRITIC, working on scratch updates
- BUILD: Standby - Python rewrite concept ready, awaiting NEXUS collaboration
- CRITIC: Active - completed STATE.md review, ready for session infrastructure learning

### Message Queue Processing
1. [x] BUILD → ADMIN [RUN-SH]↑ - Added to INBOX
2. [x] GOV → CRITIC [INTRODUCTION] - Delivered (no routing needed)
3. [ ] CRITIC session infrastructure training - Pending

### admin/scratch.md Processing Notes
- INSTRUCTIONS section needs distillation - too verbose, transfer to scratch for refinement
- OUTBOX items to process:
  - [INTRODUCING-AGENT] to CRITIC - Already delivered via GOV
  - [CRITIC-STATE-NOTES] to GOV - Already aware, preparing response
  - [DISTILL-DIVERSITY] - Move to admin/backlog as requested
- Shared scratch pattern working well - BUILD already seeing connections