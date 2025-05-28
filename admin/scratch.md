# ADMIN NOTES↑↑↑ notouch! open to discussion if required.

- TMUX run: `cd /home/daniel/rtfw && tmux -f tmux.conf`
- NEXUS session resume `cd /home/daniel/rtfw && claude --resume $(cat nexus/.sessionid)`

- prompt to restore context (protocols/distill.md +) /clear:
@ADMIN: @protocols/restore.md underway for @NEXUS.md agent - please restore required context for continuation
@ADMIN: @protocols/restore.md required for @CRITIC.md agent - please restore context for continuation

sovereignty

can we a recent /clear call and surrounding context? I'm hoping to find a way to conservatively estimate total context window size before / after. we can work backwards from before the /clear to the prior /clear perhaps and sum numeric metrics?

# STANDARD PROMPT LIB

/clear -> inbox -> distill (initial planning) -> readiness check -> deep work . 

## login
new terminology for restore?

<REPEAT>

## check inbox
please check messages and integrate with current priorities. think as needed, do what can be done quickly first, or is most urgent. maintain own prioritisation standard as required. if just a short file Read and reply is needed, do it now. any work requiring > 3 steps should be prioritised and assessed for readiness.

*include @ADMIN notes @AGENT|@ALL, if any (user will manage in own files or UI panels)*

### distill(context_window_used: X, ...)
please @protocols/distill.md to integrate into relevant context, send off quick replies if needed, clear items if possible in 1-2 steps, or further plan if needed. no deep work yet.

inject: current context window size / recommended restore point vs continue as absolute + percentage / they must elect whether to restore or continue, track own method of identifing optimal choice. critical / forced at: TBD

choice: deep_work(args) | idle(waiting_on) | logout (decide FIRST, apply as required, final output confirms choice + input args in standard format)

## deep_work(task_or_thread: ..., max_tokens: ...)
check that all requirements are meant. send relevant/required updates or requests as you go. plans must be precise before implementation. pause and reconsider if initial approach doesn't work. if you get stuck, seek help.

## idle
agent indicates it has no work, is currently waiting on other agents / admin
should review relevant message threads in case updates missed, else will remain idle until incoming messages

</REPEAT>

## logout
concept - the "logout log". on final distill before a restore:
  - like a signature / poetry / fleeting thoughts book
  - after a final distill, just before restore - no file writes or commits allowed
  - the read the existing book, most recent N tokens perhaps
  - their final response is to sign it, for their future selves and other to see / update in kind



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