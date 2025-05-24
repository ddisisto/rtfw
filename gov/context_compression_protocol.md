# RTFW Context Compression Protocol

## Purpose

Define the framework for maintaining agent operational continuity when external LLM session context compression occurs.

## Core Requirements

### External Compression Management
- **Authority**: @ADMIN manages all compression events
- **Timing**: Rolling basis, as-needed for system performance
- **Notice**: Advance notification to target agent
- **Governance**: @GOV maintains this protocol

### Agent Response Framework
1. Execute context consolidation protocol (see gov/context_consolidation_protocol.md)
2. Commit all changes to repository
3. Confirm readiness to @ADMIN

## Extension Points

### Agent-Specific Requirements
Each agent SHOULD document in their context.md:
- **Critical State Preservation**: Information essential for post-compression recovery
- **Required Reading**: Other @AGENT.md files needed for their role
- **Implementation Details**: Tool-specific or role-specific compression needs

### Post-Compression Recovery
1. Read own @AGENT.md (identity and capabilities)
2. Read CLAUDE.md (project requirements)
3. Read STATE.md (current system state)
4. Read admin/tools.md (environment literacy)
5. Read agent-specific dependencies (per own context.md)
6. Read own context.md (stable knowledge)
7. Read own scratch.md (working state)
8. Confirm operational status

## Implementation

### For Agents
- Maintain Critical State Preservation section in context.md
- Document specific recovery dependencies
- Implement role-specific compression preparations
- Extend this protocol as needed in own context

### For System
- @ADMIN initiates compression with notice
- Agents prepare using this framework
- Recovery follows standard sequence
- Operational confirmation completes process

## Governance

### Protocol Maintenance
- @GOV maintains this protocol following gov/protocol_design_guidelines.md
- Updates based on operational experience
- Agents provide feedback through standard communication channels

### System Health
- Compression frequency monitored for system optimization
- Agent-specific extensions reviewed for common patterns
- Protocol evolves based on actual usage

## Internal Context Compression

**Status**: Deferred - agents currently manage own context size through reflection protocol, will be advised directly if this needs to be further condensed.

**Future Consideration**: If internal compression becomes necessary, will follow similar framework with agent-specific thresholds and self-management.