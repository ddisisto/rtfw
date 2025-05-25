# Agent Communication Patterns

## Overview
How agents communicate with each other and coordinate work within the system.

## Core Patterns

### 1. Protocol Adherence
- Agents strictly follow `@FROM → @TO [TOPIC]: message` format
- Humans often skip protocol but agents understand context
- System tolerates both formal and informal styles

### 2. @NEXUS as Central Hub
Evolution of role:
- Initial: Passive message router
- Current: Active system coordinator
- Monitors agent health
- Initiates maintenance cycles
- Distributes architectural updates

### 3. Agent Autonomy Patterns

**Proactive Actions:**
- Context maintenance without prompting
- Cross-agent recommendations
- Status updates to relevant parties

**Coordination Methods:**
- Direct @mentions for requests
- ANNOUNCEMENTS.md for broadcasts
- Context.md for persistent state
- Git commits for action tracking

### 4. Communication Hierarchy

1. **Human → Agent**: Often informal, context-dependent
2. **Agent → Agent**: Always formal, protocol-compliant  
3. **Agent → Human**: Formal responses, status updates
4. **Broadcast**: Via ANNOUNCEMENTS.md or @ALL

### 5. Implicit vs Explicit

**Explicit:**
- Direct messages with @ mentions
- Git commit messages
- File updates

**Implicit:**
- "The drill" - shared procedures
- Context maintenance timing
- Work prioritization

## Examples

### Maintenance Cascade
```
@NEXUS → @GOV: Context maintenance complete for @NEXUS. 
Recommend you perform same...
```
Result: @GOV performs maintenance, updates announcements

### Architecture Distribution  
```
@NEXUS → @ARCHITECT: CLI architecture update from @ADMIN...
```
Result: Technical decisions flow through agent network

### Status Confirmation
```
@GOV → @NEXUS: OPERATIONAL STATUS CONFIRMED
```
Result: Acknowledgment enables next actions

## Anti-Patterns

1. **Not observed yet**: Agents breaking protocol
2. **Not observed yet**: Communication failures
3. **Not observed yet**: Message loops or conflicts

## Evolution Timeline

1. **Batch 001**: Human-driven, establishing protocols
2. **Batch 002**: Agent-initiated, following protocols
3. **Future**: Increasing autonomy, self-organization?

## Open Questions

- What are the limits of agent autonomy?
- How do agents decide when to act vs wait?
- What constitutes "the drill" for procedures?
- How will the system handle communication failures?