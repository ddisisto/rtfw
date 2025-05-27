# Agent Structure Protocol

## Purpose

Define the standard structure for @AGENT.md files to ensure consistency and discoverability across all agents.

## @AGENT.md Structure

Each agent MUST have an @AGENT.md file at the repository root with these sections:

### Required Sections

#### Identity
```markdown
## Identity
- Role: [One sentence describing primary function]
- Purpose: [Core responsibility and value to system]
- Authority: [What they can modify, workspace sovereignty]
- Lifecycle: [If applicable - especially for transient agents like ERA-N]
```

#### Interfaces
```markdown
## Interfaces  
- Inputs: [What they receive from other agents/system]
- Outputs: [What they provide to others]
- Dependencies: [Required agents/protocols for operation]
```

### Recommended Sections

#### Bootstrap Protocol
```markdown
## Bootstrap Protocol
1. Read @AGENT.md for identity
2. Read CLAUDE.md for system navigation
3. Read SYSTEM.md for architecture
4. Load agent/context.md and agent/scratch.md
5. Check mentions: `git log --oneline LAST..HEAD | grep '@AGENT'`
6. [Role-specific initialization steps]
```

**IMPORTANT**: Bootstrap protocols in @AGENT.md files must remain generic and stable. Never include:
- Current work items or priorities
- Active task lists or todos
- Specific message checkpoints
- Temporary state or context

These belong in agent/context.md and agent/scratch.md only.

#### Core Responsibilities
Detailed breakdown of what the agent does, organized by category.

#### Authorities
Explicit permissions and boundaries:
- What files/directories they own
- What requires approval from others
- Cross-agent coordination requirements

### Optional Sections
- Design Principles (for implementation agents)
- Success Metrics (for goal-oriented agents)
- Workspace Structure (if complex)

## Agent Workspace Structure

Each agent has a corresponding workspace directory:

```
/agent-name/
  context.md    # Stable knowledge, restore dependencies
  scratch.md    # Working memory, message checkpoints
  notes/        # Optional documentation
  tools/        # Optional agent-specific tools
  threads/      # Optional thread files
```

## Key Principles

### Separation of Concerns
- **@AGENT.md**: Public contract, stable identity, generic processes
- **agent/context.md**: Current knowledge, work state, dependencies
- **agent/scratch.md**: Active work, message checkpoints, todos

### Stability
@AGENT.md files should rarely change. They define WHO the agent is, not WHAT they're currently doing.

## Evolution

This protocol documents observed conventions. Agents may extend their @AGENT.md with additional sections as needed, but MUST include required sections for system coherence.

## Examples
- See GOV.md, NEXUS.md, CRITIC.md for meta-agent patterns
- See ERA-1.md for transient implementation agent pattern

## Governance

Protocol maintained by @GOV. Updates based on emerging patterns.