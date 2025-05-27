# [Analysis Title]
Started: YYYY-MM-DD
Status: PLANNING

## Research Question
[What specific question are we trying to answer?]

## Methodology
1. [Step 1 - e.g., "Extract all X from sessions between dates Y-Z"]
2. [Step 2 - e.g., "Categorize by type using criteria A, B, C"]
3. [Step 3 - e.g., "Calculate frequency and impact metrics"]

## Data Sources
- [ ] Sessions: [nexus/sessions/session_YYYY-MM-DD_*.jsonl]
- [ ] Git commits: [git log --since="YYYY-MM-DD" --until="YYYY-MM-DD"]
- [ ] Documents: [List specific files]

## Tools & Commands
```bash
# Exact commands to reproduce analysis
python critic/tools/session_query.py --agent ADMIN --date-range "2025-05-21:2025-05-26"
```

## Expected Outputs
- [ ] Raw data extract → outputs/YYYY-MM-DD_topic_raw.json
- [ ] Categorized findings → outputs/YYYY-MM-DD_topic_categorized.csv
- [ ] Summary report → this file's Findings section

---

## Findings
*[Updated when status → COMPLETE]*

### Summary
[1-2 paragraph overview]

### Detailed Results
[Categories, counts, patterns, examples]

### Confidence Levels
- HIGH: [Findings with strong evidence]
- MEDIUM: [Findings with partial evidence]
- LOW: [Hypotheses needing verification]

### Contradictions/Surprises
[Anything that challenged assumptions]

---

## Integration Notes
*[Updated when status → INTEGRATED]*

### Added to context.md
- [Specific sections updated]
- [Key insights preserved]

### Actions Taken
- [Changes to system based on findings]
- [New tracking initiated]

### Follow-up Needed
- [ ] [Future analysis suggested by findings]