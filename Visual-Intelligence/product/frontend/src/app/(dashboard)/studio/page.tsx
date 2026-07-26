"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Plus, ArrowLeft, Edit2, Trash2, Upload } from "lucide-react";
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

// --- SVG Icons ---

const FolderIcon = ({ hasMaterial }: { hasMaterial?: boolean }) => (
  <svg viewBox="0 0 105 105" className="w-full h-full drop-shadow-2xl group-hover:scale-[1.03] transition-transform duration-300">
    <path d="M 10 90 L 10 25 Q 10 15 20 15 L 35 15 L 45 25 L 85 25 Q 95 25 95 35 L 95 90 Q 95 95 90 95 L 20 95 Q 10 95 10 90 Z" fill="#F7BA3E" stroke="#111111" strokeWidth="4" strokeLinejoin="round" />
    <rect x="18" y="25" width="69" height="60" fill="#B2EBF2" stroke="#111111" strokeWidth="4" strokeLinejoin="round" />
    <rect x="18" y="35" width="69" height="50" fill="#FFFFFF" stroke="#111111" strokeWidth="4" strokeLinejoin="round" />
    <line x1="26" y1="48" x2="65" y2="48" stroke="#111111" strokeWidth="4" strokeLinecap="round" />
    <line x1="26" y1="58" x2="45" y2="58" stroke="#111111" strokeWidth="4" strokeLinecap="round" />
    <path d="M 10 90 L 10 55 Q 10 45 20 45 L 42 45 L 52 35 L 85 35 Q 95 35 95 45 L 95 90 Q 95 95 90 95 L 20 95 Q 10 95 10 90 Z" fill="#FCDA68" stroke="#111111" strokeWidth="4" strokeLinejoin="round" />
    {hasMaterial && (
      <g transform="translate(41, 53)">
        <rect x="0" y="0" width="24" height="24" fill="#FFFFFF" stroke="#111111" strokeWidth="3" rx="4" strokeLinejoin="round" />
        <circle cx="8" cy="8" r="2.5" fill="#111111" />
        <path d="M 0 20 L 8 12 L 16 20 L 24 12 L 24 24 L 0 24 Z" fill="#111111" stroke="#111111" strokeWidth="2" strokeLinejoin="round" />
      </g>
    )}
  </svg>
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

  // --- Art Direction Selectors State ---
  const [selectedBackground, setSelectedBackground] = useState<string>("");
  const [selectedPose, setSelectedPose] = useState<string>("");
  const [selectedLighting, setSelectedLighting] = useState<string>("");

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
  }, []);

  const closeCampaign = () => {
    setActiveCampaignId(null);
    setActiveCampaign(null);
    setStepOverride(null);
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
        setActiveCampaign(updated);
        if (updated.planning) {
          setSelectedBackground(updated.planning.selected_background || "");
          setSelectedPose(updated.planning.selected_pose || "");
          setSelectedLighting(updated.planning.selected_lighting || "");
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
  const handleFileDrop = async (file: File) => {
    if (!activeCampaign) return;
    setIsUploading(true);
    try {
      await uploadMaterial(activeCampaign.id, file);
      // Immediately trigger analysis
      await analyzeMaterial(activeCampaign.id);
      // Clear step override since we have new material
      setStepOverride(null);
      // Refresh campaign state and start polling for results
      const updated = await getCampaign(activeCampaign.id);
      setActiveCampaign(updated);
      setCampaigns(prev => prev.map(c => c.id === activeCampaign.id ? { ...c, has_material: true } : c));
      startPolling(activeCampaign.id);
    } catch (e) {
      console.error("Upload/analyze failed:", e);
    } finally {
      setIsUploading(false);
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
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-white/30">
            <span className="cursor-pointer hover:text-white transition-colors" onClick={closeCampaign}>
              Campaign Studio
            </span>
            {activeCampaign && (
              <>
                <span>/</span>
                <span className="text-white/60">{activeCampaign.name}</span>
              </>
            )}
          </div>
          <button
            onClick={() => {
              if (activeCampaignId) {
                closeCampaign();
              } else {
                router.back();
              }
            }}
            className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors"
            title="Go Back"
          >
            <ArrowLeft size={14} />
          </button>
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
            <div className="flex-1 flex items-center justify-center -mt-16">
              {isLoadingCampaign ? (
                <div className="text-white/30 text-sm animate-pulse">Loading workspace...</div>
              ) : activeCampaign && currentStep === 'dropzone' ? (
                // Dropzone
                <div
                  onDragOver={(e) => { e.preventDefault(); setIsDraggingOver(true); }}
                  onDragLeave={() => setIsDraggingOver(false)}
                  onDrop={onDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`w-full max-w-2xl aspect-[4/3] border border-dashed flex flex-col items-center justify-center gap-6 cursor-pointer transition-all duration-500 rounded-xl ${
                    isDraggingOver
                      ? 'border-[#E1D4C0] bg-[#E1D4C0]/10'
                      : 'border-white/10 bg-white/5 hover:border-[#E1D4C0]/50 hover:bg-[#E1D4C0]/5'
                  }`}
                >
                  <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={onDropZoneChange} />
                  {isUploading ? (
                     <div className="flex flex-col items-center gap-3 animate-pulse">
                       <div className="w-10 h-10 rounded-full border border-[#E1D4C0]/40 flex items-center justify-center">
                         <Upload size={18} className="text-[#E1D4C0]" />
                       </div>
                       <div className="text-[13px] text-[#E1D4C0]/70 tracking-wide font-light">Uploading & analyzing...</div>
                     </div>
                  ) : (
                    <>
                      <div className="w-16 h-16 rounded-full border border-white/20 flex items-center justify-center text-white/40">
                        <Plus size={24} strokeWidth={1} />
                      </div>
                      <div className="text-center">
                        <div className="text-[13px] tracking-wide text-white/50 font-light mb-1">
                          Upload material or mood image
                        </div>
                        <div className="text-[11px] text-white/20">
                          Drag & drop or click to browse
                        </div>
                      </div>
                    </>
                  )}
                </div>
              ) : activeCampaign ? (
                // Active Workspace
                <div className="w-full h-full flex items-center justify-center relative p-8">
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
                    <div className="w-full max-w-5xl flex gap-8 items-stretch h-[72vh] text-left">
                      {/* Left: Material Canvas */}
                      <div className="w-[45%] flex flex-col gap-4 relative">
                        <div className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-medium">Material Specimen</div>
                        <div className="flex-1 bg-[#111111] rounded-xl border border-white/5 overflow-hidden relative">
                          <img
                            src={getMaterialUrl(activeCampaign.material_path!)}
                            alt="Material"
                            className="w-full h-full object-cover opacity-60"
                            onError={(e) => { (e.target as HTMLImageElement).src = '/placeholder.jpg'; }}
                          />
                          {/* DNA Overlay */}
                          {activeCampaign.identity?.product_dna && (
                            <div className="absolute bottom-6 left-6 right-6 p-6 bg-black/70 backdrop-blur-xl border border-white/10 rounded-xl">
                              <div className="text-[9px] tracking-[0.15em] uppercase text-[#E1D4C0] mb-3 font-semibold">Fabric Intelligence DNA</div>
                              <div className="grid grid-cols-2 gap-4 text-xs">
                                <div>
                                  <span className="text-white/40 block text-[9px] uppercase tracking-wider mb-0.5">Weave Type</span>
                                  <span className="text-white font-medium">{String(activeCampaign.identity.product_dna.weaving_technique.value)}</span>
                                </div>
                                <div>
                                  <span className="text-white/40 block text-[9px] uppercase tracking-wider mb-0.5">Fiber Base</span>
                                  <span className="text-white font-medium">{String(activeCampaign.identity.product_dna.material.value)}</span>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Right: Art Direction Config Panel */}
                      <div className="w-[55%] flex flex-col bg-[#0c0c0c] border border-white/5 rounded-xl p-6 overflow-y-auto relative">
                        <div className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-medium mb-6">Art Direction Configurations</div>

                        <div className="flex flex-col gap-6 flex-1">
                          {/* Background Selector */}
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-semibold uppercase tracking-wider text-white/60">1. Background Environment</span>
                              {activeCampaign.planning?.recommendations?.background && (
                                <span className="text-[9px] text-[#E1D4C0] bg-[#E1D4C0]/10 px-2 py-0.5 rounded font-mono border border-[#E1D4C0]/20">
                                  AI Rec: {activeCampaign.planning.recommendations.background.value}
                                </span>
                              )}
                            </div>
                            <div className="flex flex-wrap gap-2 mb-2">
                              {["Heritage Fort / Palace Corridor", "Lush Garden", "Nighttime Palace", "Cinematic Studio", "Persian Carpet Backdrop"].map(bg => {
                                const isSelected = selectedBackground === bg;
                                const isRec = activeCampaign.planning?.recommendations?.background?.value === bg;
                                return (
                                  <button
                                    key={bg}
                                    onClick={() => handleOptionChange('background', bg)}
                                    className={`px-3 py-1.5 rounded-full text-[11px] font-medium tracking-wide border transition-all duration-300 ${
                                      isSelected
                                        ? 'bg-[#E1D4C0] text-black border-[#E1D4C0]'
                                        : 'bg-white/5 text-white/60 border-white/5 hover:bg-white/10 hover:text-white'
                                    }`}
                                  >
                                    {bg} {isRec && "✨"}
                                  </button>
                                );
                              })}
                            </div>
                            {activeCampaign.planning?.recommendations?.background && (
                              <p className="text-[11px] text-[#E1D4C0]/70 font-light leading-relaxed italic px-1">
                                {activeCampaign.planning.recommendations.background.reason}
                              </p>
                            )}
                          </div>

                          {/* Pose Selector */}
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-semibold uppercase tracking-wider text-white/60">2. Pose & Movement</span>
                              {activeCampaign.planning?.recommendations?.pose && (
                                <span className="text-[9px] text-[#E1D4C0] bg-[#E1D4C0]/10 px-2 py-0.5 rounded font-mono border border-[#E1D4C0]/20">
                                  AI Rec: {activeCampaign.planning.recommendations.pose.value}
                                </span>
                              )}
                            </div>
                            <div className="flex flex-wrap gap-2 mb-2">
                              {["Dynamic Fabric Spin", "Contemplative Veil Drape", "Editorial Close-Up Gaze", "The Saree Column", "Wind-Blown Toss"].map(ps => {
                                const isSelected = selectedPose === ps;
                                const isRec = activeCampaign.planning?.recommendations?.pose?.value === ps;
                                return (
                                  <button
                                    key={ps}
                                    onClick={() => handleOptionChange('pose', ps)}
                                    className={`px-3 py-1.5 rounded-full text-[11px] font-medium tracking-wide border transition-all duration-300 ${
                                      isSelected
                                        ? 'bg-[#E1D4C0] text-black border-[#E1D4C0]'
                                        : 'bg-white/5 text-white/60 border-white/5 hover:bg-white/10 hover:text-white'
                                    }`}
                                  >
                                    {ps} {isRec && "✨"}
                                  </button>
                                );
                              })}
                            </div>
                            {activeCampaign.planning?.recommendations?.pose && (
                              <p className="text-[11px] text-[#E1D4C0]/70 font-light leading-relaxed italic px-1">
                                {activeCampaign.planning.recommendations.pose.reason}
                              </p>
                            )}
                          </div>

                          {/* Lighting Selector */}
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs font-semibold uppercase tracking-wider text-white/60">3. Cinematic Lighting</span>
                              {activeCampaign.planning?.recommendations?.lighting && (
                                <span className="text-[9px] text-[#E1D4C0] bg-[#E1D4C0]/10 px-2 py-0.5 rounded font-mono border border-[#E1D4C0]/20">
                                  AI Rec: {activeCampaign.planning.recommendations.lighting.value}
                                </span>
                              )}
                            </div>
                            <div className="flex flex-wrap gap-2 mb-2">
                              {["Golden Hour (2700K-3200K)", "Ethereal Backlight / Edge Wrap", "Soft Window Light", "High-Key Window Doorway", "Moonlight / Night Ambient", "Studio Warm Key"].map(lt => {
                                const isSelected = selectedLighting === lt;
                                const isRec = activeCampaign.planning?.recommendations?.lighting?.value === lt;
                                return (
                                  <button
                                    key={lt}
                                    onClick={() => handleOptionChange('lighting', lt)}
                                    className={`px-3 py-1.5 rounded-full text-[11px] font-medium tracking-wide border transition-all duration-300 ${
                                      isSelected
                                        ? 'bg-[#E1D4C0] text-black border-[#E1D4C0]'
                                        : 'bg-white/5 text-white/60 border-white/5 hover:bg-white/10 hover:text-white'
                                    }`}
                                  >
                                    {lt} {isRec && "✨"}
                                  </button>
                                );
                              })}
                            </div>
                            {activeCampaign.planning?.recommendations?.lighting && (
                              <p className="text-[11px] text-[#E1D4C0]/70 font-light leading-relaxed italic px-1">
                                {activeCampaign.planning.recommendations.lighting.reason}
                              </p>
                            )}
                          </div>

                          {/* Warning Message Container (Soft Warning Alert) */}
                          {getConflictWarning() && (
                            <div className="bg-yellow-500/10 border border-yellow-500/20 text-yellow-200/90 text-xs px-4 py-3.5 rounded-lg flex gap-3 items-start mt-2">
                              <span className="text-yellow-500 mt-0.5">⚠️</span>
                              <div className="flex-1">
                                <span className="font-semibold block mb-0.5">Fabric Physics Mismatch Warning</span>
                                <span className="font-light leading-relaxed">{getConflictWarning()}</span>
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Submit Button */}
                        <div className="mt-8 pt-6 border-t border-white/5 flex justify-end">
                          <button
                            onClick={handleGenerate}
                            disabled={isGenerating}
                            className="px-8 py-3.5 rounded-full bg-[#E1D4C0] text-black font-semibold text-xs tracking-widest uppercase hover:bg-white transition-colors duration-300 disabled:opacity-50 shadow-xl"
                          >
                            {isGenerating ? "Synthesizing..." : "Synthesize & Generate"}
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : null}
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

      {/* Reasoning Panel */}
      <div className="w-[380px] h-full border-l border-white/5 bg-[#0D0D0D] flex flex-col shrink-0 relative z-20">
        <div className="h-24 px-8 flex items-end pb-6 border-b border-white/5 shrink-0">
          <h2 className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-medium">Reasoning Panel</h2>
        </div>

        <div className="flex-1 overflow-y-auto p-8 flex flex-col gap-8">

          {/* Default */}
          {activeCampaignId === null && (
            <div className="text-[13px] text-white/30 font-light leading-relaxed">
              Mercer AI is observing the workspace. Select or start a campaign.
            </div>
          )}

          {/* Campaign open, no material */}
          {activeCampaignId !== null && activeCampaign && !activeCampaign.material_path && !isUploading && (
            <div className="text-[13px] text-white/30 font-light leading-relaxed">
              Campaign initialized. Upload a material or mood image to begin reasoning.
            </div>
          )}

          {/* Uploading */}
          {isUploading && (
            <div className="flex items-center gap-3 animate-pulse">
              <div className="w-1.5 h-1.5 bg-[#E1D4C0] rounded-full" />
              <div className="text-[11px] tracking-wide text-[#E1D4C0]">Uploading material...</div>
            </div>
          )}

          {/* Memory Stream from backend */}
          {activeCampaign && activeCampaign.memory_stream.length > 0 && (
            <div className="flex flex-col gap-8">
              {activeCampaign.memory_stream.map((node: MemoryNode, idx) => (
                <div key={idx} className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                  <div className="text-[9px] tracking-[0.2em] uppercase text-white/30 mb-3">
                    {node.type === 'conclusion' ? 'Conclusion' : node.type === 'observation' ? 'Observation' : 'Reasoning'}
                  </div>
                  <p className="text-[13px] text-white/70 font-light leading-relaxed">
                    {node.content}
                  </p>
                </div>
              ))}

              {/* Analyzing indicator */}
              {(isAnalyzing || isGenerating) && (
                <div className="flex items-center gap-3 animate-pulse opacity-80">
                  <div className="w-1.5 h-1.5 bg-[#E1D4C0] rounded-full" />
                  <div className="text-[11px] tracking-wide text-[#E1D4C0] font-medium">Mercer AI is thinking...</div>
                </div>
              )}

              {/* Final Direction CTA */}
              {!isAnalyzing && activeCampaign.planning?.proposed_direction_title && (
                <div className="mt-4 pt-8 border-t border-white/5 animate-in fade-in duration-1000">
                  <div className="text-[9px] tracking-[0.2em] uppercase text-[#E1D4C0] mb-4">Proposed Direction</div>
                  <h3 className="font-serif text-2xl text-white/90 mb-4">{activeCampaign.planning.proposed_direction_title}</h3>
                  <p className="text-[13px] text-white/60 font-light leading-relaxed mb-8">
                    {activeCampaign.planning.proposed_direction_body}
                  </p>
                  <button 
                    onClick={handleGenerate}
                    disabled={isGenerating}
                    className="w-full py-4 bg-[#E1D4C0] text-[11px] font-medium tracking-[0.2em] uppercase text-[#0A0A0A] hover:bg-white transition-all duration-300 disabled:opacity-50">
                    {isGenerating ? "Generating..." : "Generate Moodboard"}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
