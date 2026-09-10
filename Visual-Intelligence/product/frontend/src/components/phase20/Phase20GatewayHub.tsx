"use client";

import React, { useState } from "react";
import { Cpu, Image as ImageIcon, Server, Award, Layers } from "lucide-react";
import { ModelGatewayConsole } from "./ModelGatewayConsole";
import { VisualModelStudio } from "./VisualModelStudio";
import { MCPConnectorCenter } from "./MCPConnectorCenter";
import { VisualKnowledgeDashboard } from "./VisualKnowledgeDashboard";

export function Phase20GatewayHub() {
  const [activeTab, setActiveTab] = useState<'llm' | 'visual' | 'mcp' | 'benchmark'>('llm');

  return (
    <div className="flex flex-col gap-6 w-full max-w-7xl mx-auto p-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-zinc-900/90 border border-zinc-800 p-6 rounded-2xl shadow-2xl">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-[#E1D4C0]/10 border border-[#E1D4C0]/30 flex items-center justify-center text-[#E1D4C0]">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-wide">
              Phase 20 Gateways & Visual Intelligence Control Surface
            </h1>
            <p className="text-xs text-zinc-400 mt-1">
              Model Integration, MCP Transport Connectivity & Visual Knowledge Benchmark Boundary
            </p>
          </div>
        </div>

        {/* Tab Navigation Pill Bar */}
        <div className="flex items-center bg-zinc-950 p-1.5 rounded-xl border border-zinc-800 shrink-0">
          <button
            onClick={() => setActiveTab('llm')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'llm'
                ? "bg-[#E1D4C0] text-black font-semibold shadow-md"
                : "text-zinc-400 hover:text-white hover:bg-zinc-900"
            }`}
          >
            <Cpu className="w-3.5 h-3.5" /> LLM Gateway
          </button>

          <button
            onClick={() => setActiveTab('visual')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'visual'
                ? "bg-[#E1D4C0] text-black font-semibold shadow-md"
                : "text-zinc-400 hover:text-white hover:bg-zinc-900"
            }`}
          >
            <ImageIcon className="w-3.5 h-3.5" /> Visual Gateway
          </button>

          <button
            onClick={() => setActiveTab('mcp')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'mcp'
                ? "bg-[#E1D4C0] text-black font-semibold shadow-md"
                : "text-zinc-400 hover:text-white hover:bg-zinc-900"
            }`}
          >
            <Server className="w-3.5 h-3.5" /> MCP Transport
          </button>

          <button
            onClick={() => setActiveTab('benchmark')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'benchmark'
                ? "bg-[#E1D4C0] text-black font-semibold shadow-md"
                : "text-zinc-400 hover:text-white hover:bg-zinc-900"
            }`}
          >
            <Award className="w-3.5 h-3.5" /> Benchmark (250 Cases)
          </button>
        </div>
      </div>

      {/* Tab Content Display */}
      <div className="w-full">
        {activeTab === 'llm' && <ModelGatewayConsole />}
        {activeTab === 'visual' && <VisualModelStudio />}
        {activeTab === 'mcp' && <MCPConnectorCenter />}
        {activeTab === 'benchmark' && <VisualKnowledgeDashboard />}
      </div>
    </div>
  );
}
