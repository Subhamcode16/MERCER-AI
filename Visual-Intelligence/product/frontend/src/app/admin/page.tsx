"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { apiFetch } from "@/lib/api";
import Link from "next/link";
import { 
  Users, 
  Coins, 
  Mail, 
  ShieldAlert, 
  ArrowLeft, 
  Search, 
  Loader2, 
  Sparkles, 
  RefreshCw,
  UserCheck
} from "lucide-react";

interface AdminStats {
  total_users: number;
  tier_counts: {
    free: number;
    starter: number;
    pro: number;
    studio: number;
  };
  total_credits: number;
  opt_in_rate: number;
  recent_transactions: Array<{
    id: string;
    user_email: string;
    type: string;
    amount: number;
    source: string | null;
    created_at: string | null;
  }>;
  users: Array<{
    id: string;
    email: string;
    tier: string;
    credit_balance: number;
    email_verified: boolean;
    role: string;
    receive_marketing: boolean;
    created_at: string | null;
  }>;
  resend_stats: {
    configured: boolean;
    contacts_count: number;
    audience_name: string;
    error: string | null;
  };
}

export default function AdminCRM() {
  const router = useRouter();
  const { session, profile, isLoading } = useAuth();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  const fetchStats = async () => {
    try {
      setError(null);
      const data = await apiFetch("/api/admin/stats");
      setStats(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to fetch administrative data.");
    } finally {
      setLoadingStats(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    // Redirect if loaded and not an admin
    if (!isLoading) {
      if (!session || !profile || profile.role !== "admin") {
        router.push("/studio");
      } else {
        fetchStats();
      }
    }
  }, [session, profile, isLoading, router]);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchStats();
  };

  if (isLoading || loadingStats) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex flex-col items-center justify-center gap-4 text-white">
        <Loader2 className="w-8 h-8 text-[#E1D4C0] animate-spin" />
        <p className="text-[10px] tracking-[0.25em] uppercase text-zinc-500">Loading Mercer AI CRM</p>
      </div>
    );
  }

  if (profile?.role !== "admin") {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex flex-col items-center justify-center gap-4 text-white">
        <ShieldAlert className="w-12 h-12 text-red-500/80" />
        <p className="text-[10px] tracking-[0.25em] uppercase text-zinc-500">Access Denied. Admins Only.</p>
      </div>
    );
  }

  // Filter users based on query
  const filteredUsers = stats?.users.filter(u => 
    u.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.id.includes(searchQuery) ||
    u.tier.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  return (
    <div className="min-h-screen bg-[#080808] text-zinc-300 font-sans font-light p-8 md:p-16">
      
      {/* Header */}
      <header className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-6 mb-16 pb-8 border-b border-white/5">
        <div>
          <div className="flex items-center gap-3 mb-3">
            <span className="text-[9px] tracking-[0.2em] uppercase bg-[#E1D4C0]/10 text-[#E1D4C0] px-2.5 py-1 rounded border border-[#E1D4C0]/20 font-medium">Mercer AI Command Center</span>
            {refreshing && <span className="text-[9px] text-zinc-500">Syncing...</span>}
          </div>
          <h1 className="text-4xl font-serif text-white tracking-wide">CRM & Audience Intelligence</h1>
          <p className="text-zinc-500 text-sm mt-1">Cross-platform statistics for MongoDB, Supabase, and Resend.</p>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={handleRefresh}
            disabled={refreshing}
            className="p-3 bg-white/5 hover:bg-white/10 rounded-full border border-white/10 text-white transition-colors disabled:opacity-50"
            title="Force sync live credentials"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} />
          </button>
          <Link 
            href="/studio"
            className="flex items-center gap-2 px-5 py-3 bg-[#E1D4C0] hover:bg-white text-black font-semibold text-xs tracking-wider uppercase rounded-full transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Enter Studio
          </Link>
        </div>
      </header>

      {error && (
        <div className="max-w-7xl mx-auto mb-10 p-5 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-sm">
          {error}
        </div>
      )}

      {stats && (
        <div className="max-w-7xl mx-auto space-y-16">
          
          {/* KPI Dashboard Ribbon */}
          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Widget 1 */}
            <div className="bg-gradient-to-b from-[#111] to-[#0c0c0c] border border-white/5 p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                <Users className="w-24 h-24 text-white" />
              </div>
              <p className="text-[10px] tracking-[0.2em] uppercase text-zinc-500 mb-2">Total Workspace Accounts</p>
              <h3 className="text-3xl font-serif text-white mb-4">{stats.total_users}</h3>
              <div className="flex gap-3 text-[11px] text-zinc-500">
                <span>Free: {stats.tier_counts.free}</span>
                <span>•</span>
                <span>Pro/Studio: {(stats.tier_counts.pro || 0) + (stats.tier_counts.studio || 0) + (stats.tier_counts.starter || 0)}</span>
              </div>
            </div>

            {/* Widget 2 */}
            <div className="bg-gradient-to-b from-[#111] to-[#0c0c0c] border border-white/5 p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                <Coins className="w-24 h-24 text-white" />
              </div>
              <p className="text-[10px] tracking-[0.2em] uppercase text-zinc-500 mb-2">Credits in Circulation</p>
              <h3 className="text-3xl font-serif text-white mb-4">{stats.total_credits}</h3>
              <p className="text-[11px] text-[#E1D4C0] font-medium uppercase tracking-widest">Mercer AI Ledger Active</p>
            </div>

            {/* Widget 3 */}
            <div className="bg-gradient-to-b from-[#111] to-[#0c0c0c] border border-white/5 p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                <Mail className="w-24 h-24 text-white" />
              </div>
              <p className="text-[10px] tracking-[0.2em] uppercase text-zinc-500 mb-2">Resend Audience Size</p>
              <h3 className="text-3xl font-serif text-white mb-4">
                {stats.resend_stats.configured ? stats.resend_stats.contacts_count : "Not Set"}
              </h3>
              <p className="text-[11px] text-zinc-500">
                {stats.resend_stats.configured ? `Audience: ${stats.resend_stats.audience_name}` : "Check Resend env credentials"}
              </p>
            </div>

            {/* Widget 4 */}
            <div className="bg-gradient-to-b from-[#111] to-[#0c0c0c] border border-white/5 p-6 rounded-2xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
                <Sparkles className="w-24 h-24 text-white" />
              </div>
              <p className="text-[10px] tracking-[0.2em] uppercase text-zinc-500 mb-2">Marketing Opt-in Rate</p>
              <h3 className="text-3xl font-serif text-white mb-4">{stats.opt_in_rate}%</h3>
              <p className="text-[11px] text-zinc-500">Percentage of newsletter consent</p>
            </div>

          </section>

          {/* User Directory Table */}
          <section className="bg-[#0C0C0C] border border-white/5 rounded-2xl p-6 md:p-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
              <div>
                <h2 className="text-xl font-serif text-white tracking-wide">Registered Accounts</h2>
                <p className="text-zinc-500 text-xs mt-1">Database view of MongoDB documents synced with Supabase.</p>
              </div>

              {/* Search Bar */}
              <div className="relative max-w-sm w-full">
                <Search className="w-4 h-4 text-zinc-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input 
                  type="text"
                  placeholder="Filter by email, ID or tier..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-white/5 border border-white/10 rounded-full py-2.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-white/30 transition-colors"
                />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-[10px] uppercase tracking-widest text-zinc-500">
                    <th className="pb-4 font-semibold">User Email</th>
                    <th className="pb-4 font-semibold">Account ID (Supabase UUID)</th>
                    <th className="pb-4 font-semibold">Tier</th>
                    <th className="pb-4 font-semibold">Credit Balance</th>
                    <th className="pb-4 font-semibold">Consent</th>
                    <th className="pb-4 font-semibold">Verified</th>
                    <th className="pb-4 font-semibold">Role</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {filteredUsers.map((u) => (
                    <tr key={u.id} className="hover:bg-white/[0.02] transition-colors">
                      <td className="py-4 text-white font-medium">{u.email}</td>
                      <td className="py-4 text-xs font-mono text-zinc-600 select-all">{u.id}</td>
                      <td className="py-4">
                        <span className={`text-[10px] uppercase tracking-widest px-2.5 py-1 rounded font-medium ${
                          u.tier === "studio" ? "bg-amber-500/10 text-amber-400 border border-amber-500/20" :
                          u.tier === "pro" ? "bg-purple-500/10 text-purple-400 border border-purple-500/20" :
                          u.tier === "starter" ? "bg-blue-500/10 text-blue-400 border border-blue-500/20" :
                          "bg-zinc-800 text-zinc-400"
                        }`}>
                          {u.tier}
                        </span>
                      </td>
                      <td className="py-4 font-semibold text-white">{u.credit_balance}</td>
                      <td className="py-4">
                        {u.receive_marketing ? (
                          <span className="text-[10px] uppercase tracking-wider text-emerald-400 font-semibold bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">Opt-In</span>
                        ) : (
                          <span className="text-[10px] uppercase tracking-wider text-zinc-600 font-normal">None</span>
                        )}
                      </td>
                      <td className="py-4">
                        {u.email_verified ? (
                          <span className="text-emerald-400 font-medium">Yes</span>
                        ) : (
                          <span className="text-zinc-600">Pending</span>
                        )}
                      </td>
                      <td className="py-4">
                        {u.role === "admin" ? (
                          <span className="text-[10px] font-semibold text-amber-400 uppercase tracking-widest flex items-center gap-1">
                            <UserCheck className="w-3.5 h-3.5" />
                            Admin
                          </span>
                        ) : (
                          <span className="text-zinc-500">User</span>
                        )}
                      </td>
                    </tr>
                  ))}
                  {filteredUsers.length === 0 && (
                    <tr>
                      <td colSpan={7} className="py-8 text-center text-zinc-500 text-xs">
                        No matches found for your filter query.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          {/* Ledger History (Recent Transactions) & Resend Log */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Credit Transaction Ledger */}
            <section className="lg:col-span-2 bg-[#0C0C0C] border border-white/5 rounded-2xl p-6 md:p-8">
              <h2 className="text-xl font-serif text-white tracking-wide mb-2">Ledger Transaction History</h2>
              <p className="text-zinc-500 text-xs mb-8">Auditing the immutable credit allotments, generation reservations, and system refunds.</p>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm border-collapse">
                  <thead>
                    <tr className="border-b border-white/10 text-[10px] uppercase tracking-widest text-zinc-500">
                      <th className="pb-4 font-semibold">User</th>
                      <th className="pb-4 font-semibold">Operation</th>
                      <th className="pb-4 font-semibold">Amount</th>
                      <th className="pb-4 font-semibold">Source / Event</th>
                      <th className="pb-4 font-semibold">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5 text-zinc-400">
                    {stats.recent_transactions.map((tx) => (
                      <tr key={tx.id} className="hover:bg-white/[0.01] transition-colors">
                        <td className="py-3 text-xs text-white max-w-[150px] truncate" title={tx.user_email}>
                          {tx.user_email}
                        </td>
                        <td className="py-3 text-xs">
                          <span className={`text-[10px] uppercase tracking-widest font-semibold px-2 py-0.5 rounded ${
                            tx.type === "grant" ? "bg-emerald-500/10 text-emerald-400" :
                            tx.type === "refund" ? "bg-blue-500/10 text-blue-400" :
                            "bg-red-500/10 text-red-400"
                          }`}>
                            {tx.type}
                          </span>
                        </td>
                        <td className="py-3 font-semibold text-white">
                          {tx.type === "grant" || tx.type === "refund" ? "+" : "-"}{tx.amount}
                        </td>
                        <td className="py-3 text-xs text-zinc-500 truncate max-w-[150px]">{tx.source || "System"}</td>
                        <td className="py-3 text-xs text-zinc-600 font-mono">
                          {tx.created_at ? new Date(tx.created_at).toLocaleString() : "Unknown"}
                        </td>
                      </tr>
                    ))}
                    {stats.recent_transactions.length === 0 && (
                      <tr>
                        <td colSpan={5} className="py-8 text-center text-zinc-500 text-xs">
                          No recent transactions recorded in ledger.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>

            {/* Resend API Status Card */}
            <section className="bg-[#0C0C0C] border border-white/5 rounded-2xl p-6 md:p-8 flex flex-col justify-between">
              <div>
                <h2 className="text-xl font-serif text-white tracking-wide mb-2">Resend Email Integration</h2>
                <p className="text-zinc-500 text-xs mb-8">Auditing the marketing subscriber list status.</p>

                <div className="space-y-6">
                  <div>
                    <span className="block text-[10px] uppercase tracking-widest text-zinc-500 mb-1">Integration Status</span>
                    {stats.resend_stats.configured ? (
                      <span className="text-emerald-400 font-semibold flex items-center gap-1.5 text-sm">
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        Active Connection
                      </span>
                    ) : (
                      <span className="text-zinc-500 flex items-center gap-1.5 text-sm">
                        <span className="w-2 h-2 rounded-full bg-zinc-600"></span>
                        Inactive (No Credentials)
                      </span>
                    )}
                  </div>

                  <div>
                    <span className="block text-[10px] uppercase tracking-widest text-zinc-500 mb-1">Mailing Audience</span>
                    <span className="text-white text-sm font-medium">{stats.resend_stats.audience_name}</span>
                  </div>

                  {stats.resend_stats.error && (
                    <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-xs font-mono break-words leading-relaxed">
                      <strong>Resend Connection Error:</strong><br/>
                      {stats.resend_stats.error}
                    </div>
                  )}
                </div>
              </div>

              <div className="pt-6 border-t border-white/5 mt-8">
                <span className="block text-[10px] tracking-wide text-zinc-600">
                  Contact syncing triggers automatically whenever a new signup consents to marketing emails.
                </span>
              </div>
            </section>

          </div>

        </div>
      )}
    </div>
  );
}
