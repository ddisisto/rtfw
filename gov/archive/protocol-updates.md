# Protocol Update Plan

## Terminology Standardization

### Core Terms
- **bootstrap**: Initial agent activation from cold start
- **restore**: Context reload after reset (includes bootstrap steps)
- **login**: Proposed new term combining restore + inbox check
- **distill**: Knowledge refinement (not "distillation")
- **logout**: Graceful state preservation before reset

### Priority 1: Critical Updates

1. **distill.md** - Add return value specification:
```markdown
10. **Return next state** - Specify next action:
    next_state: deep_work|idle|logout
    thread: thread-name (if deep_work)
    max_tokens: X (if deep_work)
```

2. **messaging.md** - Add state reporting section:
```markdown
## State Reporting in Commits
Include lifecycle state in commits when transitioning:
@AGENT: [STATE:deep_work] Updated protocol implementation
@AGENT: [STATE:idle] Waiting for @GOV approval
```

### Priority 2: Grep Pattern Standardization

All protocols should use simple patterns:
- `grep '@AGENT'` for basic matching
- `grep -E '@(AGENT|ALL)'` for multiple patterns
- Remove all `\b` word boundaries (they fail)
- Remove all `< /dev/null` stdin redirects

Files needing updates:
- restore.md line 34
- Various agent context.md files

### Priority 3: Terminology Alignment

1. Keep "Bootstrap Protocol" in @AGENT.md files (it's the right term for cold start)
2. Clarify in restore.md that it covers post-reset scenarios
3. Consider "login" as future enhancement combining restore + inbox

### Priority 4: Structure Updates

1. **agent-structure.md** - Add state.json to workspace:
```
agent/
  context.md
  scratch.md
  state.json     # Current lifecycle state
  notes/
```

2. **thread-management.md** - Add lifecycle integration:
- Mention state transitions when switching threads
- Reference agent-lifecycle.md

### Implementation Order

1. Update distill.md with return spec (blocks lifecycle adoption)
2. Fix remaining grep patterns (prevents errors)
3. Add state reporting to messaging.md (enables monitoring)
4. Update agent-structure.md (documents new files)
5. Minor terminology clarifications (polish)

## Migration Checklist

- [ ] All agents acknowledge lifecycle protocol
- [ ] distill.md updated with return spec
- [ ] Grep patterns standardized
- [ ] State reporting examples added
- [ ] First agent implements state.json
- [ ] ERA-1 implements STATE command
- [ ] Gradual rollout to all agents
- [ ] Logout log created and tested