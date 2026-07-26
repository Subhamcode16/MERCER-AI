"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import { apiFetch } from "@/lib/api";
import { AuthSlider } from "@/components/AuthSlider";
import { Eye, EyeOff } from "lucide-react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialView?: "login" | "signup";
  onSuccess: () => void;
}

export function AuthModal({ isOpen, onClose, initialView = "login", onSuccess }: AuthModalProps) {
  const [view, setView] = useState<"login" | "signup">(initialView);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [receiveMarketing, setReceiveMarketing] = useState(false);

  const handleSwitchView = (newView: "login" | "signup") => {
    setView(newView);
    setError(null);
    setSuccessMessage(null);
  };

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      if (view === "signup") {
        if (password !== confirmPassword) {
          setError("Passwords do not match");
          setLoading(false);
          return;
        }

        const { data, error: authError } = await supabase.auth.signUp({
          email,
          password,
        });

        if (authError) throw authError;

        if (data.session) {
          await apiFetch("/auth/provision", {
            method: "POST",
            headers: {
              Authorization: `Bearer ${data.session.access_token}`
            },
            body: JSON.stringify({ receive_marketing: receiveMarketing })
          });
          onSuccess();
        } else {
          // No session returned (means email verification is enabled by Supabase)
          // Store preference so it's applied when they click the email link
          localStorage.setItem("atelier_pending_marketing", receiveMarketing ? "true" : "false");
          setSuccessMessage("Confirmation email sent! Please check your email to verify your account, then log in.");
          setView("login");
          setPassword("");
          setConfirmPassword("");
        }
      } else {
        const { data, error: authError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (authError) throw authError;

        // Call /auth/provision on successful login to ensure user is in MongoDB
        await apiFetch("/auth/provision", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${data.session.access_token}`
          },
          body: JSON.stringify({ receive_marketing: receiveMarketing })
        });
        onSuccess();
      }
    } catch (err: any) {
      setError(err.message || `An error occurred during ${view}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[999] flex items-center justify-center p-4 sm:p-8">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal Container */}
      <div className="w-full max-w-5xl h-[650px] bg-[#0c0c0c] border border-white/10 rounded-[24px] flex overflow-hidden shadow-2xl relative z-10 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Left side: Image Slider */}
        <AuthSlider />

        {/* Right side: Form */}
        <div className="w-full lg:w-1/2 flex flex-col items-center justify-center p-8 sm:p-12 overflow-y-auto">
          <div className="w-full max-w-sm relative">
            
            {/* Close Button */}
            <button 
              onClick={onClose}
              className="absolute -top-4 -right-4 w-8 h-8 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-white/50 hover:text-white transition-colors"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>

            <div className="mb-10 text-center mt-4">
              <h2 className="text-3xl font-serif text-[#E1D4C0] mb-2">
                {view === "login" ? "Welcome Back" : "Create Account"}
              </h2>
              <p className="text-zinc-500 text-sm">
                {view === "login" ? "Enter the studio to resume your work." : "Join the creative intelligence engine."}
              </p>
            </div>

            {successMessage && (
              <div className="mb-6 p-4 border border-emerald-500/20 bg-emerald-500/10 text-emerald-400 text-sm rounded">
                {successMessage}
              </div>
            )}

            {error && (
              <div className="mb-6 p-4 border border-red-500/20 bg-red-500/10 text-red-400 text-sm rounded">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-[11px] uppercase tracking-widest text-zinc-500 mb-1">Email</label>
                <input 
                  type="email" 
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-transparent border-b border-white/10 py-2 text-[#E1D4C0] focus:outline-none focus:border-white/50 transition-colors text-sm"
                  placeholder="designer@mercerai.space"
                />
              </div>
              
              <div>
                <div className="flex items-center justify-between mb-1">
                   <label className="block text-[11px] uppercase tracking-widest text-zinc-500">Password</label>
                   {view === "login" && (
                     <a href="#" className="text-[11px] text-[#E1D4C0]/70 hover:text-[#E1D4C0] transition-colors">Recover Password?</a>
                   )}
                </div>
                <div className="relative w-full">
                  <input 
                    type={showPassword ? "text" : "password"} 
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-transparent border-b border-white/10 py-2 pr-10 text-[#E1D4C0] focus:outline-none focus:border-white/50 transition-colors text-sm"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-0 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-white transition-colors p-1"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              {view === "signup" && (
                <div>
                  <label className="block text-[11px] uppercase tracking-widest text-zinc-500 mb-1">Confirm Password</label>
                  <div className="relative w-full">
                    <input 
                      type={showPassword ? "text" : "password"} 
                      required
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      className="w-full bg-transparent border-b border-white/10 py-2 pr-10 text-[#E1D4C0] focus:outline-none focus:border-white/50 transition-colors text-sm"
                      placeholder="••••••••"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-0 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-white transition-colors p-1"
                    >
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>
              )}

              {view === "signup" && (
                <div className="pt-2 space-y-3">
                  <div className="flex items-start gap-2.5">
                    <input 
                      type="checkbox" 
                      id="acceptTerms"
                      checked={acceptTerms}
                      onChange={(e) => setAcceptTerms(e.target.checked)}
                      className="w-4 h-4 mt-0.5 bg-transparent border-white/20 rounded-sm accent-[#E1D4C0] focus:ring-1 focus:ring-[#E1D4C0]/50 cursor-pointer"
                    />
                    <label htmlFor="acceptTerms" className="text-[12px] text-zinc-400 cursor-pointer hover:text-zinc-300 transition-colors leading-snug">
                      I accept the <a href="#" className="underline hover:text-[#E1D4C0]">Terms of Service</a> & <a href="#" className="underline hover:text-[#E1D4C0]">Privacy Policy</a>
                    </label>
                  </div>

                  <div className="flex items-start gap-2.5">
                    <input 
                      type="checkbox" 
                      id="receiveMarketing"
                      checked={receiveMarketing}
                      onChange={(e) => setReceiveMarketing(e.target.checked)}
                      className="w-4 h-4 mt-0.5 bg-transparent border-white/20 rounded-sm accent-[#E1D4C0] focus:ring-1 focus:ring-[#E1D4C0]/50 cursor-pointer"
                    />
                    <label htmlFor="receiveMarketing" className="text-[12px] text-zinc-400 cursor-pointer hover:text-zinc-300 transition-colors leading-snug">
                      Send me creative updates, visual blueprints & newsletter (Optional)
                    </label>
                  </div>
                  
                  <button
                    type="button"
                    onClick={() => {
                      setAcceptTerms(true);
                      setReceiveMarketing(true);
                    }}
                    className="text-[10px] text-[#E1D4C0]/70 hover:text-[#E1D4C0] transition-colors block text-left pt-1 font-semibold tracking-widest uppercase hover:underline"
                  >
                    ⚡ Accept & Agree to All Settings
                  </button>
                </div>
              )}

              {view === "login" && (
                <div className="flex items-center gap-2 pt-2">
                  <input 
                    type="checkbox" 
                    id="rememberMe"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 bg-transparent border-white/20 rounded-sm accent-[#E1D4C0] focus:ring-1 focus:ring-[#E1D4C0]/50 cursor-pointer"
                  />
                  <label htmlFor="rememberMe" className="text-[13px] text-zinc-500 cursor-pointer hover:text-zinc-300 transition-colors">
                    Remember me
                  </label>
                </div>
              )}

              <button 
                type="submit" 
                disabled={loading || (view === "signup" && !acceptTerms)}
                className="w-full py-3.5 mt-8 bg-[#E1D4C0] rounded-full text-black font-medium text-xs tracking-widest uppercase hover:bg-white transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              >
                {loading ? "Authenticating..." : (view === "login" ? "Log In" : "Sign Up")}
              </button>
            </form>

            <div className="mt-8 flex items-center gap-4">
              <div className="h-px bg-white/10 flex-1"></div>
              <span className="text-[10px] uppercase tracking-widest text-zinc-600">OR</span>
              <div className="h-px bg-white/10 flex-1"></div>
            </div>

            <p className="mt-8 text-sm text-zinc-500 text-center">
              {view === "login" ? (
                <>New to Mercer AI? <button onClick={() => handleSwitchView("signup")} className="text-[#E1D4C0] hover:underline">Create an account</button></>
              ) : (
                <>Already have an account? <button onClick={() => handleSwitchView("login")} className="text-[#E1D4C0] hover:underline">Log in</button></>
              )}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
