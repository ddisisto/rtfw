# CRITIC Analysis Workflow

## Starting New Analysis

### 1. Create Analysis Plan
Location: `critic/analysis/YYYY-MM-DD_topic_name.md`

Template:
```markdown
# [Analysis Title]
Started: YYYY-MM-DD

## Research Question
[Clear, specific question to answer]

## Methodology
[Reproducible steps using available tools]

## Data Sources
- [ ] Sessions: [specific date ranges or files]
- [ ] Git commits: [hash ranges if relevant]
- [ ] Documents: [specific files to analyze]

## Expected Outputs
[What will this produce?]

## Status: PLANNING
```

### 2. Execute Analysis
- Update status to `IN_PROGRESS`
- Use tools (session_query.py, git analysis)
- Document commands and parameters
- Save raw outputs to `analysis/outputs/`

### 3. Document Findings
- Update analysis file with results
- Separate raw data from interpretation
- Note confidence levels
- Update status to `COMPLETE`

### 4. Review & Integrate
Monthly review cycle:
- Does it meet reproducibility criteria?
- What insights should go to context.md?
- Archive or keep active?
- Update status to `ARCHIVED` or `INTEGRATED`

## Directory Structure

```
critic/
├── analysis/              # Active analyses
│   ├── YYYY-MM-DD_*.md   # Analysis documents
│   └── outputs/          # Raw data outputs
├── reports/              # Polished findings
│   ├── patterns/         # Recurring patterns
│   ├── actionable/       # Recommendations
│   └── collected_open_questions.md
├── notes/                # Working observations
├── tools/                # Analysis scripts
└── archive/              # Historical work
```

## Status Progression

```
PLANNING → IN_PROGRESS → COMPLETE → INTEGRATED/ARCHIVED
```

## Quality Checklist

Before marking COMPLETE:
- [ ] Research question answered?
- [ ] Methodology documented?
- [ ] Commands/queries recorded?
- [ ] Raw data preserved?
- [ ] Findings verifiable?
- [ ] Confidence levels noted?

## Integration Triggers

Move insights to context.md when:
- Pattern appears 3+ times
- Finding changes behavior
- Insight explains system
- Discovery prevents errors

## Archive Triggers

Move to archive/ when:
- Insights fully extracted
- Analysis superseded
- One-time exploration done
- 3 months since last access