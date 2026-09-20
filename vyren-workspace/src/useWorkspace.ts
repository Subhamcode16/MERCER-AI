import { useCallback, useEffect, useReducer, useRef } from "react";
import { initialState, reducer } from "./store";
import { isWorking } from "./types";
import type { Agent, AgentState, Entry, Notification, Thread } from "./types";
export function useWorkspace() {
  const [state, dispatch] = useReducer(reducer, undefined, initialState);
  const latest = useRef(state);
  latest.current = state;
  const timers = useRef(new Map<string, Set<ReturnType<typeof setTimeout>>>());
  const locked = useRef(new Set<string>());
  useEffect(
    () => () => {
      timers.current.forEach((set) => set.forEach(clearTimeout));
    },
    [],
  );
  const cancel = useCallback((id: string) => {
    timers.current.get(id)?.forEach(clearTimeout);
    timers.current.delete(id);
  }, []);
  const later = useCallback((t: Thread, ms: number, fn: () => void) => {
    const set = timers.current.get(t.id) || new Set();
    timers.current.set(t.id, set);
    const timer = setTimeout(() => {
      set.delete(timer);
      if (latest.current.threads.find((x) => x.id === t.id)?.run === t.run)
        fn();
    }, ms);
    set.add(timer);
  }, []);
  const setState = useCallback(
    (t: Thread, value: AgentState, phase?: string) =>
      dispatch({
        type: "state",
        id: t.id,
        state: value,
        phase,
        now: performance.now(),
        time: Date.now(),
        run: t.run,
      }),
    [],
  );
  const entry = useCallback(
    (t: Thread, kind: Entry["kind"], text = "", actor?: Agent) =>
      dispatch({
        type: "entry",
        id: t.id,
        entry: { id: crypto.randomUUID(), kind, text, actor },
        run: t.run,
      }),
    [],
  );
  const continueWork = useCallback(
    (t: Thread) => {
      setState(t, "working", "Extracting Visual DNA and analyzing brand memory");
      entry(t, "event", "Creative authority returned to " + t.name);
      later(t, 1400, () =>
        setState(t, "working", "Cross-referencing Trend & Cultural Foresight signals"),
      );
      later(t, 2600, () => {
        entry(t, "event", "Audience intelligence synthesized by Dr. Julian Mercer");
        entry(
          t,
          "message",
          "Audience conversion analysis reveals a +24.2% organic engagement signal for warm-minimalism silhouettes. I have calibrated the direction draft accordingly.",
        );
        setState(t, "working", "Calibrating 3D material drape physics (38.4 N/m)");
      });
      later(t, 3900, () => {
        setState(t, "review_ready");
        entry(t, "review");
        entry(
          t,
          "message",
          "The campaign brief and visual direction package is ready. Please review the trade-off matrix and approve the review gate to lock parameters.",
        );
      });
    },
    [setState, entry, later],
  );
  const start = useCallback(
    (
      t: Thread,
      text = "Develop a comprehensive campaign direction. Extract Visual DNA, synthesize audience signals, and prepare visual package for human review gate.",
    ) => {
      if (
        isWorking(t.state) ||
        t.state === "action_needed" ||
        t.state === "human_control" ||
        t.state === "review_ready"
      )
        return;
      entry(t, "user", text);
      if (!t.memberIds) {
        setState(t, "thinking", "Accessing VYREN Brand Memory & Asset Vault");
        later(t, 1100, () => {
          entry(
            t,
            "message",
            "I have synthesized the strategic hypothesis. To proceed with 4K optical rendering, please grant access to the locked Brand DNA asset vault.",
          );
          setState(t, "action_needed");
          entry(t, "tool");
        });
        return;
      }
      const people = t.memberIds
        .map((id) => latest.current.agents.find((a) => a.id === id)!)
        .filter(Boolean);
      const mentioned = people.filter((a) => text.includes("@" + a.name));
      const ordered = [
        ...mentioned,
        ...people.filter((a) => !mentioned.includes(a)),
      ];
      setState(t, "working", "VYREN Creative Organization collaborating");
      dispatch({
        type: "typing",
        id: t.id,
        ids: people.map((a) => a.id),
        run: t.run,
      });
      ordered.forEach((a, i) => {
        const next = ordered[(i + 1) % ordered.length];
        later(t, 650 + i * 550, () => {
          entry(
            t,
            "message",
            `@${next.name} I am leading the ${a.role.toLowerCase()} vector for this campaign. Synthesizing domain evidence and cross-checking policy gates now.`,
            a,
          );
          dispatch({
            type: "typing",
            id: t.id,
            ids: ordered.slice(i + 1).map((a) => a.id),
            run: t.run,
          });
        });
        later(t, 1700 + i * 650, () =>
          dispatch({
            type: "typing",
            id: t.id,
            ids: ordered.slice(i).map((a) => a.id),
            run: t.run,
          }),
        );
        later(t, 2600 + i * 650, () =>
          entry(
            t,
            "message",
            `@${next.name} Recommendation locked: Maintain 2800K Tungsten specular rim lighting with 38.4 N/m brocade shearing stiffness. Does this align with the editorial copy arc?`,
            a,
          ),
        );
      });
      later(t, 3300 + people.length * 650, () => {
        entry(
          t,
          "message",
          "The creative organization has synthesized a unified direction: Direction 02 (The Modern Sovereign) is calibrated with 98% brand DNA adherence score. Ready for Human Review Gate.",
          ordered[0],
        );
        setState(t, "completed");
        entry(
          t,
          "event",
          "Collaboration complete · " +
            people.length +
            " creative specialists contributed",
        );
      });
    },
    [entry, setState, later],
  );
  const approve = useCallback(
    (t: Thread) => {
      entry(t, "user", "I approve Campaign Direction 02 (The Modern Sovereign).");
      setState(t, "completed");
      entry(t, "event", "Human Signature recorded · Direction locked to Brand DNA Profile");
      entry(
        t,
        "message",
        "Direction 02 locked successfully. Assets are queued for pre-flight packaging in the Campaign Studio.",
      );
    },
    [entry, setState],
  );
  const decide = useCallback(
    (n: Notification, decision: "Accepted" | "Declined") => {
      const current = latest.current.notifications.find((x) => x.id === n.id),
        t = latest.current.threads.find((t) => t.id === n.threadId);
      if (!current || current.resolved || !t || locked.current.has(n.id))
        return;
      if (n.runId && n.runId !== t.runId) {
        dispatch({
          type: "notification",
          id: n.id,
          patch: { resolved: "No longer pending", unread: false },
        });
        return;
      }
      locked.current.add(n.id);
      if (n.expectedState && n.expectedState !== t.state) {
        dispatch({
          type: "notification",
          id: n.id,
          patch: { resolved: "No longer pending", unread: false },
        });
        return;
      }
      dispatch({ type: "resolve", id: n.id, decision });
      if (decision === "Declined") {
        if (n.request !== "proposal") {
          cancel(t.id);
          setState(t, "completed", "Task declined");
        }
        entry(t, "event", "You declined: " + n.body);
      } else if (n.request === "access") continueWork(t);
      else if (n.request === "review") approve(t);
      else {
        dispatch({ type: "select", id: t.id });
        start(t, "Help me plan the next steps for this task.");
      }
    },
    [cancel, setState, entry, continueWork, approve, start],
  );
  const reset = useCallback(
    (id: string) => {
      cancel(id);
      dispatch({ type: "reset", id });
    },
    [cancel],
  );
  const cancelRun = useCallback(
    (id: string) => {
      cancel(id);
      dispatch({ type: "cancel", id });
    },
    [cancel],
  );
  const send = useCallback(
    (t: Thread, text: string) => {
      if (t.state === "idle" || (t.memberIds && t.state === "completed"))
        start(t, text);
      else {
        entry(t, "user", text);
        if (t.memberIds)
          entry(
            t,
            "message",
            "Your additional note is in our shared work log. We’ll keep it alongside this ongoing demo.",
            latest.current.agents.find((a) => a.id === t.memberIds![0]),
          );
        else
          entry(
            t,
            "message",
            "Your note is recorded here. Continue the current task or reset this thread to begin another run.",
          );
      }
    },
    [start, entry],
  );
  return {
    state,
    dispatch,
    start,
    send,
    reset,
    cancelRun,
    setState,
    entry,
    continueWork,
    approve,
    decide,
  };
}
