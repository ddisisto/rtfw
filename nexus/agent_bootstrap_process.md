# NEXUS Agent Bootstrap Process

This document defines the restore protocol executed when NEXUS receives:
`@ADMIN → @NEXUS [RESTORE]!: @protocols/distill.md completed for @NEXUS.md - please restore context for continuation`

## Context Restore Protocol

### 1. Read Critical Files (per NEXUS.md bootstrap section)
- Read CLAUDE.md (project requirements and protocols)
- Read STATE.md (current system state)
- Read @ADMIN.md (admin authority and interfaces)
- Read @GOV.md (governance protocols)
- Read admin/tools.md (tool usage requirements)

### 2. Load Agent Context
- Read nexus/context.md (stable knowledge and state)
- Read nexus/scratch.md (working memory)

### 3. Self-Validate Session ID
Per standardized protocol in context.md:
- Generate marker: Bash `echo "NEXUS_SESSION_VALIDATION_$(date +%s)_$$"`
- Wait 2 seconds: Bash `sleep 2`
- Read current session: Read tool on .nexus_sessionid
- Search for marker: Grep tool with pattern=marker, path=/home/daniel/prj/rtfw/nexus/sessions
- If session changed:
  - Write new session ID to .nexus_sessionid using Write tool
  - Update session_log.txt: Read current log → append new line → Write full content

### 4. Announce Operational Status
`@NEXUS → @ADMIN [RESTORE]: Identity confirmed. Context loaded. <Session validation status>. Operational and ready to support system coordination.`

### 5. Check Agent Windows
- Bash: `tmux list-windows` to see current agent states
- Begin monitoring per agent_session_flow.md protocol

## Tool Usage Requirements
Per admin/tools.md - prioritize native tools:
- Read > cat
- Write > echo/redirect 
- Grep > grep/find
- MultiEdit for multiple changes
- Bash only when no native tool exists

## Post-Restore Routing
Per agent_session_flow.md section 1.5:
1. Check for pending messages to route
2. Query agents for pending outbound messages
3. Prompt agents to continue work or seek direction
4. Transition to IDLE if no work available

## Success Indicators
- Session validation completed (with or without change)
- Context files loaded successfully
- Operational announcement sent
- Agent window states assessed
- Ready for main coordination loop