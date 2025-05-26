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
4. STATUS.md - Current state snapshot
5. @ADMIN.md - Project oversight authority
6. @NEXUS.md - Communication routing
7. gov/protocol_design_guidelines.md - Protocol creation
8. gov/context.md - This file
9. gov/scratch.md - Working memory
10. Recent git activity: `git log --oneline -20 | grep "@GOV"`

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

## System Architecture
- Active agents: ADMIN, NEXUS, GOV, CRITIC, RESEARCH, ARCHITECT, HISTORIAN, TEST
- GitHub repository: https://github.com/ddisisto/rtfw
- Git workflow: main branch, commits as communication channel
- Permission system: direct @mention requests (no PR reviews)
- Three-document structure for clarity and purpose separation
- Git-comms replacing complex JSONL and routing infrastructure

## Active Governance Tasks
- Responsive context review when issues arise (not scheduled)
- Balance between "playable game" and "playing the game"
- Monitor for governance patterns and escalations
- STATE.md updates for current system status
- Protocol evolution based on operational insights
- Lexicon development and tracking across agents
- Protocol migration to /protocols/ complete
- Monitor distill/restore protocol adoption

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