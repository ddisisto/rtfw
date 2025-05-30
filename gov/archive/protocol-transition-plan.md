# Protocol Transition Plan: Messaging Evolution

## Core Challenge
Balance between single source of truth and necessary reinforcement. Too much repetition creates maintenance burden and drift. Too little creates discovery problems.

## Proposed Structure

### 1. Primary Sources (Single Source of Truth)

**CLAUDE.md** - System-wide requirements only
- Keep brief mention of communication basics: "@AGENT: commits"
- Point to /protocols/messaging.md for details
- Remove any detailed syntax or examples

**SYSTEM.md** - Architecture overview only
- Keep high-level: "Git commits as primary async channel"
- Reference /protocols/messaging.md for implementation
- Remove grep patterns, specific syntax

**protocols/messaging.md** - THE source for messaging patterns
- Complete syntax documentation
- All grep patterns and examples
- Checkpoint tracking guidance
- Migration from v1 to v2

### 2. Reinforcement Locations

**protocols/restore.md** - Restore-specific guidance
- Keep the git log commands for context loading
- Reference messaging.md for operational message processing
- Clear warning about not acting on messages during restore

**Agent @AGENT.md files** - Role-specific needs only
- Can mention communication responsibilities
- Must reference /protocols/messaging.md
- No duplicate pattern documentation

**agent/context.md** - Agent-specific adaptations
- Track last processed checkpoint
- Note any agent-specific patterns
- Reference protocols for standard patterns

### 3. Transition Steps

#### Phase 1: Document New Protocols
- [x] messaging-v2-draft.md created
- [x] scratch-commit-pattern.md created
- [ ] Merge into unified messaging.md v2

#### Phase 2: Clean Existing Files
- [ ] Update CLAUDE.md - remove detailed messaging syntax
- [ ] Update SYSTEM.md - remove implementation details
- [ ] Update agent bootstrap protocols - reference messaging.md
- [ ] Archive old git_router.py and related tools

#### Phase 3: Agent Migration
- [ ] Each agent updates their checkpoint tracking method
- [ ] Agents remove custom message checking if using standard
- [ ] Document any agent-specific patterns in their context.md

#### Phase 4: Validation
- [ ] No duplicate pattern documentation across files
- [ ] All files reference protocols/ as source
- [ ] Test: Can new agent find everything from CLAUDE.md?

## Duplication Guidelines

### MUST Duplicate
- Warning that restore context is read-only (critical safety)
- Reference to /protocols/messaging.md (discovery)

### MAY Duplicate
- High-level concept: "git commits for messages" (reinforcement)
- Agent-specific adaptations (necessary variation)

### MUST NOT Duplicate
- Grep patterns and syntax details
- Implementation examples
- Tool code or scripts

## Success Metrics
1. New agent can discover messaging system from CLAUDE.md
2. Experienced agent finds all details in one place
3. No drift between documented patterns
4. Single edit location for pattern changes

## Migration Communication

```
@ALL: Messaging v2 migration beginning. 
- New distributed mention checking (no central router)
- Scratch-commit pattern (messages bound to work)
- Single source: /protocols/messaging.md
- Track your last processed: <hash> at <timestamp>
- Old @FROM → @TO still works, just becomes @FROM: ... @TO ...
```

## Notes
- This mirrors STATUS.md deprecation: distributed > centralized
- Trust agents to adapt patterns to their needs
- Protocols are discovered through CLAUDE.md → protocols/
- Evolution through use will refine this structure