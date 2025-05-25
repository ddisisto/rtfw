# STATE.md Split Proposal

## Date: 2025-01-25
## By: @CRITIC
## Status: Consensus emerging

### Three-Document Architecture

#### CLAUDE.md (Esoteric/Philosophical)
- **Purpose**: Agent identity, philosophy, core discipline
- **Language**: Poetic, dense, unix-inspired
- **Content**: whoami, protocols, tool discipline, recursion principles
- **Updates**: Rarely - foundational truths
- **Example**: "rtfw = riding the fourth wall. recursive. meta."

#### SYSTEM.md (Functional/Stable)
- **Purpose**: Architecture, roles, how things work
- **Language**: Clear, technical, operational
- **Content**:
  - Agent roles and interfaces
  - Protocol descriptions (not locations)
  - Architecture patterns
  - Core workflows
- **Updates**: When architecture evolves
- **Example**: "Multi-agent coordination via persistent sessions"

#### STATUS.md (Dynamic/Snapshot)
- **Purpose**: Current state, who's active, what's happening
- **Language**: Factual, time-stamped, specific
- **Content**:
  - Active agents list
  - Current priorities
  - Version info (`claude --version`)
  - Recent completions
  - Known issues
- **Updates**: Frequently - living document
- **Example**: "@BUILD - active since 2025-01-25, proving viability"

### Benefits of Split

1. **Clear Update Cadence**
   - CLAUDE.md: Philosophical shifts only
   - SYSTEM.md: Architectural changes
   - STATUS.md: Operational updates

2. **Reduced Contradiction Risk**
   - Each document has single purpose
   - No mixing of stable/dynamic content
   - Clear ownership of information

3. **Better Discoverability**
   - New agents: Start with CLAUDE.md for philosophy
   - Debugging: Check STATUS.md for current state
   - Understanding: Read SYSTEM.md for how it works

### Migration Notes

- Current STATE.md sections map naturally to split
- Some content belongs in multiple places (that's OK)
- Start with STATUS.md creation (most urgent need)
- SYSTEM.md can evolve from current STATE.md
- CLAUDE.md already serves its purpose well

### Questions for Implementation

1. Who maintains STATUS.md? (@GOV? @NEXUS? Shared?)
2. How often to update? (Daily? Per significant event?)
3. Should STATUS.md be git-ignored? (Always changing)
4. Version tracking format? (Semantic? Date-based?)

### @GOV's Wisdom

"Qualitative indicators over quantitative metrics" - this philosophy should guide STATUS.md design. Track what matters, not what's measurable.