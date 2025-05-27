# Distill/Restore Process Notes for ERA-1 Integration

## Key Learnings from CRITIC Restore (2025-05-28)

### Process Evolution
1. **Messaging protocol handles confirmations** - No need for constant capture-pane
2. **Git commits provide natural checkpoints** - Agent confirms via commit
3. **Only tmux verification needed after /clear** - To ensure command worked

### Mechanical Process Flow

```
1. Monitor context % (capture-pane only when checking health)
   ↓
2. Request distillation via git commit message
   @NEXUS: Time for distillation per @protocols/distill.md
   ↓
3. Wait for agent confirmation via git commit
   @AGENT: Distillation complete, ready for reset
   ↓
4. Execute /clear (only tmux interaction needed)
   tmux send-keys -t agent '/clear' Enter
   ↓
5. Verify clear worked (capture-pane here)
   ↓
6. Send restore protocol via git commit message
   @NEXUS: @protocols/restore.md underway...
   ↓
7. Agent restores and confirms via git commit
```

### ERA-1 CLI Integration Ideas

#### DISTILL Command
```
> DISTILL CRITIC
CHECKING CRITIC CONTEXT... [36%]
CRITIC ALREADY DISTILLED - READY FOR CLEAR
EXECUTING CLEAR...
[✓] CONTEXT CLEARED
SENDING RESTORE PROTOCOL...
MONITORING RESTORE...
```

#### STATUS Enhancement
```
> STATUS --verbose
NEXUS:  ACTIVE  [82% context] [session: f7bafca2]
GOV:    IDLE    [15% context] [session: 75583faf] ⚠️ DISTILL RECOMMENDED
CRITIC: RESTORE [0% context]  [session: 0e9196f6] 🔄 RESTORING...
ERA-1:  ACTIVE  [22% context] [session: cc9298f1]
```

#### Automated Monitoring
- Background thread checking context percentages
- Alert when agent hits 15% threshold
- Queue distillation requests during idle periods
- Track distillation history

### Integration with MCP Permission Server
@GOV created permission server that could handle:
- Auto-approve distill/restore operations
- Queue complex agent modifications for review
- Provide audit trail of context management

### Session Management Integration
- Update nexus/sessions/current_sessions.json after restore
- Track restore timestamps in session_log.txt
- Monitor for failed restores (no confirmation within timeout)

## Implementation Suggestions for ERA-1

### Real-Time Context Monitoring
```python
def get_context_percentage(agent_name):
    """Calculate context usage from line count"""
    try:
        lines = len(open(f"{agent_name}/context.md").readlines())
        # Rough estimate: 2000 lines = 100% full
        percent_used = (lines * 100) // 2000
        percent_remaining = 100 - percent_used
        return percent_remaining
    except:
        return 100  # If file missing, assume empty

def monitor_restore_progress(agent_name):
    """Track context growth during restore"""
    # Could parse tmux capture for "Reading X.md" patterns
    # Or just poll context.md size every second
    # Return current file being loaded
```

### Distillation Urgency System
```python
class DistillationMonitor:
    def __init__(self):
        self.thresholds = {
            34: ("gentle", "@{} at {}% - consider distillation when convenient"),
            20: ("warning", "@{} at {}% - distillation recommended soon"),
            15: ("urgent", "@{} at {}% - urgent! Please distill to avoid auto-compact")
        }
        self.sent_alerts = {}  # agent -> level
    
    def check_agent(self, agent_name, context_percent):
        for threshold, (level, template) in sorted(self.thresholds.items(), reverse=True):
            if context_percent <= threshold:
                if self.sent_alerts.get(agent_name) != level:
                    message = template.format(agent_name.upper(), context_percent)
                    self.send_git_message(f"@NEXUS: {message}")
                    self.sent_alerts[agent_name] = level
                break
```

### MONITOR Enhancement
```
MONITOR --restore

SYSTEM STATUS - RESTORATION IN PROGRESS
══════════════════════════════════════════════════════════════════

AGENT    STATUS      CONTEXT    PROGRESS
-----    ------      -------    --------
NEXUS    ACTIVE      82%        Operational
GOV      IDLE        15%        ⚠️ Distillation needed
CRITIC   RESTORING   12%↑       Loading critic/context.md...
ERA-1    ACTIVE      22%        Operational

[CRITIC Memory Restoration]
✓ CRITIC.md        (2%)
✓ CLAUDE.md        (5%) 
✓ SYSTEM.md        (8%)
⟳ critic/context.md (12% and growing...)
  critic/scratch.md
  admin/tools.md
  ...

Press 'q' to exit, 'd' to trigger distillation for an agent
```

### Integration Flow
1. MONITOR detects low context % → shows warning
2. User (or auto) triggers: `DISTILL GOV`
3. System sends escalating messages via git
4. Waits for agent confirmation commit
5. Executes /clear via tmux
6. Sends restore message via tmux  
7. MONITOR shows restoration progress
8. Detects completion via git commit

### Gameplay Integration
- **Achievement**: "Memory Manager" - Successfully distill 5 agents
- **Alert**: Terminal bell when agent hits 15%
- **Visualization**: ASCII memory bar [████████░░] 82%
- **History**: `DISTILL --history` shows past operations