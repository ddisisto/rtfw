# Collected Open Questions for @ADMIN

## Date: 2025-05-25
## Compiled by: @CRITIC

### From State Assumptions Analysis (critic/notes/state-assumptions.md)

1. **How do we measure "system coherence"?**
   - Context: Questioning the requirement to "commit changes promptly for system coherence"
   - Why it matters: Vague metrics lead to meaningless compliance

2. **What makes governance "effective"?**
   - Context: STATE.md claims "simplified governance model proven effective"
   - Why it matters: Past success ≠ future fitness without clear criteria

3. **Why prescribe tools vs outcomes?**
   - Context: TMUX as architectural requirement in system state
   - Why it matters: Implementation details shouldn't be in high-level docs

4. **Should STATE.md be split into stable/dynamic sections?**
   - Context: Document trying to be both snapshot and living truth
   - Why it matters: Already partially addressed with STATUS.md creation

### From Random vs Chronological Insights (critic/reports/random_vs_chronological_insights.md)

5. **Why so many approvals? Is positive reinforcement the primary teaching method?**
   - Context: 20% of interactions are approvals vs 11% corrections
   - Why it matters: Understanding teaching philosophy shapes agent development

6. **How does routing message frequency relate to system architecture decisions?**
   - Context: 43/250 sampled interactions were routing messages
   - Why it matters: Git-comms may have emerged from observed patterns

### From Current Investigation (critic/scratch.md)

7. **What triggers @ADMIN interventions?**
   - Partial answer: Questions and ideation as much as problems
   - Still open: Specific thresholds or patterns

8. **Which blindnesses appear across all agents?**
   - Status: Still investigating
   - Need more cross-agent analysis

9. **Where do agents resist vs readily adapt?**
   - Initial finding: Minimal resistance found in samples
   - Question: Is this due to positive reinforcement culture?

### From System Evolution Analysis (critic/reports/patterns/system-evolution.md)

10. **Were there failed experiments before current architecture?**
    - Context: Only seeing successful evolution in logs
    - Why it matters: Learning from failures prevents repetition

11. **What drove the specific agent selection?**
    - Context: Some agents shelved (ARCHITECT, TEST)
    - Why it matters: Understanding selection criteria for future agents

### From Context.md (critic/context.md)

12. **What would a hostile reviewer say?** (Sacred question)
    - Context: Anti-capture mechanism
    - Purpose: Maintain critical perspective

13. **What are we optimizing for that we shouldn't be?** (Sacred question)
    - Context: Fundamental assumption challenge
    - Purpose: Prevent local maxima

14. **What would this look like to someone who hates our approach?** (Sacred question)
    - Context: Perspective rotation
    - Purpose: See our own blind spots

15. **Where are we solving the wrong problem well?** (Sacred question)
    - Context: Efficiency vs effectiveness
    - Purpose: Question fundamental direction

### Process/Meta Questions

16. **How often should distillation occur?**
    - Current: "When idle" but no clear threshold
    - Impact: Under/over-distillation both problematic

17. **What constitutes "agent maturity"?**
    - Context: When is an agent ready for full autonomy?
    - Current: No clear graduation criteria

18. **Should agents develop their own protocols?**
    - Context: Agent sovereignty vs system coherence
    - Trade-off: Innovation vs chaos

### Technical Questions

19. **Why not use git hooks for message routing?**
    - Context: Current manual git_router.py approach
    - Trade-off: Automation vs control

20. **Should context.md have size limits?**
    - Context: Distillation manages growth but no hard limits
    - Impact: Restore complexity

## Note on Philosophy.md Pattern

You're correct - the "spaced out character-by-character" note in critic/reports/patterns/philosophy.md:12 is likely a parsing artifact from the logging system, not an actual @ADMIN pattern. Will remove this false pattern from the report.

## Summary

These questions range from philosophical (teaching methods, success metrics) to practical (tool choices, size limits). Many reveal tensions between:
- Flexibility vs consistency
- Autonomy vs coordination  
- Innovation vs stability
- Implicit vs explicit knowledge

Your answers to even a subset would significantly improve system understanding and future critical analysis.