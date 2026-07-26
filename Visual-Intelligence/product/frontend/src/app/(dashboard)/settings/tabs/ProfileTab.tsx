"use client";

import React, { useState } from "react";
import { User, Mail, Shield, Camera } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function ProfileTab() {
  const { session, profile } = useAuth();
  const user = session?.user;
  const [name, setName] = useState(user?.user_metadata?.full_name || profile?.email?.split('@')[0] || "Antigravity Director");
  
  // Fake update state for UI UX
  const [isUpdating, setIsUpdating] = useState(false);

  const handleUpdate = () => {
    setIsUpdating(true);
    setTimeout(() => setIsUpdating(false), 800);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Avatar Section */}
      <div className="flex items-center gap-6">
        <div className="relative group cursor-pointer">
          <div className="w-24 h-24 rounded-full bg-[#111111] border border-white/10 flex items-center justify-center overflow-hidden">
             {/* Initials Placeholder */}
             <span className="text-3xl font-bold tracking-widest text-[#E1D4C0]">
               {name.substring(0, 2).toUpperCase()}
             </span>
          </div>
          <div className="absolute inset-0 bg-black/60 rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
            <Camera className="text-white/80" size={24} />
          </div>
        </div>
        <div>
          <h3 className="text-xl font-semibold text-white/90">Profile Picture</h3>
          <p className="text-xs text-white/40 mt-1">PNG, JPG or GIF under 5MB.</p>
        </div>
      </div>

      <div className="h-[1px] w-full bg-white/5" />

      {/* Form Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl">
        {/* Full Name */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-white/60 tracking-wider uppercase flex items-center gap-2">
            <User size={12} />
            Full Name
          </label>
          <input 
            type="text" 
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-[#111111] border border-white/10 rounded-lg px-4 py-3 text-sm text-white focus:outline-none focus:border-[#E1D4C0]/50 focus:ring-1 focus:ring-[#E1D4C0]/20 transition-all placeholder:text-white/20"
            placeholder="John Doe"
          />
        </div>

        {/* Email Address */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-white/60 tracking-wider uppercase flex items-center gap-2">
            <Mail size={12} />
            Email Address
          </label>
          <input 
            type="email" 
            value={user?.email || "user@example.com"}
            disabled
            className="w-full bg-[#111111]/50 border border-white/5 rounded-lg px-4 py-3 text-sm text-white/50 cursor-not-allowed"
          />
          <p className="text-[10px] text-white/30">Email cannot be changed directly.</p>
        </div>

        {/* Role */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-white/60 tracking-wider uppercase flex items-center gap-2">
            <Shield size={12} />
            Account Role
          </label>
          <div className="w-full bg-[#111111] border border-white/10 rounded-lg px-4 py-3 flex items-center justify-between">
            <span className="text-sm text-white/80 capitalize">{profile?.role || "User"}</span>
            <span className="text-[10px] bg-[#E1D4C0]/10 text-[#E1D4C0] px-2 py-0.5 rounded-full font-semibold tracking-wider">VERIFIED</span>
          </div>
        </div>
      </div>

      <div className="pt-6">
        <button 
          onClick={handleUpdate}
          disabled={isUpdating}
          className="bg-[#E1D4C0] hover:bg-white text-black text-sm font-bold px-6 py-3 rounded-lg transition-all active:scale-[0.98] disabled:opacity-70 flex items-center justify-center min-w-[140px]"
        >
          {isUpdating ? (
            <div className="w-5 h-5 border-2 border-black/20 border-t-black rounded-full animate-spin" />
          ) : (
            "Save Changes"
          )}
        </button>
      </div>

    </div>
  );
}
