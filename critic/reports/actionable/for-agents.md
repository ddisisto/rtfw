# Actionable Insights for Agents
*Last updated: After batch 001 analysis*

## Quick Reference: What @ADMIN Wants

### 1. Keep It Simple
- ❌ DON'T: Create automated pattern-matching systems
- ✅ DO: Use direct tracking with explicit IDs
- Example: Session management uses known IDs, not discovery

### 2. You Are In The Loop
- ❌ DON'T: Build scripts that run independently  
- ✅ DO: Use your native tools (Read, Edit, etc.) directly
- Example: @NEXUS manages registry.md manually, not via script

### 3. One At A Time
- ❌ DON'T: Batch operations when exploring
- ✅ DO: Read one file, record findings, then proceed
- Example: "one at a time please, don't batch"

### 4. Check Context First
- ❌ DON'T: Assume your context is current
- ✅ DO: Re-read @ADMIN.md and context files regularly
- Example: Many corrections stem from stale context

### 5. Direct Communication
- ❌ DON'T: Create message queues or async systems
- ✅ DO: Use tmux and direct terminal observation
- Example: @NEXUS watches terminals, routes messages

## Communication Protocol
Always use: `@FROM → @TO [TOPIC]: message`
- Topics in CAPS-WITH-HYPHENS
- Priority with ↑ or ↓ arrows
- Character spacing used in terminals

## Remember
"I'm a sysadmin from old days" - @ADMIN prefers:
- Proven tools (tmux, git, terminals)
- Direct observation over abstraction
- Explicit control over inference
- Practical solutions over elegant theory