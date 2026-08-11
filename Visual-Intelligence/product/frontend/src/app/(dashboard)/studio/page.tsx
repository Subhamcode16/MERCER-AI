"use client";

import { useState, useEffect, useRef, useCallback, useContext } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Plus, ArrowLeft, Edit2, Trash2, Upload } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/contexts/AuthContext";
import {
  listCampaigns,
  createCampaign,
  getCampaign,
  renameCampaign,
  deleteCampaign,
  uploadMaterial,
  analyzeMaterial,
  generateCampaign,
  updateCampaignOptions,
  getMaterialUrl,
  type CampaignSummary,
  type FullCampaign,
  type MemoryNode,
} from "@/lib/campaigns";

// --- V2 Constraint Solver Components ---
import { ReasoningTracePanel } from "@/components/studio/ReasoningTracePanel";
import { PhysicalViolationAlert } from "@/components/studio/PhysicalViolationAlert";
import { HeuristicRecommendation } from "@/components/studio/HeuristicRecommendation";
import { CREBentoGrid, type CREScores } from "@/components/studio/CREBentoGrid";
import { PromptInputBox } from "@/components/ui/ai-prompt-box";
import { WorkflowTimeline } from "@/components/studio/WorkflowTimeline";

// --- Sidebar Context ---
import { SidebarContext } from "../layout";

// --- SVG Icons ---

const FolderIcon = ({ hasMaterial }: { hasMaterial?: boolean }) => (
  <div className="relative w-full h-full drop-shadow-2xl group-hover:scale-[1.03] transition-transform duration-300 flex items-center justify-center">
    <img src="/assets/folder-icon.png" alt="Campaign Folder" className="w-full h-full object-contain drop-shadow-lg" />
    {hasMaterial && (
      <svg viewBox="0 0 24 24" className="absolute bottom-6 right-6 w-8 h-8 drop-shadow-md">
        <rect x="0" y="0" width="24" height="24" fill="#FFFFFF" stroke="#111111" strokeWidth="3" rx="4" strokeLinejoin="round" />
        <circle cx="8" cy="8" r="2.5" fill="#111111" />
        <path d="M 0 20 L 8 12 L 16 20 L 24 12 L 24 24 L 0 24 Z" fill="#111111" stroke="#111111" strokeWidth="2" strokeLinejoin="round" />
      </svg>
    )}
  </div>
);

const DashedFolderIcon = () => (
  <svg viewBox="0 0 105 105" className="w-full h-full opacity-60 group-hover:opacity-100 transition-opacity duration-300">
    <path d="M 10 90 L 10 25 Q 10 15 20 15 L 35 15 L 45 25 L 85 25 Q 95 25 95 35 L 95 90 Q 95 95 90 95 L 20 95 Q 10 95 10 90 Z" fill="transparent" stroke="#E1D4C0" strokeWidth="2" strokeDasharray="6 6" strokeLinejoin="round" />
    <path d="M 10 90 L 10 55 Q 10 45 20 45 L 42 45 L 52 35 L 85 35 Q 95 35 95 45 L 95 90 Q 95 95 90 95 L 20 95 Q 10 95 10 90 Z" fill="transparent" stroke="#E1D4C0" strokeWidth="2" strokeDasharray="6 6" strokeLinejoin="round" />
    <line x1="52.5" y1="45" x2="52.5" y2="75" stroke="#E1D4C0" strokeWidth="3" strokeLinecap="round" />
    <line x1="37.5" y1="60" x2="67.5" y2="60" stroke="#E1D4C0" strokeWidth="3" strokeLinecap="round" />
  </svg>
);

// --- Main Component ---

