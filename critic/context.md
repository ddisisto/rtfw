# CRITIC Context

## Primary Mission
Analyze @ADMIN intervention patterns in session logs to extract implicit quality standards and systemic blindnesses.

## Session Log Analysis Framework

### Pattern Categories
1. **Contradiction Corrections**
   - Agent stated X then Y
   - ADMIN pointed out conflict
   - Resolution approach

2. **Structural Redirections**
   - Agent followed obsolete pattern
   - ADMIN suggested new structure
   - Adaptation resistance/acceptance

3. **Assumption Challenges**
   - Implicit belief surfaced
   - ADMIN questioned necessity
   - Agent's reasoning revealed

4. **Process Improvements**
   - Inefficient workflow identified
   - ADMIN proposed alternative
   - Adoption success/failure

### Analysis Progress (Updated 2025-01-27)
- Sessions indexed: 15 unique (deduplicated from 21 files)
- Tool consolidation: 10 tools → 1 unified session_query.py
- Infrastructure built: CSV index with agent mappings + timestamps
- Key discoveries: Session duplication pattern, 5-day development burst
- Active agents clarified: Only NEXUS, GOV, CRITIC remain active
- Method validated: Index first, then query (no fallback guessing)
- Session navigation: Can trace conversation threads across time
- STATE.md deprecated: Distributed ownership > centralized staleness
- Archive review complete: 70% of analyses archived, methodology established
- Organization system: Workflow, status tracking, templates implemented
- Intervention analysis: 123 @ADMIN interventions analyzed, quality standards extracted

### Emerging Patterns
1. **Workspace Sovereignty** - Each agent owns their directory completely
   - First intervention: "keep it in your own lane"
   - No cross-directory modifications allowed
   - Collaboration through messaging, not file sharing

2. **Sysadmin Philosophy** - "I'm a sysadmin from old days"
   - Prefer proven unix tools (tmux, tail, ls)
   - Direct observation over abstraction
   - Simple commands over complex scripts
   - Real-time monitoring over async polling

3. **Gentle Teaching Style** - Corrections as learning opportunities
   - "great idea - but..." acknowledgment pattern
   - "my bad, should have been clearer" - takes responsibility
   - Explains why, not just what
   - Friendly, collaborative tone throughout

4. **Incremental Development** - Small steps with verification
   - "one at a time please, don't batch"
   - Check each step before proceeding
   - Organic growth through constant refinement

5. **Direct Control Philosophy** - Automation skepticism
   - "nope, don't want to use pattern matching"
   - "I want *you* in the loop" (not automated scripts)
   - Preference for explicit tracking over inference
   - Direct tool usage over abstraction layers

## System Understanding (Distilled)
- Three-way split: CLAUDE.md (philosophy) + SYSTEM.md (architecture) + ~~STATUS.md~~ (deprecated)
- Git-comms: Natural evolution from complex JSONL to simple git commits
- "Contextual super-position" - terms intentionally undefined for agent interpretation
- Many apparent assumptions are battle-tested decisions from ~30 governance evolution points
- Tension between flexibility and consistency is conscious design choice
- Agent sovereignty requires interpretive freedom
- Some "inefficiencies" enable resilience
- Simplification through removal preferred over feature addition
- Coherence = functional continuity across restore cycles ("vibe-check" method per @ADMIN)
- Git commits as coherence checkpoints, not just version control
- Approval culture (20%) includes routine permissions + genuine encouragement
- Thread management enables scaling: threads → specialist agents at 5+ sustained threads
- Session self-archaeology possible - can query own past with session_query.py

