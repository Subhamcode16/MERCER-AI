import { useEffect, useRef } from "react";
import type { ReactNode } from "react";
import { IconButton } from "./Icon";
export function Modal({
  title,
  onClose,
  children,
  className = "",
}: {
  title: string;
  onClose: () => void;
  children: ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current!,
      focus = document.activeElement as HTMLElement;
    dialog.showModal();
    return () => {
      dialog.close();
      focus?.isConnected && focus.focus();
    };
  }, []);
  return (
    <dialog
      ref={ref}
      className={className}
      aria-label={title}
      onCancel={(e) => {
        e.preventDefault();
        onClose();
      }}
    >
      <div className="dialoghead">
        <strong>{title}</strong>
        <IconButton
          icon="close"
          label={"Close " + title.toLowerCase()}
          onClick={onClose}
        />
      </div>
      {children}
    </dialog>
  );
}
