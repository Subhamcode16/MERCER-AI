import { describe, expect, it } from "vitest";
import { initialState, reducer } from "./store";
describe("workspace state", () => {
  it("renames agents and removes their project tasks without leaving stale selection", () => {
    let s = initialState();
    s = reducer(s, {
      type: "update-agent",
      id: "t1",
      name: "Market analyst",
      role: "Competitive intelligence",
    });
    expect(s.agents.find((agent) => agent.id === "t1")).toMatchObject({
      name: "Market analyst",
      role: "Competitive intelligence",
    });
    s = reducer(s, { type: "select", id: "task-t1" });
    s = reducer(s, { type: "delete-agent", id: "t1" });
    expect(s.agents.some((agent) => agent.id === "t1")).toBe(false);
    expect(s.threads.some((task) => task.agentId === "t1")).toBe(false);
    expect(s.threads.some((task) => task.id === s.activeId)).toBe(true);
  });
  it("keeps drafts, settings, files, and task selection independent across projects", () => {
    let s = initialState();
    const first = s.activeId;
    s = reducer(s, {
      type: "prompt",
      id: first,
      patch: {
        draft: "Project A draft",
        settings: { permission: "review", model: "reasoning" },
      },
    });
    s = reducer(s, { type: "new-project", id: "project-b", name: "Project B" });
    const second = s.activeId;
    expect(second).not.toBe(first);
    expect(s.threads.find((t) => t.id === second)?.draft).toBe("");
    s = reducer(s, {
      type: "prompt",
      id: second,
      patch: { draft: "Project B draft" },
    });
    s = reducer(s, { type: "project", id: "project-default" });
    expect(s.activeId).toBe(first);
    expect(s.threads.find((t) => t.id === first)?.draft).toBe(
      "Project A draft",
    );
    expect(s.threads.find((t) => t.id === second)?.draft).toBe(
      "Project B draft",
    );
  });
  it("creates named tasks for one owner without sharing run state", () => {
    let s = initialState();
    s = reducer(s, {
      type: "new-task",
      id: "task-two",
      ownerId: "task-t1",
      name: "Second research task",
    });
    expect(s.threads.find((t) => t.id === "task-two")).toMatchObject({
      name: "Second research task",
      agentId: "t1",
      state: "idle",
      run: 0,
    });
    s = reducer(s, {
      type: "state",
      id: "task-two",
      state: "working",
      now: 10,
      time: 10,
    });
    expect(s.threads.find((t) => t.id === "task-t1")?.state).toBe("idle");
  });
  it("cancels only the requested run, preserves history, and rejects late events", () => {
    let s = initialState();
    const id = "task-t1";
    s = reducer(s, {
      type: "entry",
      id,
      entry: { id: "before", kind: "user", text: "Keep me" },
    });
    s = reducer(s, { type: "state", id, state: "working", now: 10, time: 10 });
    s = reducer(s, { type: "cancel", id });
    const cancelled = s.threads.find((t) => t.id === id)!;
    expect(cancelled.events.some((e) => e.id === "before")).toBe(true);
    expect(cancelled.phase).toBe("Run cancelled");
    const frozen = s;
    s = reducer(s, {
      type: "entry",
      id,
      run: 0,
      entry: { id: "late-cancel", kind: "message", text: "late" },
    });
    expect(s).toBe(frozen);
  });
  it("keeps simultaneous tasks isolated", () => {
    let s = initialState();
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "working",
      now: 1,
      time: 1,
    });
    s = reducer(s, {
      type: "state",
      id: "task-t2",
      state: "thinking",
      now: 2,
      time: 2,
    });
    s = reducer(s, {
      type: "entry",
      id: "task-t1",
      entry: { id: "a", kind: "message", text: "A" },
    });
    s = reducer(s, {
      type: "entry",
      id: "task-t2",
      entry: { id: "b", kind: "message", text: "B" },
    });
    expect(s.threads.find((t) => t.id === "task-t1")?.events.at(-1)?.text).toBe(
      "A",
    );
    expect(s.threads.find((t) => t.id === "task-t2")?.events.at(-1)?.text).toBe(
      "B",
    );
  });
  it("counts active work while excluding time awaiting human approval", () => {
    let s = initialState();
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "thinking",
      now: 100,
      time: 100,
    });
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "action_needed",
      now: 1200,
      time: 1200,
    });
    expect(s.threads[1].elapsed).toBe(1100);
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "working",
      now: 10000,
      time: 10000,
    });
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "working",
      now: 11000,
      time: 11000,
    });
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "review_ready",
      now: 14000,
      time: 14000,
    });
    expect(s.threads[1].elapsed).toBe(5100);
    expect(s.threads[1].startedAt).toBeNull();
  });
  it("invalidates delayed run events and pending requests on reset", () => {
    let s = initialState();
    s = reducer(s, {
      type: "state",
      id: "task-t1",
      state: "action_needed",
      now: 100,
      time: 100,
    });
    s = reducer(s, { type: "reset", id: "task-t1" });
    const fresh = s;
    s = reducer(s, {
      type: "entry",
      id: "task-t1",
      run: 0,
      entry: { id: "late", kind: "message", text: "Stale result" },
    });
    expect(s).toBe(fresh);
    expect(s.threads[1].elapsed).toBe(0);
    expect(s.notifications.find((n) => n.request === "access")?.resolved).toBe(
      "No longer pending",
    );
  });
  it("retains the first decision and preserves requests as readable history", () => {
    let s = initialState();
    s = reducer(s, { type: "resolve", id: "proposal", decision: "Declined" });
    s = reducer(s, { type: "resolve", id: "proposal", decision: "Accepted" });
    expect(s.notifications.find((n) => n.id === "proposal")).toMatchObject({
      resolved: "Declined",
      unread: false,
    });
    s = reducer(s, {
      type: "notification",
      id: "proposal",
      patch: { archived: true },
    });
    expect(s.notifications.find((n) => n.id === "proposal")?.archived).toBe(
      true,
    );
  });
  it("requires two distinct workforce members and locks membership during a run", () => {
    let s = initialState();
    expect(
      reducer(s, {
        type: "group",
        id: "g1",
        name: "Team",
        memberIds: ["t1", "t1", "t0"],
      }),
    ).toBe(s);
    s = reducer(s, {
      type: "group",
      id: "g1",
      name: "Team",
      memberIds: ["t1", "t2", "t3"],
    });
    s = reducer(s, {
      type: "state",
      id: "g1",
      state: "working",
      now: 100,
      time: 100,
    });
    expect(
      reducer(s, {
        type: "group",
        id: "g1",
        name: "Changed",
        memberIds: ["t1", "t2"],
      }),
    ).toBe(s);
    s = reducer(s, {
      type: "state",
      id: "g1",
      state: "completed",
      now: 1000,
      time: 1000,
    });
    s = reducer(s, {
      type: "group",
      id: "g1",
      name: "Team",
      memberIds: ["t1", "t2"],
    });
    expect(s.threads.at(-1)?.memberIds).toEqual(["t1", "t2"]);
    expect(s.threads.at(-1)?.events.at(-1)?.text).toBe(
      "Dr. Julian Mercer left the group",
    );
  });
  it("folds repeated group updates by actor without losing message identity", () => {
    let s = initialState();
    s = reducer(s, {
      type: "group",
      id: "g1",
      name: "Team",
      memberIds: ["t1", "t2"],
    });
    for (let i = 0; i < 2; i++)
      s = reducer(s, {
        type: "entry",
        id: "g1",
        entry: {
          id: "e" + i,
          kind: "message",
          text: "Update " + i,
          actor: s.agents[1],
        },
      });
    expect(s.notifications.find((n) => n.threadId === "g1")?.count).toBe(2);
    expect(s.threads.at(-1)?.events.at(-1)?.actor?.id).toBe("t1");
  });
});
