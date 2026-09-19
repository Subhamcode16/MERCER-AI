"use client";

import React, { useState } from "react";
import { User, Mail, Shield, Camera } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/lib/supabase";

export default function ProfileTab() {
  const { session, profile } = useAuth();
  const user = session?.user;
  const [name, setName] = useState(user?.user_metadata?.full_name || profile?.email?.split('@')[0] || "Antigravity Director");
  
  // Fake update state for UI UX
  const [isUpdating, setIsUpdating] = useState(false);

  const handleUpdate = async () => {
    setIsUpdating(true);
    try {
      const { error } = await supabase.auth.updateUser({
        data: { full_name: name }
      });
      if (error) throw error;
    } catch (err) {
      console.error("Failed to update profile name:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Avatar Section */}
      <div className="flex items-center gap-6">
        <div className="relative group cursor-pointer">
          <div className="w-24 h-24 rounded-full bg-card border border-border flex items-center justify-center overflow-hidden shadow-xs">
             {/* Initials Placeholder */}
             <span className="text-3xl font-bold tracking-widest text-primary">
               {name.substring(0, 2).toUpperCase()}
             </span>
          </div>
          <div className="absolute inset-0 bg-black/60 rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
            <Camera className="text-white/80" size={24} />
          </div>
        </div>
        <div>
          <h3 className="text-xl font-semibold text-foreground">Profile Picture</h3>
          <p className="text-xs text-muted-foreground mt-1">PNG, JPG or GIF under 5MB.</p>
        </div>
      </div>

      <div className="h-[1px] w-full bg-border" />

      {/* Form Fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl">
        {/* Full Name */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-muted-foreground tracking-wider uppercase flex items-center gap-2">
            <User size={12} />
            Full Name
          </label>
          <input 
            type="text" 
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-card border border-border rounded-lg px-4 py-3 text-sm text-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all placeholder:text-muted-foreground/40 shadow-xs"
            placeholder="John Doe"
          />
        </div>

        {/* Email Address */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-muted-foreground tracking-wider uppercase flex items-center gap-2">
            <Mail size={12} />
            Email Address
          </label>
          <input 
            type="email" 
            value={user?.email || "user@example.com"}
            disabled
            className="w-full bg-muted/50 border border-border rounded-lg px-4 py-3 text-sm text-muted-foreground cursor-not-allowed"
          />
          <p className="text-[10px] text-muted-foreground/70">Email cannot be changed directly.</p>
        </div>

        {/* Role */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-muted-foreground tracking-wider uppercase flex items-center gap-2">
            <Shield size={12} />
            Account Role
          </label>
          <div className="w-full bg-card border border-border rounded-lg px-4 py-3 flex items-center justify-between shadow-xs">
            <span className="text-sm text-foreground capitalize">{profile?.role || "User"}</span>
            <span className="text-[10px] bg-primary/10 text-primary border border-primary/20 px-2 py-0.5 rounded-full font-semibold tracking-wider">VERIFIED</span>
          </div>
        </div>
      </div>

      <div className="pt-6">
        <button 
          onClick={handleUpdate}
          disabled={isUpdating}
          className="bg-primary hover:bg-primary/90 text-primary-foreground text-sm font-bold px-6 py-3 rounded-lg transition-all active:scale-[0.98] disabled:opacity-70 flex items-center justify-center min-w-[140px] shadow-sm"
        >
          {isUpdating ? (
            <div className="w-5 h-5 border-2 border-primary-foreground/20 border-t-primary-foreground rounded-full animate-spin" />
          ) : (
            "Save Changes"
          )}
        </button>
      </div>

    </div>
  );
}
