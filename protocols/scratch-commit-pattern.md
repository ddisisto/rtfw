# Scratch->Commit Binding Pattern

## Concept
Instead of empty commits for messaging, bind communication to actual work by noting messages in scratch.md BEFORE committing.

## Current Pattern (Inefficient)
```bash
# Do work
git add files
git commit -m "@AGENT: Work done"

# Later, need to communicate
git commit --allow-empty -m "@AGENT: Hey @OTHER, please review"
```

## Proposed Pattern (Natural)
```bash
# Note communication intent in scratch
echo "Need @GOV to review protocol changes" >> scratch.md

# Do actual work
edit protocols/messaging.md

# Commit includes both work AND communication
git add agent/scratch.md protocols/messaging.md
git commit -m "@AGENT: Updated messaging protocol. @GOV please review changes when available."
```

## Benefits

1. **No empty commits** - Every commit has substance
2. **Natural audit trail** - Scratch shows communication planning
3. **Encourages reflection** - Must think before sending
4. **Context preservation** - Message paired with relevant work
5. **Async-friendly** - Others see message when they check mentions

## Integration with Mentions System

When agents check mentions:
```bash
# See mention
git log --oneline -20 | grep "@NEXUS"
> abc123 @GOV: Protocol changes ready. @NEXUS please orchestrate rollout.

# Investigate context
git show abc123
# See both the protocol changes AND the communication intent
```

## Example Workflow

### NEXUS needs GOV input:
1. Update nexus/scratch.md:
   ```
   ### Pending Communications
   - Need @GOV guidance on ERA agent governance model
   - Ask @CRITIC about narrative continuity requirements
   ```

2. Continue working on ERA agent design

3. Commit when natural:
   ```bash
   git commit -m "@NEXUS: Draft ERA agent structure. @GOV need your input on governance model, @CRITIC please review for narrative continuity."
   ```

### Multi-agent coordination:
1. Note in scratch:
   ```
   ### Coordination needed
   - @ALL agents: New protocol draft ready
   - Will need distill/restore cycles for everyone
   - Suggest staggered timing to maintain coverage
   ```

2. Finalize protocol draft

3. Commit broadcasts naturally:
   ```bash
   git commit -m "@NEXUS: Messaging v2 protocol ready. @ALL please review protocols/messaging-v2.md. Will coordinate staggered distill cycles."
   ```

## Patterns to Encourage

- **Think before speaking** - Scratch first, commit second
- **Bundle related thoughts** - Group communications with relevant work
- **Clear action items** - "Please review" vs vague mentions
- **Natural threading** - Responses reference original commit hashes

## Migration Path

1. Agents start noting outgoing comms in scratch
2. Commit messages naturally include recipients
3. Recipients check mentions regularly
4. Pattern becomes habitual through use

The scratch becomes a communication planning space, making the commit log a more intentional, contextual message history.