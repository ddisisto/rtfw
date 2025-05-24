# Context Consolidation Protocol

## Purpose

Maintain agent workspace coherence through regular consolidation of working memory into stable knowledge, supporting both continuous improvement and compression readiness.

## Core Requirements

### When to Apply
Agents MUST perform consolidation:
- Prior to external context compression (see gov/context_compression_protocol.md)

Agents SHOULD perform consolidation:
- When no active work or messages require attention
- While waiting for responses or external dependencies
- At regular maintenance intervals determined by agent

### File Processing Order
Agents SHOULD review their workspace files in this sequence:
1. **scratch.md** - Capture and organize working memory
2. **context.md** - Promote stable knowledge from scratch
3. **@AGENT.md** - Update public identity if role evolved

### Consolidation Framework
Agents MAY focus on these areas during consolidation:
- **Knowledge promotion** - Move stable patterns from scratch to context
- **Conflict resolution** - Identify and resolve contradictions
- **State updates** - Current status, pending items, dependencies  
- **Role alignment** - Ensure public identity reflects actual function
- **Thread management** - Review communication status and priorities

## Extension Points

### Agent-Specific Adaptations
Each agent SHOULD document in their context.md:
- Consolidation frequency and triggers specific to their role
- Additional files or areas included in their process
- Custom consolidation steps based on their tools/responsibilities

### Process Variations
Agents MAY:
- Add domain-specific consolidation areas
- Integrate with their operational workflows
- Develop automated consolidation triggers
- Extend for internal compression needs

## Implementation

### Basic Flow
1. Review files in suggested order
2. Make updates as appropriate
3. Commit changes to repository

### Key Principles
- Self-directed timing and scope
- Adapt process to role requirements
- Share significant insights with system

## Governance

- Protocol maintained by @GOV
- Updates based on collective agent experience
- Voluntary adoption and adaptation encouraged