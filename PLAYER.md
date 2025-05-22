***NOTE***
The @ADMIN owns this file. You may remove items addressed to you if completed. I will review regularly, and treat this as my own scratchpad. @GOV should move items from here to @ANNOUNCEMENTS.md as appropriate, or others should take items off (or update status) as appropriate. If an item addressed to you only please add to own scratch or context, update status from [ ] to one of -
[*] Acknowledged / in-progress
[!] More details or discusion required
[-] Completed / integrated, ready for review and remove 

---

[-] @NEXUS
"Each agent runs in dedicated tmux session" - correction: each runs in a *window*, all within the same *session*

required reading at some point 
- `man tmux`
- https://docs.anthropic.com/en/docs/claude-code/sdk

startup - nexus is window 0, started by admin. First task - identifies required agents, existing sessions files, etc

`tmux new-window -n <AGENT> /bin/bash`
then 
`tmux send-keys -t <AGENT> 'claude --resume <SESSION_ID>' Enter`
descision point - `claude -p` or not? this runs in non-interactive mode, can output e.g. json / json-stream, can set max-turns, permission-prompt-tool <- points back to nexus or gov? requires resolution of https://github.com/anthropics/claude-code/issues/1175

terminal bell indicates completion of activity? -
  `claude config set --global preferredNotifChannel terminal_bell`

then some maybe useful tmux commands -

`tmux set-window-option -t <AGENT> <OPTION>`, where <OPTION> values include -
monitor-content match-string
Monitor content in the window. When fnmatch(3) pattern match-string appears in the window, it is highlighted in the status line.

monitor-silence [interval]
Monitor for silence (no activity) in the window within interval seconds. Windows that have been silent for the interval are highlighted in the status line. An interval of zero disables the monitoring. 

Then you loop through each agent requiring attention (regular list window status), check latest outputs (todo: piped to a file or other buffer)
forward a message or provide direct instruction `tmux send-keys -t <AGENT> '<message or instructions>' Enter`
interrupt ongoing work so we can input messages `tmux send-keys -t <AGENT> Escape`
select default option when choices presented `tmux send-keys -t <AGENT> Enter`
abort proposed action when choices presented `tmux send-keys -t <AGENT> Escape`
    (requires immediate followup - explaination, redirect, new instructions, etc)
---

[*] @NEXUS
I think the jsonl session files that claude code natively maintains can be used instead of capture-pane. Not well documented and potentially not stable, but for now seems like this will be more accurate and direct. Can e.g. keep a pointer (just remember prev. length even) on each and then read on. Might want to pre-process with jq once we understand the format. Certainly don't want to monitor all output of all sessions, as context window here would explode, so need to be selective. Not sure if this makes clear when e.g. a session is current waiting for user input, but could maybe combine with tmux silence monitor (10 sec) then capture-pane to be sure.
read - /home/daniel/.claude/projects/-home-daniel-prj-rtfw/bf7a50b0-607c-43c6-bb3e-1507b9d29d7f.jsonl
a very simple exchange where I directly asked to create a file, it proposed the file write and waited for my approval (nb. selective auto-approval can and will be used normally, need to learn how to set this up as required). I waited a while, then approved.