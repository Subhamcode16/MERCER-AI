import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

interface ProvenanceBadgeProps {
  source: string;
  confidence: number;
  initialVerified: boolean;
  onVerify?: (isVerified: boolean) => void;
}

export const ProvenanceBadge: React.FC<ProvenanceBadgeProps> = ({ 
  source, 
  confidence, 
  initialVerified,
  onVerify 
}) => {
  const [verified, setVerified] = useState(initialVerified);

  const handleToggle = () => {
    const newState = !verified;
    setVerified(newState);
    if (onVerify) onVerify(newState);
  };

  const isHighConfidence = confidence >= 0.85;

  return (
    <div className="flex items-center gap-2 p-2 rounded border border-neutral-800 bg-neutral-900/50">
      <div className="flex items-center gap-1 text-xs text-neutral-400">
        <span className="font-mono">{source}</span>
        <span>•</span>
        <span className={isHighConfidence ? "text-emerald-500" : "text-amber-500"}>
          {(confidence * 100).toFixed(0)}% Confidence
        </span>
      </div>
      
      <button 
        onClick={handleToggle}
        className={`ml-auto flex items-center gap-1 px-2 py-1 text-xs rounded transition-colors ${
          verified 
            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
            : "bg-amber-500/10 text-amber-400 border border-amber-500/20 hover:bg-amber-500/20"
        }`}
      >
        {verified ? <ShieldCheck size={14} /> : <ShieldAlert size={14} />}
        {verified ? 'User-Verified' : 'Unverified'}
      </button>
    </div>
  );
};
