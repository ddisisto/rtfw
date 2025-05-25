# Agent Messaging Protocol

## Format

All messages use:
```
@FROM → @TO [TOPIC]: message
```
With optional ↑↓ priority:
  - ↑, ↑↑ `... [TEST-FAILURES]↑: search string not found...`
  - ↓, ↓↓ `... [DRAFT-PROCESS]↓: process doc ready for draft review at ...`

## Topics

Use CAPS-WITH-HYPHENS for thread tracking:
- `[CLI-DESIGN]` - specific feature discussion
- `[STATE-UPDATE]` - system status changes
- `[DISTILL-READY]` - pre-distillation confirmation

Topics recommended for multi-session threads.

## Examples

```
@CODE → @ARCHITECT [CLI-DESIGN]↑↑: Blocked on command structure
@NEXUS → @GOV [DISTILL-NOTICE]: Agent ready for distillation
@TEST → @CODE [BUG-REPORT]↓: Minor issue in error handling
@GOV → @ADMIN: Simple update (no topic needed)
```

## Routing

- @NEXUS routes all messages
- Priority guides order
- Topics preserve context
- No external storage

## Governance

Protocol maintained by @GOV. Extensions welcome.