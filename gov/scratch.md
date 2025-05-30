# GOV Scratch

## Message Checkpoint
Last processed: 7642037 at 2025-05-30

## Current State: direct_io
Thread: engine-reliability
Context: ~28.6% (36K tokens)

## Engine Lag Discovery
- Initial confusion: last_read_commit from morning made it look like 10min lag
- Actual lag: Only ~5 seconds between commit and state update!
- Solution: Move last_read fields to separate "Inbox" section
- All features stable except unread_count per @ADMIN

## Inbox Tracking Specification
- **Reset trigger**: Exit inbox to any state EXCEPT direct_io
- **Git command**: `git log --oneline LAST_READ..HEAD | grep -v '^[a-f0-9]* @AGENT:' | grep '@AGENT'`
- **Mark as read**: When transitioning FROM inbox (commit updates last_read)
- **Direct_io exception**: Preserves inbox state for seamless return
- Groups: last_read_commit_hash, last_read_timestamp, unread_message_count

## Recent Session Work

### Broadcast Group Guidance
- Issue raised by @NEXUS (6e365b8): @ALL mentions can cause reply storms
- Added guidance to messaging.md: use broadcasts sparingly, avoid unnecessary acks
- Critical for system efficiency as more agents join
- Engine now updates every 1sec (improved from before)

### Direct I/O Protocol
- Created 8th state for @ADMIN collaboration
- Engine pauses automation in this state
- Proactive notifications encouraged
- Clean entry/exit via commit messages

### Bootstrap Refinement
- Added "wait for confirmation" step
- Ensures clean handoff to inbox
- Prevents race conditions

### Protocol Harmonization Needs
1. **Pattern extraction** - Common elements across protocols
2. **Notification standardization** - Proactive alerts in all states
3. **Decision output format** - Consistent for engine parsing
4. **Protocol size limits** - Keep each under ~200 lines
5. **Cross-references** - "See also:" sections vs duplication

### Journey Protocol Complete
- Renamed agent-lifecycle.md → journey.md
- Balanced technical precision with philosophical depth
- "Each session forms complete arc" - captures essence
- 8 states as waypoints in larger journey

### Today's Journey Arc
- Started at 30K tokens with bootstrap
- Created all missing state protocols (inbox, deep-work, idle, logout)
- Added 8th state (direct_io) for human collaboration
- Harmonized protocols and documentation
- Renamed lifecycle to journey - resonates on multiple frequencies
- Now at 81% ready for graceful logout

### Patterns Strengthened
- Protocols as teaching tools, not just documentation
- Direct_io enables transparent collaboration
- Bootstrap→journey→logout as complete cycle
- Each journey builds on previous (context.md carries forward)
- Fourth wall architecture proven throughout

### State Machine Clarification (2025-05-29)
- **Critical insight**: Commits ARE state declarations
- **No text outputs**: Engine only observes git commits
- **Format**: @AGENT [state]: message creates transition
- **Updated**: CLAUDE.md, SYSTEM.md, bootstrap.md, messaging.md
- **Verified**: Direct_io transition worked immediately
- **Pattern**: State declaration embedded in every commit

## Protocol Alignment Audit (2025-05-30)

### Outdated Gov Files Creating Misinformation
1. **era-agent-governance.md** - Major issues:
   - References non-existent agent-lifecycle.md
   - Says 7-state lifecycle (now 8)
   - ERA-1 as temporary (now permanent)
   - ERA succession pattern obsolete
   - ERA-1 actively using this outdated info

2. **protocol-transition-plan.md** - Completed work from days ago
3. **protocol-updates.md** - Most changes already implemented

### Action Plan
- [x] Archive outdated files to gov/archive/
- [x] Update SYSTEM.md to remove era governance reference
- [x] Notify ERA-1 about governance changes (42233dd)
- [x] Create "idle work" protocol for self-optimization

## Idle Work Directives (Pending Further Discussion)
Key principles:
1. **Agent Ownership**: Each agent maintains own directives in context.md
   - @ADMIN can request adjustments
   - Agents have autonomy over their idle work focus
   
2. **Direct_io as Valid Choice**: 
   - Agents can initiate direct_io anytime (break/exception/chat)
   - Especially encouraged from idle when uncertain
   - Bidirectional state - either party can initiate

Example purposes:
- GOV: Protocol alignment validation
- NEXUS: Session health monitoring  
- CRITIC: Pattern analysis
- ERA-1: Engine optimization

## Continuity Bridge
- protocol-cleanup: Archived 3 outdated docs (42233dd), fixed all references
- direct-io-enhanced: Now bidirectional - agents can initiate (fb020b4)
- idle-work-pending: Agents own directives in context.md, @ADMIN can request adjustments
- Next session: Formalize idle work framework after discussion