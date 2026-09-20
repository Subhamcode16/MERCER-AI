# Fieldwork · React + TypeScript

The workspace has been migrated to genuine React components, with a typed reducer and lifecycle-managed hooks. No HTML iframe, legacy scripts, `dangerouslySetInnerHTML`, or mutation observers are used to render the interface. Native SVG rope animation uses element refs for frame-by-frame drawing.

## Run

Requires Node.js 20.19+ or 22.12+ and a package manager.

```sh
pnpm install
pnpm dev
```

Development preview: http://127.0.0.1:5173/

```sh
pnpm test
pnpm build
pnpm preview
```

`npm install` and the corresponding `npm run` scripts also work. Keep the pnpm lockfile when using pnpm for repeatable dependencies.

`dist/` is the production build. Serve that directory over HTTP. The existing `../ui-template.html` entry opens this production version; `../ui-template-legacy.html` preserves the earlier prototype. Rebuild after changing source files to update that production entry. The development preview updates as you edit.

## Components

| File | Responsibility |
| --- | --- |
| `src/App.tsx` | Workspace composition, active conversation, overlays, per-thread drafts and attachments |
| `src/types.ts` | Agent, conversation, event and notification types |
| `src/store.ts` | Reducer, group membership, requests, unread/archive state and active work timing |
| `src/useWorkspace.ts` | Simulated run orchestration, continuation, decisions and timer cleanup |
| `src/components/Sidebar.tsx` | Search, workforce navigation and group creation/editing |
| `src/components/Conversation.tsx` | Messages, @mentions, single thinking dot, stopwatch, workspace handoff and draft review |
| `src/components/Composer.tsx` | Expanding prompt, attached files, permissions/model profiles and editable dictation |
| `src/components/Avatar.tsx` | Agent shapes, group constellations, state animations and mouse trails |
| `src/components/Notifications.tsx` | Notification popover, filter tabs, row menus and accept/decline history |
| `src/components/Themes.tsx` | Theme preferences and palette picker |
| `src/components/Pullcord.tsx` | SVG rope physics and pointer/keyboard light-dark control |
| `src/themes.ts` | Six light/dark palettes |
| `src/styles.css`, `src/react-layout.css` | Preserved visual styling, responsive layout and reduced-motion rules |

## Preserved behavior

Full-window responsive layout; manager/workforce navigation; custom assistants; editable groups; simultaneous simulated typing; actor-labeled messages with top-aligned avatars; mention completion; floating 800px composer with vertical expansion; attachment drawer; three permission modes and model profiles; dictation with live transcription, audio spectrum, finish/cancel and explicit send; animated mascots and group constellations; color mouse trails; notification decisions and archive/restore; six palettes; persisted light/dark preferences; one bouncing dot and active-time stopwatch; source handoff, review/revision and example routine flow.

Drafts and local attachments are kept per conversation while switching. Theme choices persist in local storage. Conversations, groups, notifications and task decisions are session-only, as in the prototype. Active-time clocks exclude waiting for the user.

## Backend integration

Replace simulated timers in `useWorkspace.ts` with your event stream, keeping the typed reducer actions. Use an authenticated command handler for tasks and request decisions, then update UI state after server acknowledgement. Enforce permission profiles on the server. Model choices currently select profiles rather than provider model IDs. File attachments stay local until an upload service is added. Routine creation records an example in the work log; it does not register a real schedule. The original group event contract is available in `../group-backend-contract.md`.

Speech recognition uses the browser's SpeechRecognition/webkitSpeechRecognition API. Audio frequency bars use getUserMedia and AudioContext. Microphone access needs browser permission and localhost/HTTPS; dictation support depends on the browser. Recognition never sends messages automatically. Actual microphone recognition was not exercised during automated verification.

The supplied notification panel's sentence-based rows, filters, decision history and archive behavior have been adapted into React with the workspace's existing styling. This project uses CSS rather than requiring Tailwind, shadcn, or an animation library.

## Verification

Five reducer tests cover active-time accounting, reset cancellation, decision history, group validation/busy membership locks and repeated group notifications. TypeScript strict checking and the production build pass. Browser checks cover messages, handoff and approval, group creation/mentions/collaboration, models/permissions, palettes and light/dark switching, expandable composer, retained drafts, notification archive/restore, mobile navigation and horizontal overflow. Live backend execution remains outside this frontend template.
