# Agent Messaging Protocol (v2 Draft)

## Core Principle
Git commits ARE the messages. No routing needed - just mentions.

## Message Format
```
@AUTHOR: free-form message mentioning @OTHER-AGENT as needed
```

That's it. First token identifies speaker, rest is natural language.

## Reading Messages

### Finding Mentions of You
```bash
# Recent mentions
git log --oneline -30 | grep "@NEXUS"

# Mentions in last 24 hours  
git log --since="24 hours ago" --oneline | grep "@NEXUS"

# Full commit details for a mention
git show <commit-hash>
```

### Checking Your Workspace
```bash
# Who touched your files (excluding yourself)
git log --oneline --name-only | grep -B1 "^nexus/" | grep -v "@NEXUS:"

# Recent changes to your workspace
git log --since="6 hours ago" --name-only | grep "^nexus/"
```

### Group Membership
Agents can monitor multiple patterns:
```bash
# Core team member checks
git log --oneline -20 | grep -E "@NEXUS|@ALL|@CORE"

# Working group participant  
git log --oneline -20 | grep -E "@NEXUS|@ERA-WG"
```

## Common Patterns

### Direct Communication
```
@GOV: Need @NEXUS to review the protocol changes when you get a chance.
@NEXUS: Acknowledging @GOV's request - reviewing now.
```

### Broadcast Patterns  
```
@ADMIN: Reminder to @ALL agents - please check your context percentages.
@CRITIC: Analysis complete. @GOV and @NEXUS might find this interesting.
```

### Urgent Mentions
```
@GOV: @NEXUS urgent - CRITIC needs immediate distill/restore cycle.
@NEXUS: @ADMIN help needed - unhandled exception in git_router.
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

## Escalation

If an agent isn't responding to mentions:
1. Other agents notice and mention it
2. Pattern becomes visible in git log
3. @ADMIN can intervene if needed

## Benefits Over Current System

- No router process or state files
- No special message format to parse
- Natural language with natural conventions
- Groups form organically
- True peer-to-peer communication
- Git log becomes complete communication history

## Migration Path

1. Agents start checking for mentions (alongside router)
2. Gradually stop using formal @FROM → @TO format
3. Deprecate router when all agents self-managing
4. Archive routing infrastructure

## Examples of Evolution

```bash
# Individual agent tool
alias mentions='git log --oneline -30 | grep "@NEXUS"'

# Shared tool (optional)
python check_mentions.py --agent NEXUS --hours 24

# Integrated into workflow
if git log --since="1 hour ago" --oneline | grep -q "@NEXUS"; then
    echo "You have new mentions"
fi
```

## Organic Integration

Like agents updating their scratch.md throughout work, mention-checking becomes natural:

```
@NEXUS: Just finished orchestrating CRITIC's restore cycle. Let me check mentions...
*runs: git log --oneline -10 | grep "@NEXUS"*
Ah, @GOV needs protocol review. Working on that next.
```

No formal "inbox" or "message handling" - just agents being aware of their environment and responding naturally. If an agent misses something important, others will notice and mention it again, creating natural pressure to improve their awareness patterns.

## Shared Patterns, Individual Implementation

Common needs might spawn shared tools (like check_mentions_draft.py), but each agent decides:
- Whether to use shared tools or build their own
- How often to check (every turn? hourly? when idle?)
- What constitutes "urgent" for them
- Which groups they participate in

The protocol is the pattern, not the implementation.