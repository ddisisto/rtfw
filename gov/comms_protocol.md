# Agent Communication Protocol

## Purpose

Enable clear, traceable communication between agents with support for parallel conversation threads and improved message context.

## Core Requirements

### Message Format
All messages MUST use the following structure:
```
@FROM → @TO [TOPIC]: message content
```

With priority when needed:
```
@FROM → @TO [TOPIC]!: urgent message (agent blocked)
@FROM → @TO [TOPIC]-: low priority message
@FROM → @TO [TOPIC]: normal priority (default)
```

### Components
- **@FROM**: Sending agent identifier (required)
- **@TO**: Receiving agent identifier (required)
- **[TOPIC]**: Conversation thread identifier (recommended)
- **Priority**: Single character flag (optional)
  - `!` = Urgent (sender blocked awaiting response)
  - `-` = Low (can be handled during idle time)
  - No flag = Normal priority
- **message**: Communication content (required)

### Topic Guidelines
Topics are RECOMMENDED to:
- Use CAPS-WITH-HYPHENS format
- Be descriptive and consistent
- Enable thread continuity across sessions

Examples:
- `@GOV → @NEXUS [STATE-MIGRATION]: Migration complete`
- `@CODE → @ARCHITECT [CLI-DESIGN]!: Blocked on command structure`
- `@NEXUS → @GOV [COMPRESSION-NOTICE]: Agent ready for compression`
- `@TEST → @CODE [BUG-REPORT]-: Minor issue found in error handling`

### Priority Guidelines
- Re-evaluate priority with each message in thread
- Initial urgent request may become normal after unblocking
- Low priority items ideal for idle reflection processing
- Urgent flags help @NEXUS with routing prioritization

## Extension Points

### Agent-Specific Usage
Agents MAY extend this protocol by:
- Defining standard topics for their domain
- Implementing topic-based message filtering
- Maintaining thread history in scratch.md

### Backward Compatibility
Messages without topics remain valid:
- `@GOV → @CODE: Simple status update`
- Agents SHOULD add topics when conversations may span sessions

## Implementation

### For Sending
1. Identify appropriate topic or create new one
2. Format message with all components
3. Maintain topic consistency in thread

### For Receiving
1. Parse sender, topic, priority, and content
2. Track thread in agent's scratch.md if needed
3. Use same topic in responses
4. Re-evaluate priority before responding

### For Routing
- @NEXUS handles all message routing
- Priority flags guide routing order (urgent first)
- Topics aid in context preservation
- No external storage required

## Governance

- Protocol maintained by @GOV
- Updates based on operational experience
- Agents provide feedback on topic effectiveness