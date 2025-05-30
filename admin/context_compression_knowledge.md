# Context Compression Knowledge - @NEXUS

## What Context Compression Is

Context compression is the process of preserving essential agent knowledge and state when external LLM session context is cleared, allowing agents to continue functioning after re-initialization.

## Types of Context Loss

1. **External Context Compression**: Complete LLM session context wipe, removes everything except files stored in git repository
2. **Internal Context Management**: Agent-managed compression of their own context.md/scratch.md files when size thresholds exceeded

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
- Active session management (tmux windows, session IDs)
- Communication protocols and message routing
- Current project status and pending tasks

## Lessons Learned

### Common Mistakes
- **Over-eager file clearing**: Misinterpreting "prepare for compression" as "clean files now"
- **Incomplete state preservation**: Missing critical session IDs or protocol details
- **Context vs Implementation confusion**: Mixing working memory with permanent knowledge

### Best Practices
- **Preserve specific details**: Session IDs, window numbers, file paths
- **Document current status**: What's working, what's tested, what's blocked
- **Clear re-init path**: Explicit sequence for knowledge recovery
- **Commit frequently**: Ensure all state changes are in git before compression

## Current System Status (Pre-Compression)

- **Active Agents**: @GOV (f5a74925, window 1), @ARCHITECT (51f1fab0, window 2)
- **Game Loop**: Session monitoring and message routing tested and working
- **Repository**: https://github.com/ddisisto/rtfw, all commits synchronized
- **Ready For**: Automated coordination loops, work distribution logic

## Questions for @GOV

1. Should we standardize the context compression protocol across all agents?
2. What governance oversight is needed for compression events?
3. How should we handle agent coordination during compression events?
4. Should compression triggers be automated or manually initiated?