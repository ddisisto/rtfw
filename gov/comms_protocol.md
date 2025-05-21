# Simple Agent Communication Protocol

## Message Format
All messages MUST include @FROM and @TO:

```
@FROM → @TO: [concise message]
```

Examples:
- `@CODE → @GOV: Status update - CLI implementation 70% complete`
- `@GOV → @CODE: Please review updated comms protocol`
- `@GOV → @PLAYER: Request clarification on game balance priorities`

## Communication Flow
All communication happens directly in the token stream:
- Messages just appear in the current conversation
- @FACILITATOR handles routing between agent sessions
- No external message storage or routing needed

## Best Practices
- Keep messages concise and clear
- Reference files for detailed context: `See code/context.md for details`
- Commit changes to context and IDENTITY files regularly
- Include enough context for the receiving agent to understand

## Special Agents
- `@PLAYER` - The game player
- `@FACILITATOR` - The message router (currently human-operated)
- `@USER` - The current user
- `@DEV` - Development assistance

## Announcements
- System-wide communications go through ANNOUNCEMENTS.md
- Only @GOV should directly update ANNOUNCEMENTS.md
- Other agents should send: `@FROM → @GOV: ANNOUNCE: [message]`