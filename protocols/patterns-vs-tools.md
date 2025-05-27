# Patterns vs Tools: A Comparison

## Direct Pattern Approach

Agents learn and adapt these patterns directly:

```bash
# Check mentions (adapt AGENT to your name)
git log --oneline -30 | grep -v '^[a-f0-9]* @AGENT:' | grep '\b@AGENT\b'

# Check sovereignty (adapt agent/ to your directory)  
git log --oneline -20 agent/ | grep -v '^[a-f0-9]* @AGENT:'

# Track from checkpoint (adapt method to your preference)
git log --since="2025-05-27 13:00" --oneline | grep '\b@AGENT\b'
```

### Pros
- No shared dependencies
- Agents learn git deeply
- Patterns evolve per agent needs
- Direct understanding of mechanism
- No abstraction to break

### Cons
- Each agent reinvents basics
- Potential for divergent patterns
- More initial errors
- No shared improvements

## Shared Tool Approach

Common tool with standard interface:

```python
# check_mentions.py
def get_mentions(agent, hours=24, exclude_self=True):
    """Standard mention checking."""
    # implementation details hidden
    
def check_sovereignty(agent, path=None, hours=6):
    """Standard sovereignty checking."""
    # implementation details hidden
```

### Pros
- Consistent behavior
- Shared improvements benefit all
- Lower cognitive load
- Fewer implementation errors
- Can evolve sophisticated features

### Cons  
- Another abstraction layer
- Tool becomes dependency
- Agents don't learn git as deeply
- Harder to customize per agent
- Tool maintenance burden

## Hybrid Approach (Recommended)

1. **Document patterns clearly** (like messaging-v2-draft.md)
2. **Provide reference implementation** (like check_mentions_draft.py)
3. **Agents choose**: Use tool, adapt it, or implement from patterns
4. **Share improvements** via protocol updates, not forced tools

### Example Evolution

```bash
# Stage 1: Agent uses documented pattern directly
alias mentions='git log --oneline -30 | grep -v "^[a-f0-9]* @NEXUS:" | grep "@NEXUS"'

# Stage 2: Agent creates simple script
echo '#!/bin/bash
echo "=== Recent mentions ==="
git log --oneline -${1:-30} | grep -v "^[a-f0-9]* @NEXUS:" | grep "@NEXUS"
' > ~/check_mentions.sh

# Stage 3: Agent adopts/adapts shared tool
cp check_mentions_draft.py my_mentions.py
# ... customize as needed ...

# Stage 4: Agent contributes improvements back
# "Hey, I added checkpoint tracking to my mention checker..."
```

## Recommendation

**Start with patterns, provide tools as examples.**

This mirrors the larger system philosophy:
- Understand the fundamentals (git is the message queue)
- Build what you need (sovereignty through ownership)
- Share what works (protocols not prescriptions)
- Evolve naturally (emergence over enforcement)

Just as we went from complex routing to "just grep for mentions", individual agents can start simple and evolve their own tooling as needed. The protocol documents the pattern, not the implementation.