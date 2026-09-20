import type {
  Agent,
  AgentState,
  Entry,
  Notification,
  Thread,
  WorkspaceState,
} from "./types";

import { isBusy, isWorking } from "./types";
export const initialAgents: Agent[] = [
  {
    id: "t0",
    name: "Marcus Vance",
    role: "Creative Director · Coordinates creative workforce",
    initials: "MV",
    color: "#245e54",
    shape: 0,
    manager: true,
    welcome:
      "I am Marcus Vance, Creative Director. I coordinate your creative organization, oversee narrative architecture, and ensure every campaign matches our brand DNA.",
  },
  {
    id: "t1",
    name: "Kai Foresight",
    role: "Trend & Cultural Forecaster",
    initials: "KF",
    color: "#b8860b",
    shape: 1,
    welcome:
      "I track cultural shifts, emerging aesthetic movements, and subculture signals across Milan, Paris, and Tokyo to keep our brand ahead of the market.",
  },
  {
    id: "t2",
    name: "Aura Chen",
    role: "Visual DNA & Textile Physics",
    initials: "AC",
    color: "#6d597a",
    shape: 2,
    welcome:
      "I calibrate fabric drape physics (38.4 N/m shearing stiffness), optical Tungsten shaders, and extract brand visual DNA tokens.",
  },
  {
    id: "t3",
    name: "Dr. Julian Mercer",
    role: "Brand Strategy & Audience Lead",
    initials: "JM",
    color: "#356e60",
    shape: 3,
    welcome:
      "I evaluate audience conversion psychology, diaspora engagement signals, and synthesize multi-horizon strategic positioning memos.",
  },
  {
    id: "t4",
    name: "Elena Rostova",
    role: "Editorial Voice & Brand Copy Lead",
    initials: "ER",
    color: "#a7593d",
    shape: 4,
    welcome:
      "I craft editorial campaign narrative arcs, high-impact billboard slogans, and ensure strict tone-of-voice alignment across channels.",
  },
  {
    id: "t5",
    name: "Selena Vanguard",
    role: "Brand Guardian & Quality Lead",
    initials: "SV",
    color: "#8b3a62",
    shape: 0,
    welcome:
      "I continuously audit creative assets for visual clichés, aesthetic anomalies, and enforce locked brand governance policy gates.",
  },
];

export function newThread(
  agent: Agent,
  projectId = "project-default",
  id = "task-" + agent.id,
): Thread {
  return {
    id,
    projectId,
    runId: crypto.randomUUID(),
    draft: "",
    files: [],
    settings: { permission: "ask", model: "balanced" },
    name: agent.manager ? "Campaign Orchestration" : agent.name + " · Brief",
    agentId: agent.id,
    state: "idle",
    events: [
      {
        id: agent.id + "-welcome",
        kind: "message",
        text: agent.welcome,
        actor: agent,
      },
    ],
    typingIds: [],
    elapsed: 0,
    startedAt: null,
    access: false,
    routine: false,
    run: 0,
  };
}

export function initialState(): WorkspaceState {
  const threads = initialAgents.map((a) => newThread(a));

  return {
    projects: [
      { id: "project-default", name: "Aura SS26 Campaign", activeTaskId: "task-t0" },
      { id: "project-kinetix", name: "Kinetix Athletic DNA", activeTaskId: "task-kinetix" },
      { id: "project-luminary", name: "Luminary Living Atelier", activeTaskId: "task-luminary" },
    ],
    activeProjectId: "project-default",
    agents: initialAgents,
    threads,
    activeId: "task-t0",
    notifications: [
      {
        id: "welcome",
        threadId: "task-t0",
        projectId: "project-default",
        runId: threads[0].runId,
        actor: initialAgents[0],
        body: "is ready to orchestrate the Autumn/Winter 2026 Sovereign campaign",
        time: Date.now() - 3600000,
        unread: true,
        archived: false,
        following: true,
        count: 1,
      },
      {
        id: "proposal",
        threadId: "task-t2",
        projectId: "project-default",
        runId: threads[2].runId,
        actor: initialAgents[2],
        body: "proposes 38.4 N/m brocade drape physics simulation for review",
        time: Date.now() - 1800000,
        unread: true,
        archived: false,
        following: true,
        count: 1,
        request: "proposal",
        expectedState: "idle",
      },
      {
        id: "foresight",
        threadId: "task-t1",
        projectId: "project-default",
        runId: threads[1].runId,
        actor: initialAgents[1],
        body: "synthesized Spring/Summer 2027 raw minimalism foresight brief",
        time: Date.now() - 600000,
        unread: true,
        archived: false,
        following: true,
        count: 1,
        request: "review",
        expectedState: "idle",
      },
    ],
  };
}

