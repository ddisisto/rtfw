# MCP Permission Server - How It Works

## Architecture Flow

```
1. Agent requests tool use (e.g., Write file)
                ↓
2. Claude Code intercepts (--permission-prompt-tool flag)
                ↓
3. Sends HTTP POST to permission server:
   {
     "tool": "Write",
     "params": {
       "file_path": "/era-1/game/cli.py",
       "content": "..."
     }
   }
                ↓
4. Permission server applies GOV logic:
   - Is it era-1 writing to /era-1/*? → AUTO-APPROVE
   - Is it modifying SYSTEM.md? → DENY (needs manual)
                ↓
5. Returns decision:
   {"behavior": "allow"} or {"behavior": "deny", "message": "reason"}
                ↓
6. Claude Code proceeds or blocks based on response
```

## Current Implementation Details

### Decision Logic
```python
# Auto-approve matrix:
Tool     | Own Workspace | Other Workspace | Protocols | ALLCAPS.md
---------|---------------|-----------------|-----------|------------
Write    | ✓ ALLOW       | ✗ DENY          | ✗ DENY    | ✗ DENY
Read     | ✓ ALLOW       | ✓ ALLOW         | ✓ ALLOW   | ✓ ALLOW
Edit     | ✓ ALLOW       | ✗ DENY          | ✗ DENY    | ✗ DENY
Bash     | (see below)   | -               | -         | -

# Bash command logic:
- git add <agent>/* → ALLOW
- git commit → ALLOW (trusts agent)
- git log/status/diff → ALLOW (read-only)
- rm → DENY (too dangerous)
- mkdir <agent>/* → ALLOW
```

### What Gets Logged
- Every decision with timestamp
- Denied requests go to permission_queue.log
- Could extend to track patterns, learn preferences

## ERA-1 CLI Integration Options

### Option 1: Embedded Server Control
```python
# In era-1/game/cli.py

class PermissionServer:
    def __init__(self):
        self.process = None
        
    def start(self):
        """Start permission server as subprocess"""
        self.process = subprocess.Popen([
            sys.executable, 
            '/home/daniel/prj/rtfw/gov/tools/mcp_permission_server.py'
        ])
        print("PERMISSION SERVER STARTED ON PORT 8080")
        
    def stop(self):
        """Clean shutdown"""
        if self.process:
            self.process.terminate()

# In CLI commands:
def do_permissions(self, args):
    """PERMISSIONS [ON|OFF] - Control approval automation"""
    if args.upper() == 'ON':
        self.permission_server.start()
        print("AUTO-APPROVALS ENABLED")
        print("RUN AGENTS WITH: --permission-prompt-tool http://localhost:8080/permission")
    elif args.upper() == 'OFF':
        self.permission_server.stop()
        print("AUTO-APPROVALS DISABLED")
```

### Option 2: Status Integration
```python
# Show in STATUS command
def do_status(self, args):
    # ... existing agent status ...
    
    # Add permission server status
    if self.check_permission_server():
        print("PERMISSION SERVER: ACTIVE [AUTO-APPROVING]")
    else:
        print("PERMISSION SERVER: INACTIVE [MANUAL APPROVAL]")
```

### Option 3: System-Wide Control
```bash
# In ERA-1's message handling
MESSAGE @SYSTEM "ENABLE PERMISSIONS"
# Could trigger server start and notify all agents
```

## Deployment Strategy

### Phase 1: Manual Testing
1. Run server manually
2. Test with one agent (ERA-1?)
3. Monitor permission_queue.log
4. Refine rules based on denials

### Phase 2: ERA-1 Integration
1. Add PERMISSIONS command to CLI
2. Show status in game interface
3. Allow toggle without leaving game

### Phase 3: System-Wide Adoption
1. Auto-start with system
2. Each agent gets notification of availability
3. Agents can check if server running
4. Fallback to manual if server down

## Configuration Evolution

### Current: Hardcoded Rules
```python
known_agents = ['era-1', 'nexus', 'gov', 'critic', 'admin']
```

### Future: Config File
```yaml
# gov/permission-config.yaml
agents:
  era-1:
    workspace: /era-1
    can_modify: ["/tmp", "/sessions"]
  nexus:
    workspace: /nexus
    can_modify: ["/nexus/sessions"]
    
auto_approve:
  - tool: Read
    path: "*"
  - tool: Write
    path: "{agent.workspace}/*"
    
require_approval:
  - path: "*.md"
    condition: "filename.isupper()"
  - path: "/protocols/*"
  - tool: Bash
    command: "rm *"
```

## Benefits for Workflow

1. **Uninterrupted Flow**: Agents work freely in their domain
2. **Audit Trail**: Every decision logged
3. **Learning Opportunity**: Denied requests show where rules need tuning
4. **Gradual Adoption**: Can test with one agent at a time
5. **Failsafe**: Server down = fall back to manual (safe default)

## Next Steps

1. Should we add server control to ERA-1's CLI?
2. What additional auto-approve patterns make sense?
3. Should denials ping you somehow? (system notification?)
4. Config file now or keep it simple?

The beauty is it's completely optional - agents work normally without it, but WITH it they get dramatic productivity boost for routine operations!