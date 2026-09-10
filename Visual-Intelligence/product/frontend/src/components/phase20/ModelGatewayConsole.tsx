"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Cpu, ShieldCheck, Activity, Key, FileText, CheckCircle, AlertTriangle, Play, Eye, EyeOff, Globe, Sparkles, Lock, Crown, Zap, Check } from "lucide-react";
import { generateLLMResponse, LLMResponseDTO, fetchModelProviders, ModelProviderInfoDTO } from "@/lib/phase20Client";

export function ModelGatewayConsole() {
  const [selectedTask, setSelectedTask] = useState("TREND_ANALYSIS");
  const [selectedModel, setSelectedModel] = useState("gemini-2.5-flash");
  const [customModelName, setCustomModelName] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [showApiKey, setShowApiKey] = useState(false);
  const [userTier, setUserTier] = useState<'STANDARD' | 'PRO'>("STANDARD");
  const [prompt, setPrompt] = useState("Analyze Y2K Cyberpunk aesthetic trend directions for NOCAP Apparel.");
  const [response, setResponse] = useState<LLMResponseDTO | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showProvenanceModal, setShowProvenanceModal] = useState(false);
  const [providersList, setProvidersList] = useState<ModelProviderInfoDTO[]>([]);

  const apiKeyInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetchModelProviders().then(list => setProvidersList(list));
    // Retrieve stored settings
    const savedKey = localStorage.getItem("user_llm_api_key") || "";
    const savedBaseUrl = localStorage.getItem("user_llm_base_url") || "";
    const savedTier = (localStorage.getItem("user_tier") as 'STANDARD' | 'PRO') || "STANDARD";
    if (savedKey) setApiKey(savedKey);
    if (savedBaseUrl) setBaseUrl(savedBaseUrl);
    if (savedTier) setUserTier(savedTier);
  }, []);

  const handleSaveCredentials = () => {
    localStorage.setItem("user_llm_api_key", apiKey);
    localStorage.setItem("user_llm_base_url", baseUrl);
    localStorage.setItem("user_tier", userTier);
  };

  const currentModelInfo = providersList.find(p => p.id === selectedModel);
  const isProModel = currentModelInfo?.tier === "PRO";
  const isUnlocked = !isProModel || userTier === "PRO" || apiKey.trim().length > 0;

  const handleGenerate = async () => {
    if (!isUnlocked) return;
    setIsLoading(true);
    handleSaveCredentials();

    const activeModelName = selectedModel === "custom-model" && customModelName.trim()
      ? customModelName.trim()
      : selectedModel;

    try {
      const res = await generateLLMResponse(
        selectedTask,
        prompt,
        "client_nocap",
        activeModelName,
        apiKey || undefined,
        baseUrl || undefined
      );
      setResponse(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const isCustomModel = selectedModel === "custom-model";

  return (
    <div className="flex flex-col gap-6 w-full text-zinc-100">
      {/* Top Status Cards & User Tier Switch */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-4 flex flex-col gap-2 shadow-lg">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-mono">
            <span>USER ACCESS TIER</span>
            <Crown className={`w-4 h-4 ${userTier === 'PRO' ? 'text-amber-400' : 'text-zinc-500'}`} />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold text-white">
              {userTier === 'PRO' ? "PRO / PREMIUM TIER" : "STANDARD TIER"}
            </span>
            <button
              onClick={() => {
                const nextTier = userTier === 'STANDARD' ? 'PRO' : 'STANDARD';
                setUserTier(nextTier);
                localStorage.setItem("user_tier", nextTier);
              }}
              className={`px-3 py-1 rounded-full text-xs font-mono font-semibold transition-colors flex items-center gap-1 ${
                userTier === 'PRO'
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30'
                  : 'bg-zinc-800 text-zinc-300 border border-zinc-700 hover:bg-zinc-700'
              }`}
            >
              {userTier === 'PRO' ? <Check className="w-3 h-3 text-amber-400" /> : null}
              {userTier === 'PRO' ? "PRO ACTIVE" : "UPGRADE TO PRO"}
            </button>
          </div>
          <div className="text-xs text-zinc-500 font-mono">
            {userTier === 'PRO' ? "All Flagship Models Unlocked" : "Pro models require Pro Tier or API Key"}
          </div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-4 flex flex-col gap-2 shadow-lg">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-mono">
            <span>ACTIVE MODEL & ACCESS</span>
            <Cpu className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-sm font-semibold text-white truncate flex items-center gap-2">
            <span className="truncate">{isCustomModel ? customModelName || "Custom LLM" : selectedModel}</span>
            {isProModel ? (
              <span className="px-2 py-0.5 text-[10px] bg-amber-500/20 text-amber-300 rounded-full border border-amber-500/30 font-mono shrink-0 flex items-center gap-1">
                <Crown className="w-3 h-3" /> PRO
              </span>
            ) : (
              <span className="px-2 py-0.5 text-[10px] bg-emerald-500/20 text-emerald-300 rounded-full border border-emerald-500/30 font-mono shrink-0">
                STANDARD
              </span>
            )}
          </div>
          <div className="text-xs text-zinc-500 font-mono">
            {apiKey ? "🔑 Custom API Key Configured" : "Default Provider Key"}
          </div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-4 flex flex-col gap-2 shadow-lg">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-mono">
            <span>SECURITY & REDACTION</span>
            <ShieldCheck className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-sm font-semibold text-white flex items-center gap-2">
            <span className="text-sky-300">KEYS SCRUBBED AT GATEWAY</span>
          </div>
          <div className="text-xs text-zinc-500">API credentials redacted prior to model prompt</div>
        </div>

        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-4 flex flex-col gap-2 shadow-lg">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-mono">
            <span>LATENCY & TOKENS</span>
            <Activity className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-sm font-semibold text-white font-mono">
            {response ? `${response.latency_ms.toFixed(1)} ms | ${response.total_tokens} Tokens` : "-- ms | 0 Tokens"}
          </div>
          <div className="text-xs text-zinc-500 font-mono">Budget: 16,384 Tokens/Req</div>
        </div>
      </div>

      {/* Universal LLM Provider & Custom Credentials Panel */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 flex flex-col gap-6 shadow-2xl">
        <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
          <div className="flex items-center gap-3">
            <Globe className="w-5 h-5 text-[#E1D4C0]" />
            <div>
              <h3 className="text-lg font-medium text-white">Next-Gen Universal LLM Model Configurator</h3>
              <p className="text-xs text-zinc-400">Access flagship next-gen models (Gemini 3.5 Pro, GPT-5 Turbo, Claude 3.7 Sonnet, Fable 1 Creative, DeepSeek R1) or use any custom API endpoint.</p>
            </div>
          </div>
          <span className="text-xs font-mono px-3 py-1 bg-amber-500/10 text-amber-300 rounded-full border border-amber-500/30 flex items-center gap-1.5">
            <Crown className="w-3.5 h-3.5" /> PRO TIER MODEL ACCESSIBLE
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Model Selection */}
          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                Target LLM Model
              </span>
              {isProModel && (
                <span className="text-[10px] font-mono text-amber-400 flex items-center gap-1">
                  <Crown className="w-3 h-3" /> Flagship Pro Model
                </span>
              )}
            </label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            >
              <optgroup label="✨ Flagship & Next-Gen Pro Models">
                {providersList.filter(p => p.tier === "PRO").map(p => (
                  <option key={p.id} value={p.id}>
                    👑 [PRO] {p.provider} ({p.model_name})
                  </option>
                ))}
              </optgroup>
              <optgroup label="⚡ Standard & Free Models">
                {providersList.filter(p => p.tier === "STANDARD").map(p => (
                  <option key={p.id} value={p.id}>
                    {p.provider} ({p.model_name})
                  </option>
                ))}
              </optgroup>
            </select>
          </div>

          {/* Custom Model Name (If Selected) */}
          {isCustomModel && (
            <div className="flex flex-col gap-2">
              <label className="text-xs font-mono text-zinc-400 uppercase">Custom Model ID / Name</label>
              <input
                type="text"
                placeholder="e.g. mistral-large-2411 or custom-finetune-v1"
                value={customModelName}
                onChange={(e) => setCustomModelName(e.target.value)}
                className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
              />
            </div>
          )}

          {/* API Key Input */}
          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Key className="w-3.5 h-3.5 text-sky-400" />
                Custom API Key
              </span>
              <button
                type="button"
                onClick={() => setShowApiKey(!showApiKey)}
                className="text-zinc-500 hover:text-white text-[11px] font-mono flex items-center gap-1"
              >
                {showApiKey ? <EyeOff className="w-3 h-3" /> : <Eye className="w-3 h-3" />}
                {showApiKey ? "Hide" : "Show"}
              </button>
            </label>
            <input
              ref={apiKeyInputRef}
              type={showApiKey ? "text" : "password"}
              placeholder="Paste your API key (sk-..., gsk-..., etc.)"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            />
          </div>

          {/* Custom Base URL Endpoint */}
          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase flex items-center gap-1.5">
              <Globe className="w-3.5 h-3.5 text-purple-400" />
              Base URL Endpoint (Optional)
            </label>
            <input
              type="text"
              placeholder="Default API endpoint (e.g. https://api.deepseek.com/v1)"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            />
          </div>
        </div>

        {/* Pro Tier Lock Banner (If Selected Pro Model on Standard Tier without API Key) */}
        {!isUnlocked && (
          <motion.div
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-r from-amber-950/60 via-purple-950/60 to-zinc-900 border border-amber-500/40 p-4 rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xl"
          >
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-amber-500/20 text-amber-300 rounded-lg border border-amber-500/30">
                <Lock className="w-5 h-5" />
              </div>
              <div className="flex flex-col gap-0.5">
                <div className="text-sm font-semibold text-white flex items-center gap-2">
                  <span>Pro Model Locked: {currentModelInfo?.provider}</span>
                  <span className="px-2 py-0.5 text-[10px] bg-amber-500/20 text-amber-300 rounded font-mono">PRO</span>
                </div>
                <div className="text-xs text-zinc-400">
                  This flagship next-gen model requires either an active Pro Tier subscription OR your own custom API key.
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                type="button"
                onClick={() => {
                  setUserTier("PRO");
                  localStorage.setItem("user_tier", "PRO");
                }}
                className="px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-semibold rounded-lg text-xs transition-all shadow-lg flex items-center gap-1.5"
              >
                <Crown className="w-3.5 h-3.5 fill-current" />
                Switch to Pro Tier
              </button>
              <button
                type="button"
                onClick={() => {
                  apiKeyInputRef.current?.focus();
                  setShowApiKey(true);
                }}
                className="px-3 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-xs font-medium transition-colors flex items-center gap-1"
              >
                <Key className="w-3.5 h-3.5 text-sky-400" />
                Enter API Key
              </button>
            </div>
          </motion.div>
        )}

        {/* Task Selection & Prompt Console */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-zinc-800 pt-5">
          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Task Type Selection</label>
            <select
              value={selectedTask}
              onChange={(e) => setSelectedTask(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            >
              <option value="TREND_ANALYSIS">TREND_ANALYSIS</option>
              <option value="STRATEGY_SYNTHESIS">STRATEGY_SYNTHESIS</option>
              <option value="CREATIVE_DIRECTION">CREATIVE_DIRECTION</option>
              <option value="COPY_GENERATION">COPY_GENERATION</option>
              <option value="CRITIQUE">CRITIQUE</option>
              <option value="REVIEW_EVALUATION">REVIEW_EVALUATION</option>
            </select>
          </div>

          <div className="flex flex-col gap-2 md:col-span-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Prompt Content (Redaction Audited)</label>
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            />
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="text-xs text-zinc-500 font-mono flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isUnlocked ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`}></span>
            Routing request to: <span className="text-zinc-300 font-semibold">{isCustomModel ? customModelName || "Custom" : selectedModel}</span>
          </div>

          <button
            onClick={handleGenerate}
            disabled={isLoading || !isUnlocked}
            className="flex items-center gap-2 px-6 py-2.5 bg-[#E1D4C0] hover:bg-white text-black font-medium text-sm rounded-lg transition-colors shadow-lg disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-current" />
            {isLoading ? "Dispatching to Universal Model Gateway..." : isUnlocked ? "Execute LLM Request" : "Model Locked (Select Standard / Enter Key)"}
          </button>
        </div>

        {/* Model Output & Provenance Display */}
        {response && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 bg-zinc-950 border border-zinc-800 rounded-xl p-5 flex flex-col gap-4"
          >
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-emerald-400">
                <CheckCircle className="w-4 h-4" />
                <span>Response Validated & Provenance Recorded ({response.provenance.provider})</span>
              </div>
              <button
                onClick={() => setShowProvenanceModal(true)}
                className="flex items-center gap-1.5 text-xs font-mono text-[#E1D4C0] hover:underline"
              >
                <FileText className="w-3.5 h-3.5" />
                View Provenance Trace ({response.provenance.requestId})
              </button>
            </div>

            <pre className="text-xs font-mono text-zinc-300 bg-zinc-900 p-4 rounded-lg overflow-x-auto border border-zinc-800 leading-relaxed">
              {response.content}
            </pre>
          </motion.div>
        )}
      </div>

      {/* Provenance Trace Modal */}
      <AnimatePresence>
        {showProvenanceModal && response && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-zinc-900 border border-zinc-800 max-w-lg w-full rounded-xl p-6 flex flex-col gap-4 shadow-2xl"
            >
              <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                <h4 className="text-base font-semibold text-white">Immutable Response Provenance</h4>
                <button
                  onClick={() => setShowProvenanceModal(false)}
                  className="text-zinc-400 hover:text-white text-sm"
                >
                  ✕
                </button>
              </div>

              <div className="flex flex-col gap-2 text-xs font-mono text-zinc-300">
                <div><span className="text-zinc-500">Provider:</span> {response.provenance.provider}</div>
                <div><span className="text-zinc-500">Model:</span> {response.provenance.model} ({response.provenance.modelVersion})</div>
                <div><span className="text-zinc-500">Request ID:</span> {response.provenance.requestId}</div>
                <div><span className="text-zinc-500">Policy Version:</span> {response.provenance.policyVersion}</div>
                <div><span className="text-zinc-500">Request Hash (SHA-256):</span> {response.provenance.requestHash}</div>
                <div><span className="text-zinc-500">Structured Output Validated:</span> {String(response.provenance.structuredOutputValidated)}</div>
              </div>

              <button
                onClick={() => setShowProvenanceModal(false)}
                className="mt-2 w-full py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-xs font-medium"
              >
                Close Provenance Trace
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
