import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { isWorking } from "../types";
import type { Agent, Thread } from "../types";
import { Avatar } from "./Avatar";
import { Icon } from "./Icon";
import { Modal } from "./Modal";
import { ToolCalls } from "./ToolCalls";
export function WorkspacePreview() {
  return (
    <div className="workspace">
      <div className="mockwindow">
        <div className="mockbar">Example collection / brief workspace</div>
        <div className="mockbody">
          <strong>Source collection</strong>
          <div className="mockrow">
            <span>Interviews & notes</span>
            <span>12 sources</span>
          </div>
          <div className="mockrow">
            <span>Industry references</span>
            <span>8 sources</span>
          </div>
          <div className="mockrow">
            <span>Recommendations</span>
            <span>Pending</span>
          </div>
        </div>
      </div>
    </div>
  );
}
function Stopwatch({ thread }: { thread: Thread }) {
  const [now, setNow] = useState(() => performance.now());
  useEffect(() => {
    if (!isWorking(thread.state)) return;
    const timer = setInterval(() => setNow(performance.now()), 250);
    return () => clearInterval(timer);
  }, [thread.state]);
  const seconds = Math.floor(
      (thread.elapsed +
        (thread.startedAt === null ? 0 : Math.max(0, now - thread.startedAt))) /
        1000,
    ),
    minutes = Math.floor(seconds / 60);
  return (
    <div className="operation-stopwatch">
      <Icon name="watch" />
      <span>
        {isWorking(thread.state) ? "Working" : "Worked"} for{" "}
        {minutes ? minutes + "m " : ""}
        {seconds % 60}s
      </span>
    </div>
  );
}
function MentionText({ text, agents }: { text: string; agents: Agent[] }) {
  const regex = new RegExp(
    "(@(?:" +
      agents
        .map((a) => a.name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
        .sort((a, b) => b.length - a.length)
        .join("|") +
      "))",
    "g",
  );
  return (
    <>
      {text.split(regex).map((piece, i) =>
        piece.startsWith("@") && agents.some((a) => "@" + a.name === piece) ? (
          <span key={i} className="mention">
            {piece}
          </span>
        ) : (
          piece
        ),
      )}
    </>
  );
}
export function Conversation({
  thread,
  agents,
  onHandoff,
  onApprove,
  onRevise,
  onRoutine,
}: {
  thread: Thread;
  agents: Agent[];
  onHandoff: () => void;
  onApprove: () => void;
  onRevise: () => void;
  onRoutine: () => void;
}) {
  const feed = useRef<HTMLDivElement>(null),
    [follow, setFollow] = useState(true),
    following = useRef(true);
  const working = isWorking(thread.state),
    agent = agents.find((a) => a.id === thread.agentId),
    people = thread.memberIds
      ?.map((id) => agents.find((a) => a.id === id)!)
      .filter(Boolean);
  const lastMessage = thread.events.findLastIndex((e) => e.kind === "message");
  useLayoutEffect(() => {
    following.current = true;
    setFollow(true);
  }, [thread.id]);
  useLayoutEffect(() => {
    if (following.current && feed.current)
      feed.current.scrollTop = feed.current.scrollHeight;
  }, [thread.events, thread.state, thread.id]);
  return (
    <div
      className="feed"
      ref={feed}
      aria-label="Conversation history"
      onScroll={(e) => {
        const el = e.currentTarget,
          atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 90;
        following.current = atBottom;
        setFollow(atBottom);
      }}
    >
      <div className="feed-container">
        <div className="day">TODAY / YOUR WORK LOG</div>
        {thread.events.map((e, i) => {
          const actor = e.actor || agent,
            user = e.kind === "user";
          const timing =
            !working &&
            thread.state !== "idle" &&
            (thread.elapsed > 0 || thread.startedAt !== null) &&
            i === lastMessage;
          return (
            <div key={e.id} id={"event-" + e.id} className="event-anchor">
              {timing && <Stopwatch thread={thread} />}
              {e.kind === "event" ? (
                <div className="event entry">{e.text}</div>
              ) : e.kind === "tool" ? (
                <>
                  <ToolCalls defaultExpanded={false} />
                  <section className="tool entry">
                  <div className="tooltop">
                    <strong>Source workspace</strong>
                    <span className="badge">
                      {thread.access ? "Access granted" : "Action needed"}
                    </span>
                  </div>
                  <p>Open the workspace to grant simulated source access.</p>
                  <WorkspacePreview />
                  <div className="actions">
                    <button
                      type="button"
                      className="primary with-icon"
                      disabled={
                        !["action_needed", "human_control"].includes(thread.state)
                      }
                      onClick={onHandoff}
                    >
                      <Icon name="arrow" />
                      Open workspace
                    </button>
                  </div>
                </section>
              </>
            ) : e.kind === "review" ? (
                <section className="review entry">
                  <h2>Landscape brief · draft v1</h2>
                  <p>
                    Three recommendations grounded in the example source
                    collection.
                  </p>
                  <div className="metrics">
                    {[
                      ["20", "Sources reviewed"],
                      ["3", "Recommendations"],
                      ["1", "Draft ready"],
                    ].map(([n, label]) => (
                      <div className="metric" key={label}>
                        <strong>{n}</strong>
                        <span>{label}</span>
                      </div>
                    ))}
                  </div>
                  <p>
                    Start with one focused workflow, keep the review step visible,
                    and make recurring work easy to revisit.
                  </p>
                  <div className="actions">
                    <button
                      type="button"
                      className="primary with-icon"
                      onClick={onApprove}
                      disabled={thread.state !== "review_ready"}
                    >
                      <Icon name="check" />
                      Approve draft
                    </button>
                    <button
                      type="button"
                      className="with-icon"
                      onClick={onRevise}
                      disabled={thread.state !== "review_ready"}
                    >
                      <Icon name="reset" />
                      Request revision
                    </button>
                    <button
                      type="button"
                      className="with-icon"
                      onClick={onRoutine}
                      disabled={thread.routine}
                    >
                      <Icon name="watch" />
                      {thread.routine ? "Routine added" : "Add weekly routine"}
                    </button>
                  </div>
                </section>
              ) : (
                <article
                  className={"message-row entry " + (user ? "from-user" : "")}
                  aria-label={
                    "Message from " +
                    (user ? "You" : actor?.name || "Group assistant")
                  }
                >
                  {user ? (
                    <span className="avatar user-avatar" aria-hidden="true">
                      YO
                    </span>
                  ) : (
                    <Avatar agent={actor} />
                  )}
                  <div className="message-content">
                    <div className={"message " + (user ? "outgoing" : "")}>
                      <div className="sender-name">
                        {user ? "You" : actor?.name || "Group assistant"}
                      </div>
                      <div className="message-text">
                        <MentionText text={e.text} agents={agents} />
                      </div>
                    </div>
                  </div>
                </article>
              )}
            </div>
          );
        })}
        {working && (
          <>
            <Stopwatch thread={thread} />
            <div className="thinking" role="status">
              <Avatar agent={agent} members={people} state={thread.state} />
              <span>{thread.name}</span>
              <span className="dots" aria-hidden="true">
                <i />
              </span>
              <span>{thread.phase || "Preparing the run"}</span>
            </div>
          </>
        )}
      </div>
      {!follow && (
        <button
          type="button"
          className="newactivity"
          aria-label="Jump to latest activity"
          title="Jump to latest activity"
          onClick={() => {
            following.current = true;
            setFollow(true);
            feed.current!.scrollTop = feed.current!.scrollHeight;
          }}
        >
          <Icon name="arrowDown" />
        </button>
      )}
    </div>
  );
}
export function Handoff({
  name,
  onClose,
  onResume,
}: {
  name: string;
  onClose: () => void;
  onResume: () => void;
}) {
  const [granted, setGranted] = useState(false);
  return (
    <Modal title="Workspace access" onClose={onClose}>
      <div className="dialogbody">
        <WorkspacePreview />
        <p>
          {name} needs access to an example document collection. This is a local
          demonstration.
        </p>
        <button
          type="button"
          className="primary with-icon"
          disabled={granted}
          onClick={() => setGranted(true)}
        >
          <Icon name="check" />
          {granted ? "Demo access granted" : "Grant demo access"}
        </button>
      </div>
      <div className="dialogfoot">
        <span className="subtitle">
          {granted
            ? "Demo access is ready."
            : "Demo access has not been granted."}
        </span>
        <button
          type="button"
          className="primary with-icon"
          disabled={!granted}
          onClick={onResume}
        >
          <Icon name="arrow" />
          Return to assistant
        </button>
      </div>
    </Modal>
  );
}
