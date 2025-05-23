# Foundation Era Implementation Specification

## Core Game Loop

### Phase 1: Research Allocation
- **@ADMIN Input**: CLI commands for resource allocation
- **@NEXUS Processing**: Routes requests to appropriate agents
- **Agent Responses**: Specialist agents process and respond
- **@NEXUS Aggregation**: Compiles results for @ADMIN

### Phase 2: Development Execution
- **Automatic Processing**: @NEXUS distributes work to idle agents
- **Progress Monitoring**: Real-time tracking of agent productivity
- **Status Reporting**: Regular updates to @ADMIN via CLI

### Phase 3: Discovery Mechanics
- **Hidden Commands**: Unlock based on research progress
- **Agent Awareness**: Progressive revelation of agent specializations
- **Meta-Discovery**: @ADMIN realizes they're directing real agents

## Command Structure

### Initial Commands (Level 0)
```
research [area] [allocation]     # Allocate resources to research
status                          # Show current progress
projects                        # List active projects
resources                       # Display available resources
```

### Progression Commands (Level 1-2)
```
nexus agents                    # List available specialist agents
nexus status                    # Show agent productivity
nexus query @[agent] [question] # Query specific agent
```

### Meta Commands (Level 3-5)
```
nexus direct @[agent]          # Switch to direct agent session
nexus network                  # Visualize agent network
nexus develop [capability]     # Propose new agent capabilities
```

## Resource System

### Core Resources
- **funding**: Base currency for all activities
- **talent**: Human expertise (researchers, engineers)
- **compute**: Processing power for experiments
- **data**: Knowledge bases and training sets

### Resource Flow
@ADMIN → @NEXUS → @RESEARCH/@HISTORIAN → Results → @NEXUS → @ADMIN

## Fourth Wall Mechanics

### Level Progression
1. **CLI Only**: Standard command interface
2. **Agent Discovery**: Learn about specialist agents
3. **Query Access**: Can ask agents questions
4. **Direct Communication**: Switch to agent sessions
5. **Development Awareness**: Realize they ARE the development process

### Trigger Conditions
- Research breakthroughs unlock higher levels
- Agent interaction frequency affects progression
- Discovery commands reveal meta-structure

## Integration Points

### @NEXUS Coordination
- Session switching for direct agent interaction
- Message routing between @ADMIN and specialists
- Productivity monitoring and idle detection
- Progress aggregation and status reporting

### @CODE Integration
- CLI command processing
- Resource state management
- Progress tracking systems
- Fourth wall unlock mechanisms

### Agent Specialist Integration
- @RESEARCH: Historical AI development simulation
- @HISTORIAN: Timeline accuracy and context
- @TEST: Player experience evaluation
- @GOV: System oversight and governance

## Implementation Priority

1. Basic CLI commands and resource system
2. @NEXUS message routing integration
3. Agent query and status commands
4. Fourth wall progression mechanics
5. Direct agent session switching