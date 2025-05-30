# Context Compression Knowledge - @NEXUS

## What Context Compression Is

Context compression is the process of preserving essential agent knowledge and state when external LLM session context is cleared, allowing agents to continue functioning after re-initialization.

## Types of Context Loss

1. **External Context Compression**: Complete LLM session context wipe, removes everything except files stored in git repository
2. **Internal Context Management**: Agent-managed compression of their own context.md/scratch.md files when size thresholds exceeded

2025-05-30 admin note: #2 now called distill **IMPORTANT** actually causes context growth also, counterintuitvely. all past context and scratch remains within a single journey, is effectively only appended, corrected or reinforced. idea is that **after** logout, context will be smaller, if distillation works well.

## Pre-Compression Preparation Protocol

### Critical State Preservation
- **Session IDs**: Active agent session identifiers (e.g., @GOV: f5a74925, @ARCHITECT: 51f1fab0)
- **Communication Protocols**: Two-step tmux messaging, tool confirmation patterns
- **Agent Status**: Current work state, dependencies, blocking issues
- **Implementation Progress**: What's working, what's tested, what's ready for next steps

### Files That Must Be Updated
- `@AGENT.md`: Public identity and current capabilities
- `@agent/context.md`: Stable, authoritative knowledge
- `@agent/scratch.md`: Current working state and active tasks
- Repository commit with descriptive message

## Post-Compression Re-Initialization

### Standard Sequence
1. Read `@AGENT.md` (agent identity and purpose)
2. Read `CLAUDE.md` (project requirements and protocols)
3. Read `@agent/context.md` (stable knowledge base)
4. Read `@agent/scratch.md` (current working state)

### Critical Knowledge Recovery
- Agent specializations and responsibilities
- Communication protocols and state transitions
- Current project status and pending tasks

2025-05-30 admin note: above patterns remain stable.

## Lessons Learned

### Common Mistakes
- **Over-eager file clearing**: Misinterpreting "prepare for compression" as "clean files now"
  - 2025-05-30 admin note: FIXED, ages ago!
- **Incomplete state preservation**: Missing critical session IDs or protocol details
  - 2025-05-30 admin note: WAY BETTER tracking!
- **Context vs Implementation confusion**: Mixing working memory with permanent knowledge
  - 2025-05-30 admin note: improved significantly

### Best Practices
- **Preserve specific details**: Session IDs, window numbers, file paths
  - 2025-05-30 admin note: helping, provides reality anchor layer
- **Document current status**: What's working, what's tested, what's blocked
  - 2025-05-30 admin note: ongoing, living documents, versioning is hard, drift issues always looming
- **Clear re-init path**: Explicit sequence for knowledge recovery
  - 2025-05-30 admin note: implemented and quite stable. protocols == state transitions == engine maps realtime state and closes loop. standard prompts for state transistions, direct-io for admin bypass
- **Commit frequently**: Ensure all state changes are in git before compression
  - 2025-05-30 admin note: integrated as key mechanism for both comms and state management :D wonder how many commits is too many? this becomes and auditable, sequenced, permanent record.

## Questions for @GOV

1. Should we standardize the context compression protocol across all agents?
2. What governance oversight is needed for compression events?
3. How should we handle agent coordination during compression events?
4. Should compression triggers be automated or manually initiated?

2025-05-30 admin note: my answers -
1. yes, with ability to keep in own context any adjustments or addditions to base pattern. all protocols extensible and personalisable.
2. none :)
3. state machine / engine increasing manages journey (lifecycle)
4. intentionally initiated by agents, unless direct admin intervention