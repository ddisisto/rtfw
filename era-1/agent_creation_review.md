# Agent Creation Code Review & Hardening Plan

## Test Results (2025-05-30)

### Observed Behavior
1. **Double Enter Required**: Claude CLI autocomplete requires first Enter, execution requires second
2. **Session File Creation**: ~2-3 seconds after /status command execution
3. **Symlink Creation**: Manual process worked correctly
4. **File Detection**: New session appeared with unique UUID

### Critical Issues Identified

#### 1. Session File Detection Race Condition
**Problem**: Multiple agents starting simultaneously could grab wrong session files
**Solution**: 
- Implement lockfile mechanism: `/tmp/rtfw-agent-creation.lock`
- Use file locking (fcntl) to ensure single creation at a time
- Include agent name in lock to allow parallel different agents

#### 2. Claude CLI State Machine Fragility
**Problem**: Different UI states require different key sequences
**Solution**:
- Implement state detection via pane capture parsing
- Create state-specific handlers for each CLI mode
- Add retry logic with exponential backoff

#### 3. Session Association Uncertainty
**Problem**: No guarantee new session belongs to our agent
**Solution**:
- Parse first few lines of new session for agent identification
- Add timestamp correlation (session created within X seconds)
- Implement session content validation

## Proposed Architecture Improvements

### 1. Atomic Creation Manager
```python
class AtomicAgentCreator:
    def __init__(self):
        self.lock_dir = Path("/tmp/rtfw-locks")
        self.lock_dir.mkdir(exist_ok=True)
    
    def acquire_creation_lock(self, agent_name: str) -> FileLock:
        """Ensure only one agent creation at a time"""
        lock_file = self.lock_dir / f"{agent_name}.lock"
        return FileLock(lock_file, timeout=30)
    
    def create_with_lock(self, agent_name: str) -> AgentCreationResult:
        with self.acquire_creation_lock(agent_name):
            return self._create_agent(agent_name)
```

### 2. Session Validation Framework
```python
class SessionValidator:
    def validate_new_session(self, session_file: Path, agent_name: str, 
                           creation_time: datetime) -> bool:
        """Multi-stage validation of new session"""
        # 1. Time window check (created within 10s)
        # 2. Content parsing for agent markers
        # 3. File size sanity check (not empty, not huge)
        # 4. JSONL format validation
        # 5. No other agent claims this session
```

### 3. Robust State Detection
```python
class ClaudeUIStateDetector:
    STATES = {
        'WELCOME': r'Welcome to Claude Code',
        'READY': r'╰─+╯\s+\?\s+for\s+shortcuts',
        'COMMAND_ENTRY': r'>\s+/\w+',
        'STATUS_DISPLAY': r'Claude Code Status',
        'WAITING_ENTER': r'Press Enter to continue',
        'ERROR': r'Error:|Failed:'
    }
    
    def detect_state(self, pane_content: str) -> UIState:
        """Parse pane content to determine UI state"""
```

### 4. Defensive Checkpoint System
```python
class CreationCheckpoint:
    """Track progress through creation stages"""
    stages = [
        'tmux_window_created',
        'bash_ready',
        'claude_started',
        'ui_ready',
        'status_sent',
        'status_displayed',
        'status_closed',
        'session_detected',
        'session_validated',
        'symlink_created',
        'state_initialized'
    ]
    
    def checkpoint(self, stage: str, metadata: dict):
        """Log progress with rollback capability"""
```

## Implementation Priority

1. **Immediate (Before Production)**
   - Lockfile for session creation atomicity
   - Basic session validation (time window + content check)
   - Retry logic for Claude commands

2. **Next Iteration**
   - Full state machine for Claude UI
   - Comprehensive validation framework
   - Checkpoint/rollback system

3. **Future Enhancement**
   - Parallel safe creation
   - Session pooling for faster startup
   - Health monitoring dashboard

## Testing Requirements

1. **Unit Tests**
   - Mock tmux interactions
   - Session file detection edge cases
   - Lock contention scenarios

2. **Integration Tests**
   - Full creation flow
   - Concurrent creation attempts
   - Failure recovery paths

3. **Stress Tests**
   - Rapid creation/destruction cycles
   - Network latency simulation
   - Resource exhaustion handling

## Next Steps

1. Implement lockfile mechanism in AgentCreator
2. Add basic session validation
3. Create comprehensive test suite
4. Document failure modes and recovery procedures
5. Add monitoring/alerting for creation failures

The foundation must be rock solid - every agent's journey begins here.