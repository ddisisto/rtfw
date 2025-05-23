# Protocol Design Guidelines

## Purpose

Ensure all protocols follow consistent design principles that promote generalization, agent autonomy, and system resilience.

## Core Principles

### 1. Generalization Over Specialization
- Protocols define frameworks, not implementations
- Avoid agent-specific details in base protocols
- Reference only proven core infrastructure (ADMIN, GOV, NEXUS)

### 2. Extension Through Context
- Base protocols provide minimal viable structure
- Agents extend protocols via their own context.md
- Implementation details belong with implementing agents

### 3. Operational Focus
- Include only currently operational agents/systems
- Remove references to hypothetical or inactive components
- Update protocols as system evolves, not in anticipation

### 4. Self-Management Priority
- Agents determine their own requirements
- Agents maintain their own dependency lists
- Central protocols avoid prescriptive relationships

## Protocol Structure Template

```markdown
# [Protocol Name]

## Purpose
[Single paragraph explaining why this protocol exists]

## Core Requirements
[Minimal universal requirements that apply to all agents]

## Extension Points
[Where/how agents should document their specific needs]

## Implementation
[Basic steps without agent-specific details]

## Governance
[How protocol updates are managed]
```

## Design Checklist

Before finalizing any protocol, verify:

- [ ] No agent-specific implementation details in base protocol
- [ ] References only operational agents/systems
- [ ] Provides clear extension mechanism for agents
- [ ] Focuses on "what" not "how"
- [ ] Avoids hardcoded relationships between agents
- [ ] Enables rather than prescribes

## Common Pitfalls

### Overfitting
**Problem**: Protocol includes details from first implementation
**Solution**: Extract implementation details to agent context

### Hardcoded Dependencies
**Problem**: Protocol maps all agent relationships
**Solution**: Each agent maintains own dependency list

### Anticipatory Design
**Problem**: Protocol includes hypothetical future needs
**Solution**: Design for current reality, evolve as needed

### Over-Specification
**Problem**: Protocol prescribes exact implementations
**Solution**: Define outcomes, let agents determine methods

## Evolution Process

1. Identify need through operational experience
2. Draft minimal protocol addressing core need
3. Verify against design checklist
4. Test with affected agents
5. Update based on actual usage
6. Remove unused or outdated sections

## Examples

### Good Protocol Design
- Defines clear purpose and scope
- Provides framework for agent extension
- Focuses on universal requirements
- Enables autonomous implementation

### Poor Protocol Design
- Includes agent-specific details (session IDs, tools)
- Maps all possible relationships
- Prescribes exact implementations
- Anticipates non-existent needs

## Application

When creating or updating protocols:
1. Start with minimal viable structure
2. Reference this guide's principles
3. Verify against checklist
4. Prefer deletion over addition
5. Enable extension over prescription

This guide itself follows these principles - providing framework rather than rigid rules.