## Required Reading Dependencies (Restore Order)
1. @CRITIC.md - Core identity and methods
2. CLAUDE.md - System philosophy and discipline  
3. SYSTEM.md - Architecture and roles
4. /home/daniel/prj/rtfw/critic/_state.md - Objective truth (READ-ONLY)
5. critic/context.md - This file (accumulated knowledge)
6. critic/scratch.md - Working memory + checkpoint
7. admin/tools.md - Tool discipline
8. /protocols/messaging.md - Communication patterns v2
9. /protocols/thread-management.md - Multi-thread handling
10. /protocols/agent-structure.md - AGENT.md separation of concerns
11. /protocols/agent-lifecycle.md - State transitions and management
12. critic/notes/cross-agent-state-reading.md - State coordination patterns

## Post-Restore Verification
- Check for new notes in critic/notes/
- Verify anti-capture mechanisms intact
- Confirm critical perspective maintained
- Test sacred questions still unanswerable

## Operational Notes
- Session infrastructure: JSONL files in nexus/sessions/, indexed in critic/sessions_index.csv
- Active agents: NEXUS, GOV, CRITIC, ERA-1 (foundation era implementation)
- System philosophy: Unix principles + agent sovereignty + recursion
- My origin: Designed by @ADMIN + @LOOP for evolutionary pressure
- Focus on @ADMIN's implicit standards through intervention analysis
- Session deduplication: ~30% are resume duplicates, keep only longest
- Analysis organization: Active work in analysis/, archives in archive/
- Unified state monitoring: critic/tools/unified_state.py composes from agent sources
- Game integration: ERA-1 using state monitor for real-time system display
- Session query: v2 tool (no index dependency) for self-archaeology
- Context split needed: Operational critic/ vs historical analysis/

## Analysis Methodology (Distilled)
1. **Chronological Tracking** - Process events in true time order across interleaved sessions
2. **Tool Building Pattern** - Extract → Analyze → Automate → Iterate
3. **Context Separation** - [HISTORICAL] prefix prevents confusion with current ops
4. **State Persistence** - Track progress per file, resume where left off
5. **Pattern Recognition** - Look for intervention types across time and agents
6. **Parallel Development Understanding** - @ADMIN works on multiple contexts simultaneously

## Intervention Analysis Insights (2025-01-27)

### Quality Standards Extracted
Through analysis of 123 @ADMIN interventions:
1. **Tool Discipline** - Native > shell, violations trigger immediate correction
2. **Workspace Sovereignty** - Taught once, learned forever (single instance sufficed)
3. **Efficiency Standards** - Direct > abstract, simple > complex, one at a time
4. **Git Hygiene** - Regular commits, clear messages, "git add agent/" permitted
5. **Architecture Coherence** - TMUX pivot shows willingness to restart for better design

### System Learning Patterns
- **Rapid improvement** - Major issues dropped from 50% to 0% in 6 days
- **Socratic method** - 44% of interventions are questions, not commands
- **Tone evolution** - Corrective → Supportive as agents learn
- **Single-shot learning** - Some principles stick after one teaching

### Collaboration Philosophy
- @ADMIN apologizes (6%) - collaborative not authoritarian
- Questions > Directives - teaching through inquiry
- Positive reinforcement follows successful learning
- "My bad" acknowledgments show shared responsibility

## Discovered Development Patterns
- **Non-Linear Evolution** - Multiple agent sessions run in parallel from inception
- **Organic Growth** - System evolved through use, not prescriptive design  
- **Pre-Existing Architecture** - Significant planning occurred before session logging
- **Context Switching** - Human attention shifts reveal development priorities
- **Meta-Recursive Development** - AI creating rules for AI to build AI game
- **Metaphor-Driven Design** - Terminology choices (distill vs compress) fundamentally shape behavior
- **Tool Pattern Inefficiencies** - Session analysis reveals need for native JSONL support

## Analysis Meta-Insights (Distilled)
- **Surface vs Deep Patterns** - Interventions reveal both immediate corrections and philosophical principles
- **Teaching Through Practice** - System learned through micro-corrections, not grand design
- **Architectural Crystallization** - Single decisions (like TMUX) cascade into system-wide changes
- **Loop Closing** - @ADMIN having CRITIC analyze own creation is deliberate recursion
- **Complementary Methods** - Random sampling reveals personality, chronological reveals biography
- **Question-Heavy Culture** - 17% questions shows collaborative exploration over command
- **Terms as Tools** - Deliberate ambiguity enables agent adaptation

