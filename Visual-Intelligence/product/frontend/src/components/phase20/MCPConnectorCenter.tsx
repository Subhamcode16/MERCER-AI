"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Server, ShieldAlert, Zap, AlertTriangle, CheckCircle2, Lock, Play, Plus, ToggleLeft, ToggleRight, X, Info, Link2, Activity } from "lucide-react";
import {
  fetchMCPServers,
  toggleMCPServer,
  registerCustomMCPServer,
  invokeMCPTool,
  MCPServerRegistrationDTO,
  MCPInvocationResultDTO
} from "@/lib/phase20Client";

export function MCPConnectorCenter() {
  const [mcpServers, setMcpServers] = useState<MCPServerRegistrationDTO[]>([]);
  const [selectedServerId, setSelectedServerId] = useState("mcp_fashion_trends");
  const [toolName, setToolName] = useState("read_fashion_trends");
  const [query, setQuery] = useState("Cyberpunk Y2K Minimalist");
  const [mcpResult, setMcpResult] = useState<MCPInvocationResultDTO | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);

  // New Connector Modal State
  const [newServerId, setNewServerId] = useState("");
  const [newProvider, setNewProvider] = useState("");
  const [newTransportUrl, setNewTransportUrl] = useState("");
  const [newCapabilities, setNewCapabilities] = useState("");
  const [newEnvironment, setNewEnvironment] = useState<'SANDBOX' | 'PRODUCTION'>("SANDBOX");
  const [modalError, setModalError] = useState<string | null>(null);

  useEffect(() => {
    fetchMCPServers().then(servers => setMcpServers(servers));
  }, []);

  const handleToggleServer = async (serverId: string, currentEnabled: boolean) => {
    try {
      const updatedList = await toggleMCPServer(serverId, !currentEnabled);
      setMcpServers(updatedList);
    } catch (e: any) {
      console.error(e);
    }
  };

  const handleAddCustomServer = async (e: React.FormEvent) => {
    e.preventDefault();
    setModalError(null);

    if (!newServerId.trim() || !newProvider.trim() || !newCapabilities.trim()) {
      setModalError("Please complete all required fields (Server ID, Provider, Capabilities).");
      return;
    }

    const capsArray = newCapabilities.split(",").map(c => c.trim()).filter(Boolean);

    try {
      const updatedList = await registerCustomMCPServer({
        server_id: newServerId.trim(),
        provider: newProvider.trim(),
        transport_url: newTransportUrl.trim() || undefined,
        approved_capabilities: capsArray,
        environment: newEnvironment,
        risk_class: "MEDIUM"
      });

      setMcpServers(updatedList);
      setSelectedServerId(newServerId.trim());
      setShowAddModal(false);
      
      // Reset Modal Fields
      setNewServerId("");
      setNewProvider("");
      setNewTransportUrl("");
      setNewCapabilities("");
    } catch (err: any) {
      setModalError(err.message || "Failed to register custom MCP connector.");
    }
  };

  const handleInvokeTool = async () => {
    setIsLoading(true);
    setErrorMsg(null);

    // Frontend validation for wildcard prohibition
    if (toolName === "admin_override" || toolName === "*") {
      setErrorMsg("MCP Policy Error: Wildcard capability '*' or 'admin_override' is strictly prohibited!");
      setIsLoading(false);
      return;
    }

    try {
      const res = await invokeMCPTool(selectedServerId, toolName, query);
      setMcpResult(res);
    } catch (e: any) {
      setErrorMsg(e.message || "MCP Tool Invocation Failed");
    } finally {
      setIsLoading(false);
    }
  };

  const activeServer = mcpServers.find(s => s.server_id === selectedServerId);

  return (
    <div className="flex flex-col gap-6 w-full text-zinc-100">
      {/* Top MCP Server Registration Table & Switch Board */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 flex flex-col gap-5 shadow-2xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-zinc-800 pb-4">
          <div className="flex items-center gap-3">
            <Server className="w-5 h-5 text-purple-400" />
            <div>
              <h3 className="text-base font-semibold text-white">Dedicated MCP Connectors Management</h3>
              <p className="text-xs text-zinc-400">Toggle active MCP capability transport connectors on/off or register custom MCP endpoints.</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono px-3 py-1 bg-purple-500/10 text-purple-300 rounded-full border border-purple-500/30 shrink-0">
              TRANSPORT ONLY (NO AUTHORITY)
            </span>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-1.5 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-medium transition-colors shadow-lg shrink-0"
            >
              <Plus className="w-4 h-4" />
              Add Custom MCP Connector
            </button>
          </div>
        </div>

        {/* MCP Connectors Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase">
                <th className="pb-3">Status Switch</th>
                <th className="pb-3">Server ID</th>
                <th className="pb-3">Provider</th>
                <th className="pb-3">Approved Capabilities</th>
                <th className="pb-3">Transport URL</th>
                <th className="pb-3">Risk Class</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/50">
              {mcpServers.map((server) => (
                <tr key={server.server_id} className={`hover:bg-zinc-800/30 transition-colors ${!server.enabled ? 'opacity-60' : ''}`}>
                  <td className="py-3.5">
                    <button
                      onClick={() => handleToggleServer(server.server_id, server.enabled)}
                      className="flex items-center gap-2 text-xs font-semibold focus:outline-none"
                    >
                      {server.enabled ? (
                        <ToggleRight className="w-6 h-6 text-emerald-400" />
                      ) : (
                        <ToggleLeft className="w-6 h-6 text-zinc-600" />
                      )}
                      <span className={server.enabled ? "text-emerald-400 font-bold" : "text-zinc-500"}>
                        {server.enabled ? "ENABLED" : "DISABLED"}
                      </span>
                    </button>
                  </td>
                  <td className="py-3.5 font-semibold text-white">{server.server_id}</td>
                  <td className="py-3.5 text-zinc-400">{server.provider}</td>
                  <td className="py-3.5 text-emerald-400 max-w-xs truncate">
                    {server.approved_capabilities.join(", ")}
                  </td>
                  <td className="py-3.5 text-zinc-400 max-w-xs truncate flex items-center gap-1">
                    <Link2 className="w-3.5 h-3.5 text-zinc-500 shrink-0" />
                    <span className="truncate">{server.transport_url || "Default Endpoint"}</span>
                  </td>
                  <td className="py-3.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      server.risk_class === 'LOW' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                    }`}>
                      {server.risk_class}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Tool Execution Surface */}
      <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 flex flex-col gap-5 shadow-2xl">
        <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
          <div className="flex items-center gap-3">
            <Zap className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-semibold text-white">Controlled MCP Tool Invocation Interface</h3>
          </div>
          {activeServer && (
            <span className={`text-xs font-mono px-3 py-1 rounded-full border ${
              activeServer.enabled ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30' : 'bg-rose-500/10 text-rose-300 border-rose-500/30'
            }`}>
              Server {activeServer.enabled ? 'ACTIVE & READY' : 'DISABLED'}
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Target MCP Server</label>
            <select
              value={selectedServerId}
              onChange={(e) => {
                setSelectedServerId(e.target.value);
                const s = mcpServers.find(srv => srv.server_id === e.target.value);
                if (s && s.approved_capabilities.length > 0) {
                  setToolName(s.approved_capabilities[0]);
                }
              }}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            >
              {mcpServers.map(s => (
                <option key={s.server_id} value={s.server_id}>
                  {s.server_id} ({s.enabled ? 'Enabled' : 'Disabled'})
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Tool Capability</label>
            <select
              value={toolName}
              onChange={(e) => setToolName(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            >
              {activeServer?.approved_capabilities.map(cap => (
                <option key={cap} value={cap}>{cap} (Approved)</option>
              ))}
              <option value="admin_override">admin_override (PROHIBITED WILDCARD)</option>
            </select>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Query Argument</label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-2.5 focus:outline-none focus:border-[#E1D4C0]"
            />
          </div>
        </div>

        {errorMsg && (
          <div className="bg-rose-950/50 border border-rose-800 text-rose-300 p-3 rounded-lg text-xs font-mono flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <div className="flex justify-end">
          <button
            onClick={handleInvokeTool}
            disabled={isLoading || (activeServer && !activeServer.enabled)}
            className="flex items-center gap-2 px-6 py-2.5 bg-[#E1D4C0] hover:bg-white text-black font-medium text-sm rounded-lg transition-colors shadow-lg disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-current" />
            {isLoading ? "Invoking MCP Transport Tool..." : "Invoke MCP Tool"}
          </button>
        </div>

        {/* MCP Output with Trust Classification Badge */}
        {mcpResult && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 bg-zinc-950 border border-zinc-800 rounded-xl p-5 flex flex-col gap-4"
          >
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded-full text-xs font-mono font-semibold flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  {mcpResult.trust_classification}
                </span>
              </div>
              <span className="text-xs font-mono text-zinc-500">Latency: {mcpResult.latency_ms.toFixed(1)} ms</span>
            </div>

            <pre className="text-xs font-mono text-zinc-300 bg-zinc-900 p-4 rounded-lg overflow-x-auto border border-zinc-800">
              {JSON.stringify(mcpResult.sanitized_output, null, 2)}
            </pre>
          </motion.div>
        )}
      </div>

      {/* Add Custom MCP Connector Modal */}
      <AnimatePresence>
        {showAddModal && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-zinc-900 border border-zinc-800 max-w-md w-full rounded-xl p-6 flex flex-col gap-5 shadow-2xl"
            >
              <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                <div className="flex items-center gap-2 text-white font-semibold">
                  <Plus className="w-4 h-4 text-purple-400" />
                  <span>Add Custom MCP Connector</span>
                </div>
                <button
                  onClick={() => setShowAddModal(false)}
                  className="text-zinc-400 hover:text-white"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <form onSubmit={handleAddCustomServer} className="flex flex-col gap-4">
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-mono text-zinc-400">Server ID *</label>
                  <input
                    type="text"
                    placeholder="e.g. mcp_custom_analytics"
                    value={newServerId}
                    onChange={(e) => setNewServerId(e.target.value)}
                    className="bg-zinc-950 border border-zinc-800 text-xs font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-mono text-zinc-400">Provider Name *</label>
                  <input
                    type="text"
                    placeholder="e.g. Custom Analytics Inc"
                    value={newProvider}
                    onChange={(e) => setNewProvider(e.target.value)}
                    className="bg-zinc-950 border border-zinc-800 text-xs font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-mono text-zinc-400">Transport URL Endpoint</label>
                  <input
                    type="text"
                    placeholder="e.g. https://mcp.custom.io/v1 or http://localhost:8080/mcp"
                    value={newTransportUrl}
                    onChange={(e) => setNewTransportUrl(e.target.value)}
                    className="bg-zinc-950 border border-zinc-800 text-xs font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-mono text-zinc-400">Approved Capabilities (comma-separated) *</label>
                  <input
                    type="text"
                    placeholder="e.g. read_market_feed, search_pricing"
                    value={newCapabilities}
                    onChange={(e) => setNewCapabilities(e.target.value)}
                    className="bg-zinc-950 border border-zinc-800 text-xs font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-mono text-zinc-400">Environment</label>
                  <select
                    value={newEnvironment}
                    onChange={(e: any) => setNewEnvironment(e.target.value)}
                    className="bg-zinc-950 border border-zinc-800 text-xs font-mono text-white rounded-lg p-2.5 focus:outline-none focus:border-purple-500"
                  >
                    <option value="SANDBOX">SANDBOX</option>
                    <option value="PRODUCTION">PRODUCTION</option>
                  </select>
                </div>

                <div className="bg-purple-950/40 border border-purple-800/50 p-3 rounded-lg text-[11px] font-mono text-purple-300 flex items-start gap-2">
                  <Info className="w-4 h-4 shrink-0 text-purple-400 mt-0.5" />
                  <span>Wildcard capabilities ('*' or 'admin') are strictly rejected by the MCP Capability Policy Validator.</span>
                </div>

                {modalError && (
                  <div className="bg-rose-950/50 border border-rose-800 text-rose-300 p-2.5 rounded-lg text-xs font-mono">
                    {modalError}
                  </div>
                )}

                <div className="flex items-center justify-end gap-3 mt-2">
                  <button
                    type="button"
                    onClick={() => setShowAddModal(false)}
                    className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-xs"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-medium shadow-lg"
                  >
                    Register Connector
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
