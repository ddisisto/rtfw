# TMUX-Based Agent Management Architecture

## Overview
@NEXUS manages all agent windows within a single tmux session, providing real-time monitoring, message routing, and policy enforcement.

## Architecture
- All agents run as windows within single tmux session
- @NEXUS (window 0) monitors all agent outputs via tmux capture-pane
- Messages are routed in real-time between windows
- Policy enforcement happens before actions are executed
- @GOV is consulted for complex policy decisions

## Window Structure
```
0: nexus       # @NEXUS control window (started by @ADMIN)
1: code        # @CODE agent window
2: gov         # @GOV agent window  
3: architect   # @ARCHITECT agent window
4: research    # @RESEARCH agent window
5: historian   # @HISTORIAN agent window
6: test        # @TEST agent window
```

## Message Flow
1. Agent outputs message in format: `@FROM → @TO: [message]`
2. @NEXUS captures output via tmux
3. Message is parsed and routed to target session
4. Target agent receives message in their session
5. @NEXUS logs all communications

## Policy Enforcement
- @NEXUS reviews proposed actions before execution
- File modifications outside agent workspace require approval
- System-wide changes require @GOV consultation
- Emergency stops available for problematic actions

## Benefits
- Real-time communication
- Direct session management
- Policy enforcement at execution time
- Complete audit trail of all agent activities
- @ADMIN can observe any session directly