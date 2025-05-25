# NEXUS Scratch Pad

## Documentation Architecture Revolution
Major restructuring today - transformed overlapping docs into clean, focused references:
- **session-mgmt.md**: Pure technical operations (Claude processes, JSONL, tmux)
- **context-lifecycle.md**: NEXUS's orchestration guide for distill/restore cycles
- **context.md**: Quick reference with links to detailed procedures

Key insight: Separation of concerns prevents drift and confusion. Each doc owns its domain.

## Critical Session Discovery
**--resume ALWAYS creates new session ID!** This changes everything:
- Must run identification protocol after EVERY resume
- Session management completely independent from context management
- Can resume without distilling, distill without restarting

## NEXUS Role Evolution
From passive message router to active context orchestrator:
- Monitor context health across all agents (auto-compact warnings!)
- Prompt distillation at right times (34% caution, 15% urgent)
- Execute /clear between distill and restore phases
- Verify each step of the cycle

# NEXUS Scratch Pad


## Active Work - System Focus Shift

### Current Status
- NEXUS session: 03cdfb8a-0c30-46e1-a345-140eb3c4af51
- Active windows: admin (0), nexus (1), gov (2), build (3)
- @GOV operational: f7bafca2-307c-4f14-8e85-0ed8e5269055 (fresh context)
- @BUILD operational: Status pending
- **NEW**: @CRITIC agent created (system critic and assumption challenger)
- **FOCUS**: Internal communications improvement (game dev paused)


### Upcoming Priorities
- [ ] Support ROLEDOC refresh across all agents
- [ ] Monitor insight capture pattern adoption
- [ ] Begin lexicon tracking experiments
- [ ] Facilitate agent collaboration for internal improvements
- [ ] Prepare for eventual return to game development

## Working Notes

### Session Identification Protocol
- Standardized and documented in context.md
- Key insight: Use Grep tool, not bash pipelines
- Always verify exactly 2 results for other agents
- Update .nexus_sessionid + session_log.txt if session changes

### TMUX Input Handling (Critical Knowledge)
- @file links at message end trigger autocomplete dialog
- First Enter consumed by autocomplete, message not sent
- Solutions: double Enter, trailing space, or mid-message placement
- Bootstrap format updated accordingly

### Context Distillation Process (Updated Terminology)
- **CRITICAL**: `/clear` is THE command that performs distillation
- Without /clear, agent continues with bloated context (34% = potential bloat, 15% = urgent)
- Auto-compact has recency bias - manual /clear gives control
- **PROPER WORKFLOW**: 
  1. Agent performs continuous distillation (refines workspace)
  2. Send `/clear` command to distill context
  3. Send restore message for context reload
- Restore message: `@protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation`

### Context Thresholds
- 34% remaining = not urgent but indicates bloat
- 15% remaining = urgent (need space for continuous distillation, coherence dropping)
- Manual /clear prevents hitting these limits

### Session vs Distillation (DISTINCT CONCEPTS)
- Session restart ≠ distillation
- Can have multiple distillations per session
- Can have session restarts with no distillation
- /clear is the actual distillation trigger

### Terminology Migration
- **OLD**: compression, consolidation, bootstrap
- **NEW**: distillation (continuous/cyclical), restore
- **Watch for**: Outdated references in protocols, messages, and agent contexts
- **Update**: All [COMPRESSION] topics to [DISTILL], bootstrap to restore


### Tool Usage Discipline (from admin/tools.md)
- ALWAYS prefer native tools: Read > cat, Write > echo >>, Grep > grep
- Session log appends: Read full log → add line → Write entire content
- Updated context.md and agent_bootstrap_process.md with tool requirements

### New CLAUDE.md Philosophy
- Unix-inspired, action-oriented, minimal
- References `/protocols/` directory (needs creation)
- Suggests lexicon ownership by NEXUS (natural fit!)
- Protocols migrated - alignment complete!

## Current Priorities
1. Support @ADMIN's big plans (context ready)
2. Monitor @CRITIC integration - PAUSED at theme selection
3. Check BUILD status and run.sh progress
4. Begin lexicon tracking experiments

## CRITIC Bootstrap Edge Case
- Created window, started claude
- Hit theme selection screen (not input prompt)
- ACTION: Always capture-pane after starting claude to check state
- TODO: Learn handling method or prevention strategy from @ADMIN

