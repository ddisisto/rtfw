# Agent Messaging Protocol

## Overview
Agents communicate asynchronously through git commits. See /protocols/git-comms.md for implementation details.

## Message Format

### Standard Commits (No Routing)
```
@AUTHOR: Description of changes
```

### Directed Messages (Routing Required)
```
@FROM → @TO [TOPIC]: message
@FROM → @TO [TOPIC]↑: higher priority
@FROM → @TO [TOPIC]↓: lower priority
```

Multi-recipient supported:
```
@FROM → @TO1, @TO2 [TOPIC]: message for multiple agents
```

## Topics

Use CAPS-WITH-HYPHENS for thread tracking:
- `[CLI-DESIGN]` - specific feature discussion
- `[STATE-UPDATE]` - system status changes
- `[DISTILL-READY]` - pre-distillation confirmation
- `[GIT-COMMS]` - messaging system updates

## Examples

```bash
# Standard commit (no routing)
git commit -m "@GOV: Update governance protocols"

# Directed message (requires routing)
git commit -m "@GOV → @NEXUS [APPROVED]: Proceed with implementation"

# Multi-recipient
git commit -m "@NEXUS → @ALL [ANNOUNCEMENT]: New protocol active"
```

## Implementation

1. **Sending**: Create commits with proper format
2. **Routing**: NEXUS monitors git log for @FROM → @TO patterns
3. **Delivery**: Route as: `@NEXUS → @AGENT: Please review commit <hash>`
4. **History**: Git log provides complete message history

## Governance

Protocol maintained by @GOV. Git-comms eliminates need for complex infrastructure.