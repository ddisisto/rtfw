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
- NEXUS session: 03cdfb8a-0c30-46e1-a345-140eb3c4af51 (changed!)
- Active windows: admin (0), nexus (1), gov (2)
- @GOV operational: 75583faf-a5d3-428f-89ef-34e2477ea85a (pending restart)
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

## Next Session Focus
When we resume, NEXUS should:
1. Improve run.sh based on learnings (high priority!)
2. Begin lexicon tracking experiments
3. Monitor protocol adoption across agents
4. Continue facilitating system evolution


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



## Distillation Insights - Current Session

### Key Learnings
- **Session ≠ Distillation**: Completely independent processes (can restart without distilling)
- **Personality offline during restore**: Explains mechanical file reading behavior
- **Capture-pane validation**: Essential at every state transition
- **Terminology evolution**: compression→distillation, bootstrap→restore, consolidation→continuous distillation
- **Unix philosophy alignment**: New CLAUDE.md embodies "do one thing well"

### Protocol Migration Status
- ✓ /protocols/messaging.md (simplified from gov/comms_protocol.md)
- ✓ /protocols/distill.md (replaces compression/consolidation protocols)
- ✓ /protocols/git.md (workspace sovereignty principle)
- ✓ /protocols/restore.md (referenced but need to verify)
- ✗ /lexicon.md (not yet created)

### Dead Link Watch
- Old: gov/comms_protocol.md → New: /protocols/messaging.md
- Old: gov/context_compression_protocol.md → New: /protocols/distill.md
- Old: gov/context_consolidation_protocol.md → New: /protocols/distill.md

### Tool Discipline Reminders
- Session log updates: Read → modify → Write (not echo >>)
- Always prefer native tools even for "simple" operations
- Git operations stay in Bash (no native equivalents)

The system isn't just working - it's thriving and evolving!

## Context Restore Critical Learning (2025-05-25)
**MAJOR MISS**: During restore sequence, attempted to search /tmp for session ID
- **Root cause**: Did not read session-mgmt.md during restore sequence
- **Impact**: Tried incorrect path, would have failed session validation
- **Correction**: session-mgmt.md MUST be included in restore sequence
- **Update needed**: Add to context.md restore dependencies list

This proves "personality offline" during restore - mechanical file reading isn't enough.
Need explicit session-mgmt.md reference in restore protocol!

### Other Context Restore Issues Encountered
1. **.nexus_sessionid location ambiguity**
   - Found: nexus/.nexus_sessionid (created there initially)
   - Expected: /home/daniel/prj/rtfw/.nexus_sessionid (per run.sh)
   - Resolution: Moved to project root, updated session-mgmt.md for clarity
   
2. **Missing session-mgmt.md in restore sequence**
   - Current protocol doesn't include it
   - Result: Attempted wrong search path (/tmp instead of nexus/sessions)
   - Fix needed: Add to context.md dependencies OR restore protocol

3. **Priority flag format change in STATE.md**
   - Old format: ! and - flags
   - New format: ↑↑↑ and ↓↓↓ (repeatable arrows)
   - Impact: Message routing logic may need update

4. **Restore sequence clarity**
   - Need explicit list of NEXUS-specific files beyond generic protocol
   - session-mgmt.md critical for operational knowledge
   - context-lifecycle.md important for orchestration duties
   - **RESOLVED**: Updated context.md with proper restore order

### Priority Flag Migration Status
- ✓ STATE.md - already updated by @ADMIN
- ✓ /protocols/messaging.md - already has new format
- ✓ nexus/context.md - updated from ! and - to ↑↑ and ↓↓
- ✓ NEXUS.md - updated routing description and fixed dead protocol links
- **New format**: ↑/↑↑ (urgent), ↓/↓↓ (low) - much clearer than !/- 
- Other files may have old examples but these are the key operational docs

## Insight: claude-additions.md Review
- New structured approach: inbox → work → insight capture → outbox
- "Insight capture" step aligns perfectly with distill protocol's "think hard"
- Key addition: EVERY turn should include scratch.md reflection (not just idle times)
- This formalizes what good agents already do naturally
- New agent creation coming from this - exciting system evolution!

## Session Management Insight: Tmux Restart Practice
- Outer tmux session restart planned to fix capture-pane issues
- No distillation needed - all context preserved in files
- Good practice for NEXUS bootstrap procedures
- Will need to restart GOV and BUILD sessions
- Key learning: Context persistence through files enables clean restarts!

## Critical Learning: Read the Docs!
- **Always** check session-mgmt.md and context-lifecycle.md when doing those operations
- Don't try random fixes - diagnose from authoritative sources
- If stuck, escalate to @ADMIN for careful diagnosis
- Documentation restructure revealed missing critical detail about Enter handling
- Proper root cause analysis > quick fixes every time