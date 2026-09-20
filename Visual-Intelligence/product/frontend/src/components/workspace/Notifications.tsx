import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import type { Dispatch } from "react";
import type { Notification, Project, Thread } from "./types";
import type { Action } from "./store";
import { Icon } from "./Icon";
const tabs = ["all", "inbox", "following", "archived"] as const;
type Tab = (typeof tabs)[number];
export function Notifications({
  items,
  dispatch,
  onDecision,
  onOpen,
  projects,
  threads,
}: {
  items: Notification[];
  dispatch: Dispatch<Action>;
  onDecision: (n: Notification, d: "Accepted" | "Declined") => void;
  onOpen: (id: string) => void;
  projects: Project[];
  threads: Thread[];
}) {
  const [open, setOpen] = useState(false),
    [tab, setTab] = useState<Tab>("all"),
    [menu, setMenu] = useState<{
      id: string;
      left: number;
      top: number;
    } | null>(null),
    [position, setPosition] = useState({ left: 12, top: 70 });
  const bell = useRef<HTMLButtonElement>(null),
    panel = useRef<HTMLElement>(null),
    rowMenu = useRef<HTMLDivElement>(null),
    rowTrigger = useRef<HTMLButtonElement | null>(null);
  const unread = items.filter((n) => n.unread && !n.archived).length;
  const shown = items.filter((n) =>
    tab === "archived"
      ? n.archived
      : !n.archived &&
        (tab === "inbox"
          ? n.unread || (n.request && !n.resolved)
          : tab === "following"
            ? n.following
            : true),
  );
  const current = items.find((n) => n.id === menu?.id);
  function close() {
    setOpen(false);
    setMenu(null);
    bell.current?.focus();
  }
  useLayoutEffect(() => {
    if (!open) return;
    function place() {
      const r = bell.current!.getBoundingClientRect(),
        p = panel.current!;
      setPosition({
        left: Math.max(
          12,
          Math.min(r.right - p.offsetWidth, innerWidth - p.offsetWidth - 12),
        ),
        top: Math.min(
          r.bottom + 10,
          Math.max(12, innerHeight - p.offsetHeight - 12),
        ),
      });
      setMenu(null);
    }
    place();
    window.addEventListener("resize", place);
    return () => window.removeEventListener("resize", place);
  }, [open, items, tab]);
  useEffect(() => {
    if (!open) return;
    const outside = (e: PointerEvent) => {
      const target = e.target as Node;
      if (
        !panel.current?.contains(target) &&
        !bell.current?.contains(target) &&
        !rowMenu.current?.contains(target)
      )
        close();
    };
    const key = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        if (rowMenu.current) {
          setMenu(null);
          rowTrigger.current?.focus();
        } else close();
      }
    };
    document.addEventListener("pointerdown", outside);
    document.addEventListener("keydown", key);
    panel.current
      ?.querySelector<HTMLButtonElement>("[aria-selected=true]")
      ?.focus();
    return () => {
      document.removeEventListener("pointerdown", outside);
      document.removeEventListener("keydown", key);
    };
  }, [open]);
  useEffect(() => {
    if (menu) rowMenu.current?.querySelector("button")?.focus();
  }, [menu]);
  function age(time: number) {
    const m = Math.floor((Date.now() - time) / 60000);
    return m < 1
      ? "Just now"
      : m < 60
        ? m + " min ago"
        : Math.floor(m / 60) + " hours ago";
  }
  const patch = (id: string, values: Partial<Notification>) =>
    dispatch({ type: "notification", id, patch: values });
  return (
    <>
      <button
        ref={bell}
        type="button"
        id="notificationBell"
        className="icon-only"
        aria-label={"Notifications" + (unread ? ", " + unread + " unread" : "")}
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-controls="notificationPanel"
        onClick={() => (open ? close() : setOpen(true))}
      >
        <Icon name="bell" />
        {unread > 0 && (
          <span className="notification-dot" aria-hidden="true">
            {unread > 9 ? "9+" : unread}
          </span>
        )}
      </button>
      {open &&
        createPortal(
          <section
            ref={panel}
            id="notificationPanel"
            role="dialog"
            aria-labelledby="notificationTitle"
            style={position}
          >
            <div className="notification-head">
              <h2 id="notificationTitle">Notifications</h2>
              <div className="notification-head-actions">
                <button
                  type="button"
                  className="icon-only notification-mark-all"
                  aria-label="Mark all as read"
                  title="Mark all as read"
                  disabled={!unread}
                  onClick={() => dispatch({ type: "read-all" })}
                >
                  <Icon name="checkCheck" />
                </button>
                <button
                  type="button"
                  className="icon-only"
                  aria-label="Close notifications"
                  title="Close notifications"
                  onClick={close}
                >
                  <Icon name="close" />
                </button>
              </div>
            </div>
            <div
              className="notification-tabs"
              role="tablist"
              aria-label="Notification filters"
            >
              {tabs.map((t, i) => (
                <button
                  key={t}
                  type="button"
                  role="tab"
                  aria-selected={tab === t}
                  tabIndex={tab === t ? 0 : -1}
                  aria-controls="notificationList"
                  onClick={() => setTab(t)}
                  onKeyDown={(e) => {
                    if (
                      ["ArrowRight", "ArrowLeft", "Home", "End"].includes(e.key)
                    ) {
                      e.preventDefault();
                      const next =
                        e.key === "Home"
                          ? 0
                          : e.key === "End"
                            ? 3
                            : (i + (e.key === "ArrowRight" ? 1 : 3)) % 4;
                      setTab(tabs[next]);
                      e.currentTarget
                        .parentElement!.querySelectorAll<HTMLButtonElement>(
                          "button",
                        )
                        [next].focus();
                    }
                  }}
                >
                  {t[0].toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
            <div
              className="notification-list"
              id="notificationList"
              role="tabpanel"
              aria-label={tab + " notifications"}
              onScroll={() => setMenu(null)}
            >
              {shown.map((n) => (
                <article
                  key={n.id}
                  className={"notification-row " + (n.unread ? "unread" : "")}
                >
                  <div
                    className="notification-face"
                    aria-hidden="true"
                    style={{ color: n.actor.color }}
                  >
                    {n.actor.initials}
                    <span style={{ background: n.actor.color }}>
                      <Icon name={n.request ? "attention" : "file"} />
                    </span>
                  </div>
                  <div className="notification-copy">
                    <div className="notification-top">
                      <button
                        type="button"
                        className="notification-open"
                        onClick={() => {
                          patch(n.id, { unread: false });
                          onOpen(n.threadId);
                          close();
                        }}
                      >
                        <p className="notification-sentence">
                          <strong>{n.actor.name}</strong> {n.body}
                        </p>
                        <div className="notification-meta">
                          {age(n.time)} ·{" "}
                          {projects.find((p) => p.id === n.projectId)?.name ||
                            "Project"}{" "}
                          ·{" "}
                          {threads.find((t) => t.id === n.threadId)?.name ||
                            "Task"}
                          {n.count > 1 ? " · " + n.count + " updates" : ""}
                        </div>
                      </button>
                      <button
                        type="button"
                        className="notification-options"
                        aria-label={
                          "Options for notification from " + n.actor.name
                        }
                        aria-haspopup="menu"
                        aria-expanded={menu?.id === n.id}
                        onClick={(e) => {
                          if (menu?.id === n.id) {
                            setMenu(null);
                            return;
                          }
                          rowTrigger.current = e.currentTarget;
                          const r = e.currentTarget.getBoundingClientRect(),
                            p = panel.current!.getBoundingClientRect();
                          setMenu({
                            id: n.id,
                            left: Math.max(
                              12,
                              Math.min(r.right - 170, innerWidth - 182),
                            ),
                            top: Math.max(
                              p.top + 12,
                              Math.min(
                                r.bottom + 5,
                                p.bottom - 88,
                                innerHeight - 100,
                              ),
                            ),
                          });
                        }}
                      >
                        <Icon name="more" />
                      </button>
                      {n.unread && (
                        <span
                          className="notification-unread"
                          aria-label="Unread"
                        />
                      )}
                    </div>
                    {n.resolved ? (
                      <p className="notification-result" role="status">
                        <Icon
                          name={n.resolved === "Accepted" ? "check" : "close"}
                        />
                        {n.resolved}
                      </p>
                    ) : n.request ? (
                      <div className="notification-actions">
                        <button
                          type="button"
                          className="primary"
                          onClick={() => onDecision(n, "Accepted")}
                        >
                          <Icon name="check" />
                          Accept
                        </button>
                        <button
                          type="button"
                          onClick={() => onDecision(n, "Declined")}
                        >
                          <Icon name="close" />
                          Decline
                        </button>
                      </div>
                    ) : null}
                  </div>
                </article>
              ))}
              {!shown.length && (
                <div className="notification-empty">
                  You’re all caught up here.
                </div>
              )}
            </div>
            <div className="notification-footer">
              Local demo · task decisions stay in this session
            </div>
          </section>,
          document.body,
        )}
      {menu &&
        current &&
        createPortal(
          <div
            ref={rowMenu}
            role="menu"
            id="notificationMenu"
            style={{ left: menu.left, top: menu.top }}
            onKeyDown={(e) => {
              if (["ArrowDown", "ArrowUp", "Home", "End"].includes(e.key)) {
                e.preventDefault();
                const buttons =
                    e.currentTarget.querySelectorAll<HTMLButtonElement>(
                      "button",
                    ),
                  i = Array.from(buttons).indexOf(
                    document.activeElement as HTMLButtonElement,
                  );
                buttons[
                  e.key === "Home" ? 0 : e.key === "End" ? 1 : (i + 1) % 2
                ].focus();
              }
            }}
          >
            <button
              type="button"
              role="menuitem"
              onClick={() => {
                patch(current.id, { unread: !current.unread });
                setMenu(null);
                rowTrigger.current?.focus();
              }}
            >
              <Icon name="check" />
              {current.unread ? "Mark as read" : "Mark as unread"}
            </button>
            <button
              type="button"
              role="menuitem"
              onClick={() => {
                patch(current.id, { archived: !current.archived });
                setMenu(null);
                panel.current
                  ?.querySelector<HTMLButtonElement>("[aria-selected=true]")
                  ?.focus();
              }}
            >
              <Icon name="archive" />
              {current.archived ? "Move to inbox" : "Archive"}
            </button>
          </div>,
          document.body,
        )}
    </>
  );
}
