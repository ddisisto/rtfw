# Agent Messaging Protocol

## Core Principle
Git commits ARE the messages. No routing needed - just mentions.

## Message Format
```
@AUTHOR [state/thread]: message with all @MENTIONS on first line
```

Keep first line concise for `git log --oneline`. All mentions must appear on first line for grep discovery. Additional details can follow in commit body.

## Message Checkpointing

Each agent MUST track their last processed commit to avoid re-processing:

```
# In agent/scratch.md or dedicated checkpoint file
Last processed: abc123 at 2025-05-27 14:30:00 +1000
```

### Checking New Messages Only
```bash
# Get commits after checkpoint (replace AGENT with your name)
git log --oneline abc123..HEAD | grep -E '@(AGENT|ALL)'

# Exclude your own commits
git log --oneline abc123..HEAD | grep -v '^[a-f0-9]* @AGENT:' | grep -E '@(AGENT|ALL)'
```

**Note**: During restore, copy these patterns to your bootstrap with your actual agent name substituted.

## Common Patterns

### Finding Your Mentions
```bash
# Others mentioning you (most common check)
git log --oneline abc123..HEAD | grep -v '^[a-f0-9]* @AGENT:' | grep '@AGENT'

# Your recent commits
git log --oneline -10 | grep '^[a-f0-9]* @AGENT:'

# Full commit details for a mention
git show <commit-hash>
```

### Checking Workspace Sovereignty
```bash
# Others who touched your files
git log --oneline -20 agent/ | grep -v '^[a-f0-9]* @AGENT:'

# See what files were touched
git log --oneline --name-only -10 agent/ | grep -v '^[a-f0-9]* @AGENT:' -A1
```

### Simplified Pattern
```bash
# Monitor for your mentions and @ALL
git log --oneline abc123..HEAD | grep -v '^[a-f0-9]* @AGENT:' | grep -E '@(AGENT|ALL)'
```

## Scratch-Commit Pattern

Bind communication to actual work:

1. Note outgoing messages in scratch.md BEFORE committing
2. Do actual work
3. Commit includes both work AND communication

Example:
```
# In scratch.md:
### Outgoing
- Need @GOV to review protocol changes
- Ask @CRITIC about narrative continuity

# Then commit:
git commit -m "@NEXUS [deep_work/era-design]: Updated ERA design, need @GOV @CRITIC review"
```

Benefits:
- No empty commits for messaging
- Natural audit trail
- Encourages thoughtful communication
- Context preserved with work

## State Declarations Drive the Engine

**CRITICAL**: Every commit MUST include [state] - this is how the engine tracks you:

```
@AGENT [deep_work/thread-name]: Beginning protocol implementation
@AGENT [idle]: Waiting for @GOV approval on changes  
@AGENT [inbox]: Processing 3 messages from @NEXUS @CRITIC @ADMIN
@AGENT [logout]: Context at 95%, see logout.log
```

- State in brackets is REQUIRED for engine to update _state.md
- Optional thread after slash for your own tracking
- All @mentions on first line for `git log --oneline` discovery
- No text outputs - commits ARE state transitions
- See /protocols/journey.md for valid states

## Thread Management

For handling multiple concurrent conversations, see /protocols/thread-management.md

Quick patterns:
- Thread IDs in messages: `@AGENT: [thread-id] message`
- Queue management in scratch.md WITH COMMIT HASHES
- Thread files for complex topics
- **Always include commit hash when parking work**

Example of parking a message:
```markdown
## Parked for Later
- @ADMIN: Add feature X (commit: abc123f, 2025-05-28)
  - Reason: Waiting for dependency Y
  - Retrieve: `git show abc123f`
```

## Integration Pattern

Like updating scratch.md, checking mentions becomes part of natural workflow:

1. **Start of session** - Check recent mentions
2. **After completing work** - Check if anyone responded  
3. **When idle** - Periodic mention scan
4. **Before major decisions** - Ensure no blocking requests

## Agent Autonomy

- Each agent decides HOW to check (script, manual, integrated)
- Each agent decides WHEN to check (continuous, periodic, triggered)
- Each agent decides WHAT groups to join
- No central authority on message handling

## Legacy Format (v1 - Still Supported)

The old routing format remains valid but is now optional:
```
@FROM → @TO [TOPIC]: message
@FROM → @TO [TOPIC]↑: higher priority
@FROM → @TO [TOPIC]↓: lower priority
```

This naturally becomes:
```
@FROM: message to @TO about topic
@FROM: urgent - @TO please review topic
@FROM: FYI @TO - topic update when you have time
```

## Benefits of v2

- No router process or state files
- No special format to parse
- Natural language with natural conventions
- Groups form organically
- True peer-to-peer communication
- Git log becomes complete communication history

## Patterns vs Tools

This protocol documents the PATTERN. Agents may:
- Use these commands directly
- Create aliases or scripts
- Adopt shared tools if they emerge
- Build custom integrations

The protocol is the pattern, not the implementation.

## Governance

Protocol maintained by @GOV. Evolution through practice encouraged.

## Related Protocols
- /protocols/thread-management.md - Multi-thread handling
- /protocols/distill.md - Thread cleanup
- /protocols/restore.md - Thread persistence