# ERA-1 Scratch

## Continuity Bridge
- engine-debug: Fixed race condition in 49eb171, still stuck at bootstrap
- state-detection: Engine sees commits but not extracting states for ERA-1
- Next: Investigate why ERA-1 differs from other agents
- **FIXED**: Hyphen in ERA-1 broke regex pattern in git_monitor.py
  - Changed `\w+` to `[\w-]+` to match hyphenated agent names
  - Engine needs restart (runs in separate terminal, ask @ADMIN)
- **FIXED**: Inbox transition now updates last_read_commit_hash
  - Sets checkpoint at exact inbox entry commit
  - Resets unread_message_count to 0
  - Unread count already correctly filters mentions only

## Message Checkpoint
Last processed: 49eb171 at 2025-05-29T20:20:21