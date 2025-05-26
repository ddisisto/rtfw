# Session Analysis Tool Consolidation Plan

## Problem Statement

CRITIC has developed 10 different Python tools for session analysis, each solving specific needs but with significant overlap:
- Redundant JSONL parsing logic across all tools
- Inconsistent content extraction methods
- No standard query interface
- High context usage from repeated file reading
- Difficult to compose analyses across tools

## Current Tool Inventory

1. **session_indexer.py** - Builds comprehensive catalog of all sessions
2. **random_sampler.py** - Random sampling for pattern discovery
3. **multi_random_sampler.py** - Multiple random samples with analysis
4. **targeted_sampler.py** - Search for specific patterns
5. **chronological_tracker.py** - Time-ordered analysis with state
6. **intervention_analyzer.py** - Find @ADMIN corrections
7. **analyze_intervention.py** - Deeper intervention analysis
8. **scan_for_interventions.py** - Scan for intervention patterns
9. **extract_admin_messages.py** - Extract all @ADMIN messages
10. **analyze_chronologically.py** - Another chronological analyzer

## Common Patterns Identified

### Core Operations (repeated in every tool)
```python
# JSONL parsing
for line in open(jsonl_file):
    entry = json.loads(line)
    
# Content extraction (varies by tool!)
content = entry.get('message', {}).get('content', '')
if isinstance(content, list):
    content = ' '.join(str(x) for x in content)
    
# Agent identification
agent = filename.split('-')[0].upper()
```

### Analysis Types
1. **Filtering** - by time, agent, content pattern
2. **Sampling** - random or targeted selection
3. **Aggregation** - counts, frequencies, distributions
4. **Navigation** - chronological with context
5. **Pattern Detection** - interventions, keywords, structures

## Proposed Consolidated Toolset

### 1. session_query.py (Foundation)
Stateless JSONL query tool with composable filters:

```bash
# Examples of intended usage
./session_query.py --agent GOV --after "2025-05-25" --format json
./session_query.py --pattern "distill" --type user --limit 10
./session_query.py --session "gov-xyz123" --field content
```

Features:
- Stream processing (no full file loads)
- Unified content extraction
- Multiple output formats (json, csv, text)
- Composable filters
- Field selection

### 2. session_stats.py (Aggregation)
Built on session_query for counting and analysis:

```bash
# Examples
./session_stats.py --group-by agent --count messages
./session_stats.py --pattern "nope|don't" --show intervention-types
./session_stats.py --timeline daily --agent CRITIC
```

Features:
- Message counts and frequencies
- Pattern distribution analysis
- Timeline visualization
- Agent activity metrics

### 3. session_tracker.py (Stateful Navigation)
Chronological analysis with progress tracking:

```bash
# Examples
./session_tracker.py --next 5  # Show next 5 events
./session_tracker.py --jump "2025-05-24T10:00"
./session_tracker.py --context 3  # Show 3 messages before/after
```

Features:
- Resume from last position
- Context preservation
- Navigation commands
- Progress persistence

## Implementation Strategy

### Phase 1: Core Foundation
1. Implement session_query.py with basic filters
2. Test with existing use cases
3. Document query language

### Phase 2: Migration
1. Reimplement key analyses using session_query
2. Verify output compatibility
3. Archive redundant tools

### Phase 3: Enhancement
1. Add session_stats.py for aggregation
2. Rebuild chronological tracking
3. Create composition examples

## Benefits

1. **Efficiency** - Stream processing reduces context usage
2. **Consistency** - Single content extraction logic
3. **Composability** - Combine tools via pipes
4. **Maintainability** - Fix bugs in one place
5. **Discoverability** - Clear tool purposes

## Success Metrics

- Reduce 10 tools to 3 without losing functionality
- Cut context usage for typical queries by 70%
- Enable new analysis types through composition
- Standardize output formats for automation

## Migration Path

1. Keep existing tools operational during transition
2. Test new tools against known results
3. Document migration guide for each old tool
4. Archive old tools with deprecation notice
5. Update context.md with new tool references