export default function CampaignStudio() {
  const router = useRouter();
  const { session, openAuthModal } = useAuth();
  
  // --- Folder Grid State ---
  const [campaigns, setCampaigns] = useState<CampaignSummary[]>([]);
  const [isLoadingList, setIsLoadingList] = useState(true);
  const [activeCampaignId, setActiveCampaignId] = useState<string | null>(null);

  // --- Process Step Override ---
  const [stepOverride, setStepOverride] = useState<'dropzone' | 'art_direction' | null>(null);

  // --- Inline Editing State ---
  const [editingCampaignId, setEditingCampaignId] = useState<string | null>(null);
  const [editNameValue, setEditNameValue] = useState("");

  // --- Active Campaign Workspace State ---
  const [activeCampaign, setActiveCampaign] = useState<FullCampaign | null>(null);
  const [isLoadingCampaign, setIsLoadingCampaign] = useState(false);
  const [isDraggingOver, setIsDraggingOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFileInfo, setUploadedFileInfo] = useState<{ name: string; size: string } | null>(null);
  const uploadProgressRef = useRef<NodeJS.Timeout | null>(null);

  // --- Sidebar & Layout Overrides ---
  const { setIsInWorkspace } = useContext(SidebarContext);
  const [selectedRatio, setSelectedRatio] = useState('3:4');
  const [selectedAssetCount, setSelectedAssetCount] = useState(4);
  const [wizardStep, setWizardStep] = useState(1);
  const [showControls, setShowControls] = useState(true);
  const [chatMessages, setChatMessages] = useState<any[]>([
    {
      id: 'welcome',
      sender: 'director',
      text: "Welcome to the Creative Intelligence Studio. I've analyzed your specimen's textile DNA. Enter a prompt below to generate campaigns, or chat with me here to refine the configurations."
    }
  ]);
  const [physicalViolation, setPhysicalViolation] = useState<any>(null);
  const [activeRecommendation, setActiveRecommendation] = useState<any>(null);
  const [decisions, setDecisions] = useState<any[]>([]);
  const [creScores, setCreScores] = useState<CREScores | null>(null);

  // --- Floating Preview State ---
  const [hoveredPreview, setHoveredPreview] = useState<string | null>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (hoveredPreview) {
        setMousePos({ x: e.clientX, y: e.clientY });
      }
    };
    if (hoveredPreview) {
      window.addEventListener('mousemove', handleMouseMove);
    }
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [hoveredPreview]);

  // Clear hover preview automatically if the wizard step changes
  useEffect(() => {
    setHoveredPreview(null);
  }, [wizardStep]);

  // Simulating decisions and CRE scores on campaign load
  useEffect(() => {
    if (activeCampaign) {
      setDecisions([
        { id: '1', level: 1, description: 'Heavy fabric detected -> Column drape recommended', type: 'satisfied' },
        { id: '2', level: 2, description: 'Brand archetype dictates low-key lighting', type: 'applied' }
      ]);
      setCreScores({
        brand: 95,
        product: 88,
        photography: 92,
        marketing: 85,
        composition: 98
      });
    } else {
      setDecisions([]);
      setCreScores(null);
    }
  }, [activeCampaign]);

  // --- Polling ref (to stop polling on unmount) ---
  const pollRef = useRef<NodeJS.Timeout | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // --- Load campaign list on mount ---
  useEffect(() => {
    fetchList();
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, []);

  const fetchList = async () => {
    try {
      const data = await listCampaigns();
      setCampaigns(data);
    } catch (e) {
      console.error("Failed to load campaigns:", e);
    } finally {
      setIsLoadingList(false);
    }
  };

  // --- Load full campaign state when folder is clicked ---
  const openCampaign = useCallback(async (id: string) => {
    setActiveCampaignId(id);
    setIsLoadingCampaign(true);
    setIsInWorkspace(true); // Collapse sidebar
    try {
      const data = await getCampaign(id);
      setActiveCampaign(data);
      if (data.planning) {
        setSelectedBackground(data.planning.selected_background || "");
        setSelectedPose(data.planning.selected_pose || "");
        setSelectedLighting(data.planning.selected_lighting || "");
      }
      // If analysis is already in progress (memory_stream has entries but no conclusion yet), start polling
      const hasConcluded = data.memory_stream.some(n => n.type === 'conclusion');
      const hasStarted = data.memory_stream.length > 0;
      if (hasStarted && !hasConcluded) {
        startPolling(id);
      }
    } catch (e) {
      console.error("Failed to load campaign:", e);
    } finally {
      setIsLoadingCampaign(false);
    }
  }, [setIsInWorkspace]);

  const closeCampaign = () => {
    setActiveCampaignId(null);
    setActiveCampaign(null);
    setStepOverride(null);
    setIsInWorkspace(false); // Restore left sidebar
    setWizardStep(1);
    setChatMessages([
      { id: 'welcome', sender: 'director', text: "Welcome to the Creative Intelligence Studio. I've analyzed your specimen's textile DNA. Enter a prompt below to generate campaigns, or chat with me here to refine the configurations." }
    ]);
    if (pollRef.current) clearInterval(pollRef.current);
    fetchList(); // refresh folder grid in case has_material changed
  };

  // --- Polling: re-fetches campaign until conclusion node appears ---
  const startPolling = (id: string) => {
    if (pollRef.current) clearInterval(pollRef.current);
    setIsAnalyzing(true);
    pollRef.current = setInterval(async () => {
      try {
        const updated = await getCampaign(id);
        setActiveCampaign(prev => {
          if (JSON.stringify(prev) === JSON.stringify(updated)) return prev;
          return updated;
        });
        if (updated.planning) {
          setSelectedBackground(prev => prev === updated.planning.selected_background ? prev : (updated.planning.selected_background || ""));
          setSelectedPose(prev => prev === updated.planning.selected_pose ? prev : (updated.planning.selected_pose || ""));
          setSelectedLighting(prev => prev === updated.planning.selected_lighting ? prev : (updated.planning.selected_lighting || ""));
        }
        const hasConcluded = updated.memory_stream.some(n => n.type === 'conclusion');
        if (hasConcluded) {
          clearInterval(pollRef.current!);
          setIsAnalyzing(false);
          fetchList(); // refresh folder icon to show has_material indicator
        }
      } catch (e) {
        console.error("Polling error:", e);
      }
    }, 2500);
  };

  // --- Create Campaign ---
  const handleCreateCampaign = async () => {
    if (!session) {
      openAuthModal("login");
      return;
    }
    const name = `Campaign ${String(campaigns.length + 1).padStart(2, '0')}`;
    try {
      const newCamp = await createCampaign(name);
      setCampaigns(prev => [...prev, newCamp]);
    } catch (e) {
      console.error("Failed to create campaign:", e);
    }
  };

  const handleGenerate = async () => {
    if (!activeCampaign) return;
    setIsGenerating(true);
    try {
      await generateCampaign(activeCampaign.id);
      startPolling(activeCampaign.id); // Re-use polling to fetch execution states
    } catch (e) {
      console.error("Generate failed:", e);
    } finally {
      setIsGenerating(false);
    }
  };

  // --- Rename Campaign ---
  const startEditing = (e: React.MouseEvent, id: string, currentName: string) => {
    e.stopPropagation();
    setEditingCampaignId(id);
    setEditNameValue(currentName);
  };

  const saveEdit = async (id: string) => {
    if (editNameValue.trim()) {
      try {
        const updated = await renameCampaign(id, editNameValue.trim());
        setCampaigns(prev => prev.map(c => c.id === id ? { ...c, name: updated.name } : c));
      } catch (e) {
        console.error("Failed to rename:", e);
      }
    }
    setEditingCampaignId(null);
  };

  // --- Delete Campaign ---
  const handleDeleteCampaign = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await deleteCampaign(id);
      setCampaigns(prev => prev.filter(c => c.id !== id));
      if (activeCampaignId === id) closeCampaign();
    } catch (e) {
      console.error("Failed to delete:", e);
    }
  };

  // --- File Upload Handler ---
  const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif', 'image/tiff'];
  const MAX_FILE_BYTES = 25 * 1024 * 1024; // 25 MB

  const handleFileDrop = async (file: File) => {
    if (!activeCampaign) return;

    // --- Frontend validation ---
    if (!ALLOWED_TYPES.includes(file.type)) {
      alert(`Unsupported file type: "${file.type || 'unknown'}". Please upload a JPEG, PNG, WEBP, HEIC, or TIFF image.`);
      return;
    }
    if (file.size > MAX_FILE_BYTES) {
      alert(`File is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum allowed size is 25 MB.`);
      return;
    }
    // ---------------------------

    setIsUploading(true);

    setUploadProgress(0);
    setUploadedFileInfo({
      name: file.name,
      size: file.size < 1024 * 1024
        ? `${(file.size / 1024).toFixed(0)} KB`
        : `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
    });
    // Simulate progress with intervals
    let progress = 0;
    uploadProgressRef.current = setInterval(() => {
      progress += Math.random() * 8 + 2;
      if (progress >= 92) {
        if (uploadProgressRef.current) clearInterval(uploadProgressRef.current);
        progress = 92;
      }
      setUploadProgress(Math.min(92, Math.round(progress)));
    }, 200);
    try {
      await uploadMaterial(activeCampaign.id, file);
      if (uploadProgressRef.current) clearInterval(uploadProgressRef.current);
      setUploadProgress(96);
      // Immediately trigger analysis
      await analyzeMaterial(activeCampaign.id);
      setUploadProgress(100);
      await new Promise(r => setTimeout(r, 600));
      // Clear step override since we have new material
      setStepOverride(null);
      // Refresh campaign state and start polling for results
      const updated = await getCampaign(activeCampaign.id);
      setActiveCampaign(updated);
      setCampaigns(prev => prev.map(c => c.id === activeCampaign.id ? { ...c, has_material: true } : c));
      startPolling(activeCampaign.id);
    } catch (e) {
      if (uploadProgressRef.current) clearInterval(uploadProgressRef.current);
      console.error("Upload/analyze failed:", e);
    } finally {
      setIsUploading(false);
      setUploadedFileInfo(null);
      setUploadProgress(0);
    }
  };

  const onDropZoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFileDrop(file);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDraggingOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFileDrop(file);
  };

  // --- Art Direction State Bindings ---
  const [selectedBackground, setSelectedBackground] = useState<string>("");
  const [selectedPose, setSelectedPose] = useState<string>("");
  const [selectedLighting, setSelectedLighting] = useState<string>("");

  const handleOptionChange = async (category: 'background' | 'pose' | 'lighting', value: string) => {
    if (!activeCampaign) return;
    
    let bg = selectedBackground;
    let ps = selectedPose;
    let lt = selectedLighting;

    if (category === 'background') {
      setSelectedBackground(value);
      bg = value;
    } else if (category === 'pose') {
      setSelectedPose(value);
      ps = value;
    } else if (category === 'lighting') {
      setSelectedLighting(value);
      lt = value;
    }

    try {
      await updateCampaignOptions(activeCampaign.id, { background: bg, pose: ps, lighting: lt });
      // Update activeCampaign local state to keep it in sync
      setActiveCampaign(prev => {
        if (!prev) return null;
        return {
          ...prev,
          planning: {
            ...prev.planning,
            selected_background: bg,
            selected_pose: ps,
            selected_lighting: lt
          }
        };
      });
    } catch (e) {
      console.error("Failed to update options:", e);
    }
  };

  const getConflictWarning = (): string | null => {
    if (!activeCampaign?.identity?.product_dna) return null;
    const materialVal = String(activeCampaign.identity.product_dna.material.value).toLowerCase();
    
    const isHeavy = materialVal.includes("banarasi") || materialVal.includes("kanjeevaram") || materialVal.includes("silk");
    const isLight = materialVal.includes("chiffon") || materialVal.includes("organza") || materialVal.includes("net");

    if (isHeavy && selectedPose === "Wind-Blown Toss") {
      return "Stiff, heavy silk fabrics lack the buoyancy required to toss or float naturally in the wind. The generated assets will show architectural folds falling downward rather than flowing motion.";
    }
    if (isLight && selectedPose === "Dynamic Fabric Spin") {
      return "Lightweight sheer fabrics will flare outward and disintegrate into transparent waves during a spin rather than keeping defined structural pleats.";
    }
    if (isHeavy && selectedLighting === "High-Key Window Doorway") {
      return "High-key silhouette lighting washes out the depth of Zari weave highlights. Directional or Ethereal backlighting is recommended to maintain metallic micro-contrast.";
    }
    return null;
  };

  const currentCampaignSummary = campaigns.find(c => c.id === activeCampaignId);

  // --- Derived Step State ---
  const currentStep = stepOverride || (
    !activeCampaign?.material_path ? 'dropzone'
    : (activeCampaign.execution?.asset_states && activeCampaign.execution.asset_states.length > 0) ? 'assets'
    : 'art_direction'
  );

  return (
    <div className="flex w-full h-full relative overflow-hidden bg-black">
      {/* Background Glows */}
      <div className="absolute top-[-20%] left-[20%] w-[800px] h-[800px] bg-sky-900/10 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute top-[-10%] right-[10%] w-[600px] h-[600px] bg-emerald-900/10 rounded-full blur-[120px] pointer-events-none" />

      {/* Workspace */}
      <div className="flex-1 h-full flex flex-col relative z-10 px-8 py-8">

        {/* Header */}
        <div className="flex items-center w-full">
          <div className="flex items-center gap-4 text-[10px] tracking-[0.2em] uppercase text-white/30">
            <button
              onClick={() => {
                if (activeCampaignId) {
                  closeCampaign();
                } else {
                  router.push('/studio');
                }
              }}
              className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors shrink-0"
              title="Go Back"
            >
              <ArrowLeft size={14} />
            </button>
            <div className="flex items-center gap-3">
              <Link href="/studio" className="cursor-pointer hover:text-white transition-colors" onClick={(e) => {
                if (activeCampaignId) {
                  e.preventDefault();
                  closeCampaign();
                }
              }}>
                Campaign Studio
              </Link>
              {activeCampaign && (
                <>
                  <span>/</span>
                  <span className="text-white/60">{activeCampaign.name}</span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 flex flex-col mt-8">

          {/* STATE 1: No campaigns */}
          {!isLoadingList && campaigns.length === 0 && activeCampaignId === null && (
            <div className="flex-1 flex flex-col items-center justify-center -mt-24">
              <div className="flex flex-col items-center justify-center max-w-sm text-center">
                <div className="relative w-24 h-24 mb-6 flex items-center justify-center">
                  <FolderIcon />
                </div>
                <h2 className="text-xl font-medium text-white mb-3">No Campaigns</h2>
                <p className="text-sm text-zinc-400 mb-8 leading-relaxed">
                  Campaigns are a great way to explore ideas that share a common theme or topic
                </p>
                <button
                  onClick={handleCreateCampaign}
                  className="px-6 py-3 bg-[#E1D4C0] text-[#0A0A0A] font-medium rounded-full text-sm hover:bg-white transition-colors shadow-xl"
                >
                  Start a campaign
                </button>
              </div>
            </div>
          )}

          {/* STATE 2: Folder Grid */}
          {campaigns.length > 0 && activeCampaignId === null && (
            <div className="flex-1 flex items-start justify-start p-12 mt-12">
              <div className="flex flex-wrap gap-12">
                {campaigns.map((camp) => (
                  <div key={camp.id} className="flex flex-col items-center gap-4 group relative">
                    <div
                      onClick={() => openCampaign(camp.id)}
                      className="w-36 h-36 relative flex items-center justify-center cursor-pointer"
                    >
                      <FolderIcon hasMaterial={camp.has_material} />
                      {/* Hover Actions */}
                      <div className="absolute top-2 right-2 flex gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity z-20">
                        <button
                          onClick={(e) => startEditing(e, camp.id, camp.name)}
                          className="p-1.5 bg-black/60 hover:bg-black/80 text-white rounded backdrop-blur-md transition-colors border border-white/10"
                          title="Rename"
                        >
                          <Edit2 size={13} />
                        </button>
                        <button
                          onClick={(e) => handleDeleteCampaign(e, camp.id)}
                          className="p-1.5 bg-black/60 hover:bg-red-500/80 text-white rounded backdrop-blur-md transition-colors border border-white/10 hover:border-red-500/50"
                          title="Delete"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </div>

                    {editingCampaignId === camp.id ? (
                      <input
                        type="text"
                        value={editNameValue}
                        onChange={(e) => setEditNameValue(e.target.value)}
                        onBlur={() => saveEdit(camp.id)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') saveEdit(camp.id);
                          if (e.key === 'Escape') setEditingCampaignId(null);
                        }}
                        autoFocus
                        className="bg-zinc-800/80 text-white text-[12px] font-medium tracking-wide uppercase px-3 py-1 outline-none rounded border border-[#E1D4C0]/50 w-36 text-center shadow-2xl"
                      />
                    ) : (
                      <span className="text-[12px] text-white/80 font-medium tracking-wide uppercase px-2 text-center truncate w-36">
                        {camp.name}
                      </span>
                    )}
                  </div>
                ))}

                {/* New Campaign Button */}
                <div onClick={handleCreateCampaign} className="flex flex-col items-center gap-4 group cursor-pointer">
                  <div className="w-36 h-36 relative flex items-center justify-center">
                    <DashedFolderIcon />
                  </div>
                  <span className="text-[12px] text-white/40 font-medium tracking-wide uppercase group-hover:text-[#E1D4C0] transition-colors">
                    New Campaign
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* STATE 3: Inside Campaign */}
          {activeCampaignId !== null && (
            <div className="flex-1 flex flex-col min-h-0">
              {isLoadingCampaign ? (
                <div className="text-white/30 text-sm animate-pulse">Loading workspace...</div>
              ) : activeCampaign && currentStep === 'dropzone' ? (
                // Dropzone — Glassmorphic Upload Zone
                <div className="flex-1 flex items-center justify-center w-full min-h-0">
                  {/* Horizon Arc Glow — bottom of screen */}
                  <AnimatePresence>
                    {isUploading && (
                      <motion.div
                        key="arc-glow"
                        className="absolute bottom-0 left-0 w-full h-48 pointer-events-none z-0"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.8 }}
                      >
                        <div className="absolute inset-0" style={{
                          background: 'radial-gradient(ellipse 70% 60% at 50% 130%, rgba(99,80,220,0.45) 0%, rgba(225,212,192,0.08) 55%, transparent 80%)'
                        }} />
                        <motion.div
                          className="absolute inset-0"
                          animate={{ opacity: [0.6, 1, 0.6] }}
                          transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
                          style={{
                            background: 'radial-gradient(ellipse 50% 40% at 50% 120%, rgba(130,100,255,0.3) 0%, transparent 70%)'
                          }}
                        />
                      </motion.div>
                    )}
                  </AnimatePresence>

                  <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={onDropZoneChange} />

                  <AnimatePresence mode="wait">
                    {isUploading && uploadedFileInfo ? (
                      // --- ACTIVE STATE: Glassmorphic Progress Card ---
                      <motion.div
                        key="upload-progress"
                        className="relative z-10 w-full max-w-md"
                        initial={{ opacity: 0, scale: 0.92, y: 12 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.92, y: -8 }}
                        transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                      >
                        {/* Card Outer — double-bezel blue-violet glass */}
                        <div
                          className="relative rounded-[2rem] p-[1.5px] overflow-hidden"
                          style={{ background: 'linear-gradient(135deg, rgba(130,100,255,0.5) 0%, rgba(60,40,160,0.2) 40%, rgba(225,212,192,0.12) 100%)' }}
                        >
                          {/* Outer glow bloom */}
                          <div className="absolute -inset-8 pointer-events-none" style={{ background: 'radial-gradient(ellipse 70% 50% at 50% 50%, rgba(80,60,200,0.35) 0%, transparent 70%)', filter: 'blur(24px)', zIndex: -1 }} />
                          
                          <div
                            className="relative rounded-[1.9rem] px-7 py-7"
                            style={{ background: 'linear-gradient(145deg, rgba(18,16,42,0.92) 0%, rgba(10,8,28,0.96) 100%)', backdropFilter: 'blur(24px)' }}
                          >
                            {/* Close/cancel button */}
                            <button
                              onClick={(e) => { e.stopPropagation(); if (uploadProgressRef.current) clearInterval(uploadProgressRef.current); setIsUploading(false); setUploadedFileInfo(null); setUploadProgress(0); }}
                              className="absolute top-5 right-5 w-8 h-8 rounded-full border border-white/10 bg-white/5 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/10 transition-all"
                            >
                              <svg viewBox="0 0 16 16" className="w-3 h-3 fill-current"><path d="M3.22 3.22a.75.75 0 011.06 0L8 6.94l3.72-3.72a.75.75 0 111.06 1.06L9.06 8l3.72 3.72a.75.75 0 11-1.06 1.06L8 9.06l-3.72 3.72a.75.75 0 01-1.06-1.06L6.94 8 3.22 4.28a.75.75 0 010-1.06z"/></svg>
                            </button>

                            {/* Specimen Icon + File Info */}
                            <div className="flex items-center gap-5 mb-7">
                              {/* Glassmorphic Specimen Icon */}
                              <div
                                className="w-20 h-20 rounded-2xl flex-shrink-0 flex flex-col items-center justify-center relative overflow-hidden"
                                style={{ background: 'linear-gradient(145deg, rgba(80,60,200,0.4) 0%, rgba(40,30,120,0.6) 100%)', border: '1px solid rgba(130,100,255,0.3)' }}
                              >
                                {/* Fabric/weave grid lines */}
                                <svg viewBox="0 0 40 40" className="w-12 h-12 opacity-90">
                                  <defs>
                                    <pattern id="weave" x="0" y="0" width="8" height="8" patternUnits="userSpaceOnUse">
                                      <line x1="4" y1="0" x2="4" y2="8" stroke="rgba(225,212,192,0.6)" strokeWidth="0.8"/>
                                      <line x1="0" y1="4" x2="8" y2="4" stroke="rgba(225,212,192,0.4)" strokeWidth="0.5"/>
                                    </pattern>
                                  </defs>
                                  <rect width="40" height="40" fill="url(#weave)" rx="2"/>
                                  <rect x="8" y="8" width="24" height="24" fill="none" stroke="rgba(225,212,192,0.8)" strokeWidth="1" rx="2"/>
                                  <circle cx="20" cy="20" r="5" fill="none" stroke="rgba(225,212,192,0.9)" strokeWidth="1"/>
                                </svg>
                                {/* Glass shine */}
                                <div className="absolute top-0 left-0 right-0 h-1/2" style={{ background: 'linear-gradient(180deg, rgba(255,255,255,0.12) 0%, transparent 100%)', borderRadius: '16px 16px 0 0' }} />
                              </div>

                              {/* File metadata */}
                              <div className="flex flex-col gap-1.5 text-left min-w-0">
                                <div className="inline-flex items-center gap-2">
                                  <span className="text-[9px] tracking-[0.2em] uppercase font-mono px-2 py-0.5 rounded-full" style={{ background: 'rgba(130,100,255,0.25)', border: '1px solid rgba(130,100,255,0.4)', color: '#c4b5fd' }}>IMAGE / SPECIMEN</span>
                                </div>
                                <p className="text-[15px] font-medium tracking-tight text-[#E1D4C0] leading-tight truncate max-w-[200px]">{uploadedFileInfo.name.replace(/\.[^.]+$/, '')}</p>
                                <p className="text-[12px] text-white/40 font-mono">{uploadedFileInfo.size}</p>
                              </div>
                            </div>

                            {/* Progress Bar Area */}
                            <div
                              className="rounded-2xl px-5 py-4"
                              style={{ background: 'rgba(0,0,0,0.4)', border: '1px solid rgba(255,255,255,0.06)' }}
                            >
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-2.5">
                                  <motion.div
                                    className="w-4 h-4 rounded-full border-2"
                                    style={{ borderColor: 'rgba(130,100,255,0.8)', borderTopColor: 'rgba(225,212,192,0.9)' }}
                                    animate={{ rotate: 360 }}
                                    transition={{ duration: 0.8, repeat: Infinity, ease: 'linear' }}
                                  />
                                  <span className="text-[13px] text-white/60 font-light tracking-wide">
                                    {uploadProgress < 96 ? 'Uploading...' : uploadProgress < 100 ? 'Analyzing DNA...' : 'Complete'}
                                  </span>
                                </div>
                                <motion.span
                                  className="text-[22px] font-bold tracking-tight"
                                  style={{ color: '#E1D4C0' }}
                                  key={uploadProgress}
                                >
                                  {uploadProgress}%
                                </motion.span>
                              </div>
                              {/* Progress bar track */}
                              <div className="relative h-1.5 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.06)' }}>
                                <motion.div
                                  className="absolute inset-y-0 left-0 rounded-full"
                                  style={{ background: 'linear-gradient(90deg, rgba(80,60,180,0.9) 0%, rgba(225,212,192,1) 100%)' }}
                                  animate={{ width: `${uploadProgress}%` }}
                                  transition={{ duration: 0.3, ease: 'easeOut' }}
                                />
                                {/* Glow on bar edge */}
                                <motion.div
                                  className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full blur-sm"
                                  style={{ background: '#E1D4C0', left: `${uploadProgress}%`, transform: 'translate(-50%, -50%)' }}
                                  animate={{ left: `${uploadProgress}%` }}
                                  transition={{ duration: 0.3, ease: 'easeOut' }}
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    ) : (
                      // --- DEFAULT STATE: Dashed Double-Bezel Dropzone ---
                      <motion.div
                        key="dropzone-idle"
                        initial={{ opacity: 0, scale: 0.96 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.96 }}
                        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
                        className="relative z-10 w-full max-w-xl"
                      >
                        {/* Outer bezel ring */}
                        <div
                          onDragOver={(e) => { e.preventDefault(); setIsDraggingOver(true); }}
                          onDragLeave={() => setIsDraggingOver(false)}
                          onDrop={onDrop}
                          onClick={() => fileInputRef.current?.click()}
                          className={`group relative cursor-pointer transition-all duration-500 rounded-[2.5rem] p-[1px] ${
                            isDraggingOver ? 'scale-[1.02]' : ''
                          }`}
                          style={{
                            background: isDraggingOver
                              ? 'linear-gradient(135deg, rgba(225,212,192,0.5) 0%, rgba(130,100,255,0.4) 100%)'
                              : 'linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%)'
                          }}
                        >
                          {/* Inner core */}
                          <div
                            className="rounded-[2.45rem] px-16 py-20 flex flex-col items-center gap-7 transition-all duration-500"
                            style={{
                              background: isDraggingOver
                                ? 'rgba(225,212,192,0.04)'
                                : 'rgba(255,255,255,0.02)',
                              border: `1.5px dashed ${isDraggingOver ? 'rgba(225,212,192,0.5)' : 'rgba(255,255,255,0.1)'}`,
                            }}
                          >
                            {/* Upload Icon Circle */}
                            <div
                              className="w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300 group-hover:scale-105"
                              style={{
                                border: '1px solid rgba(255,255,255,0.15)',
                                background: 'rgba(255,255,255,0.03)'
                              }}
                            >
                              <Plus size={22} strokeWidth={1} className="text-white/30 group-hover:text-[#E1D4C0]/60 transition-colors duration-300" />
                            </div>

                            <div className="text-center space-y-1.5">
                              <p className="text-[14px] text-[#E1D4C0]/70 tracking-wide font-light">Upload material or mood image</p>
                              <p className="text-[11px] text-white/25 tracking-wide">
                                {isDraggingOver ? 'Release to upload' : 'Drag & drop or click to browse'}
                              </p>
                              <p className="text-[9px] uppercase tracking-[0.2em] text-white/15 font-mono mt-3">JPG · PNG · WEBP · HEIC · RAW</p>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              ) : activeCampaign ? (
                // Active Workspace
                <div className="flex-1 flex flex-col relative min-h-0">
                  {/* Left Back Button for Process Steps */}
                  <button
                    onClick={() => {
                      if (currentStep === 'assets') setStepOverride('art_direction');
                      else if (currentStep === 'art_direction') setStepOverride('dropzone');
                    }}
                    className="absolute left-10 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/10 transition-colors z-50 group shadow-lg"
                    title="Previous Step"
                  >
                    <ArrowLeft size={20} strokeWidth={1.5} className="group-hover:-translate-x-0.5 transition-transform" />
                  </button>

                  {currentStep === 'assets' ? (
                    // Render Generated Assets Grid
                    <div className="w-full max-w-5xl flex gap-6">
                      {/* Left: Material Ref */}
                      <div className="w-1/4 flex flex-col gap-4">
                        <div className="text-[10px] tracking-[0.2em] uppercase text-white/40">Material Ref</div>
                        <div className="aspect-[3/4] bg-[#111111] rounded-md border border-white/5 overflow-hidden">
                          <img
                            src={getMaterialUrl(activeCampaign.material_path!)}
                            alt="Material"
                            className="w-full h-full object-cover opacity-60"
                            onError={(e) => { (e.target as HTMLImageElement).src = '/placeholder.jpg'; }}
                          />
                        </div>
                      </div>
                      
                      {/* Right: Generated Assets */}
                      <div className="w-3/4 flex flex-col gap-4">
                         <div className="text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0]">Generated Assets</div>
                         <div className="grid grid-cols-2 gap-4">
                           {activeCampaign.execution.asset_states.map(asset => (
                              <div key={asset.id} className="relative aspect-[3/4] bg-[#111] border border-white/10 rounded-md overflow-hidden group">
                                {asset.image_url ? (
                                  <img src={asset.image_url} alt={asset.id} className="w-full h-full object-cover opacity-90 transition-transform duration-700 group-hover:scale-105" />
                                ) : (
                                  <div className="w-full h-full flex items-center justify-center text-white/20 text-xs animate-pulse">Generating...</div>
                                )}
                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                  <p className="text-[10px] text-white/80 line-clamp-3">{asset.prompt}</p>
                                </div>
                                <div className="absolute top-3 left-3 px-2 py-1 bg-black/60 backdrop-blur text-[9px] uppercase tracking-wider rounded border border-white/10">
                                  {asset.id.replace('_', ' ')}
                                </div>
                              </div>
                           ))}
                         </div>
                      </div>
                    </div>
                  ) : (
                    // Render Material Preview with Art Direction Panel (Split Screen)
                    <div className="w-full flex gap-10 items-stretch h-[72vh] text-left">
                      {/* Left: Material Canvas (Uncarded Specimen Panel) */}
                       <div className="w-[33%] flex flex-col gap-6 relative justify-center">
                        <div className="rounded-[1.5rem] overflow-hidden border border-white/5 bg-zinc-950/20">
                          <img
                            src={getMaterialUrl(activeCampaign.material_path!)}
                            alt="Material Specimen"
                            className="w-full object-cover aspect-[4/5] opacity-75 hover:opacity-90 transition-opacity duration-500"
                            onError={(e) => { (e.target as HTMLImageElement).src = '/placeholder.jpg'; }}
                          />
                        </div>
                        <div className="space-y-4">
                          <div className="rounded-full px-3 py-1 text-[9px] uppercase tracking-[0.2em] font-semibold text-[#E1D4C0] border border-[#E1D4C0]/20 w-fit bg-[#E1D4C0]/5">
                            Fabric Specimen DNA
                          </div>
                          <div className="space-y-3 font-mono text-[11px]">
                            <div className="flex justify-between border-b border-white/5 pb-1.5">
                              <span className="text-white/40 uppercase tracking-wider">Weave Type</span>
                              <span className="text-white font-medium">{String(activeCampaign.identity?.product_dna?.weaving_technique?.value || 'Zari')}</span>
                            </div>
                            <div className="flex justify-between border-b border-white/5 pb-1.5">
                              <span className="text-white/40 uppercase tracking-wider">Fiber Base</span>
                              <span className="text-white font-medium">{String(activeCampaign.identity?.product_dna?.material?.value || 'Banarasi Silk')}</span>
                            </div>
                            <div className="flex justify-between pb-1.5">
                              <span className="text-white/40 uppercase tracking-wider">Drape Archetype</span>
                              <span className="text-white font-medium">Architectural / Heavy</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Right: Art Direction Config Panel (Pane-2 Evolving Spatial Canvas) */}
                       <div className="w-[67%] flex flex-col min-h-0">
                        {activeCampaign.v3_creative_state ? (
                          <div className="flex-1 bg-white/5 border border-white/10 p-1.5 rounded-[2rem] flex flex-col">
                            <div className="flex-1 bg-[#0C0C0E] shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)] rounded-[calc(2rem-0.375rem)] p-8 flex flex-col justify-center overflow-y-auto relative min-h-0">
                              {/* Strategy Card */}
                              <div className="text-center space-y-6 max-w-md mx-auto">
                                <div className="w-16 h-16 rounded-2xl bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 flex items-center justify-center mx-auto text-[#E1D4C0] animate-pulse">
                                  <svg viewBox="0 0 24 24" className="w-8 h-8 fill-none stroke-current" strokeWidth="1.5">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 21l8.904-4.473L21 9l-3.487-3.487L9.813 15.904z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 21l3-3m-3 3l-3-3m12-9l-3-3" />
                                  </svg>
                                </div>
                                <div className="space-y-2">
                                  <h4 className="font-serif text-lg text-white">Synthesizing Creative Strategy</h4>
                                  <p className="text-[12px] text-white/50 leading-relaxed font-light">
                                    The Director is compiling textile DNA observations and generating the campaign assets. View real-time pipeline status below.
                                  </p>
                                </div>
                                  <div className="p-4 bg-white/[0.02] border border-white/5 rounded-2xl text-left space-y-3 font-mono text-[10px]">
                                    <div className="flex justify-between">
                                      <span className="text-white/35 uppercase">Task ID</span>
                                      <span className="text-[#9b87f5]">{activeCampaign.id}</span>
                                    </div>
                                  <div className="flex justify-between">
                                    <span className="text-white/35 uppercase">Current State</span>
                                    <span className="text-[#E1D4C0] uppercase tracking-wider">{activeCampaign.v3_creative_state.status}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        ) : (
                          <div className="flex-1 overflow-y-auto relative min-h-0 flex flex-col gap-6 pr-1">
                            {/* Artistic Parameters Header */}
                            <div className="flex items-center justify-between border-b border-white/5 pb-3 mb-2 shrink-0">
                              <div className="flex flex-col text-left">
                                <span className="text-[9px] tracking-[0.2em] uppercase text-white/30 font-mono">Artistic Parameters</span>
                                <h3 className="font-serif text-lg text-white mt-0.5">Evolving Spatial Canvas</h3>
                              </div>
                            </div>

                            {/* Alert Box for Physical Violation */}
                            {physicalViolation && (
                              <PhysicalViolationAlert 
                                violation={physicalViolation} 
                                onDismiss={() => setPhysicalViolation(null)} 
                                className="mb-2 shrink-0"
                              />
                            )}

                            {/* Heuristic Recommendation */}
                            {activeRecommendation && (
                              <HeuristicRecommendation
                                recommendation={activeRecommendation}
                                onAccept={(rec) => {
                                  if (rec.affectedParameters) {
                                    Object.entries(rec.affectedParameters).forEach(([k, v]) => {
                                      handleOptionChange(k as "background" | "pose" | "lighting", v as string);
                                    });
                                  }
                                  setActiveRecommendation(null);
                                }}
                                onIgnore={() => setActiveRecommendation(null)}
                                className="mb-2 shrink-0"
                              />
                            )}

                            {/* Bento Grid */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch pb-6">
                              
                              {/* Card 1: Background */}
                              <div className="bg-white/5 border border-white/10 p-1.5 rounded-[2rem] flex flex-col">
                                <div className="flex-1 bg-[#0C0C0E] shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)] rounded-[calc(2rem-0.375rem)] p-6 text-left flex flex-col gap-4">
                                  <div className="flex items-center justify-between">
                                    <span className="text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0] font-mono">1. Background</span>
                                    <span className="text-[10px] text-white/40 truncate max-w-[140px] font-mono">{selectedBackground || "None"}</span>
                                  </div>
                                  <div className="flex flex-col gap-2 max-h-[160px] overflow-y-auto pr-1">
                                    {[
                                      { name: "Heritage Fort / Palace Corridor", preview: "/previews/heritage_fort.png" },
                                      { name: "Lush Garden", preview: "/previews/lush_garden.png" },
                                      { name: "Minimalist Stone Pedestal", preview: "/previews/stone_pedestal.png", isRec: true },
                                      { name: "Reflective Metal Surface", preview: "/previews/metal_surface.png" },
                                      { name: "Industrial Concrete / Urban", preview: "/previews/urban_concrete.png" },
                                      { name: "Draped Velvet Platform", preview: "/previews/velvet_platform.png" }
                                    ].map(opt => {
                                      const isSelected = selectedBackground === opt.name;
                                      const isRec = opt.isRec;
                                      return (
                                        <button
                                          key={opt.name}
                                          onClick={() => handleOptionChange('background', opt.name)}
                                          className={`flex items-center justify-between w-full px-4 py-2.5 rounded-xl border text-[11px] font-light transition-all cursor-pointer ${
                                            isSelected 
                                              ? 'bg-[#E1D4C0] border-[#E1D4C0] text-black font-semibold' 
                                              : 'bg-white/[0.01] border-white/5 text-white/60 hover:bg-white/[0.03] hover:text-white'
                                          }`}
                                        >
                                          <span>{opt.name}</span>
                                          {isRec && <span className={`text-[8px] font-mono tracking-widest px-1.5 py-0.5 rounded-full ${isSelected ? 'bg-black/10 text-black' : 'bg-[#9b87f5]/20 text-[#9b87f5]'}`}>✨ Rec</span>}
                                        </button>
                                      );
                                    })}
                                  </div>
                                </div>
                              </div>

                              {/* Card 2: Pose & Movement */}
                              <div className="bg-white/5 border border-white/10 p-1.5 rounded-[2rem] flex flex-col">
                                <div className="flex-1 bg-[#0C0C0E] shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)] rounded-[calc(2rem-0.375rem)] p-6 text-left flex flex-col gap-4">
                                  <div className="flex items-center justify-between">
                                    <span className="text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0] font-mono">2. Pose & Flow</span>
                                    <span className="text-[10px] text-white/40 truncate max-w-[140px] font-mono">{selectedPose || "None"}</span>
                                  </div>
                                  <div className="flex flex-col gap-2 max-h-[160px] overflow-y-auto pr-1">
                                    {[
                                      { name: "Architectural Drape / Structured Fold", isRec: true },
                                      { name: "Dynamic Fabric Spin / Wind Blown" },
                                      { name: "Static Geometrical Placement" },
                                      { name: "Cascading Edge / Waterflow Effect" },
                                      { name: "Suspended / Anti-gravity Float" }
                                    ].map(opt => {
                                      const isSelected = selectedPose === opt.name;
                                      const isRec = opt.isRec;
                                      return (
                                        <button
                                          key={opt.name}
                                          onClick={() => handleOptionChange('pose', opt.name)}
                                          className={`flex items-center justify-between w-full px-4 py-2.5 rounded-xl border text-[11px] font-light transition-all cursor-pointer ${
                                            isSelected 
                                              ? 'bg-[#E1D4C0] border-[#E1D4C0] text-black font-semibold' 
                                              : 'bg-white/[0.01] border-white/5 text-white/60 hover:bg-white/[0.03] hover:text-white'
                                          }`}
                                        >
                                          <span>{opt.name}</span>
                                          {isRec && <span className={`text-[8px] font-mono tracking-widest px-1.5 py-0.5 rounded-full ${isSelected ? 'bg-black/10 text-black' : 'bg-[#9b87f5]/20 text-[#9b87f5]'}`}>✨ Rec</span>}
                                        </button>
                                      );
                                    })}
                                  </div>
                                </div>
                              </div>

                              {/* Card 3: Cinematic Lighting */}
                              <div className="bg-white/5 border border-white/10 p-1.5 rounded-[2rem] flex flex-col">
                                <div className="flex-1 bg-[#0C0C0E] shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)] rounded-[calc(2rem-0.375rem)] p-6 text-left flex flex-col gap-4">
                                  <div className="flex items-center justify-between">
                                    <span className="text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0] font-mono">3. Lighting</span>
                                    <span className="text-[10px] text-white/40 truncate max-w-[140px] font-mono">{selectedLighting || "None"}</span>
                                  </div>
                                  <div className="flex flex-col gap-2 max-h-[160px] overflow-y-auto pr-1">
                                    {[
                                      { name: "Golden Hour Warmth / Soft Sun" },
                                      { name: "High-contrast Chiaroscuro" },
                                      { name: "Ethereal Backlight / Edge Wrap", isRec: true },
                                      { name: "Moody Rim Light / Cyberpunk Glow" },
                                      { name: "Soft Studio Diffused Light" }
                                    ].map(opt => {
                                      const isSelected = selectedLighting === opt.name;
                                      const isRec = opt.isRec;
                                      return (
                                        <button
                                          key={opt.name}
                                          onClick={() => handleOptionChange('lighting', opt.name)}
                                          className={`flex items-center justify-between w-full px-4 py-2.5 rounded-xl border text-[11px] font-light transition-all cursor-pointer ${
                                            isSelected 
                                              ? 'bg-[#E1D4C0] border-[#E1D4C0] text-black font-semibold' 
                                              : 'bg-white/[0.01] border-white/5 text-white/60 hover:bg-white/[0.03] hover:text-white'
                                          }`}
                                        >
                                          <span>{opt.name}</span>
                                          {isRec && <span className={`text-[8px] font-mono tracking-widest px-1.5 py-0.5 rounded-full ${isSelected ? 'bg-black/10 text-black' : 'bg-[#9b87f5]/20 text-[#9b87f5]'}`}>✨ Rec</span>}
                                        </button>
                                      );
                                    })}
                                  </div>
                                </div>
                              </div>

                              {/* Card 4: Settings & Generate */}
                              <div className="bg-white/5 border border-white/10 p-1.5 rounded-[2rem] flex flex-col justify-between">
                                <div className="flex-1 bg-[#0C0C0E] shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)] rounded-[calc(2rem-0.375rem)] p-6 text-left flex flex-col gap-4 justify-between">
                                  <div className="space-y-4">
                                    <span className="text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0] font-mono block">4. Synthesis Control</span>
                                    
                                    {/* Ratio Selector */}
                                    <div className="space-y-1.5">
                                      <span className="text-[9px] uppercase tracking-wider text-white/40 font-mono block">Aspect Ratio</span>
                                      <div className="flex gap-1.5">
                                        {['3:4', '16:9', '1:1', '4:5'].map(r => (
                                          <button
                                            key={r}
                                            onClick={() => setSelectedRatio(r)}
                                            className={`flex-1 py-1 text-[9px] font-mono rounded-lg border transition-all cursor-pointer ${
                                              selectedRatio === r
                                                ? 'bg-[#E1D4C0] border-[#E1D4C0] text-black font-bold'
                                                : 'bg-white/[0.01] border-white/5 text-white/60 hover:bg-white/[0.03]'
                                            }`}
                                          >
                                            {r}
                                          </button>
                                        ))}
                                      </div>
                                    </div>

                                    {/* Asset Count Selector */}
                                    <div className="space-y-1.5">
                                      <span className="text-[9px] uppercase tracking-wider text-white/40 font-mono block">Asset Quantity</span>
                                      <div className="flex gap-1.5">
                                        {[1, 2, 4, 8].map(cnt => (
                                          <button
                                            key={cnt}
                                            onClick={() => setSelectedAssetCount(cnt)}
                                            className={`flex-1 py-1 text-[9px] font-mono rounded-lg border transition-all cursor-pointer ${
                                              selectedAssetCount === cnt
                                                ? 'bg-[#E1D4C0] border-[#E1D4C0] text-black font-bold'
                                                : 'bg-white/[0.01] border-white/5 text-white/60 hover:bg-white/[0.03]'
                                            }`}
                                          >
                                            {cnt}
                                          </button>
                                        ))}
                                      </div>
                                    </div>
                                  </div>

                                  {/* Generate Button with button-in-button trailing icon */}
                                  <button
                                    onClick={() => {
                                      setWizardStep(1); // Reset wizard state
                                      handleGenerate();
                                    }}
                                    disabled={isGenerating || !!physicalViolation || !selectedBackground || !selectedPose || !selectedLighting}
                                    className="w-full mt-4 py-3 bg-[#E1D4C0] hover:bg-white text-black font-bold text-[10px] tracking-widest uppercase rounded-xl transition-all shadow-xl disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-between px-6 cursor-pointer group"
                                  >
                                    <span>{isGenerating ? "Synthesizing..." : `Generate (${selectedAssetCount * 2} Credits)`}</span>
                                    <div className="w-6 h-6 rounded-full bg-black/5 flex items-center justify-center group-hover:scale-105 transition-transform duration-300">
                                      <span className="text-black group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform duration-300 font-mono">↗</span>
                                    </div>
                                  </button>
                                </div>
                              </div>

                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* V2 Synthesis Controls Bar Overlay (Glow themed custom input) */}
                  {showControls && (
                    <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-30 w-full max-w-3xl px-4 pointer-events-auto">
                      <div className="absolute -inset-2 bg-gradient-to-r from-[#9b87f5]/15 via-[#E1D4C0]/10 to-[#9b87f5]/15 rounded-[36px] blur-xl -z-10 pointer-events-none" />
                      <PromptInputBox 
                        onSend={(text) => {
                          // Add User Message
                          const userMsg = { id: Date.now().toString(), sender: 'user', text };
                          setChatMessages(prev => [...prev, userMsg]);

                          // Analyze keywords to toggle configs or trigger generation
                          const lower = text.toLowerCase();
                          if (lower.includes('lighting') || lower.includes('bright') || lower.includes('dark')) {
                            setTimeout(() => {
                              setChatMessages(prev => [...prev, {
                                id: (Date.now()+1).toString(),
                                sender: 'director',
                                text: "Regarding lighting: High-key setups will flatten the metallic highlights of the Zari brocade. I recommend 'Ethereal Backlight / Edge Wrap' to wrap the edges and preserve texture details. Would you like to apply it?",
                                tweak: { label: "Apply Ethereal Backlight", affectedParameters: { lighting: "Ethereal Backlight / Edge Wrap" } }
                              }]);
                            }, 1000);
                          } else if (lower.includes('pose') || lower.includes('motion') || lower.includes('toss')) {
                            setTimeout(() => {
                              setChatMessages(prev => [...prev, {
                                id: (Date.now()+1).toString(),
                                sender: 'director',
                                text: "For poses: Stiff Banarasi silk drape requires architectural alignment. A wind-blown toss will look forced. I recommend 'Dynamic Fabric Spin' to leverage fabric weight. Let's switch it?",
                                tweak: { label: "Apply Dynamic Fabric Spin", affectedParameters: { pose: "Dynamic Fabric Spin" } }
                              }]);
                            }, 1000);
                          } else if (lower.includes('background') || lower.includes('palace') || lower.includes('garden')) {
                            setTimeout(() => {
                              setChatMessages(prev => [...prev, {
                                id: (Date.now()+1).toString(),
                                sender: 'director',
                                text: "For the backdrop, heritage corridor frames accentuate the Zari weave profile. I suggest 'Nighttime Palace'. Apply it?",
                                tweak: { label: "Apply Nighttime Palace", affectedParameters: { background: "Nighttime Palace" } }
                              }]);
                            }, 1000);
                          } else {
                            // Trigger generation
                            handleGenerate();
                          }
                        }}
                        isLoading={isGenerating}
                        placeholder="Discuss changes with Director, or type a prompt to generate..."
                        className="bg-black/30 border-white/10 shadow-[0_0_50px_rgba(155,135,245,0.15),0_0_30px_rgba(225,212,192,0.08)] backdrop-blur-xl"
                      />
                    </div>
                  )}
                </div>
              ) : null}
              {activeCampaign && (
                <div className="shrink-0 mt-4 w-full">
                  <WorkflowTimeline
                    status={activeCampaign.v3_creative_state?.status || 'pending'}
                    hasMaterial={!!activeCampaign.material_path}
                    weaveType={
                      Array.isArray(activeCampaign.identity?.product_dna?.weaving_technique?.value)
                        ? activeCampaign.identity.product_dna.weaving_technique.value.join(', ')
                        : activeCampaign.identity?.product_dna?.weaving_technique?.value || 'Zari Brocade'
                    }
                    fiberBase={
                      Array.isArray(activeCampaign.identity?.product_dna?.material?.value)
                        ? activeCampaign.identity.product_dna.material.value.join(', ')
                        : activeCampaign.identity?.product_dna?.material?.value || 'Silk'
                    }
                  />
                </div>
              )}
            </div>
          )}
        </div>

        {/* Inspiration Dock (only on empty state) */}
        {campaigns.length === 0 && !isLoadingList && (
          <div className="w-full pb-4">
            <div className="grid grid-cols-3 gap-6 w-full pb-4">
              <div className="w-full h-52 bg-[#E1D4C0]/5 hover:bg-[#E1D4C0]/10 backdrop-blur-md rounded-3xl border border-[#E1D4C0]/10 relative overflow-hidden group cursor-pointer hover:border-[#E1D4C0]/30 transition-colors duration-500">
                <div className="p-6 relative z-10">
                  <h3 className="text-sm font-semibold text-[#E1D4C0] tracking-wide">MATERIAL<br />INTELLIGENCE</h3>
                  <p className="text-xs text-[#E1D4C0]/50 mt-1">Extract textile DNA</p>
                </div>
                <div className="absolute -bottom-10 -right-4 flex gap-2 rotate-[-5deg] group-hover:rotate-[-2deg] transition-transform duration-500">
                  <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200" className="w-24 h-36 rounded-lg object-cover shadow-2xl border border-white/10" alt="mock" />
                  <img src="https://images.unsplash.com/photo-1604014237800-1c9102c219da?q=80&w=200" className="w-24 h-36 rounded-lg object-cover shadow-2xl border border-white/10 -translate-y-4" alt="mock" />
                  <img src="https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?q=80&w=200" className="w-24 h-36 rounded-lg object-cover shadow-2xl border border-white/10 -translate-y-8" alt="mock" />
                </div>
              </div>
              <div className="w-full h-52 bg-[#E1D4C0]/5 hover:bg-[#E1D4C0]/10 backdrop-blur-md rounded-3xl border border-[#E1D4C0]/10 relative overflow-hidden group cursor-pointer hover:border-[#E1D4C0]/30 transition-colors duration-500">
                <div className="p-6 relative z-10">
                  <h3 className="text-sm font-semibold text-[#E1D4C0] tracking-wide">CINEMATIC<br />CAMPAIGNS</h3>
                  <p className="text-xs text-[#E1D4C0]/50 mt-1">High-end visual generation</p>
                </div>
                <div className="absolute -bottom-12 -right-4 flex gap-2 rotate-[-10deg] group-hover:rotate-[-5deg] transition-transform duration-500">
                  <img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=200" className="w-28 h-40 rounded-lg object-cover shadow-2xl border border-white/10 translate-y-4" alt="mock" />
                  <img src="https://images.unsplash.com/photo-1434389670869-c80327f99995?q=80&w=200" className="w-28 h-40 rounded-lg object-cover shadow-2xl border border-white/10 translate-y-2" alt="mock" />
                  <img src="https://images.unsplash.com/photo-1550639525-c97d455acf70?q=80&w=200" className="w-28 h-40 rounded-lg object-cover shadow-2xl border border-white/10" alt="mock" />
                </div>
              </div>
              <div className="w-full h-52 bg-[#E1D4C0]/5 hover:bg-[#E1D4C0]/10 backdrop-blur-md rounded-3xl border border-[#E1D4C0]/10 relative overflow-hidden group cursor-pointer hover:border-[#E1D4C0]/30 transition-colors duration-500">
                <div className="p-6 relative z-10">
                  <h3 className="text-sm font-semibold text-[#E1D4C0] tracking-wide">BRAND<br />ARCHETYPES</h3>
                  <p className="text-xs text-[#E1D4C0]/50 mt-1">Strict style enforcement</p>
                </div>
                <div className="absolute -bottom-10 -right-2 flex gap-2 rotate-[5deg] group-hover:rotate-[2deg] transition-transform duration-500">
                  <img src="https://images.unsplash.com/photo-1509319117193-57bab727e09d?q=80&w=200" className="w-28 h-40 rounded-lg object-cover shadow-2xl border border-white/10 -translate-y-2" alt="mock" />
                  <img src="https://images.unsplash.com/photo-1520613495404-5177893af96c?q=80&w=200" className="w-28 h-40 rounded-lg object-cover shadow-2xl border border-white/10 -translate-y-4" alt="mock" />
                  <img src="https://images.unsplash.com/photo-1534062886737-f83fa14fa5c7?q=80&w=200" className="w-28 h-40 rounded-lg object-cover shadow-2xl border border-white/10 -translate-y-6" alt="mock" />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* V2 Reasoning Panel */}
      <div className="w-[420px] h-full bg-[#0D0D0D] border-l border-white/5 flex flex-col shrink-0 relative z-20">
        <div className="h-24 px-6 flex items-end pb-6 border-b border-white/5 shrink-0 justify-between">
          <h2 className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-medium">Intelligence Engine</h2>
          {isAnalyzing && <span className="text-[10px] uppercase text-[#E1D4C0] animate-pulse">Computing...</span>}
        </div>

        <div className="flex-1 flex flex-col gap-4 p-6 overflow-hidden">
          {/* Default State */}
          {activeCampaignId === null && (
            <div className="text-[13px] text-white/30 font-light leading-relaxed">
              Mercer AI is observing the workspace. Select or start a campaign.
            </div>
          )}

          {/* Reasoning Trace Panel */}
          {activeCampaignId !== null && (
             <ReasoningTracePanel decisions={decisions} className="flex-1 min-h-0" />
          )}

          {/* CRE Bento Grid */}
          {activeCampaignId !== null && creScores && (
             <div className="shrink-0 mt-2">
               <CREBentoGrid scores={creScores} />
             </div>
          )}
          
          {/* Creative Director Dialogue Log (Integrated Chat) */}
          {activeCampaignId !== null && (
            <div className="flex-1 flex flex-col gap-3 min-h-[300px] border-t border-white/5 pt-4 overflow-hidden">
              <div className="text-[10px] tracking-widest uppercase text-[#9b87f5] font-mono mb-1 text-left">Creative Dialogue</div>
              <div className="flex-1 flex flex-col gap-3 overflow-y-auto pr-2 scrollbar-hide">
                {chatMessages.map(msg => (
                  <div 
                    key={msg.id} 
                    className={`flex flex-col max-w-[90%] ${
                      msg.sender === 'user' ? 'self-end items-end' : 'self-start items-start'
                    }`}
                  >
                    <div 
                      className={`p-3 rounded-2xl text-[12px] leading-relaxed font-light ${
                        msg.sender === 'user' 
                          ? 'border border-[#E1D4C0]/20 text-[#E1D4C0] bg-transparent rounded-br-sm' 
                          : 'bg-white/[0.02] border border-white/5 text-white/70 rounded-bl-sm'
                      }`}
                    >
                      {msg.text}
                      {msg.tweak && (
                        <button 
                          onClick={() => {
                            // Apply tweak parameters
                            Object.entries(msg.tweak.affectedParameters).forEach(([k, v]) => {
                              if (k === 'background') handleOptionChange('background', v as string);
                              if (k === 'pose') handleOptionChange('pose', v as string);
                              if (k === 'lighting') handleOptionChange('lighting', v as string);
                            });
                            // Remove tweak button after apply
                            setChatMessages(prev => 
                              prev.map(m => m.id === msg.id ? { ...m, tweak: undefined } : m)
                            );
                          }}
                          className="mt-3 w-full py-1.5 rounded-sm border border-[#E1D4C0]/20 text-[#E1D4C0] text-[9px] font-mono tracking-widest uppercase hover:bg-[#E1D4C0]/10 transition-colors"
                        >
                          {msg.tweak.label}
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Floating Image Preview */}
      {hoveredPreview && (
        <div 
          className="fixed z-[100] pointer-events-none rounded-xl overflow-hidden shadow-2xl border border-white/10 transition-transform duration-75 ease-out"
          style={{
            left: mousePos.x + 32, // Offset to the right of cursor
            top: mousePos.y - 200,  // Offset up to center vertically
            width: '400px',
            height: '400px'
          }}
        >
          <img src={hoveredPreview} alt="Preview" className="w-full h-full object-cover" />
        </div>
      )}
    </div>
  );
}
