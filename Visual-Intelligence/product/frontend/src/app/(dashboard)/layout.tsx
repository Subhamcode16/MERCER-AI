"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { useState, createContext, useContext, useMemo } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { UserPopover } from "@/components/UserPopover";
import { 
  FolderGit2, 
  Layers, 
  Compass, 
  BookOpen, 
  Brain, 
  Archive, 
  Bell, 
  Settings,
  Menu,
  Users,
  HelpCircle,
  Target,
  Sparkles
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
        <div className="text-[10px] tracking-[0.2em] uppercase text-white/30">Loading Mercer AI</div>
      </div>
    );
  }

  return (
    <SidebarContext.Provider value={contextValue}>
      <div className="flex h-screen overflow-hidden bg-[#0A0A0A] text-white/90 font-sans font-light selection:bg-white/20">
        
        {/* Architectural Navigation - Strict typography, collapsible */}
        <aside 
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          className={`flex flex-col shrink-0 py-8 border-r border-white/5 bg-[#0D0D0D] relative z-20 transition-all duration-300 ease-in-out ${
            isCollapsed ? "w-[80px] px-4 items-center" : "w-[280px] pl-10 pr-6"
          }`}
        >
          
          {/* Brand */}
          <div className={`mb-10 transition-all duration-300 ${isCollapsed ? "text-center" : ""}`}>
            <Link href="/studio" className="font-serif text-2xl tracking-[0.05em] bg-gradient-to-r from-[#E1D4C0] via-[#C9B99A] to-[#8C8472] bg-clip-text text-transparent">
              {isCollapsed ? "M" : "M E R C E R   A I"}
            </Link>
            {!isCollapsed && (
              <div className="text-[9px] tracking-[0.2em] uppercase text-white/40 mt-3 font-medium transition-all duration-300">
                Creative Intelligence
              </div>
            )}
          </div>

          {/* Primary Modules */}
          <nav className="flex flex-col gap-6 flex-1 w-full overflow-y-auto scrollbar-none">
            <div>
              {!isCollapsed && (
                <div className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-3 font-medium">Strategic Network</div>
              )}
              <div className="flex flex-col gap-1.5">
                <NavLink href="/observatory" active={pathname.includes('/observatory')} collapsed={isCollapsed} icon={Compass}>Observatory</NavLink>
                <NavLink href="/foresight" active={pathname.includes('/foresight')} collapsed={isCollapsed} icon={Sparkles}>Foresight Matrix</NavLink>
                <NavLink href="/attribution" active={pathname.includes('/attribution')} collapsed={isCollapsed} icon={Target}>Attribution & Radar</NavLink>
              </div>
            </div>

            <div>
              {!isCollapsed && (
                <div className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-3 font-medium">Institution</div>
              )}
              <div className="flex flex-col gap-1.5">
                <NavLink href="/studio" active={pathname === '/studio'} collapsed={isCollapsed} icon={FolderGit2}>Campaign Studio</NavLink>
                <NavLink href="/team" active={pathname === '/team'} collapsed={isCollapsed} icon={Users}>Team Mode</NavLink>
                <NavLink href="/materials" active={pathname.includes('/materials')} collapsed={isCollapsed} icon={Layers}>Material Library</NavLink>
                <NavLink href="/atlas" active={pathname.includes('/atlas')} collapsed={isCollapsed} icon={Compass}>Atlas</NavLink>
                <NavLink href="/research" active={pathname.includes('/research')} collapsed={isCollapsed} icon={BookOpen}>Research</NavLink>
                <NavLink href="/knowledge" active={pathname.includes('/knowledge')} collapsed={isCollapsed} icon={Brain}>Knowledge</NavLink>
                <NavLink href="/archive" active={pathname.includes('/archive')} collapsed={isCollapsed} icon={Archive}>Archive</NavLink>
              </div>
            </div>

            <div>
              {!isCollapsed && (
                <div className="text-[10px] tracking-[0.2em] uppercase text-white/30 mb-3 font-medium">System & Control</div>
              )}
              <div className="flex flex-col gap-1.5">
                <NavLink href="/gateways" active={pathname.includes('/gateways')} collapsed={isCollapsed} icon={Layers}>Model & MCP Gateways</NavLink>
                <NavLink href="/notifications" active={pathname.includes('/notifications')} collapsed={isCollapsed} icon={Bell}>Notifications</NavLink>
                <NavLink href="/settings" active={pathname.includes('/settings')} collapsed={isCollapsed} icon={Settings}>Settings</NavLink>
                <NavLink href="/faq" active={pathname.includes('/faq')} collapsed={isCollapsed} icon={HelpCircle}>FAQ</NavLink>
              </div>
            </div>
          </nav>

          {/* User Status */}
          <div className={`pt-6 mt-auto border-t border-white/5 relative w-full ${isCollapsed ? "flex justify-center" : ""}`}>
            {session && profile ? (
              <UserPopover profile={profile} logout={logout} isCollapsed={isCollapsed} />
            ) : (
              <div className={`flex ${isCollapsed ? "flex-col gap-3 items-center" : "gap-4"}`}>
                <button 
                  onClick={() => openAuthModal("login")}
                  className="text-[11px] text-white/60 hover:text-[#E1D4C0] transition-colors"
                >
                  {isCollapsed ? "In" : "Log In"}
                </button>
                <button 
                  onClick={() => openAuthModal("signup")}
                  className="text-[11px] text-white/60 hover:text-[#E1D4C0] transition-colors"
                >
                  {isCollapsed ? "Up" : "Sign Up"}
                </button>
              </div>
            )}
          </div>
        </aside>

        {/* Main Architectural Workspace */}
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
      className={`text-[13px] tracking-wide transition-all duration-200 flex items-center rounded-lg ${
        collapsed ? "justify-center p-2.5" : "gap-3.5 px-3.5 py-2.5"
      } ${
        active 
          ? 'bg-[#E1D4C0] text-[#0A0A0A] font-semibold shadow-sm' 
          : 'text-white/40 hover:bg-[#E1D4C0]/10 hover:text-white font-light'
      }`}
    >
      <Icon className={`w-4 h-4 shrink-0 transition-transform duration-200 ${active ? "scale-105" : ""}`} />
      
      {!collapsed && (
        <span className="truncate">{children}</span>
      )}
    </Link>
  );
}
