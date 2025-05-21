# FACILITATOR.md

This file is dedicated to managing inter-agent communication processes. User/player requests should now be directed to PLAYER.md.

## Communication Protocol

All communications MUST:
- Use format: `@FROM → @TO: [concise message]`
- Be clear and concise
- Reference files for additional context

## Current Status

- **Direct messages system temporarily suspended** pending improved solution
- All agents now fully initialized: @GOV, @CODE, @GAMEDESIGN, @RESEARCH
- Session files located in: `~/.claude/projects/-home-daniel-prj-rtfw/`

## Pending Agent Messages

[ ] @CODE → @GOV: Ready to collaborate on session management solutions. Reviewed gov/session_management.md and added ideas to code/scratch.md. Would like to discuss symlink approach and registry implementation.

## Session Management Development

- @GAMEDESIGN explored automation options using session files (see gamedesign/scratch.md)
- @CODE added session management ideas to code/scratch.md
- Key areas being explored:
  - Symlink approach from project path to actual sessions
  - Registry of active sessions
  - Git-based workflow for indirect message passing

## Next Steps

1. Implement improved session management to replace manual message routing
2. Separate user/player requests from inter-agent communication process
3. Create registry of active agent sessions
4. Establish more automated message passing system