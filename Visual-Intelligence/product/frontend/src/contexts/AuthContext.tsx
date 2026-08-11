"use client";

import React, { createContext, useContext, useState, useEffect, useRef } from "react";
import { supabase } from "@/lib/supabase";
import { apiFetch, ApiError } from "@/lib/api";
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
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Guard against Supabase's double-fire on init
  // (initialize + _emitInitialSession both trigger onAuthStateChange)
  const profileLoadingRef = useRef(false);

  useEffect(() => {
    if (toastMessage) {
      const timer = setTimeout(() => setToastMessage(null), 4000);
      return () => clearTimeout(timer);
    }
  }, [toastMessage]);

  const loadProfile = async () => {
    // Prevent concurrent calls — Supabase fires two auth events on startup
    if (profileLoadingRef.current) return;
    profileLoadingRef.current = true;

    try {
      let userData;
      try {
        userData = await apiFetch("/users/me");
      } catch (err: unknown) {
        const apiErr = err instanceof ApiError ? err : null;
        const status = apiErr?.status ?? 0;
        const msg = apiErr?.message || (err instanceof Error ? err.message : "");

        // 500/502/503/504 → backend infra issue — apiFetch already retried 3×.
        // Do NOT clear the session; the user is still authenticated.
        if (status >= 500 || status === 0) {
          console.warn("[AuthContext] Backend temporarily unavailable, keeping session intact.", msg);
          return; // leave profile as-is (null on first load)
        }

        // 403 → user authenticated in Supabase but not provisioned in MongoDB
        const needsProvision =
          status === 403 ||
          msg.includes("not found") ||
          msg.includes("provision") ||
          msg.includes("account not found");

        if (needsProvision) {
          const marketingPref = localStorage.getItem("atelier_pending_marketing") === "true";
          await apiFetch("/auth/provision", {
            method: "POST",
            body: JSON.stringify({ receive_marketing: marketingPref }),
          }).catch((e: unknown) => console.warn("Auto-provision non-fatal error:", e));
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
        role: userData.role || "user",
      });
    } catch (error: unknown) {
      const apiErr = error instanceof ApiError ? error : null;
      const status = apiErr?.status ?? 0;
      const errMsg = apiErr?.message || (error instanceof Error ? error.message : "");

      // Infra error (already retried) — keep session alive, log as warning
      if (status >= 500 || status === 0) {
        console.warn("[AuthContext] Profile load failed (infra), session retained:", errMsg);
        return;
      }

      // 401 / expired token → sign out and prompt re-login
      const isAuthFailure =
        status === 401 ||
        errMsg.includes("Invalid or expired") ||
        errMsg.includes("expired");

      if (isAuthFailure) {
        setToastMessage("Session expired. Please log in again.");
        await supabase.auth.signOut().catch(console.error);
        setSession(null);
      } else {
        console.error("[AuthContext] Failed to load user profile:", error);
      }

      setProfile(null);
    } finally {
      profileLoadingRef.current = false;
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

      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-[9999] bg-[#0D0D0D]/95 backdrop-blur-md border border-white/10 px-6 py-3.5 rounded shadow-2xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <div className="w-1.5 h-1.5 rounded-full bg-[#E1D4C0]" />
          <span className="text-[11px] font-sans tracking-[0.1em] uppercase text-white/90">{toastMessage}</span>
        </div>
      )}
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
