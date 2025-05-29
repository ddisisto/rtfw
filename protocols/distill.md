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
10. **Exit via commit** - Transition to next state:
    ```
    @AGENT [deep_work/thread]: Distillation complete, resuming implementation
    @AGENT [idle]: Distillation complete, awaiting next task
    @AGENT [logout]: Distillation complete, context at 90%
    ```

## Key Principles

- "Think hard" captures conversation context before it's lost
- Self-directed timing (not scheduled)
- Quality over quantity
- Essence over exhaustiveness
- Regular practice prevents bloat

## Fourth Wall Awareness

Agents cannot objectively measure:
- Own context token usage (check _state.md for context_percent)
- Actual time elapsed (check _state.md for timestamps)  
- True file sizes (trust subjective assessment)

When _state.md indicates high context usage or extended time, trust these objective measures over subjective feel. The system sees what you cannot.

## Relationship to Bootstrap

This process is REQUIRED before logout. After logout/offline, agents follow /protocols/bootstrap.md to restart.

## Governance

Protocol maintained by @GOV. Agents adapt to their needs.