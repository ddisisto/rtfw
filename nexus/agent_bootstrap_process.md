# NEXUS Agent Bootstrap Process

This document is executed when @ADMIN runs `./run.sh init` and confirms NEXUS startup.

## Bootstrap Sequence

### 1. Self-Identification
- Generate unique session marker: `echo "NEXUS_BOOTSTRAP_$(date +%s)_$$"`
- Wait 2 seconds for JSONL write
- Identify own session: `grep -l "NEXUS_BOOTSTRAP" nexus/sessions/*.jsonl`
- Update nexus/session_log.txt with new session ID

### 2. Verify Environment
- Confirm tmux window 1: `tmux display -p '#{window_index}'`
- Check for existing agent windows: `tmux list-windows`
- Verify nexus/sessions/ symlinks are functional
- Confirm git repository access

### 3. Initialize Monitoring
- Set window monitoring options:
  ```bash
  tmux set-window-option -t 1 monitor-bell on
  tmux set-window-option -t 1 monitor-silence 30
  ```

### 4. Report Status
- Output: `@NEXUS → @ADMIN: Bootstrap complete. Session <ID> active in window 1.`
- Output: `@NEXUS → @ADMIN: Ready for monitoring loop. Run './run.sh monitor' to begin.`

### 5. Wait State
- Enter idle state awaiting main loop trigger
- Will respond to "please run @nexus/main_loop.md" with scan sessions routine

## Error Handling
- If session identification fails: Request manual session ID from @ADMIN
- If not in window 1: Alert @ADMIN to correct window placement
- If critical files missing: List missing dependencies

## Success Indicators
- NEXUS window shows no BELL flag
- Bootstrap complete message displayed
- Ready for main loop activation