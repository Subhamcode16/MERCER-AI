# Phase 27: Command Palette & Interaction Grammar

## 1. Interaction Grammar
Operators can control the Studio through graphical modals or the integrated Command Palette:

| Slash Command | Natural Language Directive | Minimum Required Role |
|---|---|---|
| `/synthesize` | "Synthesize creative intelligence" | `STAFF_OPERATOR` |
| `/direction select <id>` | "Select direction <id>" | `STAFF_OPERATOR` |
| `/render` | "Generate visual asset drafts" | `STAFF_OPERATOR` |
| `/review <id>` | "Review asset <id>" | `STAFF_OPERATOR` |
| `/approve <id>` | "Approve asset <id>" | `CREATIVE_DIRECTOR` |
| `/launch stage` | "Stage multi-channel launch" | `STAFF_OPERATOR` |
| `/launch execute` | "Execute campaign launch" | `CREATIVE_DIRECTOR` |

## 2. Invariant: Natural Language Command ≠ Permission
Attempting privileged operations (like `/approve`) without the required role returns a structured `DENIED` status and logs a security audit event.
