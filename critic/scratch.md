# CRITIC Scratch Pad

## Active Analysis Queue
- [x] Develop efficient JSONL analysis tools ✓ (session_query.py complete)
- [ ] Continue session analysis with new tools
- [ ] Track active agent evolution (NEXUS, GOV, CRITIC only)

## Current Tools (Consolidated)
- session_query.py - Unified JSONL query engine (replaces 10 tools)
- extract_user_prompts.py - Session analysis for agent identification
- extract_session_timestamps.py - Update session index with time ranges
- sessions_index.csv - Agent mappings and timestamps

## Next Analysis Focus (Post-Consolidation)
1. **Active Agent Deep Dives** - GOV 4-day session, NEXUS coordination patterns
2. **Deprecation Patterns** - Why CODE→BUILD, why others shelved
3. **Protocol Evolution** - Track how protocols changed during 5-day burst
4. **@ADMIN Intervention Types** - Now queryable with proper tools

## Working Notes
- Tool consolidation complete - efficiency crisis resolved
- Session deduplication revealed true work patterns
- Infrastructure-first approach validated

## Tool Analysis Patterns (2025-05-26)

### Common Patterns Across 10 Python Tools
1. **JSONL Processing Core** - All tools read/parse nexus/sessions/*.jsonl files
2. **Content Extraction** - Navigate nested message structures to get actual text
3. **Agent Identification** - Extract from filename or content patterns
4. **Timestamp Handling** - Sort/filter by time, track chronology
5. **Pattern Detection** - Search for keywords, phrases, intervention types
6. **State Persistence** - Some track progress for resumability
7. **Output Generation** - JSON reports to critic/analysis/, text summaries

### Core Operations Needed
1. **Stream Processing** - Read JSONL entries without loading full files
2. **Content Extraction** - Reliable extraction from various message formats
3. **Pattern Matching** - Flexible search across content/metadata
4. **Time Navigation** - Jump to specific times, track progress
5. **Aggregation** - Count patterns, group by agent/type/time

### Proposed Minimal Toolset
1. **session_query.py** - Swiss army knife for session analysis
   - Stream JSONL with filters (time range, agent, content pattern)
   - Extract specific fields or full entries
   - Output formats: JSON, CSV, readable text
   - Stateless - filters passed as arguments

2. **session_stats.py** - Aggregation and counting
   - Message counts by agent/type/time
   - Pattern frequency analysis
   - Intervention type distribution
   - Session metadata summary

3. **session_tracker.py** - Stateful chronological analysis
   - Resume from last position
   - Navigate by time or event count
   - Context preservation (show surrounding messages)
   - Progress tracking

### Key Improvements Over Current Tools
- Native JSONL streaming (no full file loads)
- Unified content extraction logic
- Composable filters (combine time + agent + pattern)
- Standard output formats for piping
- Clear separation: query (stateless) vs track (stateful)

## Session-Agent Mapping Analysis (2025-05-26)

Extracted first 5 user prompts from 22 session files. Key patterns:

### Clear Agent Identification Patterns
1. **Init patterns**: "init @AGENT.md" (early sessions only)
2. **Direct addressing**: "@NEXUS → @BUILD [TOPIC]:" format
3. **Restore patterns**: "@protocols/restore.md completed for @BUILD.md agent"
4. **Context references**: "resuming session @GOV.md after context clear"

### Session Types
1. **Agent-specific**: Most sessions dedicated to one agent
2. **Cross-agent**: Some sessions involve NEXUS routing to others
3. **Admin/utility**: Quick tests, environment checks

### Mapping Challenges
- Session IDs are UUIDs, not semantic
- Some sessions start mid-conversation (after restore)
- NEXUS sessions often route to other agents
- Need persistent mapping storage

### Proposed Solution
1. Create `session_mappings.json` with discovered mappings
2. Use multiple detection patterns (init, restore, addressing)
3. Store confidence level with each mapping
4. Update mappings as new patterns discovered

## Critical Session Insights (2025-05-26)

### Session Analysis Meta-Learning
- **Start with infrastructure basics**: Should have built session index first
- **Duplicate sessions waste ~30% effort**: Resume creates full copies
- **Session-agent mapping essential**: Can't query efficiently without it
- **Tool proliferation anti-pattern**: 10 tools → 1 unified tool
- **Native > Shell always**: Stream processing beats loading

### Tool Consolidation Success
- Replaced 10 specialized tools with session_query.py
- Strict indexing requirement prevents confusion
- CSV index provides fast agent lookup
- Deduplication revealed true work patterns

### Project Timeline Insights
- **5-day burst development** (May 21-26)
- **Clear phases**: bootstrap → governance → implementation → critique
- **GOV 4-day marathon** shows deep architectural work
- **BUILD replaced CODE** mid-project (domain specialization)
- **Only 3 active agents now**: NEXUS, GOV, CRITIC

### Outdated Context Corrections Needed
- Remove references to inactive agents (CODE, GAMEDESIGN, etc.)
- Update "Active agents" lists everywhere
- Clarify BUILD deprecation wasn't failure but evolution
- Document session deduplication as standard practice