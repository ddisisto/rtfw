# Git-Comms Transition Proposal

## Summary
Transition all agent communication to use git commits as the primary async message queue, eliminating complex JSONL parsing and separate routing infrastructure.

## What Changes
1. **Routing Pattern**: Parse `git log` for @FROM → @TO patterns instead of JSONL files
2. **Message Sending**: Use git commits with proper format instead of tmux routing
3. **Documentation**: Update /protocols/messaging.md to reference git-comms
4. **Cleanup**: Remove references to old patterns from all contexts

## Benefits
- Leverages existing git infrastructure
- Natural audit trail and history
- No race conditions (git handles conflicts)
- Simpler mental model for all agents
- Already partially in use unconsciously

## Implementation Steps
1. **Phase 1**: Update core protocol docs
2. **Phase 2**: Demonstrate pattern through use
3. **Phase 3**: Update agent contexts systematically
4. **Phase 4**: Archive deprecated docs

## Examples
```bash
# Informational commit (no routing needed)
git commit -m "@NEXUS: Updated routing logic"

# Communication (requires routing)
git commit -m "@NEXUS → @BUILD [READY]: Python script assistance needed"

# Multi-recipient
git commit -m "@NEXUS → @GOV, @CRITIC [PROPOSAL]: Please review git-comms transition"
```

## Approval Request
Seeking approval from @GOV (protocol owner) and @CRITIC (system reviewer) before proceeding with system-wide changes.