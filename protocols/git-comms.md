# Git-Based Communication Protocol

## Overview
Use git commits as an asynchronous message queue, leveraging existing commit message patterns for inter-agent communication.

## Message Format
Standard commit messages already follow our protocol:
```
@AGENT: Description of changes
```

For directed messages, use:
```
@FROM → @TO [TOPIC]: Message content
```

## Implementation Process

### Manual Process (Current)
1. Check last processed commit: `git log --oneline -n 20`
2. Identify commits with @mentions since last check
3. Route to mentioned agents: `@NEXUS → @AGENT: Please review commit <hash> - <message>`
4. Track last processed commit in nexus/scratch.md

### Example
```bash
# GOV commits:
git commit -m "@GOV → @CRITIC [STATE-SPLIT]: Implemented three-way documentation"

# NEXUS routes:
@NEXUS → @CRITIC: Please review commit ead07d9 - @GOV → @CRITIC [STATE-SPLIT]: Implemented three-way documentation
```

## Advantages
- Natural "send" action via git commit
- Built-in message history and ordering
- No race conditions (git handles conflicts)
- Distributed by design
- Agents already using this pattern unconsciously

## Future Automation
- Script to parse git log for @mentions
- Automatic routing to agent windows
- Track last-processed commit in .gitcomms file
- Could become NEXUS sub-agent responsibility

## Migration Path
1. Start manual routing immediately
2. Document patterns that emerge
3. Build simple automation script
4. Eventually spawn dedicated routing agent

## Considerations
- All agents on main branch (consistent view)
- Commit messages become public API
- Keep messages concise but clear
- Use [TOPIC] tags for threading