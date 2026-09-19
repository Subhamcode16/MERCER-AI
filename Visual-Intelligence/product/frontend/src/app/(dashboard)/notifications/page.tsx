"use client";

export default function NotificationsPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative bg-background text-foreground">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-muted-foreground/60 mb-12">
        <span>System</span>
        <span>/</span>
        <span className="text-foreground">Notifications</span>
      </div>

      {/* Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-2xl mx-auto w-full text-center">
        <div className="text-[13px] text-muted-foreground font-normal">
          System is quiet. No recent events.
        </div>
      </div>

    </div>
  );
}
