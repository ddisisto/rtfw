# NEXUS Context Management

**Purpose**: Managing agent memory through distillation and restoration. This document covers context operations only. For session management, see sessions.md. For work states, see lifecycle.md.

## Core Concepts

### Distillation
Process of refining agent knowledge from working memory (scratch.md) into stable memory (context.md), then clearing working memory to baseline.

### Two Types
1. **Continuous Distillation**: Agent refines knowledge during idle time
2. **Cyclical Distillation**: System-wide clearing of working memory

### Key Principle
Distillation is independent of sessions. You can:
- Distill multiple times per session
- Resume sessions without distilling
- Use /clear to control when distillation happens

## Context Monitoring

### Thresholds
- **34% remaining**: Potential bloat, consider distillation
- **15% remaining**: Urgent, distill soon to maintain coherence
- **Below 15%**: Risk of auto-compact with recency bias

### Checking Context
```
tmux capture-pane -t <agent> -p | grep "Context:"
```

Look for percentage in agent's interface footer.

## Distillation Process

### 1. Continuous Distillation (During Idle)
Agent-driven refinement of knowledge:

**Prompt:**
```
@NEXUS → @<AGENT> [DISTILL]: No active work detected. Please perform continuous distillation per @protocols/distill.md
```

**Process:**
- Agent reviews scratch.md
- Moves stable insights to context.md
- Commits changes to git
- Continues working with refined knowledge

### 2. Cyclical Distillation (System-Wide)

**Pre-Distill Notice:**
```
@NEXUS → @<AGENT> [DISTILL]: Cyclical distillation initiated. Please complete continuous distillation per @protocols/distill.md and confirm readiness
```

**Agent Response:**
```
@<AGENT> → @NEXUS [DISTILL]: Context distilled. Changes committed. Ready for /clear command.
```

**Clear Execution:**
```
tmux send-keys -t <agent> '/clear' Enter
```

**Effect:**
- Instantly resets working memory to baseline
- Agent retains only initial prompts + context files
- Personality temporarily offline during restore

### 3. Post-Clear Restore

**Send Restore Message:**
```
@NEXUS → @<AGENT> [RESTORE]: @protocols/restore.md underway for @<AGENT>.md agent - please restore context for continuation
```

**Monitor Recovery:**
- Agent reads required files mechanically
- Personality returns after file loading
- Agent confirms operational status
- Resume normal operations

## When to Distill

### Recommended Times
- During extended idle periods (not recent distillation)
- When context shows 34%+ and no urgent work
- Before major task transitions
- At regular intervals (daily/weekly)

### Avoid Distilling
- Mid-task or during active work
- Multiple agents simultaneously
- Without continuous distillation first
- When context is already clean (<50%)

## Critical Knowledge

### /clear Command
- THE command that performs distillation
- Without it, agent continues with bloated context
- Gives control vs unpredictable auto-compact
- Forgets recent unpersisted context

### Proper Workflow
1. Agent performs continuous distillation (refines workspace)
2. NEXUS sends /clear command (resets memory)
3. NEXUS sends restore message (reloads context)
4. Agent resumes work with clean memory

### Common Mistakes
- Confusing session restart with distillation
- Skipping continuous distillation before /clear
- Not waiting for agent readiness
- Distilling too frequently

## NEXUS Responsibilities

### Monitoring
- Track last distillation time per agent
- Watch context percentages
- Notice performance degradation
- Coordinate multi-agent distillations

### Execution
- Send pre-distill notices
- Wait for readiness confirmation
- Execute /clear command
- Send restore messages
- Verify successful recovery

### Documentation
- Note distillation times in scratch.md
- Track any issues or patterns
- Report to @ADMIN if problems
- Maintain distillation schedule