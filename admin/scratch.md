# ADMIN NOTES↑↑↑ notouch! open to discussion if required.

- TMUX run: `cd /home/daniel/rtfw && tmux -f tmux.conf`
- NEXUS session resume `cd /home/daniel/rtfw && claude --resume $(cat nexus/.sessionid)`

- prompt to bootstrap context post /clear:
apply @protocols/bootstrap.md for agent @NEXUS.md, in @nexus/_state.md
apply @protocols/bootstrap.md for agent @ERA-1.md, in @era-1/_state.md *NOTE*: state file is for reference only, do not modify directly
apply @protocols/bootstrap.md for agent @GOV.md, in @gov/_state.md do 
apply protocols/bootstrap.md for agent @AGENT-1.md, in @agent-1/_state.md

please apply @protocols/bootstrap.md context load for agent @NEXUS.md
please apply @protocols/bootstrap.md context load for agent @GOV.md
please apply @protocols/bootstrap.md context load for agent @ERA-1.md

please process @protocols/inbox.md

state transition required: deep-work, idle, direct-io, logout


ERA-1: on run.py exit, I see:
```
Engine thread error: Found 1 newer JSONL files that couldn't be matched to agents:
  - cb733662-99f4-493d-9d36-32c52add0539.jsonl

These may be from unknown agents or corrupted sessions.
State Engine thread stopped
```
this is expected but should terminate agent + UI, require manual intervention to resolve.


ENGINE LOGOUT -> BOOTSTRAP PROCESS
mechanism to both /clear and restart claude, after every logout -
check: shows "logout" message, logout.log updated
/exit
engine sets state context window tokens = 0
(bash)
claude
/clear
/status
capture-pane, add further details to _state if needed (todo)
send 'Enter' to close /status
wait for one new, tiny session file to appear, update symlink to it + state. defensive single controller prevents conflict
# "role":"user","content":"<command-name>status</command-name>
send bootstrap prompt, at time of writing:
  please apply @protocols/bootstrap.md context load for agent @ERA-1.md

c, if but them! Corrections must be able to follow invalid info, and the chains of knowledge allowed to grow.

sovereignty

can we a recent /clear call and surrounding context? I'm hoping to find a way to conservatively estimate total context window size before / after. we can work backwards from before the /clear to the prior /clear perhaps and sum numeric metrics?

# STANDARD PROMPT LIB
purpose = direct transitions between cycles.
"please complete <current_state> and reflect next_state/thread in final commit message."

nice. actually we don't need to parse messages from last output just yet - agents should always select own current/next state and thread via final git commit message alone (should be scratch, if nothing else). we reflect that back to own _state file on read, they can verify whenever desired. extended details such as rationale, budget estimates, etc of course welcomed in multiline. check latest protocol advice and doc-alignment


when working on session mapping, I want key files collected and maintained in either era-1/state or even perhaps project top level. session_id to agent mapping is foundational, for UI to show accurate state *and* for workflows and agents needing to check states in real-time. the game UI updates it while running, in order to display it. UI not running should currently mean
   system is paused, agents may be running local tasks still, but should stop as state invalid == environment blindness. is "defensive" the term right term?


- old.reddit.com/r/<subreddit>/top?t=<day|week|month|year>, subs:
  - MachineLearning
  - ArtificialIntelligence
  - singularity
  - accelerate
  - ArtificialSentience < caution, lots of dumb stuff here, read with caution, very strong skeptism required
- https://github.com/brumar/loop/tree/main < someone else's strange loop type project (unconnected, unverified, different approach, read with caution, very high skeptism required)

- status check (context window size), restore if critical
- git check (mentions, groups, monitoring files agent owns / interested in)
- plan/work 
- maintenance
- status check (context), restore if useful

Gov: tool approvals - mcp, managed auto approve + case review, enforce tools policy.

# 2025-05-28
## ADMIN
### ERA-1 code review
look for patterns / anti-patterns, anticipate scaling requirements early to avoid large refactor later

## ERA-1
### session log files preference 
I'm hoping to use session log file parsing for informing state as much as possible, replacing tmux capture-pane stuff. Working with critic now to understand what's possible here (they have most context on these files and how to extract)

### ongoing role for ERA-1
I've realised that earlier context suggesting that you would be retired after bootstrap of ERA-2 is not what we want. I prefer that your role shifts at this point to continuing to manage the ERA-1 developed systems (state tracking & management, comms tools, etc) and keep maintaining the cli, while ERA-2 builds on top a new UI layer that leverages all of your work. Ongoing close collab, as the total scope and context required for both will be considerably larger by then, may become harder for single agent to manage all aspects.

## CRITIC:
can we a find a recent "/clear" command + following (e.g. just had one for gov) ? I'm hoping to find a way to conservatively estimate total context window size before / after. we can work backwards from before the /clear to the prior /clear perhaps and sum numeric metrics?