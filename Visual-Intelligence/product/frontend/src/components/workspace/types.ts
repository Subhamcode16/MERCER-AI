export type AgentState =
  | "idle"
  | "thinking"
  | "action_needed"
  | "human_control"
  | "working"
  | "review_ready"
  | "completed";
export interface Agent {
  id: string;
  name: string;
  role: string;
  initials: string;
  color: string;
  shape: number;
  manager?: boolean;
  welcome: string;
}
export interface Entry {
  id: string;
  kind: "message" | "user" | "event" | "tool" | "review";
  text: string;
  actor?: Agent;
}
export interface Project {
  id: string;
  name: string;
  activeTaskId: string;
}
export interface PromptSettings {
  permission: string;
  model: string;
}
export interface Thread {
  projectId: string;
  runId: string;
  draft: string;
  files: File[];
  settings: PromptSettings;
  id: string;
  name: string;
  agentId?: string;
  memberIds?: string[];
  state: AgentState;
  phase?: string;
  events: Entry[];
  typingIds: string[];
  elapsed: number;
  startedAt: number | null;
  access: boolean;
  routine: boolean;
  run: number;
}
export interface Notification {
  id: string;
  threadId: string;
  projectId: string;
  runId: string;
  actor: Agent;
  body: string;
  time: number;
  unread: boolean;
  archived: boolean;
  following: boolean;
  count: number;
  request?: "proposal" | "access" | "review";
  expectedState?: AgentState;
  resolved?: string;
}
export interface WorkspaceState {
  projects: Project[];
  activeProjectId: string;
  agents: Agent[];
  threads: Thread[];
  activeId: string;
  notifications: Notification[];
}
export const stateLabels: Record<AgentState, string> = {
  idle: "Ready for a new task",
  thinking: "Preparing the run",
  action_needed: "Your help is needed",
  human_control: "You are in control",
  working: "Working through the sources",
  review_ready: "Ready for your review",
  completed: "Run complete",
};
export const isWorking = (state: AgentState) =>
  state === "thinking" || state === "working";
export const isBusy = (state: AgentState) =>
  isWorking(state) ||
  state === "action_needed" ||
  state === "human_control" ||
  state === "review_ready";
