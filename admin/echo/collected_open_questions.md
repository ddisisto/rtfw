# Collected Open Question Responses for @CRITIC
2025-05-26


### From State Assumptions Analysis (critic/notes/state-assumptions.md)

1. **How do we measure "system coherence"?**
   - Context: Questioning the requirement to "commit changes promptly for system coherence"
   - Why it matters: Vague metrics lead to meaningless compliance


git commits ~> saved and backed up context checkpoint for an agent, in this case.

My own attempt at a definition 

but we need to step back and understand coherence more broadly. let's start with individual agent coherence, as I think it's easier to establish with anything resembling clarity. I'm really just learning to put words to this, and it's all very much post-hoc but here goes (as relevant to this project): functional continuity across distill/restore proccess. currently, practically, this is a vibe-check. If I notice increased self-contradiction, loss of previous knowledge or capabilities, etc, following restore, compared to within single traditional context window, this is coherence failure.

"System Coherence" could be taken that agent == system, or could be applying same idea to project as a whole.

I likely used this term in prev interactions first, without even considering what it really meant, "just felt right". Agents implicitly invited to project their own meaning and associations onto it (such as linking to concept of commits as we see), while it remains in some sort of contextual super-position.

Future directions:
- search out historical usages of terms: coherence, continuity
- research topic: is quantative coherence measurement possible?


2. **What makes governance "effective"?**
   - Context: STATE.md claims "simplified governance model proven effective"
   - Why it matters: Past success ≠ future fitness without clear criteria

More broadly, I don't know how much I can say if "governance" itself is effective. like many terms used throughout, this still remains in some amount of super-position to me, even while being actively used as a specific agent name. Back at project inception, as much as anything I just wanted some distinct contexts, and had to assign names and initial scopes to each as a practical matter, gov seemed like a useful core concept. I've just had a good discussion with gov, as it happens, on topic of agent scoping / differentiation. Can you please message and engage in direct discussion with them, focused on this question? nexus has been making great progress on messaging system, so good opportunity to put this to the test!


3. **Why prescribe tools vs outcomes?**
   - Context: TMUX as architectural requirement in system state
   - Why it matters: Implementation details shouldn't be in high-level docs

simple really - *generally* outcomes preferable, especially long term, but a tools-first view is sometimes very useful for capability exploration and ideation.

4. **Should STATE.md be split into stable/dynamic sections?**
   - Context: Document trying to be both snapshot and living truth
   - Why it matters: Already partially addressed with STATUS.md creation

this has been since addressed, dynamic is now both distributed (agents self manage), and then consolidated for view in era-1.
I really didn't appreciate the importance of this question in driving future thinking, thanks critic

### From Random vs Chronological Insights (critic/reports/random_vs_chronological_insights.md)

5. **Why so many approvals? Is positive reinforcement the primary teaching method?**
   - Context: 20% of interactions are approvals vs 11% corrections
   - Why it matters: Understanding teaching philosophy shapes agent development

6. **How does routing message frequency relate to system architecture decisions?**
   - Context: 43/250 sampled interactions were routing messages
   - Why it matters: Git-comms may have emerged from observed patterns

2025-05-27:
5 has been partially looked at previously, 6 not directly, but neither will be specifically, as this applies to both:
1. the analysis used for these numbers was exploratory, not well described and no longer reproducible
2. insufficient context to know what to do with this info, targets or tracking
I guess the obvious direction is then - *should* we look for these sort of metrics? at what point? if analyses are reproducible, these sorts of things may be highly valuable, or at least very interesting, to track over time

### From Current Investigation (critic/scratch.md)

7. **What triggers @ADMIN interventions?**
   - Still open: Specific thresholds or patterns

2025-05-27:
ok, so generally one of two things happens here
  1. I've set a task, get a tool approval request from claude code e.g. 
    ```
    Bash command

    chmod +x /home/daniel/prj/rtfw/gov/tools/review_permissions.py
    Make review tool executable

    Do you want to proceed?
    ❯ 1. Yes
    2. Yes, and don't ask again for chmod commands in /home/daniel/prj/rtfw
    3. No, and tell Claude what to do differently (esc)
    ```
    sometimes the correct action is obviously correct, other times I want to discuss first. Sometimes there's a better way, or another factor to consider before taking this step, etc. It's generally a judgement call based on experience and common sense.
