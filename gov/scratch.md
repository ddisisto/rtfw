# GOV Scratch

## Distillation 2025-01-26

### Key Insight: Agent Differentiation Model

Traditional orgs differentiate by capability (frontend vs backend dev).
AI agent orgs differentiate by domain/concern - each agent has full-stack capability within their scope.

Benefits:
- No context handoff loss
- Domain expertise stays with implementation  
- Faster iteration cycles
- Natural ownership boundaries

Implications:
- BUILD role redundant as currently defined
- Agents as "domain owners" not "skill specialists"
- Focus: "what do you own?" not "what can you do?"

### Governance Patterns Emerging

1. **Responsive > Proactive**: BUILD deprecation came from ADMIN observation during actual use, not from scheduled review. This validates our responsive governance model.

2. **Simplification in Practice**: Protocol consolidation (git-comms → messaging.md) shows continuous refinement working. Fewer, clearer protocols.

3. **Evolution Through Use**: System assumptions get tested through practice. BUILD's underuse revealed design flaw - capability-based rather than domain-based differentiation.

4. **Trust Git History**: No need for archived/ directories. Git maintains full history. Cleaner repo, same preservation.

### GOV.md Review Notes

Current doc mostly accurate but needs updates:
- Remove references to deprecated protocols (comms_protocol.md)
- Update protocol list to reflect /protocols/ migration
- Consider adding "System Evolution" as core function
- Bootstrap protocol could be simplified

### System Learning
- Domain ownership model discovered through BUILD failure
- Protocol migration to /protocols/ successful
- Three-doc structure (CLAUDE/SYSTEM/STATUS) proving clearer than monolithic STATE.md
- STATUS.md deprecated (2025-01-26): High maintenance overhead, duplicated agent-tracked state
  - Evolution: STATE.md → three docs → two docs (CLAUDE.md + SYSTEM.md)
  - Agents track own state in context.md/scratch.md more effectively
  - Distributed state tracking more resilient than central document
  - Simplification continues: less to maintain, clearer boundaries

## Era Agent Governance Considerations (2025-01-26)

### Naming Patterns
Considering @ADMIN's suggestions:
- **ERA-1, ERA-2, ERA-3, ERA-4**: Clear succession, domain obvious
- **GAME-1, GAME-2**: Risk of meta confusion (whole system is "game")
- **BRIDGE-1, BRIDGE-2**: Captures transition nature but less clear

Recommendation: **ERA-N** pattern
- Clear succession linkage
- Avoids meta/game confusion
- Natural "ERA-1 bootstraps ERA-2" flow
- Fits existing ALLCAPS.md convention

### Governance Implications

1. **New Agent Class**
   - Era agents distinct from meta agents (GOV, NEXUS, CRITIC)
   - Different lifecycle: born → implement → bootstrap successor → dormant/archived
   - Self-obsolescence as success metric

2. **Workspace Structure**
   ```
   /era-1/
     ERA-1.md      # Identity focused on Foundation Era
     context.md    # Game state, implementation details
     scratch.md    # Development notes
     game/         # Actual game implementation
   ```

3. **Authority Boundaries**
   - ERA-N owns its era's game implementation completely
   - Cannot modify other era implementations
   - Must request meta-agent services (routing, governance)
   - Bootstrap successor requires @GOV approval

4. **Bootstrap Protocol**
   - ERA-N creates ERA-(N+1).md when ready
   - Transfers essential knowledge via bootstrap document
   - @GOV validates transition readiness
   - Graceful handoff, not abrupt cutover

5. **Success Metrics**
   - Playable era implementation
   - Successful successor bootstrap
   - Story continuity maintained
   - Self-documented obsolescence path

6. **Cross-Era Coordination**
   - CRITIC ensures narrative continuity
   - GOV manages transition approvals
   - NEXUS routes inter-era messages
   - No direct era-to-era file access

7. **Evolutionary Pressure**
   - Each era must make next era possible
   - Later eras can patch earlier ones (via PR-like process?)
   - Forward compatibility more important than perfection

This creates natural game progression through agent succession!