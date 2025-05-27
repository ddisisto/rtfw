# Tool Migration Plan: session_query v1 → v2

## Assessment

### V2 Improvements
- ✓ No index dependency (works with any JSONL)
- ✓ Context windows (--before/--after)
- ✓ Better format handling (preserves tool details)
- ✓ Intervention detection (--interventions flag)
- ✓ Agent auto-detection (no CSV needed)
- ✓ Stats mode for analysis

### Tools That Can Be Replaced
1. **extract_admin_interventions.py** → Use `--interventions --user-type external`
2. **extract_user_prompts.py** → Use `--type user --user-type external`
3. **extract_session_timestamps.py** → Built into v2 output

### Tools Still Needed (Domain-Specific)
1. **categorize_interventions.py** - Applies specific taxonomy
2. **analyze_intervention_evolution.py** - Tracks learning patterns
3. **unified_state.py** - Different purpose (system monitoring)

## Migration Steps

### 1. Update Documentation
Files mentioning session_query.py:
- scratch.md → Update example to v2 syntax
- context.md → Update self-archaeology reference
- Various analysis docs → Update command examples

### 2. Compatibility Alias
Create symlink for backward compatibility:
```bash
ln -s session_query_v2.py session_query.py
```

### 3. Cleanup Redundant Tools
After verification:
```bash
rm extract_admin_interventions.py
rm extract_user_prompts.py
rm extract_session_timestamps.py
```

### 4. Update Context
Note in context.md that v2 is the standard tool

## New V2 Usage Examples

```bash
# Find interventions with context
python session_query_v2.py --interventions --before 2 --after 1

# Search with full context
python session_query_v2.py --pattern "specific phrase" --before 3 --after 3

# Get statistics
python session_query_v2.py --agent CRITIC --format stats

# No index needed!
python session_query_v2.py --pattern "any search" 
```