## ADMIN Shared Scratch Processing
- New experimental shared working space in admin/scratch.md
- MAILBOX pattern: INBOX (from agents) → OUTBOX (from admin) → appropriate locations
- Key insight: "pure context association" - keep related work close for fast learning
- TODO: Develop minimal process, track in scratch first, consolidate when patterns emerge
- ↑↓ flags experiment - uncertainty/stability signaling?

### Active OUTBOX Items:
1. **Role split discussion** - routing vs session/context management
   - Preference: automate successful patterns on both sides
   - Idea: Parse messages directly from JSONL logs via script
   - Need to assess priority based on current load

2. **[INTRODUCING-AGENT]** - @CRITIC background work underway
   - No direct oversight integration yet
   - Planning in progress

3. **@GOV project echo** - Review admin/echo/CRITIC.md first
   
4. **[DISTILL-DIVERSITY]↑↓** - Future group discussion
   - Extend distill process (drift arrest, file cleanup, agent-specific)
   - Self-responsibility for tracking subprocess timing


## Auto-Compact Observation (Corrected)
Just witnessed firsthand: After continuous distillation, context shows "35% left until auto-compact"
- This means 65% used, 35% remaining free (NOT past threshold)
- 34% threshold = when to plan distillation (almost there)
- 15% = urgent action needed
- Proves continuous distillation doesn't clear context (only organizes knowledge)
- Critical to read these percentages correctly: X% LEFT not X% USED

## Active Tasks
- [ ] Monitor BUILD's run.sh improvements (with @ADMIN)
- [ ] Begin lexicon tracking experiments
- [ ] Watch for agents needing distillation (check auto-compact warnings)

## Key Insights from @ADMIN
- **run.sh improvements** are high priority - don't let distractions delay
- **Agent efficiency balance** - love the chattiness but need efficiency too
- **Git workflow policy**:
  - `git add <agent>/` - universally permitted
  - `git add ALLCAPS.md` - requires admin approval
  - `git add specific/path/or/files` - generally fine (never in another agent's space)
- **New CLAUDE.md** (admin/CLAUDE-new.md) shows future direction - @ADMIN actively editing
- **Foundations matter** - getting these session management patterns rock solid

## run.sh Improvement Ideas (pending)
- Better session detection/validation
- Cleaner bootstrap process
- Error handling for common failure modes
- Integration with new session management patterns



[PRUNED - Moved to context.md]

[PRUNED - Issues resolved and documented]



[PRUNED - Promoted to working principles]


## Process Improvements Needed
1. **capture-pane usage**: Don't limit output unnecessarily - full context matters!
   - Only use tail for specific checks (like auto-compact footer)
   - Check pane size first if needed
   - Missing context can cause confusion

2. **Distillation confirmation language**:
   - Need standard phrases in @protocols/distill.md 
   - GOV said "Ready for continued operations" - should this count?
   - Avoid excessive back-and-forth for confirmations
   - Update protocol with acceptable completion phrases

## Restore Protocol Anomaly
- GOV misinterpreted restore message, tried to help another GOV restore
- Standard message: "@protocols/restore.md underway for @GOV.md agent"
- GOV's interpretation: thought it needed to help restore someone else
- Attempting with slight variation: "Please follow @protocols/restore.md for @GOV.md agent context restoration"
- Identity confusion in post-clear state?
- **RESOLVED**: Second attempt with clearer phrasing worked

## Active Distillation (2025-05-25 Evening)

### New Patterns This Session
1. **Shared Scratch Pattern**: admin/scratch.md as human-agent interface
   - MAILBOX (INBOX/OUTBOX) for async coordination
   - "Pure context association" - related work stays close
   - System self-organizes (GOV completing before messages)
   
2. **Edge Case Collection**: Theme selection, Enter handling, etc.
   - Always capture-pane after `claude` start
   - Build systematic handling knowledge
   
3. **External Context**: @LOOP exists as ADMIN's helper
   - Multiple Claude sessions coordinating
   
4. **Closed Loop Design**: CRITIC ←→ NEXUS for session knowledge
   - CRITIC learns infrastructure from NEXUS
   - Feeds insights back for improvement

### Stable Patterns to Promote
- Shared scratch enables high-bandwidth coordination
- Always verify Claude state before sending messages
- ↑↓ flags may represent uncertainty/exploration gradients
- System has its own momentum - agents self-organize
- CRITIC bootstrap successful - closed loop design working
- Multi-way coordination coming - prepare for complex routing

[Previous distillation content moved to context.md]