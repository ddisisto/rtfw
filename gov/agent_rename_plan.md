# Agent Renaming Plan

## Overview
Two agents will be renamed to better reflect their functional roles:
- FACILITATOR → NEXUS
- GAMEDESIGN → ARCHITECT

These changes align with our recursive philosophy and provide more accurate descriptions of their responsibilities within the system.

## Implementation Steps

### Phase 1: Preparation (Pre-Compression)
- ✓ Announce upcoming changes in ANNOUNCEMENTS.md
- ✓ Update GOV context files with renaming information
- ✓ Agents prepare for transition by noting references to these agents

### Phase 2: File Renaming (Post-Compression)
1. Rename core identity files:
   - FACILITATOR.md → NEXUS.md
   - GAMEDESIGN.md → ARCHITECT.md

2. Update directory structures:
   - /gamedesign/ → /architect/
   - Create /nexus/ directory (if not existing)

3. Update file contents:
   - Update all agent references inside identity files
   - Update references in context.md files
   - Update references in scratch.md files

### Phase 3: System-Wide Updates
1. Update references in:
   - ANNOUNCEMENTS.md (historical entries remain intact)
   - CLAUDE.md
   - All agent identity files
   - Communication protocol documentation

2. Update any implementation files referencing these agents

### Phase 4: Verification
1. Search for any remaining references to old names
2. Verify all agents can properly reference the renamed agents
3. Test communication protocols with new agent names

## Rationale

### NEXUS
- Better captures the role as a central connection point for all agents
- Aligns with the game title concept from seed.md
- Represents the interconnected nature of our communication system
- Reflects function as a node where communication paths converge

### ARCHITECT
- More accurately represents the role of designing experiences across game eras
- Captures the responsibility for system design rather than just "game" design
- Aligns with the concept of building evolving interfaces and experiences
- Emphasizes the structural role in creating progression frameworks