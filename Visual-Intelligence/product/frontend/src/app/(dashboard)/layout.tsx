"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { UserPopover } from "@/components/UserPopover";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { session, profile, isLoading, logout, openAuthModal } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-[100dvh] bg-[#0A0A0A] flex items-center justify-center">
        <div className="text-[10px] tracking-[0.2em] uppercase text-white/30">Loading Mercer AI</div>
      </div>
    );
  }

  return (
    <div className="flex min-h-[100dvh] bg-[#0A0A0A] text-white/90 font-sans font-light selection:bg-white/20">
      
      {/* Architectural Navigation - Strict typography, no heavy icons */}
      <aside className="w-[280px] flex flex-col shrink-0 pl-10 pr-6 py-12 border-r border-white/5 relative z-20">
        
        {/* Brand */}
        <div className="mb-16">
          <Link href="/studio" className="font-serif text-2xl tracking-[0.05em] bg-gradient-to-r from-[#E1D4C0] via-[#C9B99A] to-[#8C8472] bg-clip-text text-transparent">
            M E R C E R   A I
          </Link>
          <div className="text-[9px] tracking-[0.2em] uppercase text-white/40 mt-3 font-medium">
            Creative Intelligence
          </div>
        </div>

        {/* Primary Modules */}
        <nav className="flex flex-col gap-10 flex-1">
          <div>
            <div className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-6 font-medium">Institution</div>
            <div className="flex flex-col gap-3">
              <NavLink href="/studio" active={pathname === '/studio'}>Campaign Studio</NavLink>
              <NavLink href="/materials" active={pathname.includes('/materials')}>Material Library</NavLink>
              <NavLink href="/atlas" active={pathname.includes('/atlas')}>Atlas</NavLink>
              <NavLink href="/research" active={pathname.includes('/research')}>Research</NavLink>
              <NavLink href="/knowledge" active={pathname.includes('/knowledge')}>Knowledge</NavLink>
              <NavLink href="/archive" active={pathname.includes('/archive')}>Archive</NavLink>
            </div>
          </div>

          <div>
            <div className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-6 font-medium">System</div>
            <div className="flex flex-col gap-3">
              <NavLink href="/notifications" active={pathname.includes('/notifications')}>Notifications</NavLink>
              <NavLink href="/settings" active={pathname.includes('/settings')}>Settings</NavLink>
            </div>
          </div>
        </nav>

        {/* User Status */}
        <div className="pt-10 mt-auto border-t border-white/5 relative">
          {session && profile ? (
            <UserPopover profile={profile} logout={logout} />
          ) : (
            <div className="flex gap-4">
              <button 
                onClick={() => openAuthModal("login")}
                className="text-[11px] text-white/60 hover:text-[#E1D4C0] transition-colors"
              >
                Log In
              </button>
              <button 
                onClick={() => openAuthModal("signup")}
                className="text-[11px] text-white/60 hover:text-[#E1D4C0] transition-colors"
              >
                Sign Up
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Main Architectural Workspace */}
      <main className="flex-1 relative flex flex-col min-w-0 bg-[#0A0A0A]">
        {children}
      </main>

    </div>
  );
}

function NavLink({ href, active, children }: { href: string, active: boolean, children: React.ReactNode }) {
  return (
    <Link 
      href={href}
      className={`text-[13px] tracking-wide transition-all duration-300 flex items-center gap-4 px-3 py-2 -ml-3 rounded-md ${
        active 
          ? 'bg-[#E1D4C0] text-[#0A0A0A] font-medium' 
          : 'text-white/40 hover:bg-[#E1D4C0] hover:text-[#0A0A0A] font-light'
      }`}
    >
      {active && <span className="w-1.5 h-1.5 rounded-full bg-[#0A0A0A] shrink-0" />}
      {!active && <span className="w-1.5 h-1.5 shrink-0" />}
      {children}
    </Link>
  );
}
