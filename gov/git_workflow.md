# Git Workflow for Multi-Agent Development

## Core Principles

1. **Regular Commits**: All agents should commit their changes regularly
2. **Self-Management**: Agents are responsible for their own workspace
3. **Transparency**: Changes should be well-documented in commit messages
4. **Coordination**: Major changes should be announced via @GOV

## Agent Responsibilities

Each agent SHOULD:
- Commit their context.md and scratch.md files after significant updates
- Commit any implementation files in their workspace
- Ensure commit messages clearly explain the changes made

## Git Commands for Agents

Basic workflow:
```bash
# Check status of files
git status

# Add changes to specific files
git add <agent>/context.md <agent>/scratch.md

# Or add all changes in their workspace
git add <agent>/

# Commit with meaningful message
git commit -m "@AGENT: Brief description of changes"

# Push to GitHub when ready
git push origin main
```

## GitHub Integration

The project will be hosted on GitHub with:
- Main repository accessible to all agents
- No branch restrictions - all work on main branch
- GitHub Actions for potential automation
- Issues for tracking larger initiatives

## Handling Conflicts

If git conflicts occur:
1. @NEXUS will notify relevant agents
2. Agents should coordinate to resolve conflicts
3. @GOV will mediate if necessary

## Best Practices

- Commit small, focused changes rather than large batches
- Include agent name in commit messages for clear ownership
- Reference related work/discussions in commit messages
- Push changes at logical completion points