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
- **NEXUS**: Session lifecycle, distributed messaging, orchestration
- **CRITIC**: Story continuity, era coherence, narrative validation

### Era Agents
- **ERA-1**: Foundation Era (permanent senior architect for CLI/terminal)
- **ERA-2**: GUI Era implementation (future)
- **ERA-3**: Advanced GUI Era (future)
- **ERA-4**: Neural Era implementation (future)

## ERA Agent Lifecycle Pattern
1. **Born**: Created when previous era ready to bootstrap
2. **Implement**: Full ownership of era game mechanics
3. **Bootstrap**: Create successor when era "complete"
4. **Dormant**: Archived after successful handoff

Note: This is the macro lifecycle for ERA succession. For operational states during implementation, ERA agents follow the standard 7-state lifecycle in /protocols/agent-lifecycle.md

## Workspace Structure
```
/era-n/
  context.md    # Game state, implementation details
  scratch.md    # Development notes
  _state.md     # READ-ONLY objective state (maintained by game)
  game/         # Actual game implementation
/ERA-N.md       # Public identity at root level
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
1. ERA-N signals readiness to bootstrap successor
2. Creates draft /ERA-(N+1).md following /protocols/agent-structure.md
3. @GOV reviews transition readiness
4. @CRITIC validates story continuity
5. @GOV approves creation with git commit
6. ERA-(N+1) follows /protocols/bootstrap.md to begin

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