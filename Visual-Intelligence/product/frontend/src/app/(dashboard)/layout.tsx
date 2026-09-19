"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { useState, createContext, useContext, useMemo } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { UserPopover } from "@/components/UserPopover";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
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
  Activity,
  LogIn
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
      <div className="min-h-[100dvh] bg-background flex items-center justify-center">
        <div className="text-[10px] tracking-[0.2em] uppercase text-muted-foreground animate-pulse">Loading VYREN</div>
      </div>
    );
  }

  return (
    <SidebarContext.Provider value={contextValue}>
      <div className="flex h-screen overflow-hidden bg-background text-foreground font-sans font-light selection:bg-accent">
        
        {/* Architectural Navigation - Strict typography, 5-group hierarchy */}
        <aside 
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          className={`flex flex-col shrink-0 py-7 border-r border-border/40 bg-card/95 backdrop-blur-md relative z-20 transition-all duration-300 ease-in-out shadow-sm ${
            isCollapsed ? "w-[72px] px-3 items-center" : "w-[260px] pl-7 pr-5"
          }`}
        >
          
          {/* Brand Wordmark */}
          <div className={`mb-7 transition-all duration-300 ${isCollapsed ? "text-center" : ""}`}>
            <Link href="/home" className="font-serif text-2xl tracking-[0.1em] text-foreground hover:opacity-90 transition-opacity">
              {isCollapsed ? "V" : "V Y R E N"}
            </Link>
            {!isCollapsed && (
              <div className="text-[8.5px] tracking-[0.25em] uppercase text-muted-foreground mt-1 font-medium transition-all duration-300">
                Brand Intelligence OS
              </div>
            )}
          </div>

          {/* Canonical 3-Group Minimalist Primary Navigation */}
          <nav className="flex flex-col gap-5 flex-1 w-full overflow-y-auto scrollbar-none pr-1">
            
            {/* 1. ROOM */}
            <div>
              <div className="flex flex-col gap-1">
                <NavLink href="/home" active={pathname === '/home' || pathname === '/' || pathname === '/room'} collapsed={isCollapsed} icon={Sparkles}>VYREN Room</NavLink>
              </div>
            </div>

            {/* 2. STUDIO */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-muted-foreground mb-2 font-semibold px-2">Studio</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/studio" active={pathname.includes('/studio')} collapsed={isCollapsed} icon={Palette}>Creative Studio</NavLink>
                <NavLink href="/projects" active={pathname.includes('/projects')} collapsed={isCollapsed} icon={FolderKanban}>Projects</NavLink>
                <NavLink href="/campaigns" active={pathname.includes('/campaigns') || pathname.includes('/attribution')} collapsed={isCollapsed} icon={Target}>Campaigns</NavLink>
                <NavLink href="/team" active={pathname.includes('/team')} collapsed={isCollapsed} icon={Users}>AI Team</NavLink>
              </div>
            </div>

            {/* 3. INTELLIGENCE & SYSTEM */}
            <div>
              {!isCollapsed && (
                <div className="text-[9px] tracking-[0.22em] uppercase text-muted-foreground mb-2 font-semibold px-2">Intelligence</div>
              )}
              <div className="flex flex-col gap-1">
                <NavLink href="/brand" active={pathname.includes('/brand')} collapsed={isCollapsed} icon={Fingerprint}>Brand Identity</NavLink>
                <NavLink href="/visual-dna" active={pathname.includes('/visual-dna')} collapsed={isCollapsed} icon={Dna}>Visual DNA</NavLink>
                <NavLink href="/assets" active={pathname.includes('/assets') || pathname.includes('/materials') || pathname.includes('/archive')} collapsed={isCollapsed} icon={Box}>Assets</NavLink>
                <NavLink href="/activity" active={pathname.includes('/activity') || pathname.includes('/notifications')} collapsed={isCollapsed} icon={Activity}>Activity</NavLink>
                <NavLink href="/settings" active={pathname.includes('/settings') || pathname.includes('/gateways') || pathname.includes('/faq')} collapsed={isCollapsed} icon={Settings}>Settings</NavLink>
              </div>
            </div>

          </nav>

          {/* Theme Switcher & User Status / Auth Footer */}
          <div className="pt-4 mt-auto border-t border-border/40 relative w-full flex flex-col gap-3">
            {/* Theme Toggle Pill */}
            <div className={`flex ${isCollapsed ? "justify-center" : "justify-between items-center px-1"}`}>
              {!isCollapsed && (
                <span className="text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Theme</span>
              )}
              <ThemeToggle showLabel={!isCollapsed} />
            </div>

            {session && profile ? (
              <UserPopover profile={profile} logout={logout} isCollapsed={isCollapsed} />
            ) : (
              <div className={`flex ${isCollapsed ? "justify-center" : "gap-2 px-1"}`}>
                {isCollapsed ? (
                  <button 
                    onClick={() => openAuthModal("login")}
                    title="Log In / Sign Up"
                    className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                  >
                    <LogIn className="w-4 h-4" />
                  </button>
                ) : (
                  <>
                    <button 
                      onClick={() => openAuthModal("login")}
                      className="flex-1 py-1.5 px-3 rounded-lg text-xs font-medium text-muted-foreground hover:text-foreground hover:bg-accent transition-colors border border-border/50 text-center"
                    >
                      Log In
                    </button>
                    <button 
                      onClick={() => openAuthModal("signup")}
                      className="flex-1 py-1.5 px-3 rounded-lg text-xs font-medium bg-primary text-primary-foreground hover:opacity-90 transition-opacity text-center shadow-sm"
                    >
                      Sign Up
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        </aside>

        {/* Main Workspace Surface */}
        <main className="flex-1 h-full min-h-0 relative flex flex-col min-w-0 bg-background overflow-hidden">
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
          ? 'bg-primary text-primary-foreground font-semibold shadow-sm' 
          : 'text-muted-foreground hover:bg-accent hover:text-foreground font-light'
      }`}
    >
      <Icon className={`w-4 h-4 shrink-0 transition-transform duration-200 ${active ? "scale-105" : ""}`} />
      
      {!collapsed && (
        <span className="truncate">{children}</span>
      )}
    </Link>
  );
}
