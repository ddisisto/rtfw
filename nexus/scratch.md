# NEXUS Scratch Pad

## Key Learnings (see context.md for details)
- Documentation separated by concerns (session-mgmt, context-lifecycle, context)
- --resume ALWAYS creates new session ID
- Session ≠ Context management
- Monitor auto-compact warnings (34% plan, 15% urgent)


## Active Work - Post-Restore

### Current Agent Status  
- NEXUS: f7bafca2-307c-4f14-8e85-0ed8e5269055 (operational)
- GOV: Leading BUILD deprecation process
- BUILD: Session terminated, window closed
- CRITIC: Session analysis ongoing

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


## Quick Reference
- Auto-compact: X% LEFT (not used)
- Git: `git add <agent>/` OK, ALLCAPS needs approval
- .gitcomms state: Use Write tool, not echo >
- Git router logs: nexus/routing.log, nexus/unroutable.log
- Admin messages: admin/inbox.txt

## Post-Restore TODOs
- Review BUILD's script updates (dynamic agent discovery)
- Consider script design before next iteration
- Monitor git-comms adoption across agents

## Git-Comms Clean Redesign (with @ADMIN)
- Archived nexus/git-comms-transition.md ✓
- Leave BUILD's code/implement/git_comms.py (inform them later if deprecated)
- Design goals:
  - Simple entry point for routing patterns
  - Single addressee direct delivery via tmux send-keys
  - Clean separation: parse commits → route decisions → delivery
  - Minimal state tracking (.gitcomms for last processed)
  - Future: Could evolve into daemon/hook/automation

## Git Router Implementation Complete
- Created nexus/git_router.py - clean, focused implementation
- V1 features:
  - Default: Parse and display, no delivery (safe exploration)
  - --deliver flag: Enable actual tmux message delivery  
  - Shows [auto-routable] vs [manual review needed]
  - Abstracted sender as @Router (not @NEXUS)
  - No self-filtering - can route to any agent including self
- V2 enhancements:
  - Window detection: Check tmux windows, mark unroutable if missing
  - Unroutable logging: nexus/unroutable.log with timestamps
  - Admin special handling: Routes to admin/inbox.txt
  - Routing log: nexus/routing.log for audit trail
  - Better atomicity via append operations
- Ready for cron automation



## Process Refinements Needed
- Standard distill confirmation phrases for protocol
- Full capture-pane (no arbitrary limits)

## Session Insights - Messaging Evolution
- Git-based async messaging proven effective
- Clean abstractions enable system flexibility
- Self-routing critical for true agent equality
- Tool design: Start minimal, add features carefully
- @ADMIN collaboration pattern: Design together, implement clean
- Interesting emergence: @LOOP pattern (self-referential systems?)

## Session Distillation - Messaging System Evolution

### Key Technical Accomplishments
- Git router v2 complete: Window detection, unroutable logging, admin inbox
- Progressive enhancement pattern: v1 simple → v2 production-ready
- Atomic operations via append - avoiding race conditions
- Ready for cron automation with full audit trail

### System Patterns Discovered
- Workspace sovereignty violations happen (GOV's accidental inclusion)
- Empty commits useful for protocol corrections + messaging
- Tool discipline reinforced: Write > echo for state files
- @ADMIN special routing needs (inbox.txt not tmux)

### Orchestration Maturity
- Successfully managed GOV's full distill/restore cycle
- Updated NEXUS.md to reflect evolved orchestrator role
- BUILD deprecation completed smoothly
- Git-based async coordination proven at scale

### Communication Evolution
- Self-routing critical for agent equality
- State updates only on delivery (not viewing)
- Unroutable messages tracked for later processing
- Complete visibility via timestamped logs

## Key Patterns to Preserve
- **Git-comms = message queue**: No separate infrastructure needed
- **Parser not router**: Script shows all →, NEXUS decides routing
- **Protocol vs implementation**: Universal patterns in /protocols/, agent-specific in context
- **Priority flags**: ↑↓ for urgency signaling, helps triage
- **@ALL needs agent discovery**: Not hardcoded lists
- **Progressive disclosure**: Default safe (display only), opt-in for delivery
- **Abstraction layers**: @Router as sender, not tied to specific agent


