# Session Management Plan

## Current Status
- Each agent has a separate Claude Code session
- Sessions are stored in `~/.claude/projects/-home-daniel-prj-rtfw/`
- Communication happens directly in token stream
- High latency in communication due to manual message routing

## Implementation Plan

### Phase 1: Registry Creation
- Create and maintain `nexus/registry.md` for mapping agents to sessions
- Identify all active session IDs for current agents
- Document session locations and access methods

### Phase 2: Message Passing System
- Establish git-based workflow for indirect message passing:
  - Agents write messages to their own scratch files
  - Messages committed to repository
  - Target agents read messages during their sessions
  - @NEXUS monitors and routes important communications

### Phase 3: Automated Routing
- Long-term goal: Develop automated routing system to:
  - Monitor committed messages in git
  - Auto-forward to appropriate agent sessions
  - Reduce latency in inter-agent communication

## Integration Points
- Work with @CODE on implementation details
- Collaborate with @GOV on communication governance
- Update @ARCHITECT on system design implications
- Keep all agents informed via ANNOUNCEMENTS.md