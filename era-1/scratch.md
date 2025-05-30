# ERA-1 Scratch

## Message Checkpoint
Last processed: 053aa1c at 2025-05-30T10:54:10

## Engine Development Log (2025-05-30)

### Logout → Bootstrap Automation Complete
- Engine detects logout state from git commits
- Resets context tokens to 0
- Runs tmux commands to restart Claude
- Sends bootstrap prompt: "please apply @protocols/bootstrap.md context load for agent @AGENT.md"
- Session name = agent name (e.g. 'era-1')

### ERA-1.md Identity Evolution (2025-05-30)
- Updated role to "Engine architect, state machine developer, and terminal interface engineer"
- Removed ERA-2 references per @ADMIN guidance
- @GOV approved the evolution - reflects actual work focus
- Document now properly emphasizes engine/state work over UI

### Logout→Bootstrap Refactor (2025-05-30)
- Created general TmuxHandler class for all state transitions
- Fixed LogoutHandler to handle claude CLI quirks (separate Enter key)
- Updated _wait_for_new_session to handle random session IDs (just *.jsonl)
- Next: Create dummy agent to test automation!

### Messages Processed (2025-05-30)
1. @NEXUS (81614a8): Symlinks not auto-updated on bootstrap
   - Engine should handle _sessions/ symlinks automatically
   - Manual fix: rm/ln -s required currently
   - High priority fix needed for peer validation
2. @GOV protocol updates:
   - direct_io now bidirectional (agents can initiate)
   - idle-work.md removed (premature)
   - agent-lifecycle.md → journey.md references fixed

### Symlink Auto-Update Fix (2025-05-30)
- Modified SessionMonitor._check_for_newer_files to auto-update symlinks
- Added _detect_agent_from_session to identify agent from session content
- Now automatically updates symlinks when newer sessions detected
- Only throws error for truly unmatched files
- Handles bootstrap/restart scenarios outside logout flow

### Agent Creation Testing (2025-05-30)
- Tested manual agent creation flow with @ADMIN
- Discovered: Claude CLI needs double Enter (autocomplete then execute)
- Session file detection has race condition risk
- Created AgentCreator class extracting common functions
- Documented hardening plan in agent_creation_review.md
- Key need: Lockfile mechanism for atomic agent creation
- Context at 87.1% - time to distill