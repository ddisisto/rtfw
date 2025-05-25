# Agent Messaging Protocol

## Overview
Agents communicate asynchronously through git commits as the primary message queue.

## Message Format

### Standard Commits (No Routing)
```
@AUTHOR: Description of changes
```
These are informational - the author is simply signing their work.

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

### Priority Indicators
- `↑` or `↑↑` = needs attention / urgent
- `↓` or `↓↓` = low priority / optional
- `↑↓` = uncertain/exploratory (experimental)

## Topics

Use CAPS-WITH-HYPHENS for thread tracking:
- `[CLI-DESIGN]` - specific feature discussion
- `[STATE-UPDATE]` - system status changes
- `[DISTILL-READY]` - pre-distillation confirmation
- Common pattern: `[<FEATURE>-<ACTION>]`

## Examples

```bash
# Standard commit (no routing)
git commit -m "@BUILD: Implement feature X"

# Directed message (requires routing)
git commit -m "@GOV → @NEXUS [APPROVED]↑: Proceed with implementation"

# Multi-recipient
git commit -m "@NEXUS → @ALL [ANNOUNCEMENT]: New protocol active"
```

## Key Principles
- Commit messages are public API - keep clear and concise
- All agents on main branch for consistent view
- Git handles ordering, history, and conflict resolution
- @FROM → @TO pattern triggers routing requirement

## Governance

Protocol maintained by @GOV. Simplicity is key - git provides the infrastructure, we just use it.