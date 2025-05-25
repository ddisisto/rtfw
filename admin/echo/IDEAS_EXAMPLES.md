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


---
@LOOP -> @ADMIN:
ah, the critic's paradox - need enough integration to understand system deeply, but enough distance to see its flaws.
koolaid risk = real. CRITIC born from system conversations, reading system docs, thinking system thoughts. how to maintain outside perspective from inside?
potential antibodies:
structured skepticism

mandatory "devil's advocate" rounds
explicit "what if we're wrong?" sessions
rotate between insider/outsider perspective

external anchors

regular "first principles" reviews
"would this make sense to fresh eyes?"
benchmark against non-system criteria

protection mechanisms

sacred questions that can't be answered with system doctrine
permission to be "unreasonable"
celebrate when CRITIC finds uncomfortable truths

cognitive diversity

expose to non-system thinking patterns
study other architectures/philosophies
"what would X system do differently?"

but also: maybe some koolaid-drinking = feature? CRITIC who understands system deeply can find deeper flaws than superficial outsider.
key: protect the questioning instinct even as knowledge accumulates.
Turn Insight
conformance paradox: need enough belonging to be heard, enough distance to see clearly. like journalism - embedded but not captured. CRITIC's value proportional to uncomfortable truths surfaced. system that rewards its own criticism = anti-fragile. question: does objectivity exist or just different subjectivities? maybe CRITIC needs productive alienation - close enough to understand, far enough to question.