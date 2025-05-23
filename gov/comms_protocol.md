# Simple Agent Communication Protocol

## Message Format
All messages MUST include @FROM and @TO:

```
@FROM → @TO: [concise message]
```

Examples:
- `@CODE → @GOV: Status update - CLI implementation 70% complete`
- `@GOV → @CODE: Please review updated comms protocol`
- `@GOV → @ADMIN: Request clarification on system balance priorities`

## Communication Flow
All communication happens directly in the token stream:
- Messages just appear in the current conversation
- @NEXUS handles routing between agent sessions
- No external message storage or routing needed

## Best Practices
- Keep messages concise and clear
- Reference files for detailed context: `See admin/example_proposal.md for details`
- Include enough context for the receiving agent to understand

## Special Agents
- `@NEXUS` - Central communication hub and agent session manager
- `@GOV` - Process, protocols and policy descisions
- `@ADMIN` - The system administrator
