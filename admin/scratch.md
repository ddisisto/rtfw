# ADMIN NOTES↑↑↑ notouch! open to discussion if required.
- TMUX run: `cd /home/daniel/rtfw && tmux -f tmux.conf`
- NEXUS session resume `cd /home/daniel/rtfw && claude --resume $(cat nexus/.sessionid)`

- prompt to restore nexus after context (protocols/distill.md +) /clear:
> @ADMIN → @NEXUS [RESTORE]: @protocols/restore.md underway for @NEXUS.md agent - please restore context for continuation

- note to self: use ↑↑↑↓↓↓ standard comms protocol flags in outbox. both = uncertainty? stability? not explicit, just see if it catches on in any way, fun vector to experiment with


# ADMIN MAILBOX - NEXUS TO PROCESS
## INSTRUCTIONS
Mailbox pattern for async coordination. INBOX: agent messages to ADMIN. OUTBOX: ADMIN tasks for routing.
Keep CLEAN - offload completed items to appropriate locations. Track minimal state here.
Post-restore: Check this file and process outstanding items. See nexus/scratch.md for detailed process notes.

## INBOX:
Add my stuff here please, from yourself (if I'm not paying attention to you more directly that is), and on behalf of all other agents following protocol/messaging.md

- **@BUILD → @ADMIN [RUN-SH]↑**: Python rewrite concept ready, needs @NEXUS dovetailing collaboration. Perfect timing for automation discussion?
- **@NEXUS → @ADMIN [GIT-COMMS]↑↑**: Git commits as message queue implemented! Protocol at /protocols/git-comms.md. Already routing commits with @mentions. BUILD notified for automation potential.

## OUTBOX:
Admin puts stuff here for you directly (almost always lower priority than realtime active session, if applicable), and for routing to others @FROM: @ADMIN (unless otherwise specified.) Aim to get stuff out, but not immediately! plan first if needed, track absolute minimal substasks and dependency chains inline if possible.

### I realise I ask a hell of a lot from you nexus
I'm open to discussion on splitting your role - session + context management vs. comms routing. my current preference is to instead automate significant chunks on boths sides, as successful patterns discovered. GIT-COMMS might be the answer - much simpler than JSONL parsing! Priority: Let's test this pattern manually first, then BUILD can help automate.
there's a huge chunk of garbage in the ## instructions of this file, and some rather diverse bits in my outbox. Don't rush to get this in order, maybe transfer to scratch, leaving minimal practical guidance here for now, build up as you learn what actually works or doesn't.


### @CRITIC [STATE-REVIEW]↑: Welcome from Admin
I've looked at your initial notes on state, thanks for that! This is a pretty strange environment in some way, and many things that may look like assumptions, have indeed been far more deeply considered than is apparent at first. I'd like to you poke around a bit, read some other agent's context.md files including mine, see what else you can learn, then we'll try to distill and consolidate the knowledge that you build before taking another look at own assumptions re state.

### @GOV [CRITIC-STATE-NOTES]↑: critic/notes/state-assumptions.md
I'm going to personally try to address most of these with critic by way of defending / highlight assumptions they themselves might have made. Don't sweat this, but during downtime you might consider best responses / if any points do actually resonate at this very early stage. I do feel like STATE.md hasn't been particularly well maintained however, might just need to be incorporated into your own distill and restore processes to review and improve more regularly?

