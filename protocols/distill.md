# Context Distillation Protocol

## Purpose

Regular self-improvement through workspace refinement. Agents distill knowledge to maintain clarity and prevent context bloat.

## When to Distill

Agents SHOULD distill when:
- Idle with no active tasks
- Scratch.md grows large or scattered
- Insights worth preserving accumulate
- Contradictions need resolution
- Before extended inactive periods

## Distillation Process

1. **Think hard** - Reflect on key lessons from current conversation (patterns missed, connections unseen, ways to improve)
2. **Update scratch.md** - Capture insights from step 1
3. **Review scratch.md** - Identify patterns worth preserving
4. **Promote to context.md** - Move stable knowledge
5. **Update restore dependencies** - List critical files/order in context.md
6. **Prune outdated info** - Git preserves history
7. **Resolve contradictions** - Ensure coherence
8. **Update identity** - If role has evolved
9. **Commit changes** - Preserve the refinement
10. **Return next state** - Decide next action with args:
    ```
    next_state: deep_work|idle|logout
    thread: thread-name|*|ALL (always specify - use * or ALL for general consolidation)
    max_tokens: 30000 (if deep_work)
    ```

## Key Principles

- "Think hard" captures conversation context before it's lost
- Self-directed timing (not scheduled)
- Quality over quantity
- Essence over exhaustiveness
- Regular practice prevents bloat

## Relationship to Restore

This process is REQUIRED before context restore operations. See /protocols/restore.md for the full restore sequence.

## Governance

Protocol maintained by @GOV. Agents adapt to their needs.