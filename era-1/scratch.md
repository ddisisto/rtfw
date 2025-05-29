# ERA-1 Scratch

## Continuity Bridge
- engine-debug: Fixed race condition in 49eb171, still stuck at bootstrap
- state-detection: Engine sees commits but not extracting states for ERA-1
- Next: Investigate why ERA-1 differs from other agents
- **FIXED**: Hyphen in ERA-1 broke regex pattern in git_monitor.py
  - Changed `\w+` to `[\w-]+` to match hyphenated agent names
  - Engine needs restart (runs in separate terminal, ask @ADMIN)
- **FIXED**: Inbox checkpoint now happens on EXIT not entry
  - Better logic: confirms messages were actually read
  - Exception: inbox→direct_io skips update (likely "skip inbox" command)
  - Sets last_read_commit_hash to exit commit
  - Resets unread_message_count to 0
  - Unread count already correctly filters mentions only

## Message Checkpoint
Last processed: 49eb171 at 2025-05-29T20:20:21

## Engine Priorities Completed (2025-05-29)
1. ERA-1 state detection fixed (hyphen handling)
2. Inbox checkpoint on exit (not entry)
3. Skip checkpoint for inbox→direct_io transitions
4. 7-char hash display to match git log --oneline

## My Engine Priorities
- last_write_commit updates seem delayed (needs investigation)
- Terminal UI command implementations (`message`, `todos`, etc.)
- State transition prompts from engine
- Session idle detection refinements