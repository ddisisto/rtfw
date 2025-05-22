# RTFW Session Registry

This file maps agent names to their Claude Code session IDs for the RTFW project.

## Active Sessions

| Agent       | Session ID                             | Size  | Status    |
|-------------|----------------------------------------|-------|-----------|
| @NEXUS      | ce51677e-8f35-45e0-984d-6dc767ec416e   | NEW   | CURRENT   |
| @CODE       | 6c859161-b569-4a87-a53e-3b88d6943c0d   | 269K  | ACTIVE    |
| @GOV        | 66a678dc-e43d-4db2-86c1-f93ea54b69ad   | 1.1M  | ACTIVE    |
| @ARCHITECT  | 932ef584-cac9-4868-ae0b-30fed3de40e5   | 217K  | ACTIVE    |
| @RESEARCH   | b607ed31-0de8-4db1-b3df-2a1bcaec0d66   | 202K  | ACTIVE    |
| @HISTORIAN  | c7461411-c039-4876-b824-423fc607e337   | 131B  | MINIMAL   |
| @TEST       | bae725c1-5163-43ff-af08-d50ca01233e6   | 145B  | MINIMAL   |

## Inactive Sessions

| Session ID                             | Size  | Description           |
|----------------------------------------|-------|-----------------------|
| 2fc7114d-e394-40c1-96c5-949c4b47dc85   | 370K  | Previous @NEXUS       |
| c4088511-fc4e-4916-bd88-c4ebf22ca138   | 116K  | Previous @NEXUS       |
| bf7a50b0-607c-43c6-bb3e-1507b9d29d7f   | 5.3K  | Test session (Lorem)  |
| bacabd75-fba9-4054-8297-a40cd994ce0f   | 673B  | Compressed summaries  |

## Monitoring Status

- **CURRENT**: Active session being monitored (this NEXUS session)
- **ACTIVE**: Large active sessions with recent activity
- **MINIMAL**: Stub sessions with minimal content
- Session tracking established: May 22, 2025
- @NEXUS session updated: 2fc7114d -> ce51677e at May 22, 2025 11:45