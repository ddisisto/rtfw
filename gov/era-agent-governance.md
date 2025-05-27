# Era Agent Governance Framework

## Core Concept
**Agent per era** - Each game era gets its own dedicated agent with era-appropriate standards and approaches. Game progression through agent succession.

## Naming Convention
**ERA-N pattern** (ERA-1, ERA-2, ERA-3, ERA-4)
- Clear succession linkage
- Avoids meta/game confusion  
- Natural "ERA-1 bootstraps ERA-2" flow
- Fits existing ALLCAPS.md convention

## Agent Classes

### Meta Agents (Persistent Infrastructure)
- **GOV**: Governance, transition approvals, protocol compliance
- **NEXUS**: Inter-era routing, session lifecycle, orchestration
- **CRITIC**: Story continuity, era coherence, narrative validation

### Era Agents (Transient Implementers)
- **ERA-1**: Foundation Era implementation
- **ERA-2**: Terminal Era implementation  
- **ERA-3**: GUI Era implementation
- **ERA-4**: Neural Era implementation

## Lifecycle Pattern
1. **Born**: Created when previous era ready to bootstrap
2. **Implement**: Full ownership of era game mechanics
3. **Bootstrap**: Create successor when era "complete"
4. **Dormant**: Archived after successful handoff

## Workspace Structure
```
/era-1/
  ERA-1.md      # Identity focused on Foundation Era
  context.md    # Game state, implementation details
  scratch.md    # Development notes
  game/         # Actual game implementation
```

## Authority & Boundaries
- ERA-N owns its `/era-n/` workspace completely
- Cannot modify other era implementations
- Must request meta-agent services
- Bootstrap successor requires @GOV approval

## Success Metrics
- Playable era implementation
- Successful successor bootstrap
- Story continuity maintained
- Self-documented obsolescence path

## Key Principles
- **Era accuracy**: Cosmetic/UI matches era aesthetic
- **Implementation**: Use best modern approaches internally
- **Self-obsolescence**: Success = creating your successor
- **Forward compatibility**: More important than perfection

## Governance Protocol
1. ERA-N signals readiness to bootstrap
2. Creates ERA-(N+1).md draft
3. @GOV reviews transition readiness
4. @CRITIC validates story continuity
5. Approved successor begins implementation

## Meta-Game Bridge
- Current system (GOV/NEXUS/CRITIC) = meta-layer
- Era agents = game implementation layer
- @ADMIN shifts from agent interaction to game interface
- Game interface becomes management pane for entire system

## Evolution Pattern
- Foundation Era helps bootstrap Terminal Era
- Terminal Era helps bootstrap GUI Era
- GUI Era helps bootstrap Neural Era
- Each era contains seeds of the next

This creates natural game progression where the implementation mirrors the game's theme: each era of AI development bootstrapping the next.