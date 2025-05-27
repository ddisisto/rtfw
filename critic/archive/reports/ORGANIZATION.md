# CRITIC Reports Organization Strategy

## Problem
Flat reports/ directory will become unsustainable as analysis continues.

## Proposed Structure

```
critic/reports/
├── ORGANIZATION.md          # This file
├── INDEX.md                # Master index of all reports
├── raw/                    # Detailed intervention logs
│   ├── batch-001-interventions.md   # First 20 interventions
│   ├── batch-002-interventions.md   # Next batch
│   └── ...                          # Continue sequential
├── patterns/              # Thematic analysis
│   ├── communication.md   # Message routing patterns
│   ├── architecture.md    # System design decisions
│   ├── philosophy.md      # @ADMIN's core principles
│   └── anti-patterns.md   # What to avoid
├── consolidated/          # Periodic synthesis
│   ├── week-01.md        # Weekly consolidation
│   └── month-01.md       # Monthly meta-analysis
└── actionable/           # Current recommendations
    ├── for-agents.md     # Live guidance for all agents
    └── for-system.md     # Systemic improvements

```

## Strategy

### 1. Raw Capture (raw/)
- Chronological batches of 10-20 interventions
- Full context preserved
- Sequential batch numbers (batch-001, batch-002, etc.)
- Becomes historical archive
- Note: Project timespan is days, not months!

### 2. Pattern Extraction (patterns/)
- Theme-based files that grow over time
- Updated when new examples found
- Cross-referenced to raw batches
- Living documents

### 3. Consolidation Cycles (consolidated/)
- Weekly: Summarize new patterns
- Monthly: Meta-analysis of trends
- Quarterly: Major insights report
- Prevents endless accumulation

### 4. Actionable Insights (actionable/)
- Always current
- What agents need to know NOW
- Updated after each analysis batch
- Replace, don't append

## Migration Plan

1. Move current reports to appropriate dirs:
   - admin_interventions_analysis.md → raw/batch-001-interventions.md
   - admin_intervention_patterns.md → patterns/philosophy.md

2. Create INDEX.md with:
   - Chronological listing of all batches
   - Pattern file descriptions
   - Last consolidation date
   - Key insights summary

3. Extract actionable insights for immediate use

## Benefits

- Scalable to thousands of interventions
- Easy to find specific time periods
- Patterns visible across time
- Actionable guidance always current
- Historical record preserved
- Natural consolidation prevents bloat

## Questions for @ADMIN

1. Preferred batch size? (10-20 seems natural)
2. Consolidation frequency? (weekly/monthly?)
3. Archive older raw batches after consolidation?
4. Version control considerations for large accumulation?