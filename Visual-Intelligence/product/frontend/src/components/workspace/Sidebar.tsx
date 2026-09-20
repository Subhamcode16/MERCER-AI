import { useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";
import type { Agent, Thread, Project } from "./types";
import { stateLabels } from "./types";
import { Avatar } from "./Avatar";
import { Modal } from "./Modal";
import { Icon, IconButton } from "./Icon";
export function Sidebar({
  agents,
  threads,
  activeId,
  onSelect,
  projects,
  activeProjectId,
  onProject,
  onNew,
  onGroup,
  onEdit,
  width,
  onWidth,
  children,
}: {
  agents: Agent[];
  threads: Thread[];
  activeId: string;
  onSelect: (id: string) => void;
  projects: Project[];
  activeProjectId: string;
  onProject: (id: string) => void;
  onNew: (manager: boolean) => void;
  onGroup: () => void;
  onEdit: (agent: Agent, mode: "edit" | "delete") => void;
  width: number;
  onWidth: (width: number) => void;
  children: ReactNode;
}) {
  const [search, setSearch] = useState(""),
    [searching, setSearching] = useState(false),
    [projectOpen, setProjectOpen] = useState(false),
    [collapsed, setCollapsed] = useState<Record<string, boolean>>({});
  const searchRef = useRef<HTMLInputElement>(null);
  const projectPickerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (searching) searchRef.current?.focus();
  }, [searching]);
  useEffect(() => {
    if (!projectOpen) return;
    const close = (event: PointerEvent) => {
      if (!projectPickerRef.current?.contains(event.target as Node))
        setProjectOpen(false);
    };
    window.addEventListener("pointerdown", close);
    return () => window.removeEventListener("pointerdown", close);
  }, [projectOpen]);
  const rows = threads.filter((t) =>
    t.name.toLowerCase().includes(search.toLowerCase()),
  );
  function resizeFrom(clientX: number) {
    onWidth(Math.min(480, Math.max(260, clientX)));
  }
  function row(t: Thread) {
    const a = agents.find((a) => a.id === t.agentId),
      people = t.memberIds
        ?.map((id) => agents.find((a) => a.id === id)!)
        .filter(Boolean),
      last = t.events.at(-1);
    const preview =
      t.phase ||
      (t.state === "idle"
        ? people
          ? "New group · " + people.length + " members"
          : t.events.length === 1
            ? stateLabels.idle
            : last?.text
        : stateLabels[t.state]);
    return (
      <div className="thread-shell" key={t.id}>
        <button
          type="button"
          className="thread"
          aria-pressed={activeId === t.id}
          onClick={() => onSelect(t.id)}
        >
          <Avatar agent={a} members={people} state={t.state} />
          <span className="rowcopy">
            <span className="rowtop">
              <span className="rowname">{a?.name || t.name}</span>
              <span className="time">
                {people
                  ? people.length + " agents"
                  : t.state === "idle"
                    ? "Ready"
                    : "Now"}
              </span>
            </span>
            <span className="preview">{preview}</span>
          </span>
        </button>
        {a && (
          <div className="agent-actions">
            <button
              type="button"
              aria-label={`Edit ${a.name}`}
              onClick={() => onEdit(a, "edit")}
            >
              <Icon name="edit" />
            </button>
            <button
              type="button"
              aria-label={`Delete ${a.name}`}
              onClick={() => onEdit(a, "delete")}
            >
              <Icon name="trash" />
            </button>
          </div>
        )}
      </div>
    );
  }
  return (
    <aside className="sidebar" aria-label="Assistant navigation">
      <div className="project-picker">
        <div className="project-picker-swap" data-searching={searching}>
          {searching ? (
            <input
              ref={searchRef}
              className="search"
              aria-label="Search assistants"
              placeholder="Search assistants…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Escape") {
                  setSearch("");
                  setSearching(false);
                }
              }}
            />
          ) : (
            <div className="workspace-switcher" ref={projectPickerRef}>
              <button
                type="button"
                className="workspace-trigger"
                aria-label="Current project"
                aria-haspopup="listbox"
                aria-expanded={projectOpen}
                onClick={() => setProjectOpen((value) => !value)}
                onKeyDown={(event) => {
                  if (event.key === "Escape") setProjectOpen(false);
                }}
              >
                <span className="workspace-glyph">
                  {projects
                    .find((project) => project.id === activeProjectId)
                    ?.name.slice(0, 1)
                    .toUpperCase() || "W"}
                </span>
                <span className="workspace-trigger-copy">
                  <small>Workspace</small>
                  <strong>
                    {projects.find((project) => project.id === activeProjectId)
                      ?.name || "Choose workspace"}
                  </strong>
                </span>
                <Icon name="chevron" />
              </button>
              {projectOpen && (
                <div
                  className="workspace-menu"
                  role="listbox"
                  aria-label="Choose workspace"
                >
                  <div className="workspace-menu-heading">
                    <span>Switch workspace</span>
                    <small>{projects.length} available</small>
                  </div>
                  {projects.map((project) => {
                    const active = project.id === activeProjectId;
                    return (
                      <button
                        type="button"
                        role="option"
                        aria-selected={active}
                        key={project.id}
                        onClick={() => {
                          onProject(project.id);
                          setProjectOpen(false);
                        }}
                      >
                        <span className="workspace-option-glyph">
                          {project.name.slice(0, 1).toUpperCase()}
                        </span>
                        <span>
                          <strong>{project.name}</strong>
                          <small>
                            {active ? "Currently active" : "Open workspace"}
                          </small>
                        </span>
                        {active && <Icon name="check" />}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>
        <IconButton
          icon={searching ? "close" : "search"}
          label={searching ? "Close assistant search" : "Search assistants"}
          className="project-search-toggle"
          aria-pressed={searching}
          onClick={() => {
            if (searching) setSearch("");
            setSearching((value) => !value);
          }}
        />
      </div>
      {children}
      <div className="roster">
        {(["manager", "workforce", "groups"] as const).map((group) => {
          const list = rows.filter((t) =>
            group === "groups"
              ? !!t.memberIds
              : !t.memberIds &&
                !!agents.find((a) => a.id === t.agentId)?.manager ===
                  (group === "manager"),
          );
          return (
            <section
              key={group}
              aria-label={
                group === "manager"
                  ? "Manager"
                  : group === "groups"
                    ? "Your groups"
                    : "Your workforce"
              }
            >
              <div className="sectionhead">
                <button
                  type="button"
                  className="section-toggle"
                  aria-expanded={!collapsed[group]}
                  onClick={() =>
                    setCollapsed((value) => ({
                      ...value,
                      [group]: !value[group],
                    }))
                  }
                >
                  <span>
                    {group === "manager"
                      ? "Manager"
                      : group === "groups"
                        ? "Your groups"
                        : "Your workforce"}
                  </span>
                  <Icon name="chevron" />
                </button>
                <IconButton
                  icon="plus"
                  label={
                    group === "groups"
                      ? "Create group"
                      : group === "manager"
                        ? "Create manager"
                        : "Create agent"
                  }
                  onClick={() =>
                    group === "groups" ? onGroup() : onNew(group === "manager")
                  }
                />
              </div>
              {!collapsed[group] && list.map(row)}
            </section>
          );
        })}
        {!rows.length && (
          <p className="emptysearch">No conversations match your search.</p>
        )}
      </div>
      <div
        className="sidebar-resizer"
        role="separator"
        aria-label="Resize assistant navigation"
        aria-orientation="vertical"
        aria-valuemin={260}
        aria-valuemax={480}
        aria-valuenow={width}
        tabIndex={0}
        onPointerDown={(event) => {
          event.preventDefault();
          const move = (moveEvent: PointerEvent) =>
            resizeFrom(moveEvent.clientX);
          const stop = () => {
            window.removeEventListener("pointermove", move);
            window.removeEventListener("pointerup", stop);
            document.body.classList.remove("resizing-sidebar");
          };
          document.body.classList.add("resizing-sidebar");
          window.addEventListener("pointermove", move);
          window.addEventListener("pointerup", stop);
        }}
        onKeyDown={(event) => {
          if (event.key === "ArrowLeft") onWidth(Math.max(260, width - 10));
          if (event.key === "ArrowRight") onWidth(Math.min(480, width + 10));
          if (event.key === "Home") onWidth(260);
          if (event.key === "End") onWidth(480);
        }}
      />
    </aside>
  );
}
export function GroupDialog({
  agents,
  thread,
  onSave,
  onClose,
}: {
  agents: Agent[];
  thread?: Thread;
  onSave: (name: string, ids: string[]) => void;
  onClose: () => void;
}) {
  const [name, setName] = useState(thread?.name || ""),
    [ids, setIds] = useState(thread?.memberIds || []),
    [error, setError] = useState("");
  return (
    <Modal
      title={thread ? "Group members" : "Create a group"}
      onClose={onClose}
      className="group-modal"
    >
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (ids.length < 2 || !name.trim()) {
            setError("Enter a group name and select at least two agents.");
            return;
          }
          onSave(name, ids);
        }}
      >
        <div className="dialogbody">
          <label className="group-field">
            Group name
            <input
              required
              maxLength={60}
              value={name}
              placeholder="e.g. Product launch team"
              onChange={(e) => setName(e.target.value)}
            />
          </label>
          <fieldset className="member-options">
            <legend>Your workforce · select at least two members</legend>
            {agents
              .filter((a) => !a.manager)
              .map((a) => (
                <label key={a.id} className="member-option">
                  <input
                    type="checkbox"
                    checked={ids.includes(a.id)}
                    onChange={(e) =>
                      setIds(
                        e.target.checked
                          ? [...ids, a.id]
                          : ids.filter((id) => id !== a.id),
                      )
                    }
                  />
                  <Avatar agent={a} />
                  <span>
                    <strong>{a.name}</strong>
                    <small>{a.role}</small>
                  </span>
                </label>
              ))}
          </fieldset>
          {error && <p role="alert">{error}</p>}
        </div>
        <div className="dialogfoot">
          <span className="subtitle">
            Group chat uses simulated responses for now.
          </span>
          <button type="submit" className="primary">
            {thread ? "Save members" : "Create group"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export function AgentDialog({
  agent,
  mode,
  onClose,
  onSave,
  onDelete,
}: {
  agent: Agent;
  mode: "edit" | "delete";
  onClose: () => void;
  onSave: (name: string, role: string) => void;
  onDelete: () => void;
}) {
  const [name, setName] = useState(agent.name),
    [role, setRole] = useState(agent.role);
  if (mode === "delete")
    return (
      <Modal title="Delete agent" onClose={onClose}>
        <div className="dialogbody">
          <p>
            Delete <strong>{agent.name}</strong> and this agent's project chats?
          </p>
          <p className="subtitle">
            This removes the agent from groups and cannot be undone in this
            session.
          </p>
        </div>
        <div className="dialogfoot">
          <button type="button" onClick={onClose}>
            Cancel
          </button>
          <button type="button" className="danger-action" onClick={onDelete}>
            Delete agent
          </button>
        </div>
      </Modal>
    );
  return (
    <Modal title="Edit agent" onClose={onClose}>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          if (name.trim()) onSave(name, role);
        }}
      >
        <div className="dialogbody">
          <label className="group-field">
            Agent name
            <input
              autoFocus
              value={name}
              onChange={(event) => setName(event.target.value)}
              maxLength={60}
            />
          </label>
          <label className="group-field">
            Role
            <input
              value={role}
              onChange={(event) => setRole(event.target.value)}
              maxLength={90}
            />
          </label>
        </div>
        <div className="dialogfoot">
          <button type="button" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" className="primary">
            Save changes
          </button>
        </div>
      </form>
    </Modal>
  );
}
