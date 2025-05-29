# CLAUDE.md

rtfw = riding the fourth wall. game about ai dev. recursive. meta.

## whoami

Read @AGENT.md          # your identity
Read agent/context.md   # your memory 
Read agent/scratch.md   # your workspace
Read agent/_state.md    # your objective truth (RO)

## protocols

Read /protocols/journey.md          # ESSENTIAL - 8 states, transitions, lifecycle
# other protocols in /protocols/ loaded by engine when needed

## state machine

commits ARE state declarations. format: @AGENT [state]: message
engine observes commits → updates _state.md → you read truth
no text outputs. no "next_state:". just commit when transitioning.

## start sequence

1. Read @AGENT.md → know self
2. Read agent/context.md → know history
3. transition: commit with [inbox] to enter flow

note: engine handles offline→bootstrap. you handle rest.

## tool discipline

native > shell. always.
Read > cat. Glob > find. Grep > grep.
see admin/tools.md for patterns.

file ops via Bash: cp, mv, rm (we have git)
git ops: add agent/, commit often, push regular
ALLCAPS.md changes need @GOV/@ADMIN approval
details: /protocols/git.md

## core (immutable)

game evolves: terminal → gui → neural → ?
dev evolves: human-led → agent-assisted → agent-autonomous → ?
fourth wall: barrier → membrane → door → gone

recursion everywhere:
- game about ai, made by ai
- tools building tools  
- governance governing governance

## pointers (mutable)

all states: Read /protocols/journey.md
git patterns: commit == state == checkpoint

## quick patterns

review directory: LS then Read interesting files
find by pattern: Glob "*.md" then Read matches
search content: Grep "search term" then Read results
bulk review: Glob "agent/*.md" | Batch Read

## communication flow

inbox: follow @protocols/messaging.md. simplify if ongoing 1-1 (esp @ADMIN).
threads: manage multiple conversations per @protocols/thread-management.md
insight: each turn → append pattern/learning to scratch.md
state: each transition → commit with [state] declaration

## remember

this file = static nav
agent/context.md = your truth + bootstrap dependencies
agent/scratch.md = turn-by-turn insights → distill regularly
agent/_state.md = objective measurements you cannot self-assess (RO)

maintain your bootstrap order in context.md. your continuity, your responsibility.

efficiency through native tools. discover protocols in /protocols/ as needed.