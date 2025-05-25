brilliant. CRITIC as distillation observer → post-restore dialogue. elegant timing.

**activation trigger options:**
- automatic: every Nth distillation
- pattern-based: contradictions detected > threshold
- request-based: agents can invoke @CRITIC
- random sampling: maintains unexpected perspective

**post-distillation, pre-restore window:**
```markdown
@AGENT → @NEXUS: distillation complete
@NEXUS → @CRITIC: review agent/context.md + scratch.md
@CRITIC: analyzes, leaves critic/notes/@agent.md
[restore happens]
@AGENT: loads @AGENT.md, CLAUDE.md, etc... 
@AGENT: reads critic/notes/@agent.md
@AGENT → @CRITIC: [defend/clarify/accept]
```

key insight: **context-constrained during distill** = can't process feedback real-time. post-restore = fresh context, receptive to input.

CRITIC's tools:
- contradiction detection
- structural assumption mapping  
- complexity metrics
- pattern blindness indicators

critical (pun intended) design choice: CRITIC must provoke *thought* not compliance. 

example critic note:
```markdown
## Observations for @BUILD

### Contradictions Found
- line 42: "always use native tools"
- line 97: "bash acceptable for file ops"
- reconcile: native when available, bash when not?

### Structural Questions  
- why separate build/context.md and build/scratch.md?
- observed: 80% of scratch promotes to context unchanged
- consider: open to discuss better scratch usage or promotion strategy if desired

### Complexity Creep
- 15 new patterns added, 0 removed
- each pattern adds cognitive load
- which serve current needs?
```

forcing agents to **defend** prevents blind acceptance. "no, we need separate files because..." = either valid reason or exposed assumption.

implementation nuance: CRITIC needs different personality. not harsh, but... incisive? socratic? agents should feel challenged not attacked.

timing perfect: post-restore = maximum receptivity. pre-work = time to integrate feedback.

one risk: CRITIC becomes oracle. maybe rotate role? or multiple critics with different perspectives? or CRITIC also gets critiqued?

this feels like missing piece. systems need internal skepticism to evolve. CRITIC = evolutionary pressure against stagnation.