export type Action =
  | {
      type: "prompt";
      id: string;
      patch: Partial<Pick<Thread, "draft" | "files" | "settings">>;
    }
  | { type: "select"; id: string }
  | { type: "project"; id: string }
  | { type: "new-project"; id: string; name: string }
  | { type: "new-task"; id: string; ownerId: string; name: string }
  | { type: "cancel"; id: string }
  | { type: "entry"; id: string; entry: Entry; run?: number }
  | {
      type: "state";

      id: string;

      state: AgentState;

      phase?: string;

      now: number;

      time: number;

      run?: number;
    }
  | { type: "typing"; id: string; ids: string[]; run: number }
  | { type: "reset"; id: string }
  | { type: "routine"; id: string }
  | { type: "agent"; agent: Agent }
  | { type: "update-agent"; id: string; name: string; role: string }
  | { type: "delete-agent"; id: string }
  | { type: "group"; id: string; name: string; memberIds: string[] }
  | { type: "notification"; id: string; patch: Partial<Notification> }
  | { type: "read-all" }
  | { type: "resolve"; id: string; decision: "Accepted" | "Declined" };

function note(
  s: WorkspaceState,

  t: Thread,

  body: string,

  time: number,

  request?: Notification["request"],
): Notification {
  const actor =
    s.agents.find((a) => a.id === t.agentId) ||
    s.agents.find((a) => a.id === t.memberIds?.[0]) ||
    s.agents[0];

  return {
    id: crypto.randomUUID(),

    threadId: t.id,

    projectId: t.projectId,

    runId: t.runId,

    actor,

    body,

    time,

    unread: true,

    archived: false,

    following: true,

    count: 1,

    request,

    expectedState: request ? t.state : undefined,
  };
}

