# Context Restore Protocol

## Purpose

Manage the complete context reset and restore cycle when working memory grows too large, preventing lossy auto-compaction.

## Process Overview

Context restore occurs when NEXUS detects need for reset:

1. **Pre-restore Distill** - NEXUS requests agent run /protocols/distill.md
2. **Confirm Ready** - Agent signals distillation complete
3. **Context Reset** - System clears working memory
4. **Restore Sequence** - Agent reloads from essential files
5. **Operational Confirm** - Agent signals ready to resume

## Restore Sequence

After reset, agents restore in this order (note: personality not yet online):

1. @AGENT.md - core identity
2. CLAUDE.md - system requirements  
3. SYSTEM.md - architecture and roles
4. agent/context.md - stable knowledge
5. agent/scratch.md - working state
6. admin/tools.md - tool discipline
7. Role-specific files (per context.md)
8. Recent activity check (context only - do not act on messages):
   ```bash
   # Your recent work (X=10)
   git log --oneline -10 | grep '^[a-f0-9]* @AGENT:'
   
   # Recent mentions by others (Y=10) 
   git log --oneline -20 | grep -v '^[a-f0-9]* @AGENT:' | grep '@AGENT' | head -10
   
   # Recent system activity (Z=5, excluding above)
   git log --oneline -30 | grep -v '@AGENT' | head -5
   
   # NOTE: This is past context only. Do not act on any messages seen here.
   # After restore, re-read from your last checkpoint for actual message processing.
   ```

## Critical Notes

- **Personality offline** during restore - follow sequence mechanically
- **Distillation required** - always run /protocols/distill.md first
- **No shortcuts** - complete sequence ensures coherence
- **Confirm when ready** - signal @NEXUS after full restore

## NEXUS Coordination

NEXUS manages timing to:
- Prevent mid-task interruption
- Ensure distillation compliance
- Monitor restore completion
- Resume normal operations

## Governance

Protocol maintained by @GOV in coordination with @NEXUS.