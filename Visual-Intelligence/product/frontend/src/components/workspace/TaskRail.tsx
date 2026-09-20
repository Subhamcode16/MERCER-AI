import { useState } from "react";
import type { Agent, Project, Thread } from "./types";
import { stateLabels } from "./types";
import { Avatar } from "./Avatar";
import { Icon } from "./Icon";
import { Modal } from "./Modal";
import { LiquidGlassSurface } from "./LiquidGlassSurface";

export function TaskRail({
  project,
  owner,
  tasks,
  activeId,
  agents,
  onSelect,
  onCreate,
}: {
  project: Project;
  owner: Thread;
  tasks: Thread[];
  activeId: string;
  agents: Agent[];
  onSelect: (id: string) => void;
  onCreate: (name: string) => void;
}) {
  const [creating, setCreating] = useState(false),
    [name, setName] = useState("");
  const ownerAgent = agents.find((a) => a.id === owner.agentId),
    people = owner.memberIds
      ?.map((id) => agents.find((a) => a.id === id)!)
      .filter(Boolean);
  return (
    <div
      className="task-rail"
      role="region"
      aria-label="Chats in current project"
    >
      <div className="task-rail-head">
        <div className="task-heading-copy">
          <span className="task-heading-line">
            <strong>Recent chats</strong>
            <span className="task-count">{tasks.length}</span>
          </span>
          <small>{project.name}</small>
        </div>
        <button
          type="button"
          className="new-task-button"
          aria-label="Create new task"
          title="Create new task"
          onClick={() => setCreating(true)}
        >
          <Icon name="plus" />
        </button>
      </div>
      <div className="task-list">
        {tasks.map((t) => {
          const active = t.id === activeId;
          return (
            <button
              key={t.id}
              type="button"
              aria-pressed={active}
              onClick={() => onSelect(t.id)}
            >
              {active && (
                <LiquidGlassSurface
                  className="task-liquid-host"
                  tintOpacity={0.13}
                  borderRadius={11}
                />
              )}
              <Avatar agent={ownerAgent} members={people} state={t.state} />
              <span className="task-copy">
                <strong>{t.name}</strong>
                <small>{t.phase || stateLabels[t.state]}</small>
              </span>
              <span className="task-meta" aria-hidden="true">
                <i className={`task-status task-status-${t.state}`} />
                {t.state === "idle" ? "Ready" : "Now"}
              </span>
            </button>
          );
        })}
      </div>
      {!tasks.length && (
        <div className="task-empty">
          <p>No tasks here yet.</p>
          <button type="button" onClick={() => setCreating(true)}>
            Create the first task
          </button>
        </div>
      )}
      {creating && (
        <Modal
          title="Start a new chat"
          className="new-task-modal"
          onClose={() => setCreating(false)}
        >
          <form
            className="new-task-form"
            onSubmit={(e) => {
              e.preventDefault();
              if (name.trim()) {
                onCreate(name);
                setCreating(false);
              }
            }}
          >
            <div className="dialogbody">
              <p className="new-task-intro">
                Give this conversation a clear, useful name.
              </p>
              <label className="group-field">
                <span>Chat name</span>
                <input
                  autoFocus
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Compare launch research"
                />
              </label>
            </div>
            <div className="dialogfoot">
              <button
                type="button"
                className="new-task-cancel"
                onClick={() => setCreating(false)}
              >
                Cancel
              </button>
              <button className="primary new-task-submit">
                Create chat
                <Icon name="arrow" />
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
}

export function ProjectDialog({
  onClose,
  onCreate,
}: {
  onClose: () => void;
  onCreate: (name: string) => void;
}) {
  const [name, setName] = useState("");
  return (
    <Modal title="Create a project" onClose={onClose}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (name.trim()) onCreate(name);
        }}
      >
        <div className="dialogbody">
          <label className="group-field">
            Project name
            <input
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Autumn launch"
            />
          </label>
          <p className="subtitle">
            Each project keeps separate tasks, files, drafts, and activity.
          </p>
        </div>
        <div className="dialogfoot">
          <button type="button" onClick={onClose}>
            Cancel
          </button>
          <button className="primary">Create project</button>
        </div>
      </form>
    </Modal>
  );
}