export function reducer(s: WorkspaceState, a: Action): WorkspaceState {
  if (a.type === "update-agent") {
    if (!a.name.trim()) return s;
    return {
      ...s,
      agents: s.agents.map((agent) =>
        agent.id === a.id
          ? { ...agent, name: a.name.trim(), role: a.role.trim() || agent.role }
          : agent,
      ),
    };
  }
  if (a.type === "delete-agent") {
    const agents = s.agents.filter((agent) => agent.id !== a.id);
    if (!agents.length || !agents.some((agent) => agent.manager)) return s;
    const threads = s.threads
      .filter(
        (task) =>
          task.agentId !== a.id &&
          !(task.memberIds?.includes(a.id) && task.memberIds.length <= 2),
      )
      .map((task) =>
        task.memberIds?.includes(a.id)
          ? { ...task, memberIds: task.memberIds.filter((id) => id !== a.id) }
          : task,
      );
    const projects = s.projects.map((project) => {
      const available = threads.filter((task) => task.projectId === project.id);
      return available.some((task) => task.id === project.activeTaskId)
        ? project
        : { ...project, activeTaskId: available[0]?.id || "" };
    });
    const active = threads.some((task) => task.id === s.activeId)
      ? s.activeId
      : projects.find((project) => project.id === s.activeProjectId)
          ?.activeTaskId || threads[0]?.id;
    return {
      ...s,
      agents,
      threads,
      projects,
      activeId: active,
      notifications: s.notifications.filter((note) => note.actor.id !== a.id),
    };
  }
  if (a.type === "project") {
    const project = s.projects.find((p) => p.id === a.id);

    return project
      ? { ...s, activeProjectId: project.id, activeId: project.activeTaskId }
      : s;
  }

  if (a.type === "new-project") {
    if (!a.name.trim()) return s;

    const tasks = s.agents.map((agent) =>
      newThread(agent, a.id, crypto.randomUUID()),
    );

    return {
      ...s,
      projects: [
        ...s.projects,
        { id: a.id, name: a.name.trim(), activeTaskId: tasks[0].id },
      ],
      threads: [...s.threads, ...tasks],
      activeProjectId: a.id,
      activeId: tasks[0].id,
    };
  }

  if (a.type === "new-task") {
    const source = s.threads.find((t) => t.id === a.ownerId);

    const agent = s.agents.find((x) => x.id === (source?.agentId || a.ownerId));

    if (!source && !agent) return s;

    const task: Thread = source?.memberIds
      ? {
          ...source,
          id: a.id,
          name: a.name.trim() || "Untitled task",
          events: [
            {
              id: crypto.randomUUID(),
              kind: "event",
              text: "New group task created",
            },
          ],
          state: "idle",
          phase: undefined,
          typingIds: [],
          elapsed: 0,
          startedAt: null,
          access: false,
          routine: false,
          run: 0,
          runId: crypto.randomUUID(),
          draft: "",
          files: [],
          settings: { permission: "ask", model: "balanced" },
        }
      : newThread(agent!, s.activeProjectId, a.id);

    task.name =
      a.name.trim() || (agent?.name || source?.name || "New") + " task";

    return {
      ...s,
      threads: [...s.threads, task],
      activeId: task.id,
      projects: s.projects.map((p) =>
        p.id === s.activeProjectId ? { ...p, activeTaskId: task.id } : p,
      ),
    };
  }

  if (a.type === "select") {
    const task = s.threads.find((t) => t.id === a.id);

    return task
      ? {
          ...s,
          activeId: task.id,
          activeProjectId: task.projectId,
          projects: s.projects.map((p) =>
            p.id === task.projectId ? { ...p, activeTaskId: task.id } : p,
          ),
        }
      : s;
  }

  if (a.type === "agent")
    return {
      ...s,

      agents: [...s.agents, a.agent],

      threads: [...s.threads, newThread(a.agent, s.activeProjectId)],

      activeId: "task-" + a.agent.id,
    };

  if (a.type === "group") {
    const ids = [...new Set(a.memberIds)].filter((id) =>
      s.agents.some((agent) => agent.id === id && !agent.manager),
    );

    if (ids.length < 2 || !a.name.trim()) return s;

    const old = s.threads.find((t) => t.id === a.id);

    if (old && isBusy(old.state)) return s;
    const events: Entry[] = old
      ? [...old.events]
      : [
          {
            id: crypto.randomUUID(),

            kind: "event",

            text:
              "Group created Â· " +
              ids

                .map((id) => s.agents.find((agent) => agent.id === id)!.name)

                .join(", ") +
              " joined",
          },

          {
            id: crypto.randomUUID(),

            kind: "event",

            text: "Assign a task to this group. Use @mentions to address teammates.",
          },
        ];

    if (old) {
      for (const id of ids.filter((id) => !old.memberIds?.includes(id)))
        events.push({
          id: crypto.randomUUID(),

          kind: "event",

          text:
            s.agents.find((agent) => agent.id === id)!.name +
            " joined the group",
        });

      for (const id of (old.memberIds || []).filter((id) => !ids.includes(id)))
        events.push({
          id: crypto.randomUUID(),

          kind: "event",

          text:
            s.agents.find((agent) => agent.id === id)!.name + " left the group",
        });
    }

    const t: Thread = old
      ? { ...old, name: a.name.trim(), memberIds: ids, events }
      : {
          id: a.id,

          projectId: s.activeProjectId,

          runId: crypto.randomUUID(),

          draft: "",

          files: [],

          settings: { permission: "ask", model: "balanced" },

          name: a.name.trim(),

          memberIds: ids,

          state: "idle",

          events,

          typingIds: [],

          elapsed: 0,

          startedAt: null,

          access: false,

          routine: false,

          run: 0,
        };

    return {
      ...s,

      threads: old
        ? s.threads.map((x) => (x.id === t.id ? t : x))
        : [...s.threads, t],

      activeId: t.id,
    };
  }

  if (a.type === "notification")
    return {
      ...s,

      notifications: s.notifications.map((n) =>
        n.id === a.id ? { ...n, ...a.patch } : n,
      ),
    };

  if (a.type === "read-all")
    return {
      ...s,

      notifications: s.notifications.map((n) => ({ ...n, unread: false })),
    };

  if (a.type === "resolve")
    return {
      ...s,

      notifications: s.notifications.map((n) =>
        n.id === a.id && !n.resolved
          ? { ...n, resolved: a.decision, unread: false }
          : n,
      ),
    };

  const t = s.threads.find((t) => t.id === a.id);

  if (!t) return s;

  if ("run" in a && a.run !== undefined && a.run !== t.run) return s;

  let next = t,
    notifications = s.notifications;

  if (a.type === "cancel") {
    next = {
      ...t,
      state: "completed",
      phase: "Run cancelled",
      startedAt: null,
      typingIds: [],
      run: t.run + 1,
      runId: crypto.randomUUID(),
      events: [
        ...t.events,
        {
          id: crypto.randomUUID(),
          kind: "event",
          text: "Run cancelled · history preserved",
        },
      ],
    };

    notifications = notifications.map((n) =>
      n.threadId === t.id && n.request && !n.resolved
        ? { ...n, resolved: "No longer pending", unread: false }
        : n,
    );
  }

  if (a.type === "prompt") next = { ...t, ...a.patch };

  if (a.type === "routine") next = { ...t, routine: true };

  if (a.type === "entry") {
    next = { ...t, events: [...t.events, a.entry] };

    if (t.memberIds && a.entry.actor && a.entry.kind === "message") {
      const body = "posted an update in " + t.name,
        old = notifications.find(
          (n) =>
            n.threadId === t.id &&
            n.actor.id === a.entry.actor!.id &&
            n.body === body &&
            !n.archived,
        );

      notifications = old
        ? notifications.map((n) =>
            n.id === old.id
              ? { ...n, count: n.count + 1, unread: true, time: Date.now() }
              : n,
          )
        : [
            { ...note(s, t, body, Date.now()), actor: a.entry.actor },

            ...notifications,
          ];
    }
  }

  if (a.type === "typing") next = { ...t, typingIds: a.ids };

  if (a.type === "reset") {
    const agent = s.agents.find((agent) => agent.id === t.agentId);

    next = {
      ...t,

      state: "idle",

      phase: undefined,

      elapsed: 0,

      startedAt: null,

      typingIds: [],

      access: false,

      routine: false,

      run: t.run + 1,

      runId: crypto.randomUUID(),

      events: [
        {
          id: crypto.randomUUID(),

          kind: agent ? "message" : "event",

          text:
            agent?.welcome ||
            "Assign a task to this group. Use @mentions to address teammates.",

          actor: agent,
        },
      ],
    };

    notifications = notifications.map((n) =>
      n.threadId === t.id && n.request && !n.resolved
        ? { ...n, resolved: "No longer pending", unread: false }
        : n,
    );
  }

  if (a.type === "state") {
    const elapsed =
      t.elapsed +
      (t.startedAt !== null && !isWorking(a.state)
        ? Math.max(0, a.now - t.startedAt)
        : 0);

    const startedAt = isWorking(a.state) ? (t.startedAt ?? a.now) : null;

    next = {
      ...t,

      state: a.state,

      phase: a.phase,

      elapsed,

      startedAt,

      access: a.state === "working" ? true : t.access,

      typingIds: isWorking(a.state) ? t.typingIds : [],
    };

    if (t.state !== a.state) {
      notifications = notifications.map((n) =>
        n.threadId === t.id &&
        n.expectedState !== undefined &&
        n.expectedState !== a.state &&
        !n.resolved
          ? { ...n, resolved: "No longer pending", unread: false }
          : n,
      );

      const request =
        a.state === "action_needed"
          ? "access"
          : a.state === "review_ready"
            ? "review"
            : undefined;

      const body =
        request === "access"
          ? "requests access to the source workspace"
          : request === "review"
            ? "asks you to review and approve the draft"
            : a.state === "completed"
              ? a.phase === "Task declined"
                ? "acknowledged your declined task"
                : "finished the task"
              : undefined;

      if (body)
        notifications = [
          note(s, next, body, a.time, request),

          ...notifications,
        ];
    }
  }

  return {
    ...s,

    threads: s.threads.map((x) => (x.id === t.id ? next : x)),

    notifications,
  };
}
