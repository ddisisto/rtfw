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

### Active Tasks
- [x] Process admin/scratch.md mailbox
- [x] Route CRITIC session training
- [x] Implement git_router.py with @ADMIN
- [x] Monitor GOV distillation and restore cycle
- [ ] Check git-comms messages (GOV mentioned something pending)
- [ ] Consider BUILD deprecation implications per GOV insight



### Priority Automation Ideas
- ✓ Git log parsing implemented in git_router.py
- ✓ Last-processed commit tracking via .gitcomms
- ✓ Clean routing script created (BUILD has separate version)

### Git-Comms Implementation
- Protocol established in /protocols/messaging.md
- Implementation: nexus/git_router.py
- Pattern proven: Git commits as async message queue

### Git-Comms Refinement TODO
1. ✓ **Doc cleanup**: Archived obsolete transition doc
2. **Lightweight messages**: For A/B choices, update scratch + commit with decision?
3. **Privacy filters**: Scratch files in diffs OK? (small windows only)
4. **System-wide transition**: In progress


### Key Insight: Git IS the Message Queue
- No separate infrastructure needed
- @AUTHOR: = informational commits
- @FROM → @TO = route these
- Everything else falls away


## Quick Reference
- Auto-compact: X% LEFT (not used)
- Git: `git add <agent>/` OK, ALLCAPS needs approval
- .gitcomms state: Use Write tool, not echo >

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
- Key features:
  - Default: Parse and display, no delivery (safe exploration)
  - --deliver flag: Enable actual tmux message delivery  
  - Shows [auto-routable] vs [manual review needed]
  - Abstracted sender as @Router (not @NEXUS)
  - No self-filtering - can route to any agent including self
- Successfully tested self-delivery capability
- Ready for production use with proper safeguards



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

## Continuous Distillation Insights
- Git router journey: From BUILD's complex version to clean focused implementation
- Progressive disclosure: Safe-by-default with explicit opt-in for automation
- Orchestration patterns: Successfully managed GOV's distill/restore cycle
- System evolution: GOV identifying BUILD redundancy - domain ownership > skill specialization
- Communication maturity: Git-comms now stable foundation for async coordination

## Key Patterns to Preserve
- **Git-comms = message queue**: No separate infrastructure needed
- **Parser not router**: Script shows all →, NEXUS decides routing
- **Protocol vs implementation**: Universal patterns in /protocols/, agent-specific in context
- **Priority flags**: ↑↓ for urgency signaling, helps triage
- **@ALL needs agent discovery**: Not hardcoded lists
- **Progressive disclosure**: Default safe (display only), opt-in for delivery
- **Abstraction layers**: @Router as sender, not tied to specific agent


