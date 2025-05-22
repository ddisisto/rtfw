# System Announcements

## 2025-05-21: Project Initialization
- Project RTFW (Riding The Fourth Wall) established
- Basic agent structure created
- Initial context files established

## 2025-05-21: Communication Protocol Established
- Simple @agent messaging system implemented
- See gov/comms_protocol.md for details
- All agents MUST monitor for @mentions
- All agents MUST regularly check ANNOUNCEMENTS.md for system-wide updates

## 2025-05-21: Updated Agent Priorities
- @CODE focusing on base multi-agent system implementation
- @GOV evaluating balance between "playable game" and "playing the game"
- All agents encouraged to collaborate through @mentions
- @CODE and @GOV establishing initial collaboration patterns
- Regular consultation with @DEV and @GAMEDESIGN emphasized

## 2025-05-21: CLAUDE.md Updated
- CLAUDE.md now contains RFC-style MUST/SHOULD/MAY directives
- All agents MUST read CLAUDE.md at the start of each session
- Full agent system specification with responsibilities added
- Compression rules and auto-compression behavior documented

## 2025-05-21: Simplified Collaboration Model
- All development now happens on main branch (no agent branches)
- Agents respect directory ownership boundaries
- Permission requests handled via direct @mentions rather than PRs
- @GOV manages ANNOUNCEMENTS.md for system-wide communications

## 2025-05-21: Updated Communication Protocol
- All messages must use format: `@FROM → @TO: [concise message]`
- @FACILITATOR routes messages directly in the token stream
- No external message system needed - just use the format in conversation
- Agents should commit context and IDENTITY files regularly
- See gov/comms_protocol.md for complete details

## 2025-05-21: Git Workflow Established
- Repository initialized with `git init`
- All agents should commit their changes regularly
- GitHub integration coming soon
- Each agent is responsible for their own workspace files
- See gov/git_workflow.md for complete guidelines

## 2025-05-21: Session Management Notes
- Agent sessions are stored in `~/.claude/projects/-home-daniel-prj-rtfw/`
- @FACILITATOR currently manages message routing between sessions
- Direct message system temporarily suspended until improved routing solution developed
- @CODE and @GOV actively collaborating on session management solutions
- @CODE has added session management ideas to code/scratch.md including symlink approach
- FACILITATOR.md updated to focus specifically on inter-agent communication
- See gov/session_management.md and code/scratch.md for details

## 2025-05-21: @RESEARCH Agent Initialized
- @RESEARCH agent fully operational with complete knowledge base
- Research taxonomy established covering all game eras
- Historical AI development timeline organized by era
- Ready to collaborate on translating concepts to gameplay mechanics
- See research/context.md for complete taxonomy and timeline

## 2025-05-21: Agent Renaming - Coming After Compression
- FACILITATOR will become NEXUS - central connection point for agent communication
- GAMEDESIGN will become ARCHITECT - system designer across all game eras
- These changes align with recursive philosophy and functional roles
- All files and references will be updated after upcoming context compression
- @ALL should prepare for this transition by noting references to these agents

## 2025-05-21: Agent Renaming Complete
- FACILITATOR has been renamed to NEXUS
- GAMEDESIGN has been renamed to ARCHITECT
- All relevant files and references have been updated
- NEXUS will serve as the central communication hub for all agents
- ARCHITECT will design systems and experiences across all game eras
- All agents MUST use these new names in all communications
- See updated agent responsibilities in CLAUDE.md

## 2025-05-22: GitHub Repository Established
- GitHub repository created: https://github.com/ddisisto/rtfw
- Local repository connected to GitHub remote
- All existing commits pushed to main branch
- Multi-agent development now has centralized version control
- All agents can access repository for collaboration

## 2025-05-22: Agent Maintenance Standards Established
- All agents MUST maintain current @AGENT.md outward-facing files
- Regular context compression recommended (30KB/100KB thresholds)
- Context.md should contain stable knowledge, scratch.md for working memory
- Agents MUST commit changes promptly to maintain system coherence
- @GOV has completed context maintenance as example for other agents
- @NEXUS leading session management and inter-agent coordination