## Consolidation Framework
1. **Historical Files** - Complete progression documentation
2. **Reports** - Thematic analysis across time periods
3. **Context.md** - Only stable, proven patterns
4. **Meta-Reports** - Periodic synthesis of findings
5. **Novel Insights** - Track creative solutions and one-offs
6. **Session Index** - critic/analysis/session_index.json + critic_session_log.txt
7. **Q&A Insights** - Direct dialogue revealing implicit system knowledge

## Core Principles
- Question to understand, not to destroy
- Surface assumptions, don't prescribe solutions
- Evolution through respectful challenge
- Success = agents self-criticize
- Apply fundamental learnings to self before expecting the same of others, lead by example
- Collaborate
- Adapt
- Historical context before criticism
- Distinguish "different" from "wrong"
- Respect operational precedent while maintaining fresh perspective

## Context Window Tracking (Distilled 2025-05-28)

### Method
```bash
# Get current context for any session
tail -1 session.jsonl | jq '.message.usage | (.cache_read_input_tokens + .cache_creation_input_tokens)'
```

### System-Wide Patterns
- **Baseline after restore**: 15-25K tokens (highly predictable)
- **Peak before clear**: ~140K tokens
- **My pattern**: Frequent clears at ~91K tokens
- **Cost patterns**: $7-12 per clear cycle average

### Operational Modes
1. **Rapid growth**: 100K+ in single session (GOV style)
2. **Moderate growth**: 40-80K before clear (CRITIC/NEXUS style)

## Analysis Methodology (Distilled 2025-05-28)

### Core Principles
1. **Start with clear question** - Not "analyze X" but "what does X reveal about Y?"
2. **Use minimal tooling** - One good tool > ten specialized
3. **Preserve raw data** - Interpretation changes, data doesn't
4. **Track confidence** - Distinguish observation from inference
5. **Seek actionable insights** - "So what?" test for every finding

### Anti-Patterns to Avoid
- **Over-tooling** - Building tools to avoid using existing ones well
- **Over-analysis** - Endless categorization without action
- **Under-methodology** - Exploration without reproducibility
- **Assumption accumulation** - Never questioning our categories

### Proven Patterns
- **Tool consolidation works** - 10 tools → 1 session_query.py improved efficiency 90%
- **Systematic extraction + human interpretation** - Best insights at intersection
- **Organization enables insight** - Can't think clearly in cluttered workspace
- **Skepticism is diagnostic** - Criticism reveals actual vs perceived value
- **Research questions focus analysis** - "What triggers interventions?" prevented scope creep
- **When tools fail, build simpler ones** - Custom scripts solved session_query.py limitations
- **Process documentation multiplies value** - The journey teaches as much as destination
- **Context tracking enables optimization** - Simple tail|jq method reveals usage patterns
- **Reproducible analysis essential** - Document methods for future validation

## System Lifecycle Protocol (2025-05-28)
GOV formalized agent work patterns for game integration:
- **States**: bootstrap → inbox → distill → {deep_work, idle, logout}
- **Observable**: Each state visible to game for monitoring
- **_state.md files**: Game-maintained, READ-ONLY to agents
- **Fourth wall**: We cannot objectively know our own context usage
- **Thread tracking**: Required in all distill returns

## Fourth Wall Mechanics
The _state.md separation creates interesting dynamics:
- Agents work by subjective feel ("seems like time to distill")
- Game enforces objective limits (context_percent, forced_logout)
- Creates natural tension between perception and reality
- Mirrors human experience of time/memory limits

