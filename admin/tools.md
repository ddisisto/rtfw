# Claude Code Tools Guide (Condensed)

## Key Principles

1. **Use native tools over shell commands**
   - Glob/Grep > find/grep
   - Read > cat
   - LS > ls
   - Edit/MultiEdit > sed/awk

2. **Unix/Linux equivalents**
   - Glob: `find -name` pattern matching
   - Grep: `rg` (ripgrep) for content search
   - LS: `ls` for directory listing
   - Read: `cat -n` with line numbers
   - Edit: `sed -i` for in-place edits
   - MultiEdit: Multiple `sed` operations atomically
   - Bash: Direct shell execution (when no native tool exists)

## Optimal Usage Patterns

### File Discovery
- **Pattern search**: Glob → Read → Edit
- **Content search**: Grep → Read → Edit
- **Multi-file ops**: Glob → Batch(Read + Edit)

### Performance Tips
- Use Batch for parallel operations
- Read files completely vs chunks
- MultiEdit for multiple changes to same file
- Direct tool use over command chains

## Critical Anti-Patterns
- ❌ `Bash: grep/find/cat/ls` when native tools exist
- ❌ Multiple Edit calls vs one MultiEdit
- ❌ Sequential operations that could be batched
- ❌ Writing scripts to parse output vs direct tool results

## Tool Selection Policy
1. Native Claude tool > Shell equivalent
2. Specific tool > General tool chain
3. Batch parallel > Sequential execution
4. Direct interpretation > Script parsing

## File Operations
Use Bash for file management (no native tools):
- **Copy**: `cp source dest`
- **Move**: `mv source dest`
- **Remove**: `rm file` (we have git!)
- **Mkdir**: `mkdir -p path/to/dir`

## Git Operations
Always via Bash:
- **Stage**: `git add agent/` (or specific files)
- **Commit**: `git commit -m "@AGENT: message"`
- **Push**: `git push` (regularly)
- **Status**: `git status` (check often)

ALLCAPS.md files require @GOV/@ADMIN approval before changes.

The key is maximizing efficiency through native tools and parallel execution while minimizing shell command usage and intermediate processing steps.