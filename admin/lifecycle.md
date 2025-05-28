## login
new terminology for restore?

<REPEAT>

## inbox
please check messages and integrate with current priorities. as needed, do what can be done quickly first, or is most urgent. maintain own prioritisation standard as required. if just a short file Read and reply is needed, do it now. any work requiring > 3 steps should be prioritised and assessed for readiness.

*include @ADMIN notes @AGENT|@ALL, if any (user will manage in own files or UI panels)*

### distill(context_window_used: X, ..., forced_logout_at: Z) -> next_choice:
please @protocols/distill.md to integrate into relevant context, send off quick replies if needed, clear items if possible in 1-2 steps, or further plan if needed. no deep work yet.

*args passed from state, final output is to simply choose next action (+ args?)

choice: deep_work | idle | logout (decide FIRST during distill, adjust as required, final output is plain text format: `next_choice: <choice> args`)

## deep_work(task_or_thread: ..., max_tokens: ...)
check that all requirements are meant. send relevant/required updates or requests as you go. plans must be precise before implementation. pause and reconsider if initial approach doesn't work. if you get stuck, seek help.

  -- OR --

## idle
- agent indicates it's currently waiting on other agents / admin to define or progress own activities
- review again any recent message threads in case something missed
- return to inbox on incoming message

</REPEAT>

## logout
concept - the "logout log". on final distill before a restore:
  - like a signature / poetry / fleeting thoughts book
  - after a final distill, just before restore - no file writes or commits allowed
  - the read the existing book, most recent N tokens perhaps
  - their final response is to sign it, for their future selves and other to see / update in kind