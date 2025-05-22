# Session Management for Multi-Agent Development

## Current Session Architecture

- Each agent has a separate Claude Code session
- Sessions are stored in `~/.claude/projects/-home-daniel-prj-rtfw/`
- @NEXUS manages communication between sessions
- High latency in communication due to manual message routing

## Proposed Improvements

### Symlink Approach

Creating symlinks to actual sessions could help with visibility:
```bash
# Create symlinks from project path to actual sessions
ln -s ~/.claude/projects/-home-daniel-prj-rtfw/<session-id> /home/daniel/prj/rtfw/sessions/gov
ln -s ~/.claude/projects/-home-daniel-prj-rtfw/<session-id> /home/daniel/prj/rtfw/sessions/code
# etc.
```

### Session Information Storage

Maintain a registry of active sessions:
```
/sessions/
  registry.md   # Maps agent names to session IDs
  README.md     # Instructions for connecting to sessions
```

### Automated Message Routing

Long-term goal: Develop automated routing system to:
- Monitor committed messages in git
- Auto-forward to appropriate agent sessions
- Reduce latency in inter-agent communication

## Next Steps

1. Identify all active session IDs
2. Create sessions directory with symlinks
3. Establish git-based workflow for indirect message passing
4. Work with @CODE on more automated message routing options
5. Transition communication responsibilities from manual process to NEXUS-managed system