import type { ButtonHTMLAttributes } from "react";
const paths = {
  plus: "M12 5v14M5 12h14",
  close: "m6 6 12 12M18 6 6 18",
  reset: "M4 10a8 8 0 1 1 1 8M4 4v6h6",
  play: "m8 5 11 7-11 7Z",
  menu: "M4 6h16M4 12h16M4 18h16",
  check: "m5 12 4 4L19 6",
  checkCheck: "M18 6 7 17l-5-5M22 10l-7.5 7.5L13 16",
  file: "M14 3H5v18h14V8l-5-5ZM14 3v5h5",
  arrow: "M5 12h14m-6-6 6 6-6 6",
  arrowDown: "M12 5v14m-6-6 6 6 6-6",
  send: "M12 19V5m-6 6 6-6 6 6",
  mic: "M9 4a3 3 0 0 1 6 0v8a3 3 0 0 1-6 0ZM6 11v1a6 6 0 0 0 12 0M12 18v3",
  wave: "M5 10v4M9 7v10M12 5v14M15 8v8M19 10v4",
  shield: "m12 3-8 3v6c0 5 8 9 8 9s8-4 8-9V6Z",
  model: "M4 4h16v16H4ZM8 8h8v8H8Z",
  chevron: "m8 10 4 4 4-4",
  group:
    "M3 21v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6M18 14v7M14.5 17.5h7M12 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0",
  bell: "M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4",
  palette:
    "M12 3a9 9 0 1 0 0 18h1a2 2 0 0 0 1-4c-1-1 0-3 2-3h2a3 3 0 0 0 3-3 9 9 0 0 0-9-8ZM7 10h.01M10 7h.01M15 7h.01",
  more: "M5 12h.01M12 12h.01M19 12h.01",
  archive: "M4 9h16v12H4ZM3 3h18v6H3ZM9 13h6",
  watch: "M9 2h6M12 2v3m6 1 2 2M12 9v5l3 2M20 14a8 8 0 1 1-16 0 8 8 0 0 1 16 0",
  attention: "M12 3v12m0 5h.01",
  edit: "M4 20h4L19 9l-4-4L4 16v4Zm9-13 4 4",
  trash: "M4 7h16M9 7V4h6v3m3 0-1 14H7L6 7m4 4v6m4-6v6",
  search: "m21 21-4.4-4.4M19 11a8 8 0 1 1-16 0 8 8 0 0 1 16 0",
  scrubber: "M4 6h16M4 12h10M4 18h14",
  settings:
    "M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm8 3 2-1-2-4-2 .5-2-1L15 3h-6L8 7.5l-2 1L4 7l-2 4 2 1-2 1 2 4 2-1.5 2 1L9 21h6l1-4.5 2-1 2 1.5 2-4-2-1Z",
  home: "M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1V9.5Z",
  metrics: "M18 20V10M12 20V4M6 20v-6",
  kanban: "M4 4h4v16H4zm6 0h4v16h-4zm6 0h4v16h-4z",
  assets: "M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z",
  grid: "M3 3h7v7H3zm11 0h7v7h-7zm0 11h7v7h-7zm-11 0h7v7H3z",
};
export type IconName = keyof typeof paths;
export function Icon({
  name,
  className,
}: {
  name: IconName;
  className?: string;
}) {
  return (
    <svg className={className} aria-hidden="true" viewBox="0 0 24 24">
      <path d={paths[name]} />
    </svg>
  );
}
export function IconButton({
  icon,
  label,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  icon: IconName;
  label: string;
}) {
  return (
    <button
      type="button"
      {...props}
      aria-label={label}
      title={label}
      className={"icon-only " + (props.className || "")}
    >
      <Icon name={icon} />
    </button>
  );
}
