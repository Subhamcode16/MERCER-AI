import React from 'react';
import { CheckCircle2, Play } from 'lucide-react';

interface StrategyCardProps {
  title: string;
  reasoning: string;
  proposedLighting: string;
  proposedComposition: string;
  onGreenSignal: () => void;
  status: 'pending' | 'approved' | 'rendering';
}

export const StrategyCard: React.FC<StrategyCardProps> = ({
  title,
  reasoning,
  proposedLighting,
  proposedComposition,
  onGreenSignal,
  status
}) => {
  return (
    <div className="p-6 border border-neutral-800 bg-neutral-950 rounded-lg max-w-2xl mx-auto">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-white mb-1">Creative State: {title}</h3>
          <p className="text-sm text-neutral-400">Intelligence Layer Strategy (LAW-002)</p>
        </div>
        {status === 'approved' && (
          <span className="flex items-center gap-1 text-emerald-500 text-sm font-medium">
            <CheckCircle2 size={16} /> Approved
          </span>
        )}
      </div>

      <div className="space-y-4 mb-6 text-sm text-neutral-300">
        <p className="leading-relaxed">
          <span className="text-white font-medium">Strategic Reasoning: </span>
          {reasoning}
        </p>
        <div className="grid grid-cols-2 gap-4">
          <div className="p-3 bg-neutral-900 rounded border border-neutral-800">
            <span className="block text-neutral-500 text-xs uppercase tracking-wider mb-1">Lighting</span>
            <span className="font-medium text-neutral-200">{proposedLighting}</span>
          </div>
          <div className="p-3 bg-neutral-900 rounded border border-neutral-800">
            <span className="block text-neutral-500 text-xs uppercase tracking-wider mb-1">Composition</span>
            <span className="font-medium text-neutral-200">{proposedComposition}</span>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-neutral-800 flex justify-end">
        <button
          onClick={onGreenSignal}
          disabled={status !== 'pending'}
          className={`flex items-center gap-2 px-6 py-2 rounded font-medium transition-all ${
            status === 'pending'
              ? 'bg-emerald-500 hover:bg-emerald-600 text-black'
              : 'bg-neutral-800 text-neutral-500 cursor-not-allowed'
          }`}
        >
          {status === 'pending' ? 'Give Green Signal' : status === 'approved' ? 'Signal Given' : 'Rendering...'}
          {status === 'pending' && <Play size={16} />}
        </button>
      </div>
    </div>
  );
};
