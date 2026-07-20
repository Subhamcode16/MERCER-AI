import Link from 'next/link';

export function Sidebar() {
  return (
    <aside className="w-[280px] flex flex-col h-screen border-r border-white/5 bg-[#0a0a0a] flex-shrink-0 z-50">
      {/* Brand */}
      <div className="p-8 pb-12 flex flex-col items-start cursor-pointer hover:opacity-80 transition-opacity">
        <h1 className="font-serif text-[24px] tracking-[0.25em] mb-2 text-white">ATELIER</h1>
        <p className="text-[9px] tracking-[0.3em] uppercase text-white/40 font-medium ml-1">Creative Intelligence</p>
      </div>

      {/* Navigation - Institution */}
      <div className="px-6 flex flex-col flex-1">
        <p className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-6 ml-2">Institution</p>
        <nav className="flex flex-col gap-2">
          <Link href="/studio" className="flex items-center gap-4 px-4 py-3 rounded-lg bg-white/5 border border-white/10 text-[13px] font-medium text-[var(--color-warm-ivory)]">
            <div className="w-4 h-4 rounded-sm border border-[var(--color-warm-ivory)]/50 grid grid-cols-2 gap-0.5 p-0.5">
              <div className="bg-[var(--color-warm-ivory)] rounded-[1px]"></div>
              <div className="bg-[var(--color-warm-ivory)] rounded-[1px]"></div>
              <div className="bg-[var(--color-warm-ivory)] rounded-[1px]"></div>
              <div className="bg-[var(--color-warm-ivory)] rounded-[1px]"></div>
            </div>
            Campaign Studio
          </Link>
          <NavItem active={false} label="Material Library" />
          <NavItem active={false} label="Atlas" />
          <NavItem active={false} label="Research" />
          <NavItem active={false} label="Knowledge" />
          <NavItem active={false} label="Archive" />
        </nav>

        {/* Navigation - System */}
        <p className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-6 ml-2 mt-12">System</p>
        <nav className="flex flex-col gap-2">
          <NavItem active={false} label="Notifications" />
          <NavItem active={false} label="Activity" />
          <NavItem active={false} label="Settings" />
        </nav>
      </div>

      {/* User */}
      <div className="p-6 border-t border-white/5">
        <div className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-white/5 transition-colors cursor-pointer">
          <div className="w-8 h-8 rounded-full bg-white/10 overflow-hidden flex items-center justify-center border border-white/20">
            <img src="/public_backup/assets/fashion_hero_3_1783581286733.png" alt="User" className="w-full h-full object-cover" />
          </div>
          <div className="flex flex-col">
            <span className="text-[12px] font-medium text-white/90">Creative Director</span>
            <span className="text-[10px] text-white/40 mt-0.5">creative@atelier.com</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

function NavItem({ label, active }: { label: string; active?: boolean }) {
  return (
    <Link href="#" className="flex items-center gap-4 px-4 py-3 rounded-lg text-[13px] text-white/50 hover:text-white hover:bg-white/5 transition-colors group">
      <div className="w-4 h-4 flex flex-col items-center justify-center">
        <div className="w-[3px] h-[3px] bg-white/40 group-hover:bg-white/80 rounded-full transition-colors" />
      </div>
      {label}
    </Link>
  );
}
