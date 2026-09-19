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
    <div className="flex flex-col gap-6 w-full max-w-7xl mx-auto p-6 bg-background text-foreground">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-card border border-border p-6 rounded-2xl shadow-xs">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground tracking-wide">
              Phase 20 Gateways & Visual Intelligence Control Surface
            </h1>
            <p className="text-xs text-muted-foreground mt-1">
              Model Integration, MCP Transport Connectivity & Visual Knowledge Benchmark Boundary
            </p>
          </div>
        </div>

        {/* Tab Navigation Pill Bar */}
        <div className="flex items-center bg-muted/40 p-1.5 rounded-xl border border-border shrink-0">
          <button
            onClick={() => setActiveTab('llm')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'llm'
                ? "bg-primary text-primary-foreground font-semibold shadow-xs"
                : "text-muted-foreground hover:text-foreground hover:bg-muted"
            }`}
          >
            <Cpu className="w-3.5 h-3.5" /> LLM Gateway
          </button>

          <button
            onClick={() => setActiveTab('visual')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'visual'
                ? "bg-primary text-primary-foreground font-semibold shadow-xs"
                : "text-muted-foreground hover:text-foreground hover:bg-muted"
            }`}
          >
            <ImageIcon className="w-3.5 h-3.5" /> Visual Gateway
          </button>

          <button
            onClick={() => setActiveTab('mcp')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'mcp'
                ? "bg-primary text-primary-foreground font-semibold shadow-xs"
                : "text-muted-foreground hover:text-foreground hover:bg-muted"
            }`}
          >
            <Server className="w-3.5 h-3.5" /> MCP Transport
          </button>

          <button
            onClick={() => setActiveTab('benchmark')}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-lg transition-colors ${
              activeTab === 'benchmark'
                ? "bg-primary text-primary-foreground font-semibold shadow-xs"
                : "text-muted-foreground hover:text-foreground hover:bg-muted"
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
