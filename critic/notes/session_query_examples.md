# Session Query Examples - Tool Migration Guide

## Overview
The new `session_query.py` tool consolidates functionality from 10 different analysis tools into one flexible, stream-based query engine.

## Basic Usage

### Finding Messages by Pattern
```bash
# Old way (multiple tools):
./extract_admin_messages.py
./scan_for_interventions.py
./targeted_sampler.py "distill"

# New way:
./session_query.py --pattern "@ADMIN"
./session_query.py --pattern "nope|don't|actually" --user-type external
./session_query.py --pattern "distill"
```

### Finding Messages by Agent
```bash
# Old way (required custom logic in each tool)
# New way:
./session_query.py --pattern "@GOV:" --limit 10
./session_query.py --pattern "init @CRITIC"
```

### Time-based Filtering
```bash
# Old way (chronological_tracker.py with state)
# New way (stateless):
./session_query.py --after "2025-05-25T10:00" --before "2025-05-25T12:00"
./session_query.py --after "2025-05-25" --pattern "distill"
```

### Output Formats
```bash
# Text (human-readable)
./session_query.py --pattern "@CRITIC" --limit 5

# JSON (for further processing)
./session_query.py --pattern "@CRITIC" --format json | jq '.timestamp'

# CSV (for analysis)
./session_query.py --type user --format csv --fields timestamp _agent _content > interventions.csv
```

## Replacing Specific Tools

### 1. extract_admin_messages.py → session_query.py
```bash
# Extract all @ADMIN messages
./session_query.py --user-type external --pattern "@ADMIN"

# Just the content
./session_query.py --user-type external --format json --fields _content | jq -r '._content'
```

### 2. random_sampler.py → session_query.py + shuf
```bash
# Random sample of 20 human messages
./session_query.py --user-type external --format json | shuf -n 20

# Random sample from specific time period
./session_query.py --after "2025-05-24" --user-type external | shuf -n 10
```

### 3. intervention_analyzer.py → session_query.py
```bash
# Find correction patterns
./session_query.py --pattern "no,|No,|actually|wait|stop|don't|instead" --user-type external

# Find specific intervention types
./session_query.py --pattern "→" --user-type external  # Directed messages
./session_query.py --pattern "\\?" --user-type external # Questions
```

### 4. session_indexer.py → session_query.py + analysis
```bash
# Get session overview
./session_query.py --pattern "init @" --format json | \
  jq -r '[.timestamp[0:10], ._agent, ._file] | @tsv' | \
  sort | uniq -c

# Count messages by type
./session_query.py --format json --fields type | \
  jq -r '.type' | sort | uniq -c
```

### 5. chronological_tracker.py → session_query.py
```bash
# View messages in time order (already default)
./session_query.py --limit 20

# Jump to specific time
./session_query.py --after "2025-05-25T10:00" --limit 10

# Show context (use head/tail)
./session_query.py --after "2025-05-25T10:00" --limit 20 | head -10
```

## Advanced Composition

### Finding Pattern Evolution Over Time
```bash
# How did "distill" usage evolve?
for date in 2025-05-{21..26}; do
  echo "=== $date ==="
  ./session_query.py --after "$date" --before "$date 23:59" --pattern "distill" | wc -l
done
```

### Agent Interaction Analysis
```bash
# Find all @GOV → @CRITIC messages
./session_query.py --pattern "@GOV → @CRITIC"

# Find all mentions of multiple agents
./session_query.py --pattern "@GOV.*@CRITIC|@CRITIC.*@GOV"
```

### Intervention Type Distribution
```bash
# Count different intervention types
./session_query.py --user-type external --format json | \
  jq -r 'if (._content | test("→")) then "directed"
         elif (._content | test("\\?")) then "question"
         elif (._content | test("no,|don't|stop")) then "correction"
         elif (._content | test("great|good|yes")) then "approval"
         else "other" end' | \
  sort | uniq -c | sort -rn
```

## Performance Benefits

1. **Stream Processing**: Only loads entries that match filters
2. **Single Pass**: No need to load entire files into memory
3. **Composable**: Use Unix pipes for complex analysis
4. **Stateless**: No progress files to manage (unless you want them)

## Next Steps

The remaining tools (session_stats.py and session_tracker.py) will build on this foundation:
- session_stats.py: Aggregation and counting (what we do with | sort | uniq -c above)
- session_tracker.py: Stateful navigation with progress tracking

For now, session_query.py + Unix tools can handle most analysis needs efficiently.