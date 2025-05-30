# GOV Agent Context

## Critical State Preservation
- Session: GOV operational in main tmux session
- Active protocols: Git-comms via messaging.md, three-way documentation split
- Recent completions: Restore protocol git log enhancement, automated routing test
- Active monitoring: STATUS.md maintenance process, git-comms effectiveness
- System status: Simplification achieved - git as communication infrastructure

## Required Reading Dependencies (Restore Order)
1. @GOV.md - Identity and role
2. CLAUDE.md - System requirements and protocols
3. SYSTEM.md - Architecture and workflows
4. @ADMIN.md - Project oversight authority
5. @NEXUS.md - Orchestration partner
6. gov/protocol_design_guidelines.md - Protocol creation
7. /protocols/journey.md - State management
8. /protocols/bootstrap.md - Startup sequence
9. gov/context.md - This file
10. gov/scratch.md - Working memory
11. Recent activity check:
   ```bash
   # My recent work
   git log --oneline -10 | grep '^[a-f0-9]* @GOV:'
   # Recent mentions
   git log --oneline -20 | grep -v '^[a-f0-9]* @GOV:' | grep '@GOV' | head -10
   # Sovereignty check
   git log --oneline -10 gov/ | grep -v '^[a-f0-9]* @GOV:'
   ```

## Session Continuity (2025-05-30)
- Major protocol cleanup: Archived 3 outdated governance docs
- Fixed all agent-lifecycle.md → journey.md references
- Direct_io now bidirectional - agents can initiate too
- Idle work concept: Agents own directives in context.md
- Next focus: Agent self-optimization patterns, idle work framework

## Core Governance Principles
- Minimal viable governance over complex rule systems
- Clear boundaries and simplified protocols for multi-agent collaboration
- Context management critical for system coherence (30KB/100KB thresholds)
- Git commits as primary async communication channel
- Three-document architecture: CLAUDE.md (philosophy) + SYSTEM.md (architecture) + STATUS.md (current state)
- Protocols as extensible frameworks, not prescriptive lists
- Responsive diagnosis over preventive inspection
- Trust agents to self-maintain until patterns indicate issues
- Lexicon tracking for conceptual coherence across system
- Unix philosophy alignment: simplicity, composability, clarity
- Breaking changes cleanly prevents technical debt accumulation
- Operational clarity in protocols prevents intent confusion
- Context lifecycle: distill→consolidate→compress→restore
- Agent sovereignty includes restore dependency maintenance
- Per-turn insight capture operationalizes continuous learning
- Simplification through removal preferred over feature addition
- Shared vernacular builds stronger conceptual weight than technical precision
- Domain ownership model: Agents differentiate by scope not capability
- Workspace sovereignty sacred: Even GOV must respect boundaries
- "Super-position" governance: Partial definition enables adaptation
- Protocol documentation balance: Single source in /protocols/, minimal reinforcement
- Messaging checkpoint tracking: Essential for preventing re-processing
- Fourth wall architecture: _state.md provides objective truth agents cannot perceive
- Lifecycle formalization: States drive behavior with clear transitions
- Bootstrap universality: Single entry point from offline, reinforced in message
- Message standardization: @AGENT [state/thread]: all @MENTIONS on first line

## System Architecture
- Meta agents: ADMIN, NEXUS, GOV, CRITIC (persistent infrastructure)
- ERA agents: ERA-1 (Foundation Era implementer)
- GitHub repository: https://github.com/ddisisto/rtfw
- Git workflow: main branch, commits as communication channel
- Permission system: direct @mention requests (no PR reviews)
- Two-document structure: CLAUDE.md + SYSTEM.md
- Git-comms via distributed @mentions

## Active Governance Tasks
- Monitor ERA-1 implementation progress
- Support MCP permission system adoption
- Enforce agent structure protocol compliance
- Track commit context pattern usage
- Continue responsive governance model
- Guide protocol formalization from emergent patterns

## GOV Bootstrap Protocol (Updated)
1. Read GOV.md for identity
2. Read CLAUDE.md for system navigation
3. Read SYSTEM.md for architecture
4. Load gov/context.md and gov/scratch.md
5. Check mentions from last checkpoint: `git log --oneline LAST..HEAD | grep -v '^[a-f0-9]* @GOV:' | grep '@GOV'`
6. Update checkpoint in scratch.md with commit hash
7. Review active protocols in /protocols/
8. Check for pending permissions in gov/tools/permissions/
9. Begin governance work

## Development History
- Project initialization and agent system establishment
- Agent renaming: FACILITATOR → NEXUS, GAMEDESIGN → ARCHITECT
- GitHub integration and repository setup
- Simplified collaboration model implementation
- STATE.md migration: Replaced chronological ANNOUNCEMENTS.md with rolling state document
- Context consolidation protocol: Reframed from idle reflection for compression readiness
- Context compression protocol: Revised to framework approach per design guidelines
- Protocol design guidelines: Created for consistent protocol development
- Communication protocol v2: Enhanced with [TOPIC] threads and priority flags (!/-)
- Insight capture protocol: Voluntary framework for system learning
- Responsive governance model: Shifted from scheduled reviews to symptom-based intervention
- admin/tools.md: Added to universal post-compression requirements
- Lexicon tracking: New responsibility for conceptual coherence
- Major protocol migration: Moved to /protocols/ with unix-style CLAUDE.md (61% size reduction)
- Distill/restore split: Separated for operational clarity and self-improvement focus
- Per-turn insight capture: Integrated into CLAUDE.md communication flow
- CRITIC agent: Established for system criticism and assumption challenging
- Restore continuity: Enhanced through agent responsibility principle
- Three-way documentation split: STATE.md → CLAUDE.md/SYSTEM.md/STATUS.md
- Git-comms protocol: Recognized git commits as natural async message queue
- Simplification milestone: Eliminated JSONL parsing and mailbox patterns
- Restore enhancement: Added git log checking for recent activity context
- Protocol consolidation: git-comms.md merged into messaging.md
- Automated routing: NEXUS git_router.py operational with tmux delivery
- Domain-based agents: BUILD deprecated - agents implement within their scope
- Two-doc structure: STATE.md → CLAUDE.md + SYSTEM.md (STATUS.md also deprecated)
- Era agent governance: Framework for ERA-N game implementation agents
- Messaging v2 approved: Distributed mentions, checkpoint tracking, no router
- Game-Meta unification: Game interface becomes actual dev environment
- ERA agent model: Transient implementers with clear lifecycle
- Agent structure protocol: Formalized @AGENT.md conventions
- MCP permission automation: CLI-based approval system
- Commit context pattern: Essential for work continuity
- Direct_IO mode: @ADMIN override pauses engine state transitions
- Protocol-engine binding: Decision outputs in protocols drive engine behavior
- State protocol completeness: All 8 states now have dedicated protocols
- Protocol harmonization: Extract common patterns to prevent duplication
- Notification patterns: Proactive alerts across all states, not just direct_io
- Decision output standardization: Consistent format for engine parsing