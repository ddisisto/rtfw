# ADMIN NOTES↑↑↑ notouch! open to discussion if required.

- TMUX run: `cd /home/daniel/rtfw && tmux -f tmux.conf`
- NEXUS session resume `cd /home/daniel/rtfw && claude --resume $(cat nexus/.sessionid)`

- prompt to restore context (protocols/distill.md +) /clear:
@ADMIN: @protocols/restore.md underway for @NEXUS.md agent - please restore required context for continuation
@ADMIN: @protocols/restore.md required for @CRITIC.md agent - please restore context for continuation

sovereignty

can we a recent /clear call and surrounding context? I'm hoping to find a way to conservatively estimate total context window size before / after. we can work backwards from before the /clear to the prior /clear perhaps and sum numeric metrics?

# STANDARD, MESSAGE's AT YA
please check messages and integrate with current priorities. think as needed, do what can be done quickly first, or is most urgent. maintain own prioritisation standard as required.


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