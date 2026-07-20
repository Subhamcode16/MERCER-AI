import { Sidebar } from '@/components/studio/Sidebar';
import { IntelligencePanel } from '@/components/studio/IntelligencePanel';

export default function StudioLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex overflow-hidden selection:bg-[var(--color-warm-ivory)] selection:text-black">
      <Sidebar />
      <main className="flex-1 overflow-y-auto overflow-x-hidden border-r border-white/5 bg-[#0d0d0d] custom-scrollbar">
        {children}
      </main>
      <IntelligencePanel />
    </div>
  );
}
