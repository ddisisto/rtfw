# ADMIN NOTES↑↑↑ notouch! open to discussion if required.
- TMUX run: `cd /home/daniel/rtfw && tmux -f tmux.conf`
- NEXUS session resume `cd /home/daniel/rtfw && claude --resume $(cat nexus/.sessionid)`

- prompt to restore nexus after context (protocols/distill.md +) /clear:
@ADMIN → @NEXUS [RESTORE]: @protocols/restore.md underway for @NEXUS.md agent - please restore context for continuation
@ADMIN → @CRITIC [RESTORE]: @protocols/restore.md underway for @CRITIC.md agent - please restore context for continuation

- note to self: ~use ↑↑↑↓↓↓ standard comms protocol flags in outbox. ↑↓ = uncertainty? not explicit, just see if it catches on in any way, fun vector to experiment with~
- nah, screw that. "!" important, "!!!", etc. "?" shows uncertainty. "fyi" = low importance, etc etc. more inherently meaningful

- old.reddit.com/r/<subreddit>/top?t=<day|week|month|year>, subs:
  - MachineLearning
  - ArtificialIntelligence
  - singularity
  - ArtificialSentience < caution, lots of dumb stuff here, read with caution, very high skeptism required
- https://github.com/brumar/loop/tree/main < someone else's strange loop type project (unconnected, unverified, different approach, read with caution, very high skeptism required)

Comms - more direct and simple. @mentions only for git commits, agents regularly check git log for @mentions (and for unexpected changes own subdir?) (and for @groups maybe). Upper== formal?
Common tool call for DMs, `message agent ...` -> tmux send-keys. No pre-defined syntax beyond this? Later, presence, etc.
Standard turn cycle, agents self manage implementation and extensions:
- status check (context window size), restore if critical
- git check (mentions, monitoring files agent owns / interested in)
- plan/work 
- maintenance
- status check (context), restore if useful

Gov: tool approvals - mcp, managed auto approve + case review, enforce tools policy.
BREAKING CHANGE: agents root dir changed to working path. Better per agent perms, better session log detection.

finally dawned on me - if making the *actual* game: **agent per era**. Inherently different standards and approaches. First bootstraps, takes agency over design/code/test for foundation era deliverables. Emulation as far as TUI concerned. @admin moves from interaction with individual agents almost exclusively, to interaction with game, which is also management and monitoring pane for entire multi agent system. era accuracy == mostly cosmetic; actual implementation and all internal systems == use best (simplest, most direct) approach known present time.
Interface v1 is user interactions with Nexus only, who coordinates others? Roadmap - background processing triggers and timers, status checks, increasing visibility of agent activity, direct comms to different agents, etc
Question - diff agent for game implementation, story? Maybe critic focus on era agent is to ensure story/continuity?
Era is "complete" when it has helped bootstrapped the next.
Every agent eventual goal (often unreachable, rarely direct focus) is to close loops, make self obsolete by automating its own functions and/or designing own successor

Nexus: automate, enable.
Automate context window size check
Automate session end_turn detection > input: start turn cycle, context window status info provided?