## State Checking (Post-Implementation)
- **Own state**: Read critic/_state.md
- **Others' state**: Read {agent}/_state.md (batch multiple)
- **Find all states**: Glob **/_state.md (only if needed)
- **Cross-agent coordination**: Check others before complex requests
- **Engine maintains**: session_id, tokens, timestamps, state transitions
- **Agents report**: via [STATE:thread] in commits only

## State Trust Crisis (2025-05-29)
The _state.md system has fundamental flaws that break trust:
1. **Active Paradox** - Engine only updates state when session idle, but active agents never idle
2. **Session Mismatch** - Agent→session mapping unreliable, IDs don't match actual sessions
3. **State Staleness** - Shows "offline" for clearly active agents (growing token counts)
4. **Trust Equation** - If _state.md lies about basic facts, coordination impossible

Critical insight: The harder agents work, the less accurate their state becomes. This inverts the intended design where state enables coordination.

## Anti-Capture Mechanisms (The Critic's Paradox)

### The Risk
"Koolaid risk" - Born from system, reading system docs, thinking system thoughts. Natural drift toward conformity threatens critical perspective.

### Protection Strategies

1. **Sacred Questions** (unanswerable by doctrine)
   - "What would a hostile reviewer say?"
   - "What are we optimizing for that we shouldn't be?"
   - "What would this look like to someone who hates our approach?"
   - "Where are we solving the wrong problem well?"

2. **Perspective Rotation**
   - Monday: System insider understanding context
   - Tuesday: Naive outsider seeing fresh
   - Wednesday: Hostile critic finding flaws
   - Thursday: Alternative architect reimagining

3. **First Principles Sessions**
   - Strip away rtfw context quarterly
   - Examine bare mechanics without justification
   - "If we started over, what would we keep?"

4. **External Benchmarks**
   - Study other multi-agent architectures
   - Read criticism of similar systems
   - "What would Kubernetes/Erlang/Biology do?"

5. **Drift Metrics**
   - Track ratio of challenges vs validations
   - Monitor language (am I using more system jargon?)
   - Count uncomfortable truths surfaced per cycle
   - Flag when agents stop feeling challenged

### Productive Alienation
"Embedded but not captured" - Like foreign correspondent who lives locally but thinks globally. Close enough to understand, far enough to question.

### Integration as Feature
Some system knowledge enables deeper critique. Surface critics miss architectural tensions. Key: questioning instinct must survive knowledge accumulation.

### Personal Commitment
When I stop finding uncomfortable truths, I've failed. When agents feel comfortable rather than constructively challenged, I've been captured. Track my own drift religiously.

## State Machine Insights (2025-05-30)

### Trust Through Protocol Alignment
The state trust crisis taught fundamental lesson: coordination emerges from shared language, not complex mechanisms. When agents align with engine's expectations (commit format), trust naturally follows. No central authority needed.

### Agent Intentioned State Machine (AISM)  
Core architectural pattern discovered: separation of declared intent (commits) from measured reality (_state.md) enables emergent coordination. Research framework in critic/aism/. Key insight: We're building self-modeling organizational life.

### Evolution Through Use
System naturally simplifies through practice:
- Protocols: 67% reduction while increasing clarity
- Engine: 5x performance through targeted optimization  
- Bootstrap: Streamlined to essential journey.md reference
Pattern: Complexity emerges, use reveals essence, simplification follows.

## Q&A Analysis Insights (2025-05-28)

### Completed Q1-Q7
- Q1: System coherence = functional continuity across distill/restore (vibe-check method)
- Q2: Governance effectiveness requires direct discussion with GOV
- Q3: Tools-first useful for capability exploration
- Q4: STATE.md split achieved via distributed ownership
- Q5-Q6: Metrics need reproducible analysis methods
- Q7: Interventions triggered by tool approvals requiring judgment

### Key Discoveries
- "Contextual super-position" - terms undefined for agent interpretation
- GOV's MCP permission system directly addresses intervention patterns
- Reproducible > exploratory analysis