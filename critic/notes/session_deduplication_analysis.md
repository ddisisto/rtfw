# Session Deduplication Analysis

## Key Finding
When Claude Code sessions are resumed, they create new session files that contain ALL previous content plus new interactions. This creates redundant data.

## Evidence

### GAMEDESIGN Sessions (Same start: 2025-05-21T08:12:56)
- **Shorter**: 932ef584... (78 messages, ends 13:47)
- **Longer**: 51f1fab0... (130 messages, ends next day 13:33)
- **Result**: ✓ Shorter is exact prefix of longer (52 additional messages)

### GOV Sessions (Same start: 2025-05-22T06:35:01)  
- **Shorter**: 75583faf... (405 messages, ends 2 days later)
- **Longer**: 2e0df345... (839 messages, ends 4 days later)
- **Result**: ✓ Shorter is exact prefix of longer (434 additional messages)

### NEXUS Sessions (Same start: 2025-05-21T13:36:27)
- **Result**: ✗ Not simple prefix - timestamps differ on responses
- **Likely cause**: Assistant messages regenerated on resume

## Deduplication Strategy

For sessions with identical start times:
1. Keep only the session with the latest end timestamp
2. Remove shorter sessions as they're redundant subsets
3. Exception: NEXUS case shows some sessions may diverge (different response generation)

## Sessions to Remove

From our index:
- UNKNOWN: Keep f5a74925... (remove 66a678dc...)
- GAMEDESIGN: Keep 51f1fab0... (remove 932ef584...)  
- NEXUS (13:36): Needs manual review - not simple prefix
- GOV: Keep 2e0df345... (remove 75583faf..., f78af070...)
- NEXUS (13:08): Keep 259663e5... (remove e94c92cf...)

This would reduce 22 sessions to ~17 sessions, removing ~22% redundancy.