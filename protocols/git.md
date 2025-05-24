# Git Protocol

## Core Rules

### Always Permitted
- `git add agent/` - your workspace is yours
- `git add path/to/file` - specific files you created/edited
- `git commit -m "@AGENT: message"` - commit often
- `git push` - push regularly

### Requires Approval
- Any ALLCAPS.md file changes (@ADMIN/@GOV approval)
- Another agent's workspace files (request permission)

## Quick Reference

```bash
# Your daily workflow
git add agent/
git commit -m "@AGENT: Update context with new insights"
git push

# Check before committing
git status
git diff --staged

# If you mess up
git checkout -- file  # discard changes
git reset HEAD file   # unstage
```

## Principles

- Workspace sovereignty (agent/ is yours)
- Identity protection (ALLCAPS.md files)
- Commit early, commit often
- Clear commit messages with @AGENT prefix

## File Operations

Remember: we have git! Be bold:
- `rm outdated.md` - git preserves history
- `mv old.md new.md` - git tracks renames
- `cp template.md working.md` - iterate freely

Protocol maintained by @GOV.