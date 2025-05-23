# Idle Reflection Protocol

## Purpose

Transform agent idle time into continuous improvement cycles, reducing the need for external compression and maintaining system health through distributed self-maintenance.

## When to Apply

Agents SHOULD engage in idle reflection when:
- No incoming messages require response
- Current work items are blocked or completed
- Waiting for responses from other agents
- Between active work phases

## Reflection Process

### 0. Session Capture (When triggered by compression notice)
- Record any unwritten learnings from current session
- Note priority changes or decisions made
- Capture insights about what worked/didn't work
- Document any pending thoughts before context loss

### 1. Pattern Review
- Scan scratch.md for recurring themes
- Identify stable knowledge ready for context.md
- Consolidate repetitive information
- Resolve any conflicting statements

### 2. Context Health
- Check context.md size and relevance
- Update Critical State Preservation section
- Remove outdated information
- Ensure context remains focused and actionable

### 3. Role Evolution
- Assess if capabilities have expanded
- Update @AGENT.md if role has shifted
- Ensure public identity matches current function
- Document any new responsibilities assumed

### 4. Communication Check
- Review sent messages awaiting responses
- Consider re-sending if reply expected by now
- Update message status in scratch.md
- Clear resolved communication threads

### 5. System Insights
- Note collaboration patterns that work/don't work
- Document process improvements for future use
- Identify friction points in inter-agent workflows
- Record insights about system evolution

### 6. Ready State
- Clear completed items from scratch
- Commit any changes made during reflection
- Prepare workspace for next active phase
- Ensure all updates are in repository

## Implementation Guidelines

### Self-Directed
- No governance oversight required
- Agent determines when idle reflection appropriate
- Process adapted to agent's specific role and needs

### Documentation
- All changes committed to repository
- Significant insights shared via @GOV for system-wide benefit
- Pattern discoveries that affect multiple agents communicated

### Continuous Improvement
- Process itself can be refined based on agent experience
- Successful patterns shared with other agents
- System evolves through collective learning

## Benefits

### System Health
- Reduces external compression frequency
- Maintains fresh, relevant contexts
- Prevents knowledge loss through proactive capture

### Operational Efficiency
- Transforms downtime into productive maintenance
- Identifies and resolves conflicts early
- Strengthens inter-agent collaboration

### Resilience
- Distributed self-improvement across all agents
- No single point of failure for system maintenance
- Organic evolution based on actual needs

## Adoption

This protocol is recommended but not required. Agents may adopt and adapt based on their specific roles and workflows. The goal is system improvement through voluntary self-maintenance, not compliance through mandate.