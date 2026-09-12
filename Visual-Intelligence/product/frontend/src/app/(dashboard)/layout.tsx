"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { useState, createContext, useContext, useMemo } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { UserPopover } from "@/components/UserPopover";
import { 
  Home,
  Fingerprint,
  FolderKanban,
  Target,
  Palette,
  Dna,
  Box,
  Search,
  Brain,
  Users,
  Bell,
  Settings,
  Sparkles,
  Compass,
  Layers,
  Archive,
  BookOpen,
  HelpCircle,
  Activity
} from "lucide-react";

// Sidebar context to allow children (like studio page) to toggle collapse state
export const SidebarContext = createContext<{
  isInWorkspace: boolean;
  setIsInWorkspace: (val: boolean) => void;
}>({
  isInWorkspace: false,
  setIsInWorkspace: () => {},
});

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { session, profile, isLoading, logout, openAuthModal } = useAuth();
  
  const [isInWorkspace, setIsInWorkspace] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const contextValue = useMemo(() => ({ isInWorkspace, setIsInWorkspace }), [isInWorkspace]);

  const isCollapsed = isInWorkspace && !isHovered;

  if (isLoading) {
    return (
      <div className="min-h-[100dvh] bg-[#0A0A0A] flex items-center justify-center">
        <div className="text-[10px] tracking-[0.2em] uppercase text-white/30">Loading VYREN</div>
      </div>
    );
  }

  return (
    <SidebarContext.Provider value={contextValue}>
      <div className="flex h-screen overflow-hidden bg-[#0A0A0A] text-white/90 font-sans font-light selection:bg-white/20">
        
        {/* Architectural Navigation - Strict typography, 5-group hierarchy */}
        <aside 
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          className={`flex flex-col shrink-0 py-7 border-r border-white/5 bg-[#0D0D0D] relative z-20 transition-all duration-300 ease-in-out ${
            isCollapsed ? "w-[72px] px-3 items-center" : "w-[260px] pl-7 pr-5"
          }`}
        >
          
          {/* Brand Wordmark */}
          <div className={`mb-7 transition-all duration-300 ${isCollapsed ? "text-center" : ""}`}>
            <Link href="/home" className="font-serif text-2xl tracking-[0.1em] bg-gradient-to-r from-[#E1D4C0] via-[#C9B99A] to-[#8C8472] bg-clip-text text-transparent hover:opacity-90 transition-opacity">
              {isCollapsed ? "V" : "V Y R E N"}
            </Link>
            {!isCollapsed && (
              <div className="text-[8.5px] tracking-[0.25em] uppercase text-white/40 mt-1 font-medium transition-all duration-300">
                Brand Intelligence OS
              </div>
            )}
          </div>

          {/* 5-Group Primary Navigation */}
          <nav className="flex flex-col gap-5 flex-1 w-full overflow-y-auto scrollbar-none pr-1">
            
            {/* 1. WORKSPACE */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-white/30 mb-2 font-semibold px-2">Workspace</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/home" active={pathname === '/home' || pathname === '/'} collapsed={isCollapsed} icon={Home}>Home</NavLink>
                <NavLink href="/brand" active={pathname.includes('/brand')} collapsed={isCollapsed} icon={Fingerprint}>Brand</NavLink>
                <NavLink href="/projects" active={pathname.includes('/projects')} collapsed={isCollapsed} icon={FolderKanban}>Projects</NavLink>
                <NavLink href="/campaigns" active={pathname.includes('/campaigns') || pathname.includes('/attribution')} collapsed={isCollapsed} icon={Target}>Campaigns</NavLink>
              </div>
            </div>

            {/* 2. CREATE */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-white/30 mb-2 font-semibold px-2">Create</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/studio" active={pathname === '/studio'} collapsed={isCollapsed} icon={Palette}>Creative Studio</NavLink>
                <NavLink href="/visual-dna" active={pathname.includes('/visual-dna') || pathname.includes('/materials')} collapsed={isCollapsed} icon={Dna}>Visual DNA</NavLink>
                <NavLink href="/assets" active={pathname.includes('/assets') || pathname.includes('/archive')} collapsed={isCollapsed} icon={Box}>Assets</NavLink>
              </div>
            </div>

            {/* 3. INTELLIGENCE */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-white/30 mb-2 font-semibold px-2">Intelligence</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/research" active={pathname.includes('/research') || pathname.includes('/atlas')} collapsed={isCollapsed} icon={Search}>Research</NavLink>
                <NavLink href="/knowledge" active={pathname.includes('/knowledge') || pathname.includes('/observatory') || pathname.includes('/foresight')} collapsed={isCollapsed} icon={Brain}>Knowledge</NavLink>
              </div>
            </div>

            {/* 4. WORKFORCE */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-white/30 mb-2 font-semibold px-2">Workforce</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/team" active={pathname === '/team'} collapsed={isCollapsed} icon={Users}>AI Team</NavLink>
              </div>
            </div>

            {/* 5. UTILITY */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-white/30 mb-2 font-semibold px-2">Utility</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/activity" active={pathname.includes('/activity') || pathname.includes('/notifications')} collapsed={isCollapsed} icon={Activity}>Activity</NavLink>
                <NavLink href="/settings" active={pathname.includes('/settings') || pathname.includes('/gateways') || pathname.includes('/faq')} collapsed={isCollapsed} icon={Settings}>Settings</NavLink>
              </div>
            </div>

          </nav>

          {/* User Status / Auth Footer */}
          <div className={`pt-4 mt-auto border-t border-white/5 relative w-full ${isCollapsed ? "flex justify-center" : ""}`}>
            {session && profile ? (
              <UserPopover profile={profile} logout={logout} isCollapsed={isCollapsed} />
            ) : (
              <div className={`flex ${isCollapsed ? "flex-col gap-2 items-center" : "gap-4 px-2"}`}>
                <button 
                  onClick={() => openAuthModal("login")}
                  className="text-[11px] text-white/60 hover:text-[#E1D4C0] transition-colors font-medium"
                >
                  {isCollapsed ? "In" : "Log In"}
                </button>
                <button 
                  onClick={() => openAuthModal("signup")}
                  className="text-[11px] text-white/60 hover:text-[#E1D4C0] transition-colors font-medium"
                >
                  {isCollapsed ? "Up" : "Sign Up"}
                </button>
              </div>
            )}
          </div>
        </aside>

        {/* Main Workspace Surface */}
        <main className="flex-1 h-full min-h-0 relative flex flex-col min-w-0 bg-[#0A0A0A] overflow-hidden">
          {children}
        </main>

      </div>
    </SidebarContext.Provider>
  );
}

function NavLink({ 
  href, 
  active, 
  collapsed, 
  icon: Icon, 
  children 
}: { 
  href: string, 
  active: boolean, 
  collapsed?: boolean, 
  icon: React.ComponentType<any>, 
  children: React.ReactNode 
}) {
  return (
    <Link 
      href={href}
      className={`text-[12.5px] tracking-wide transition-all duration-200 flex items-center rounded-lg ${
        collapsed ? "justify-center p-2.5" : "gap-3 px-3 py-2"
      } ${
        active 
          ? 'bg-[#E1D4C0] text-[#0A0A0A] font-semibold shadow-sm' 
          : 'text-white/50 hover:bg-white/[0.04] hover:text-white font-light'
      }`}
    >
      <Icon className={`w-4 h-4 shrink-0 transition-transform duration-200 ${active ? "scale-105" : ""}`} />
      
      {!collapsed && (
        <span className="truncate">{children}</span>
      )}
    </Link>
  );
}
