"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { supabase } from "@/lib/supabase";
import { apiFetch } from "@/lib/api";
import { AuthModal } from "@/components/AuthModal";

interface UserProfile {
  email?: string;
  tier: string;
  credit_balance: number;
  max_credits: number;
  role: string;
}

interface AuthContextType {
  session: any | null;
  profile: UserProfile | null;
  isLoading: boolean;
  openAuthModal: (view?: "login" | "signup") => void;
  closeAuthModal: () => void;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<any | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalView, setModalView] = useState<"login" | "signup">("login");

  const loadProfile = async () => {
    try {
      let userData;
      try {
        userData = await apiFetch("/users/me");
      } catch (err: any) {
        if (err.message.includes("not found") || err.message.includes("provision") || err.message.includes("Not authenticated")) {
          // Auto-provision if missing from MongoDB (e.g. email link login)
          const marketingPref = localStorage.getItem("atelier_pending_marketing") === "true";
          await apiFetch("/auth/provision", {
            method: "POST",
            body: JSON.stringify({ receive_marketing: marketingPref })
          }).catch(e => console.warn("Auto-provision non-fatal error:", e));
          localStorage.removeItem("atelier_pending_marketing");
          
          userData = await apiFetch("/users/me");
        } else {
          throw err;
        }
      }
      
      setProfile({
        email: userData.email,
        tier: userData.tier,
        credit_balance: userData.credit_balance,
        max_credits: userData.max_credits || 100,
        role: userData.role || "user"
      });
    } catch (error) {
      console.error("Failed to load user profile", error);
      setProfile(null);
    }
  };

  useEffect(() => {
    const checkAuth = async () => {
      const { data: { session: currentSession } } = await supabase.auth.getSession();
      setSession(currentSession);
      
      if (currentSession) {
        await loadProfile();
      } else {
        setProfile(null);
      }
      setIsLoading(false);
    };

    checkAuth();

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, currentSession) => {
      setSession(currentSession);
      if (currentSession) {
        await loadProfile();
      } else {
        setProfile(null);
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const openAuthModal = (view: "login" | "signup" = "login") => {
    setModalView(view);
    setIsModalOpen(true);
  };

  const closeAuthModal = () => {
    setIsModalOpen(false);
  };

  const logout = async () => {
    await supabase.auth.signOut();
    setSession(null);
    setProfile(null);
  };

  return (
    <AuthContext.Provider value={{
      session,
      profile,
      isLoading,
      openAuthModal,
      closeAuthModal,
      logout,
      refreshProfile: loadProfile
    }}>
      {children}
      
      <AuthModal 
        isOpen={isModalOpen} 
        onClose={closeAuthModal} 
        initialView={modalView}
        onSuccess={() => {
          closeAuthModal();
          loadProfile(); // Profile will also be loaded by onAuthStateChange, but this ensures immediacy
        }}
      />
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
