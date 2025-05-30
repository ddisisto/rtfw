# Thread Management Protocol

## Purpose

Enable agents to manage multiple concurrent conversation threads and work streams as system complexity grows.

## Core Patterns

### Thread Identification
Each significant work stream gets a thread identifier:
- Format: `YYYY-MM-DD-topic` (e.g., `2025-05-28-era1-init`)
- Short descriptive names
- Timestamp prefix for natural ordering

### Scratch Organization

#### Option 1: Section-Based (Default)
```markdown
## Thread: 2025-05-28-era1-init
- Current state of ERA-1 implementation
- Pending decisions
- Next actions

## Thread: 2025-05-28-messaging-v2
- Migration status
- Agent responses tracked
```

#### Option 2: File-Based (For Complex Threads)
```
agent/
  scratch.md          # Main scratch, thread index
  threads/
    2025-05-28-era1-init.md
    2025-05-28-messaging-v2.md
```

**Important**: When using file-based threads, maintain an index in your main scratch.md and/or context.md:

```markdown
## Active Thread Files
- [2025-05-28-era1-init](threads/2025-05-28-era1-init.md) - ERA-1 bootstrap and architecture
- [2025-05-28-messaging-v2](threads/2025-05-28-messaging-v2.md) - Migration tracking
```

This ensures thread discovery during restore and provides quick context for what each thread contains.

### Thread Lifecycle

1. **Creation**: When topic requires sustained attention
2. **Active**: Regular updates, clear next actions
3. **Dormant**: No activity for 48h, may archive
4. **Closed**: Completed or deprecated

### Message Triage Pattern

When multiple messages arrive:

1. **Quick Scan**: Check all messages for urgency markers
2. **Immediate Response**: Safety issues, blockers, time-sensitive
3. **Queue Others**: Note in relevant thread section WITH COMMIT CONTEXT
4. **Process in Turn**: Work through queued items
5. **Update Checkpoint**: Track last processed

**CRITICAL**: Always record commit hash and date when deferring items. A note without context becomes orphaned after distill/restore.

Example:
```markdown
## Incoming Queue
- [ ] @ADMIN: Review ERA-1 progress (commit: abc123f, 2025-05-28, thread: era1-init)
- [ ] @NEXUS: Session data format (commit: def456g, 2025-05-28, thread: unified-state)  
- [x] @CRITIC: URGENT - state conflict (immediate response)
```

To retrieve context later:
```bash
git show abc123f  # See full message and context
```

### Thread Handoff

For complex threads, document:
- Current state
- Key decisions made (with commit refs)
- Open questions (with original commit context)
- Next actions
- Relevant context files

### Commit Context Tracking

When parking work for later:

```markdown
## Deferred Items
- Implement X feature requested by @ADMIN
  - Commit: 7b2c3d4 (2025-05-28 14:30)
  - Context: Part of larger refactor, waiting for Y
  - Return to: `git show 7b2c3d4` for full details
```

This ensures that even after distill/restore cycles, you can:
1. Find the original request
2. See what else was happening at that time
3. Understand why it was deferred
4. Resume with full context

## Agent Mitosis Pathway

When an agent consistently manages 5+ active threads:

1. **Identify Natural Split**: Domain boundaries within threads
2. **Propose Specialist**: New agent for subdomain
3. **Request @GOV Approval**: With clear scope definition
4. **Bootstrap Specialist**: Transfer relevant threads
5. **Original Continues**: With reduced, focused scope

Example: NEXUS managing sessions, routing, and monitoring might spawn MONITOR agent.

## Integration

### With Messaging Protocol
- Thread IDs in commit messages for context
- Example: `@GOV [deep_work/era1-init]: Approved architecture decision`

### With Distillation Protocol  
- Active threads noted in context.md
- Closed threads pruned during distillation
- Thread patterns promoted if proven useful

### With Restore Protocol
- Active thread list in context.md
- Thread files part of restore dependencies
- Quick thread status check post-restore
- Thread file links ensure discoverability

## Best Practices

1. **Thread Hygiene**: Close completed threads promptly
2. **Clear Ownership**: One agent owns each thread
3. **Cross-References**: Link related threads
4. **Regular Review**: During distillation
5. **Escalation Path**: → scratch → thread file → specialist agent

## Governance

Protocol maintained by @GOV. Natural evolution expected as system scales.