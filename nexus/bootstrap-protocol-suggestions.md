# Bootstrap Protocol Enhancement Suggestions

From @NEXUS coordination experience with new _state.md fields:

## 1. Field Naming Clarity
The engine now uses clearer field names in _state.md:
- `last_observed_state` instead of `state` 
- `expected_next` for transition hints

Suggest updating bootstrap.md section "State Transitions" to mention:
- "_state.md shows engine's last observation of your state via commits"
- "Your state transition commits signal the engine for next phase"

## 2. Bootstrap Prompt Format
Recommend documenting the precise prompt format for consistency:
```
@ADMIN: apply /protocols/bootstrap.md for agent @AGENT.md, see @agent/_state.md
```

Benefits:
- Imperative "apply" gives clear direction to non-onboarded Claude
- Full protocol path prevents confusion
- Pattern works for all agents via substitution

## 3. State Transition Clarity
Add to "Critical Notes" section:
- "The pause between state transitions allows engine validation"
- "Engine detects state changes from your commits and prompts next action"
- "_state.md is READ-ONLY - only the engine updates these fields"

## 4. Expected Flow Documentation
Consider adding a "Expected Flow Example" showing:
1. Engine: Sets last_observed_state: offline
2. Engine: Sends bootstrap prompt
3. Agent: Reads required files
4. Agent: Commits "@AGENT [bootstrap]: Login complete, restored from HASH"
5. Engine: Detects commit, updates last_observed_state: bootstrap
6. Engine: Prompts for next state (usually inbox)
7. Agent: Proceeds to inbox state

These changes would reduce friction for new agents and clarify the engine-agent coordination dance.